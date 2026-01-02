from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "GenAI agent API"
    ENV: str = "local"  # local | docker
    LOG_LEVEL: str = "INFO"

    # Optional simple auth (we’ll use later)
    API_KEY: str | None = None

    # LLM config (we’ll use later)
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
