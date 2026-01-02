from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    user_input: str = Field(..., min_length=1, max_length=6000)
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier for semi-stateful mode (future).",
        examples=["demo-session-1"],
    )
    debug: bool = Field(default=False, description="Return extra debug info (future).")


class QueryResponse(BaseModel):
    request_id: str
    answer: str
    latency_ms: int
    model: str | None = None
    warnings: list[str] = []
