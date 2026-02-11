from fastmcp import FastMCP
from mcp_server.tools.calculator import safe_eval

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

if __name__ == "__main__":
    mcp.run()
