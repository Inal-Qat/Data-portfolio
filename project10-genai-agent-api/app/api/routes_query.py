import logging

from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.utils.ids import new_request_id
from app.utils.timing import timer_ms
from app.core.config import settings
from app.services.llm import call_llm, get_model_name
from app.services.guardrails import basic_guardrails

router = APIRouter(tags=["query"])
log = logging.getLogger("app.query")


@router.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest) -> QueryResponse:
    request_id = new_request_id()
    warnings = basic_guardrails(payload.user_input)

    with timer_ms() as elapsed:
        try:
            answer = await call_llm(payload.user_input)
        except Exception as e:
            log.exception("llm_call_failed", extra={"request_id": request_id})
            raise HTTPException(status_code=500, detail=str(e))

    latency_ms = max(1, elapsed())  # avoid 0ms for tiny calls
    log.info("query_ok", extra={"request_id": request_id, "latency_ms": latency_ms})

    return QueryResponse(
        request_id=request_id,
        answer=answer,
        latency_ms=latency_ms,
        model=get_model_name() if settings.LLM_PROVIDER == "groq" else None,
        warnings=warnings,
    )
