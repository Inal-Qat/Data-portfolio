from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel

from .config import get_settings


def get_llm() -> BaseChatModel:
    """
    Returns a configured Groq chat model for use across the app.
    """
    settings = get_settings()

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.1-8b-instant",  
        temperature=0.1,
        max_tokens=1024,
    )

    return llm
