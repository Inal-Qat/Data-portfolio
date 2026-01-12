from fastapi import APIRouter, Depends, Response
from app.core.security import require_api_key
from app.services.metrics import render_prometheus

router = APIRouter(tags=["metrics"])

@router.get("/metrics", dependencies=[Depends(require_api_key)])
def metrics() -> Response:
    
    body = render_prometheus()
    return Response(content=body, media_type="text/plain; version=0.0.4")
