import json
import subprocess
import threading
from typing import List, Dict, Any


class MCPStdioClient:
	"""Handles JSON-RPC 2.0 stdio transport with an external MCP Server subprocess."""

	def __init__(self, command: str, args: List[str]):
		self.process = subprocess.Popen(
			[command] + args,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			bufsize=1,
		)
		self._request_id = 0
		self._lock = threading.Lock()

	def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
		with self._lock:
			self._request_id += 1
			payload = {
				"jsonrpc": "2.0",
				"id": self._request_id,
				"method": method
			}
			if params is not None:
				payload["params"] = params

			# Send JSON line over stdin
			self.process.stdin.write(json.dumps(payload) + "\n")
			self.process.stdin.flush()

			# Read response line from stdout
			response_line = self.process.stdout.readline()
			if not response_line:
				raise RuntimeError("MCP server closed stdout unexpectedly.")
			return json.loads(response_line)

	def initialize(self):
		"""Perform the MCP handshake."""
		return self.send_request(
			"initialize",
			{
				"protocolVersion": "2026-07-28",
				"capabilities": {},
				"clientInfo": {
					"name": "AgentFrameClient",
					"version": "1.0.0"
				},
			}
		)

	def list_tools(self) -> List[Dict[str, Any]]:
		"""Fetch all tool definitions exposed by the server."""
		response = self.send_request("tools/list")
		return response.get("result", {}).get("tools", [])

	def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
		"""Invoke a tool on the MCP server and return text content."""
		response = self.send_request(
			"tools/call",
			{
				"name": name,
				"arguments": arguments
			}
		)
		result = response.get("result", {})
		content_list = result.get("content", [])

		# Combine text content items
		text_outputs = [item.get("text", "") for item in content_list if item.get("type") == "text"]
		return "\n".join(text_outputs) if text_outputs else str(result)

	def close(self):
		if self.process:
			self.process.terminate()
