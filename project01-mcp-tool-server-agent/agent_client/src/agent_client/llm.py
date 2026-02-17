from agent_client.settings import settings


async def call_llm(user_input: str) -> str:
    """
    Minimal Groq LLM call.
    Keep isolated so we can later swap LangChain/LangGraph without touching the agent.
    """
    if settings.llm_provider != "groq":
        raise RuntimeError("Unsupported LLM_PROVIDER. Only 'groq' is implemented.")

    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Set it in your .env (secret).")

    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)

    completion = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be concise and correct."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content