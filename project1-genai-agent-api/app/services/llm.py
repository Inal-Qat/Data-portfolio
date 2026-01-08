from app.core.config import settings


def get_model_name() -> str:
    return settings.GROQ_MODEL


async def call_llm(user_input: str) -> str:
    """
    Minimal Groq LLM call.
    Keep it isolated so we can later swap in LangChain/LangGraph without touching the API layer.
    """
    if settings.LLM_PROVIDER != "groq":
        raise RuntimeError("Unsupported LLM_PROVIDER. Only 'groq' is implemented.")

    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Set it in your .env (secret).")

    from groq import Groq

    client = Groq(api_key=settings.GROQ_API_KEY)

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be concise and correct."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content or ""
