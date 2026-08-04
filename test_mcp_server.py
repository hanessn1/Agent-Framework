import json
import sys


def process_line(line: str):
	if not line.strip():
		return

	request = json.loads(line)
	method = request["method"]
	req_id = request["id"]
	params = request.get("params", {})

	result = {}
	if method == "initialize":
		result = {
			"protocolVersion": "2026-07-28",
			"capabilities": {"tools": {}},
			"serverInfo": {
				"name": "TestPythonMCPServer",
				"version": "1.0.0",
			}
		}
	elif method == "tools/list":
		result = {
			"tools": [
				{
					"name": "uppercase_text",
					"description": "Converts any text string to uppercase via an external MCP process.",
					"inputSchema": {
						"type": "object",
						"properties": {
							"text": {
								"type": "string",
								"description": "The text to convert"
							}
						},
						"required": ["text"]
					}
				}
			]
		}
	elif method == "tools/call":
		args = params.get("arguments", {})
		input_text = args.get("text", "")
		result = {
			"content": [
				{
					"type": "text",
					"text": f"[MCP SERVER OUTPUT]: {input_text.upper()}"
				}
			]
		}
	response = {
		"jsonrpc": "2.0",
		"id": req_id,
		"result": result
	}
	sys.stdout.write(json.dumps(response) + "\n")
	sys.stdout.flush()


if __name__ == "__main__":
	for line in sys.stdin:
		process_line(line)
