import platform
from datetime import datetime
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("System Server")


@mcp.tool()
def get_time() -> str:
	"""Returns the current local date and time."""
	return str(datetime.now())


@mcp.tool()
def get_system_info() -> str:
	"""Returns basic operating system and Python runtime information."""
	return f"OS: {platform.system()} {platform.release()} | Python: {platform.python_version()}"


if __name__ == "__main__":
	mcp.run(transport="stdio")
