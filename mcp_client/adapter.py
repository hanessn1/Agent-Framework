import logging
from typing import Dict, Any, List

from mcp_client.client import MCPStdioClient
from tools.base import BaseTool

logger = logging.getLogger(__name__)


class MCPToolAdapter(BaseTool):
	"""Adapts a single MCP Tool definition into your framework's BaseTool."""

	def __init__(self, mcp_client: MCPStdioClient, tool_def: Dict[str, Any]):
		name = tool_def["name"]
		description = tool_def.get("description", "")
		parameters = tool_def.get("inputSchema", {"type": "object", "properties": {}})

		super().__init__(name=name, description=description, parameters=parameters)
		self.mcp_client = mcp_client

	def execute(self, **kwargs):
		logger.debug(f"Forwarding tool call '{self.name}' to MCP Server via JSON-RPC...")
		return self.mcp_client.call_tool(self.name, kwargs)


def load_mcp_tools(command: str, args: List[str] = None) -> List[BaseTool]:
	"""Helper function: connects to an MCP Server, performs handshake, and returns BaseTool list."""
	client = MCPStdioClient(command, args or [])
	client.initialize()

	raw_tools = client.list_tools()
	logger.info(f"Loaded {len(raw_tools)} tool(s) from MCP server.")
	return [MCPToolAdapter(client, tool) for tool in raw_tools]
