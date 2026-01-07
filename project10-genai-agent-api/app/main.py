from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.config import settings
from app.core.middleware import RequestContextMiddleware
from app.api.routes_health import router as health_router
from app.api.routes_query import router as query_router
from app.api.routes_metrics import router as metrics_router

setup_logging(settings.LOG_LEVEL)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(RequestContextMiddleware)

app.include_router(health_router)
app.include_router(query_router)
app.include_router(metrics_router)