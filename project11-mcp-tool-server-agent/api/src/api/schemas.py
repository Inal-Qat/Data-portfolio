from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    text: str = Field(..., min_length=1)
    tz: str = Field(default="Europe/Berlin")


class QueryResponse(BaseModel):
    request_id: str
    input: str
    tool_calls: list[dict]
    final_answer: object
    llm_latency_ms: int | None = None