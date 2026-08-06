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


class MCPServerHandle:
	"""
    Provides direct access to tools (as BaseTools), resources, and prompts.
    """

	def __init__(self, command: str, args: List[str] = None):
		self.client = MCPStdioClient(command, args or [])
		self.client.initialize()

		# load and adapt all tools as BaseTools
		raw_tools = self.client.list_tools()
		self.tools: List[BaseTool] = [MCPToolAdapter(self.client, t) for t in raw_tools]
		logger.info(f"Loaded {len(self.tools)} tool(s) from MCP server '{args}'.")

	def read_resource(self, uri: str) -> str:
		"""Fetch a resource from this MCP server."""
		return self.client.read_resource(uri)

	def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> str:
		"""Fetch a prompt template from this MCP server."""
		return self.client.get_prompt(name, arguments)

	def close(self):
		"""Shutdown the underlying process."""
		self.client.close()
