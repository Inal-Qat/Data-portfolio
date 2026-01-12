from typing import Annotated, Optional, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    """
    State for the Snowflake AI Analyst Agent.

    - messages: full conversation history (user + assistant + tool messages)
    - sql_query: the last SQL query generated/executed
    - sql_result: a stringified representation of the SQL result
    - error: any error message encountered during processing
    """

    # Conversation history (LangGraph helper "add_messages" tells it how to merge)
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # SQL-related fields
    sql_query: Optional[str]
    sql_result: Optional[str]

    # Error handling
    error: Optional[str]
