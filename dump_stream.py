import asyncio
import json
import logging
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "HomeLabAI/src"))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configuration
PYTHON_PATH = sys.executable
ARCHIVE_NODE = "HomeLabAI/src/nodes/archive_node.py"

async def dump_intercom_stream():
    archive_params = StdioServerParameters(command=PYTHON_PATH, args=[ARCHIVE_NODE])
    
    try:
        async with stdio_client(archive_params) as (ar, aw):
            async with ClientSession(ar, aw) as archive:
                await archive.initialize()
                
                result = await archive.call_tool("get_stream_dump", arguments={})
                data = json.loads(result.content[0].text)
                docs = data.get("documents", [])
                
                print("=== INTERCOM STREAM DUMP ===")
                for doc in docs:
                    print(doc)
                    print("-" * 20)
                print("============================")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(dump_intercom_stream())
