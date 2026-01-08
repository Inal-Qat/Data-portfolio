from typing import cast, List

from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END

from .state import AgentState
from .llm import get_llm
from .config import get_settings

import pandas as pd
from app.tools.snowflake_query import run_snowflake_query, run_snowflake_query_df
from app.tools.analysis_tools import is_safe_sql, ensure_limit, compact_result_text

def planner_node(state: AgentState) -> AgentState:
    llm = get_llm()
    settings = get_settings()

    user_msg = state["messages"][-1].content  # last user message

    schema_context = f"""
You are generating SQL for Snowflake.

Use ONLY this schema:
- Database.Schema (fully qualified): {settings.snowflake_database}.{settings.snowflake_schema}
- Fully qualified prefix: {settings.snowflake_database}.{settings.snowflake_schema}

Available tables (TPCH):
- CUSTOMER
- ORDERS
- LINEITEM
- PART
- PARTSUPP
- SUPPLIER
- NATION
- REGION

Rules:
1) Output ONLY SQL or NO_SQL_NEEDED (no explanations).
2) Always use fully qualified names like {settings.snowflake_database}.{settings.snowflake_schema}.CUSTOMER
3) Use double quotes only if needed (usually not needed for TPCH).
4) If the request is not answerable with these tables, return NO_SQL_NEEDED.
"""

    system_prompt = (
        "You are a precise SQL planner.\n"
        + schema_context
        + "\nUser request:\n"
        + str(user_msg)
    )

    response = llm.invoke(
        [
            {"role": "system", "content": system_prompt},
        ]
    )

    content = response.content.strip()

    return {
        **state,
        "sql_query": None if content == "NO_SQL_NEEDED" else content,
        "error": None,
    }



def sql_node(state: AgentState) -> AgentState:
    sql = state.get("sql_query")
    if not sql:
        return {**state, "sql_result": None, "error": None}

    ok, reason = is_safe_sql(sql)
    if not ok:
        return {**state, "sql_result": None, "error": reason}

    safe_sql = ensure_limit(sql, default_limit=200)

    try:
        df = run_snowflake_query_df(safe_sql)

        # Store a compact text version for the LLM
        text = df.to_string(index=False)
        compact = compact_result_text(text, max_chars=3000, head_lines=25)

        return {
            **state,
            "sql_query": safe_sql,
            "sql_result": compact,
            "error": None,
        }

    except Exception as e:
        return {**state, "sql_result": None, "error": f"ERROR: {e}"}



def chat_node(state: AgentState) -> AgentState:
    """
    Simple node that calls the LLM with the current messages
    and appends the AI's reply to the conversation history.
    """
    llm = get_llm()

    messages = list(state["messages"])  
    response = llm.invoke(messages)

    # Append the model's response to the message history
    messages.append(response)

    # Return a new state dict with updated messages
    new_state: AgentState = {
        **state,
        "messages": cast(List[BaseMessage], messages),
    }
    return new_state

def final_answer_node(state: AgentState) -> AgentState:
    """
    Compose a final user-facing answer using the SQL result (if available).
    """
    llm = get_llm()

    user_question = state["messages"][-1].content
    sql_query = state.get("sql_query")
    sql_result = state.get("sql_result")
    err = state.get("error")
    safe_sql_result = compact_result_text(str(sql_result), max_chars=3000, head_lines=25)

    if err:
        msg = (
            "I can only run read-only SQL (SELECT/WITH) against the Snowflake sample data. "
            f"{err}"
        )
        return {**state, "messages": list(state["messages"]) + [AIMessage(content=msg)]}

    if not sql_query or not sql_result or str(sql_result).startswith("ERROR"):
        # No usable SQL result -> fallback to normal chat
        response = llm.invoke(state["messages"])
        return {**state, "messages": list(state["messages"]) + [response]}

    system = SystemMessage(
        content=(
            "You are an AI data analyst. Use the SQL result to answer the user.\n"
            "Rules:\n"
            "- Be concise.\n"
            "- Use the number from the SQL result.\n"
            "- If needed, briefly restate what was measured.\n\n"
            f"SQL Query:\n{sql_query}\n\n"
            f"SQL Result (truncated):\n{safe_sql_result}\n"
        )
    )

    response = llm.invoke([system, *state["messages"]])
    return {**state, "messages": list(state["messages"]) + [response], "error": None}

# Build the graph
graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("sql", sql_node)
graph_builder.add_node("final", final_answer_node)

# Set entry point
graph_builder.set_entry_point("planner")

# Planner → SQL → Chat → END
graph_builder.add_edge("planner", "sql")
graph_builder.add_edge("sql", "final")
graph_builder.add_edge("final", END)

# Compile
graph = graph_builder.compile()
