from tools.base import BaseTool
import os


class ReadFileTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Reads and returns the text content of a file given its relative or absolute filepath.",
            parameters={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path of the file to read (e.g. 'file.txt' or 'subfolder/config.yaml'). Do not concatenate leading dots without slashes.",
                    }
                },
                "required": ["filepath"],
            },
        )

    def execute(self, filepath: str, **kwargs):
        try:
            if not os.path.exists(filepath):
                if filepath.startswith(".") and not (
                    filepath.startswith("./") or filepath.startswith("../")
                ):
                    cleaned_path = filepath[1:]
                    if os.path.exists(cleaned_path):
                        filepath = cleaned_path

            if not os.path.exists(filepath):
                return f"Error: File `{filepath}` not found."
            with open(filepath, "r", encoding="UTF-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}"
