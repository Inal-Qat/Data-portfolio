import asyncio
from typing import Any, Dict

from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


class MCPClient:
    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self._client_cm = None
        self._session_cm = None
        self.session: ClientSession | None = None

    async def connect(self) -> None:
        """
        Start the MCP server process and establish a session over stdio.
        """
        self._client_cm = stdio_client(self.server_command)
        transport = await self._client_cm.__aenter__()

        self._session_cm = ClientSession(transport)
        self.session = await self._session_cm.__aenter__()

        await self.session.initialize()

    async def close(self) -> None:
        """
        Cleanly shut down the session and server process.
        """
        if self._session_cm:
            await self._session_cm.__aexit__(None, None, None)
        if self._client_cm:
            await self._client_cm.__aexit__(None, None, None)

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP session not initialized")

        result = await self.session.call_tool(name=name, arguments=arguments)
        return result.content
