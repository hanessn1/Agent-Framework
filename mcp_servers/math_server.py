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


if __name__ == "__main__":
	mcp.run(transport="stdio")
