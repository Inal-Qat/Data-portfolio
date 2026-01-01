from fastapi import FastAPI
from app.core.logging import setup_logging
from app.api.routes_health import router as health_router

setup_logging("INFO")

app = FastAPI(title="genai-agent-api")
app.include_router(health_router)
