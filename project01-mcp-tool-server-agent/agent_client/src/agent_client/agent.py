# agent_client/src/agent_client/agent.py
import time
import uuid
from typing import Any, Dict

from agent_client.logger import log_event
from agent_client.llm import call_llm
from agent_client.tool_router import choose_tool


class Agent:
    def __init__(self, mcp_client, default_tz: str = "Europe/Berlin"):
        self.mcp = mcp_client
        self.default_tz = default_tz

    async def run(self, user_input: str) -> Dict[str, Any]:
        request_id = str(uuid.uuid4())
        tool_calls: list[dict[str, Any]] = []

        tool_name = choose_tool(user_input)

        # --- Tool path -------------------------------------------------------
        if tool_name:
            if tool_name == "calculator_safe_eval":
                args = {"expression": user_input}
            elif tool_name == "time_now_in_timezone":
                args = {"tz": self.default_tz}
            else:
                args = {}

            start = time.perf_counter()
            result = await self.mcp.call_tool(tool_name, args)
            latency_ms = int((time.perf_counter() - start) * 1000)

            tool_calls.append(
                {
                    "name": tool_name,
                    "arguments": args,
                    "latency_ms": latency_ms,
                    "result": result,
                }
            )

            log_event(
                {
                    "event": "tool_call",
                    "request_id": request_id,
                    "tool_name": tool_name,
                    "latency_ms": latency_ms,
                }
            )

            return {
                "request_id": request_id,
                "input": user_input,
                "tool_calls": tool_calls,
                "final_answer": result,
            }

        # --- LLM fallback ----------------------------------------------------
        start = time.perf_counter()
        text = await call_llm(user_input)
        latency_ms = int((time.perf_counter() - start) * 1000)

        log_event(
            {
                "event": "llm_call",
                "request_id": request_id,
                "latency_ms": latency_ms,
            }
        )

        return {
            "request_id": request_id,
            "input": user_input,
            "tool_calls": [],
            "llm_latency_ms": latency_ms,
            "final_answer": text,
        }