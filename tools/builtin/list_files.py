from tools.base import BaseTool
import os


class ListFilesTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="list_files",
            description="Lists all files and subdirectories inside a specified path. Output specifies whether each item is a [DIR] or [FILE].",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list (defaults to '.' for current directory).",
                    }
                },
                "required": [],
            },
        )

    def execute(self, path: str = ".", **kwargs):
        try:
            if not os.path.exists(path):
                return f"Error: Path `{path}` does not exist."
            if not os.path.isdir(path):
                return f"Error: Path `{path}` is a file, not a directory."

            items = os.listdir(path)
            output = []
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    output.append(f"[DIR] {item}")
                else:
                    output.append(f"[FILE] {item}")

            return "\n".join(output) if output else "Directory is empty."
        except Exception as e:
            return f"Error listing directory `{path}`: {str(e)}"
