from google.adk.tools import ToolContext
def read_format_md(context: ToolContext):
    try:
        with open("format.md", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: format.md error while reading : {e}"