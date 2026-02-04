import asyncio
import json
import os

from mcp import StdioServerParameters

from agent_client.mcp_client import MCPClient


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
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
