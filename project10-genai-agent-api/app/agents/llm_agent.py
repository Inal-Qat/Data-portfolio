from app.agents.base import Agent
from app.services.llm import call_llm
from app.services.tool_router import looks_like_math
from app.tools.calculator import safe_eval

class LLMAgent(Agent):
    async def run(self, user_input: str, session_id: str | None = None) -> tuple[str, list[str]]:
        text = user_input.strip()

        # Tool path: calculator
        if looks_like_math(text):
            expr = text.replace("^", "**")
            result = safe_eval(expr)
            return (str(result), ["calculator.safe_eval"])

        # Default path: LLM
        answer = await call_llm(text)
        return (answer, ["groq.chat.completions"])
