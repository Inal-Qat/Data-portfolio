import uuid
import time
from typing import Any, Dict

from agent_client.tool_router import choose_tool
from agent_client.llm import call_llm


class Agent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def run(self, user_input: str) -> Dict[str, Any]:
        request_id = str(uuid.uuid4())

        tool_name = choose_tool(user_input)

        # 1) Tool path
        if tool_name:
            start = time.perf_counter()

            if tool_name == "calculator_safe_eval":
                args = {"expression": user_input}
            elif tool_name == "time_now_in_timezone":
                args = {"tz": "Europe/Berlin"}  # I can also parse timezone from text
            else:
                args = {}

            result = await self.mcp.call_tool(tool_name, args)
            latency_ms = int((time.perf_counter() - start) * 1000)

            return {
                "request_id": request_id,
                "tool_used": tool_name,
                "latency_ms": latency_ms,
                "answer": result,
            }

        # 2) LLM fallback path
        start = time.perf_counter()
        text = await call_llm(user_input)
        latency_ms = int((time.perf_counter() - start) * 1000)

        return {
            "request_id": request_id,
            "tool_used": None,
            "latency_ms": latency_ms,
            "answer": text,
        }    