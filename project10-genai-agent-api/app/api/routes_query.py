import logging

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.utils.ids import new_request_id
from app.utils.timing import timer_ms
from app.core.config import settings
from app.core.security import require_api_key
from app.core.request_context import get_request_id
from app.services.llm import call_llm, get_model_name
from app.services.guardrails import basic_guardrails
from app.services.metrics import record_request
from app.agents.llm_agent import LLMAgent


router = APIRouter(tags=["query"])
log = logging.getLogger("app.query")
agent = LLMAgent()


@router.post("/query", response_model=QueryResponse, dependencies=[Depends(require_api_key)])
async def query(payload: QueryRequest) -> QueryResponse:
    request_id = get_request_id()
    warnings = basic_guardrails(payload.user_input)

    with timer_ms() as elapsed:
        try:
            answer, tool_calls = await agent.run(payload.user_input, session_id=payload.session_id)            
            success = True
        except Exception as e:
            success = False
            log.exception("llm_call_failed", extra={"request_id": request_id})
            # record metrics before raising
            latency_ms = max(1, elapsed())
            record_request(success=False, latency_ms=latency_ms)
            raise HTTPException(status_code=500, detail=str(e))

    latency_ms = max(1, elapsed())  # avoid 0ms for tiny calls
    record_request(success=True, latency_ms=latency_ms)
    log.info("query_ok", extra={"request_id": request_id, "latency_ms": latency_ms})

    return QueryResponse(
        request_id=request_id,
        answer=answer,
        latency_ms=latency_ms,
        model=get_model_name() if settings.LLM_PROVIDER == "groq" else None,
        warnings=warnings,
        tool_calls=tool_calls,
    )
