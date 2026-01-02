import logging

from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.utils.ids import new_request_id
from app.utils.timing import timer_ms
from app.core.config import settings

router = APIRouter(tags=["query"])
log = logging.getLogger("app.query")


@router.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest) -> QueryResponse:
    request_id = new_request_id()

    with timer_ms() as elapsed:
        # Placeholder logic (LLM/agent will come later)
        answer = f"Stubbed response. You said: {payload.user_input[:200]}"

    latency_ms = elapsed()
    log.info("query_ok", extra={"request_id": request_id, "latency_ms": latency_ms})

    return QueryResponse(
        request_id=request_id,
        answer=answer,
        latency_ms=latency_ms,
        model=getattr(settings, "GROQ_MODEL", None),
        warnings=[],
    )
