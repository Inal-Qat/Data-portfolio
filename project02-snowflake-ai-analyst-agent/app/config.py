from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    groq_api_key: str = Field(..., env="GROQ_API_KEY")

    # Snowflake
    snowflake_user: str = Field(..., env="SNOWFLAKE_USER")
    snowflake_password: str = Field(..., env="SNOWFLAKE_PASSWORD")
    snowflake_account: str = Field(..., env="SNOWFLAKE_ACCOUNT")
    snowflake_warehouse: str = Field(..., env="SNOWFLAKE_WAREHOUSE")
    snowflake_database: str = Field(..., env="SNOWFLAKE_DATABASE")
    snowflake_schema: str = Field(..., env="SNOWFLAKE_SCHEMA")
    snowflake_role: str | None = Field(default=None, env="SNOWFLAKE_ROLE")
    snowflake_fq_schema: str = "SNOWFLAKE_SAMPLE_DATA.TPCH_SF1"

    # Pydantic v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
