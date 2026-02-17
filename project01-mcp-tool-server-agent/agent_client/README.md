# Agent Runtime

The Agent runtime connects to an MCP tool server and optionally falls back to an LLM.

---

## Responsibilities

- Route user input
- Call MCP tools over stdio or HTTP/SSE
- Fallback to Groq LLaMA model
- Return structured tool trace
- Log latency and route metrics

---

## Routing Logic

- Math expression → calculator tool
- Time queries → time tool
- Everything else → LLM fallback

---

## CLI Usage

``` python -m agent_client.cli "12*(3+4)" ```

---

## Transport Modes

### Local (stdio)

Spawns MCP server process directly. 

### Docker (HTTP/SSE)

Connects to:

http://mcp-server:8001/mcp

---

## Observability

- Tool call trace
- Latency measurement
- Structured logging
- Metrics integration via FastAPI layer