import asyncio
import json

from agent_client.mcp_client import MCPClient


async def main():
    # Command to start the MCP server
    server_cmd = ["python", "-m", "mcp_server.main"]

    client = MCPClient(server_cmd)
    await client.connect()

    response = await client.call_tool("ping", {})
    print(json.dumps(response, indent=2))

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
