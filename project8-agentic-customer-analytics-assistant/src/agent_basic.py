# Notebook3 agent as reusable function
from typing import Dict, Any, List

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, BaseMessage
from langchain_groq import ChatGroq

from .data_tools import data_overview, return_rates, top_customers
from .model_tools import predict_return


# Tools list
tools = [data_overview, return_rates, top_customers, predict_return]
tool_map = {tool.name: tool for tool in tools}


# LLM with Groq backend
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def run_agent(user_input: str) -> str:
    """
    Simple tool-using agent loop:
    - System + user message
    - LLM decides whether to call tools
    - Tools are executed and results are fed back
    - Stops when LLM returns a normal answer
    """
    messages: List[BaseMessage] = [
        SystemMessage(
            content=(
                "You are an AI Customer Analytics Assistant. "
                "You can analyze the customer dataset and a weak return prediction model. "
                "Use the available tools when you need data or calculations. "
                "Keep answers focused and explain them in clear business language."
            )
        ),
        HumanMessage(content=user_input),
    ]

    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        tool_calls = getattr(response, "tool_calls", None)

        if tool_calls:
            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc.get("args", {}) or {}

                if tool_name not in tool_map:
                    tool_result = f"Tool {tool_name} is not available."
                else:
                    tool = tool_map[tool_name]
                    tool_result = tool.invoke(tool_args)

                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tc["id"],
                    )
                )
        else:
            return response.content
