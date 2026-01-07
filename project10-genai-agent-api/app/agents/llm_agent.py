from app.agents.base import Agent
from app.services.llm import call_llm

class LLMAgent(Agent):
    async def run(self, user_input: str, session_id: str | None = None) -> tuple[str, list[str]]:
        answer = await call_llm(user_input)
        tool_calls = ["groq.chat.completions"]  # trace string for observability
        return answer, tool_calls
