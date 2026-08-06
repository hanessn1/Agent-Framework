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

	def list_resources(self) -> List[Dict[str, Any]]:
		"""Fetch all resources exposed by the server."""
		response = self.send_request("resources/list")
		return response.get("result", {}).get("resources", [])

	def read_resource(self, uri: str) -> str:
		"""Read a resource by its URI."""
		response = self.send_request("resources/read", {"uri": uri})
		contents = response.get("result", {}).get("contents", [])
		text_outputs = [c.get("text", "") for c in contents if c.get("text")]
		return "\n".join(text_outputs)

	def list_prompts(self) -> List[Dict[str, Any]]:
		"""Fetch all prompt templates exposed by the server."""
		response = self.send_request("prompts/list")
		return response.get("result", {}).get("prompts", [])

	def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> str:
		"""Get a formatted prompt template by name."""
		response = self.send_request("prompts/get", {"name": name, "arguments": arguments or {}})
		messages = response.get("result", {}).get("messages", [])
		
		prompt_texts = []
		for msg in messages:
			content = msg.get("content", {})
			if isinstance(content, dict) and content.get("text"):
				prompt_texts.append(content["text"])
			elif isinstance(content, str):
				prompt_texts.append(content)
		return "\n".join(prompt_texts)

	def close(self):
		if self.process:
			self.process.terminate()
