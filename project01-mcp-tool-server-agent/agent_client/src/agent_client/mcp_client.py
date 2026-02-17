import json
from typing import Any, Dict, Optional

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client  


def parse_mcp_content(content: Any) -> Any:
    if isinstance(content, list) and content:
        first = content[0]
        if hasattr(first, "text"):
            text = first.text
            try:
                return json.loads(text)
            except Exception:
                return text
    return content


class MCPClient:
    def __init__(
        self,
        server_params: StdioServerParameters | None = None,
        server_url: str | None = None,
    ):
        if not server_params and not server_url:
            raise ValueError("Provide either server_params (stdio) or server_url (http).")
        self.server_params = server_params
        self.server_url = server_url

        self._transport_cm = None
        self._session_cm = None
        self.session: Optional[ClientSession] = None

    async def connect(self) -> None:
        """
        Establish MCP session.
        If anything fails mid-way, clean up in the SAME task to avoid AnyIO cancel-scope issues.
        """
        try:
            # choose transport
            if self.server_url:
                self._transport_cm = streamable_http_client(self.server_url)
            else:
                self._transport_cm = stdio_client(self.server_params)  # type: ignore[arg-type]

            entered = await self._transport_cm.__aenter__()
            read_stream, write_stream = entered[0], entered[1]

            self._session_cm = ClientSession(read_stream, write_stream)
            self.session = await self._session_cm.__aenter__()

            await self.session.initialize()

        except Exception:
            # critical: cleanup partial open resources
            try:
                await self.close()
            except Exception:
                pass
            raise

    async def close(self) -> None:
        if self._session_cm:
            await self._session_cm.__aexit__(None, None, None)
        if self._transport_cm:
            await self._transport_cm.__aexit__(None, None, None)

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP session not initialized")
        result = await self.session.call_tool(name=name, arguments=arguments)
        return parse_mcp_content(result.content)