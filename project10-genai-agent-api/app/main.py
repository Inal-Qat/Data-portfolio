from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.config import settings
from app.api.routes_health import router as health_router

setup_logging(settings.LOG_LEVEL)

app = FastAPI(title=settings.APP_NAME)
app.include_router(health_router)
