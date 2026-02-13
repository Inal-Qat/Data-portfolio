import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from mcp import StdioServerParameters
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from api.schemas import QueryRequest, QueryResponse
from agent_client.mcp_client import MCPClient
from agent_client.agent import Agent
from api.metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_LATENCY_MS, AGENT_RUNS_TOTAL, TOOL_CALLS_TOTAL, TOOL_LATENCY_MS, LLM_LATENCY_MS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load env vars from .env (nice for local dev)
    load_dotenv()

    # Ensure spawned MCP server inherits environment (incl. PYTHONPATH, GROQ_API_KEY)
    env = dict(os.environ)

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.main"],
        env=env,
    )

    mcp_client = MCPClient(server_params)
    await mcp_client.connect()

    agent = Agent(mcp_client, default_tz="Europe/Berlin")

    app.state.mcp_client = mcp_client
    app.state.agent = agent

    yield

    await mcp_client.close()


app = FastAPI(title="Project 11 - MCP Agent API", lifespan=lifespan)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000

    path = request.url.path
    HTTP_REQUEST_LATENCY_MS.labels(path=path).observe(elapsed_ms)
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method, path=path, status=str(response.status_code)
    ).inc()

    return response

@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    result = await app.state.agent.run(req.text)

    # route type
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
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)