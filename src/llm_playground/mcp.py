from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path


class MCPFileSystem:
    """MCP file-system protocol handler for writing files"""

    def __init__(self, output_dir: str = "brochure_outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(self.output_dir),
            ],
        )

    async def write_file(self, filename: str, content: str) -> dict:
        """Write content to a file using MCP file-system protocol"""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("Initializing MCP file-system session...")
                await session.initialize()
                file_path = self.output_dir / filename

                result = await session.call_tool(
                    "write_file", arguments={"path": str(file_path.absolute()), "content": content}
                )

                print("File write result:", result)
                print(f"\nFile saved to: {file_path}")
                return result

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a string to be used as a filename"""
        safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_"))
        return safe_name.strip().replace(" ", "_")
