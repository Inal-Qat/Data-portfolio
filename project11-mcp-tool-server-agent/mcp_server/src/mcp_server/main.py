from fastmcp import FastMCP

mcp = FastMCP("project11-tools")

@mcp.tool()
def ping() -> dict:
    """Health-check tool to verify MCP server wiring."""
    return {"ok": True}

if __name__ == "__main__":
    mcp.run()
