# MCP Tool Server

This service implements a Model Context Protocol (MCP) tool server.

It exposes tools via HTTP/SSE transport and can also run locally via stdio.

---

## Tools

### ping

Health-check tool.

### calculator_safe_eval(expression: str)

Safely evaluates mathematical expressions.

Example:

```json
{
  "expression": "12*(3+4)"
}
```
### time_now_in_timezone(tz: str)

Returns the current time in the specified timezone.

Default: Europe/Berlin

---

## Run Locally (stdio)

``` python -m mcp_server.main```

---

## Run via Docker (HTTP transport)

``` docker compose up mcp-server```

server runs at:

http://localhost:8001/mcp 

--- 

## Architecture Role:

The MCP server isolates tool execution from agent logic, allowing: 

- Secure tool exposure
- Independent scaling
- Protocol-driven tool invocation
- Agent-runtime decoupling

--- 
