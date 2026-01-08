# Notebook4 agent in module
from typing import Dict, Any, List, TypedDict

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    BaseMessage,
)
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from .data_tools import data_overview, return_rates, top_customers
from .model_tools import predict_return


class AgentState(TypedDict):
    messages: List[BaseMessage]


# Tools and LLM
tools = [data_overview, return_rates, top_customers, predict_return]
tool_map = {tool.name: tool for tool in tools}

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)
llm_with_tools = llm.bind_tools(tools)


def call_model(state: AgentState) -> AgentState:
    """Node that calls the LLM (with tools bound) with current messages."""
    response = llm_with_tools.invoke(state["messages"])
    new_messages = state["messages"] + [response]
    return {"messages": new_messages}


def call_tools(state: AgentState) -> AgentState:
    """Node that executes any tool calls from the last AI message."""
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None)

    if not tool_calls:
        return state

    new_messages = state["messages"].copy()

    for tc in tool_calls:
        tool_name = tc["name"]
        tool_args = tc.get("args", {}) or {}

        if tool_name not in tool_map:
            result = f"Tool {tool_name} is not available."
        else:
            tool = tool_map[tool_name]
            result = tool.invoke(tool_args)

        new_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tc["id"],
            )
        )

    return {"messages": new_messages}


def should_continue(state: AgentState) -> str:
    """Decide whether to call tools again or end."""
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None)

    if tool_calls:
        return "tools"
    return END


# Build the graph
_builder = StateGraph(AgentState)

_builder.add_node("model", call_model)
_builder.add_node("tools", call_tools)

_builder.set_entry_point("model")

_builder.add_conditional_edges(
    "model",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)

_builder.add_edge("tools", "model")

app = _builder.compile()


def run_graph_agent(user_input: str) -> str:
    """Run the LangGraph-based agent for a single user query."""
    messages: List[BaseMessage] = [
        SystemMessage(
            content=(
                "You are an AI Customer Analytics Assistant. "
                "You have tools to inspect the dataset, analyze returns, "
                "and predict return risk using a weak ML model. "
                "Use only relevant tools and explain your answers in clear business language."
            )
        ),
        HumanMessage(content=user_input),
    ]

    final_state = app.invoke({"messages": messages})
    final_messages = final_state["messages"]
    last = final_messages[-1]

    return last.content
