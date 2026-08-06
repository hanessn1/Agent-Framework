from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Math Server")


@mcp.tool()
def add(a: int, b: int) -> int:
	"""Adds two integers together."""
	return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
	"""Multiplies two integers together."""
	return a * b


@mcp.tool()
def subtract(a: int, b: int) -> int:
	"""Subtracts two integers together."""
	return a - b


@mcp.tool()
def divide(a: int, b: int) -> float:
	"""Divides two integers together."""
	return a / b


@mcp.resource("info://server_status")
def get_server_status() -> str:
	"""Returns the current status of the Math MCP Server."""
	return "Status: Operational\nServer Version: 1.0.0\nAvailable Operations: add, multiply, subtract, divide"


@mcp.prompt()
def math_tutor_prompt(topic: str) -> str:
	"""Generates a system prompt to act as a step-by-step Math Tutor."""
	return (
		f"You are a friendly Math Tutor specializing in {topic}. "
		f"Explain concepts clearly, show step-by-step calculations using your math tools, "
		f"and ask encouraging questions."
	)


if __name__ == "__main__":
	mcp.run(transport="stdio")
