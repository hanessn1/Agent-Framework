from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("Filesystem server")


@mcp.tool()
def list_dir(path: str = ".") -> str:
	"""Lists files and directories inside a specified path. Use '.' for current project directory."""
	try:
		# Normalize root slash '/' or '\\' to current working directory '.'
		if path in ["/", "\\", "", "/."]:
			path = "."

		if not os.path.exists(path):
			return f"Error: Path '{path}' does not exist."

		if not os.path.isdir(path):
			return f"Error: Path '{path}' is a file, not a directory."

		items = os.listdir(path)
		output = []
		for item in items:
			full_path = os.path.join(path, item)
			if os.path.isdir(full_path):
				output.append(f"[DIR]  {item}")
			else:
				output.append(f"[FILE] {item}")
		return "\n".join(output) if output else "Directory is empty."
	except Exception as e:
		return f"Error listing directory '{path}': {str(e)}"


@mcp.tool()
def read_file(filepath: str) -> str:
	"""Reads and returns text content of a file given its filepath."""
	try:
		# Self-healing path cleanup if leading dot missing slash
		if not os.path.exists(filepath) and filepath.startswith(".") and not (
				filepath.startswith("./") or filepath.startswith("../")):
			cleaned = filepath[1:]
			if os.path.exists(cleaned):
				filepath = cleaned
		if not os.path.exists(filepath):
			return f"Error: File '{filepath}' not found."
		with open(filepath, "r", encoding="utf-8") as f:
			return f.read()

	except Exception as e:
		return f"Error reading file '{filepath}': {str(e)}"


@mcp.tool()
def get_pwd() -> str:
	"""Returns the current working directory absolute path."""
	return os.getcwd()


if __name__ == "__main__":
	mcp.run(transport="stdio")
