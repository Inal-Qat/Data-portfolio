import asyncio
import json
import os
import sys

from mcp import StdioServerParameters
from agent_client.mcp_client import MCPClient
from agent_client.agent import Agent


async def main():
    user_input = sys.argv[1] if len(sys.argv) > 1 else "12 * (3 + 4)"

    env = dict(os.environ)

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.main"],
        env=env,
    )

    client = MCPClient(server_params)
    await client.connect()

    agent = Agent(client)
    response = await agent.run(user_input)

    print(json.dumps(response, indent=2))

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())