import os
import time
import asyncio
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from mcp import StdioServerParameters
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from api.metrics import (
    AGENT_RUNS_TOTAL,
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_LATENCY_MS,
    LLM_LATENCY_MS,
    TOOL_CALLS_TOTAL,
    TOOL_LATENCY_MS,
)
from api.schemas import QueryRequest, QueryResponse
from agent_client.agent import Agent
from agent_client.mcp_client import MCPClient

logger = logging.getLogger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    env = dict(os.environ)

    def make_mcp_client() -> MCPClient:
        """
        Create a fresh MCPClient each attempt.
        - If MCP_SERVER_URL is set -> connect over HTTP/SSE (docker)
        - Else -> spawn server via stdio (local dev)
        """
        mcp_url = os.getenv("MCP_SERVER_URL")
        if mcp_url:
            return MCPClient(server_url=mcp_url)

        server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_server.main"],
            env=env,
        )
        return MCPClient(server_params=server_params)

    retries = int(os.getenv("MCP_CONNECT_RETRIES", "30"))
    delay = float(os.getenv("MCP_CONNECT_DELAY_SEC", "0.5"))

    mcp_client: MCPClient | None = None
    last_err: Exception | None = None

    for attempt in range(1, retries + 1):
        mcp_client = make_mcp_client()
        try:
            await mcp_client.connect()
            last_err = None
            break
        except Exception as e:
            last_err = e
            try:
                await mcp_client.close()
            except Exception:
                pass

            logger.warning(
                f"MCP connect failed (attempt {attempt}/{retries}): {e}. Retrying in {delay}s"
            )
            await asyncio.sleep(delay)

    if last_err or mcp_client is None:
        raise RuntimeError(f"Failed to connect to MCP server after {retries} attempts") from last_err

    app.state.mcp_client = mcp_client
    app.state.agent = Agent(mcp_client, default_tz="Europe/Berlin")

    try:
        yield
    finally:
        await mcp_client.close()


app = FastAPI(title="Project 11 - MCP Agent API", lifespan=lifespan)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        path = request.url.path

        # Optional: exclude metrics endpoint to reduce noise
        # if path != "/metrics":
        HTTP_REQUEST_LATENCY_MS.labels(path=path).observe(elapsed_ms)
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method, path=path, status=str(status_code)
        ).inc()


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    result = await app.state.agent.run(req.text)

    if result.get("tool_calls"):
        AGENT_RUNS_TOTAL.labels(route="tool").inc()
        for call in result["tool_calls"]:
            TOOL_CALLS_TOTAL.labels(tool_name=call["name"]).inc()
            TOOL_LATENCY_MS.labels(tool_name=call["name"]).observe(call["latency_ms"])
    else:
        AGENT_RUNS_TOTAL.labels(route="llm").inc()
        if result.get("llm_latency_ms") is not None:
            LLM_LATENCY_MS.observe(result["llm_latency_ms"])

    return result


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)