import streamlit as st
from langchain_core.messages import HumanMessage

from app.graph import graph
from app.state import AgentState
from app.tools.snowflake_query import run_snowflake_query_df


st.set_page_config(page_title="Snowflake AI Analyst", layout="wide")
st.title("❄️ Snowflake AI Analyst Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask a question about the TPCH sample data...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run agent
    initial_state: AgentState = {
        "messages": [HumanMessage(content=prompt)],
        "sql_query": None,
        "sql_result": None,
        "error": None,
    }

    result = graph.invoke(initial_state)

    # Extract assistant reply (last message)
    assistant_msg = result["messages"][-1].content

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)

        # SQL transparency
        with st.expander("Show generated SQL"):
            st.code(result.get("sql_query") or "No SQL generated.", language="sql")

        with st.expander("Show SQL result"):
            if result.get("sql_query"):
                try:
                    df = run_snowflake_query_df(result["sql_query"])
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not render table: {e}")
                    st.text(result.get("sql_result") or "")
            else:
                st.text(result.get("sql_result") or "No SQL result.")

