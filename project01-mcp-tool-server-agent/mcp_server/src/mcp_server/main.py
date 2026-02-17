import os 
from fastmcp import FastMCP
from mcp_server.tools.calculator import safe_eval
from mcp_server.tools.time_tool import now_in_timezone

mcp = FastMCP("project11-tools")

@mcp.tool()
def ping() -> dict:
    """Health-check tool to verify MCP server wiring."""
    return {"ok": True}

@mcp.tool()
def calculator_safe_eval(expression: str) -> dict:
    """
    Evaluate a mathematical expression safely.
    """
    result = safe_eval(expression)
    return {"result": result}

@mcp.tool()
def time_now_in_timezone(tz: str = "Europe/Berlin") -> dict:
    """Return current time in the given timezone (IANA). Default: Europe/Berlin."""
    return {"timezone": tz, "now": now_in_timezone(tz)}

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")  # stdio (local) or http (docker)
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8001"))
    path = os.getenv("MCP_PATH", "/mcp")

    if transport == "http":
        mcp.run(transport="http", host=host, port=port, path=path)
    else:
        mcp.run()

