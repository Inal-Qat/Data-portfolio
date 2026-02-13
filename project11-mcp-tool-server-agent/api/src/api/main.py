import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
from mcp import StdioServerParameters

from api.schemas import QueryRequest, QueryResponse
from agent_client.mcp_client import MCPClient
from agent_client.agent import Agent


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


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    # Optional: you can pass tz into agent later; for now agent uses default_tz.
    result = await app.state.agent.run(req.text)
    return result