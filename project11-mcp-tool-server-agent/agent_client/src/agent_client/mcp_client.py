from typing import Any, Dict, Optional

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, server_params: StdioServerParameters):
        self.server_params = server_params
        self._stdio_cm = None
        self._session_cm = None
        self.session: Optional[ClientSession] = None

    async def connect(self) -> None:
        """
        Start the MCP server process and establish a session over stdio.
        """
        self._stdio_cm = stdio_client(self.server_params)
        read_stream, write_stream = await self._stdio_cm.__aenter__()

        self._session_cm = ClientSession(read_stream, write_stream)
        self.session = await self._session_cm.__aenter__()

        await self.session.initialize()

    async def close(self) -> None:
        """
        Cleanly shut down the session and server process.
        """
        if self._session_cm:
            await self._session_cm.__aexit__(None, None, None)
        if self._stdio_cm:
            await self._stdio_cm.__aexit__(None, None, None)

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP session not initialized")
        result = await self.session.call_tool(name=name, arguments=arguments)
        return result.content
