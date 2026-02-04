import asyncio
import json
import os

from mcp import StdioServerParameters

from agent_client.mcp_client import MCPClient

def to_jsonable(content):
    """
    MCP responses often return content objects (e.g., TextContent).
    Convert them into plain JSON-serializable structures.
    """
    if isinstance(content, list):
        out = []
        for item in content:
            # Many MCP content items have a .type and .text (TextContent)
            if hasattr(item, "type"):
                obj = {"type": item.type}
                if hasattr(item, "text"):
                    obj["text"] = item.text
                if hasattr(item, "data"):
                    obj["data"] = item.data
                out.append(obj)
            else:
                out.append(item)
        return out

    # Fallback: if it's a Pydantic-like object
    if hasattr(content, "model_dump"):
        return content.model_dump()

    # Last resort
    return str(content)

async def main():
    # IMPORTANT: server must see mcp_server/src on its PYTHONPATH too
    env = dict(os.environ)

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.main"],
        env=env,
    )

    client = MCPClient(server_params)
    await client.connect()

    response = await client.call_tool("ping", {})
    print(json.dumps(to_jsonable(response), indent=2, ensure_ascii=False))
    
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
