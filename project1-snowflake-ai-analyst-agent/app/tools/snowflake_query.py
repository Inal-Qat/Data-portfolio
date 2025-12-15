import pandas as pd
from sqlalchemy import create_engine

from ..config import get_settings


def run_snowflake_query(query: str) -> str:
    """
    Execute a SQL query on Snowflake and return the results as a string.
    """
    settings = get_settings()

    try:
        # snowflake-sqlalchemy connection string format:
        # snowflake://<user>:<password>@<account>/<database>/<schema>?warehouse=<warehouse>&role=<role>
        role_part = f"&role={settings.snowflake_role}" if settings.snowflake_role else ""

        conn_str = (
            f"snowflake://{settings.snowflake_user}:{settings.snowflake_password}"
            f"@{settings.snowflake_account}/{settings.snowflake_database}/{settings.snowflake_schema}"
            f"?warehouse={settings.snowflake_warehouse}{role_part}"
        )

        engine = create_engine(conn_str)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        return df.to_string(index=False)

    except Exception as e:
        return f"ERROR: {e}"

def run_snowflake_query_df(query: str) -> pd.DataFrame:
    settings = get_settings()

    role_part = f"&role={settings.snowflake_role}" if settings.snowflake_role else ""
    conn_str = (
        f"snowflake://{settings.snowflake_user}:{settings.snowflake_password}"
        f"@{settings.snowflake_account}/{settings.snowflake_database}/{settings.snowflake_schema}"
        f"?warehouse={settings.snowflake_warehouse}{role_part}"
    )

    engine = create_engine(conn_str)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df