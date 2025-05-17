import os
import json
import arxiv   
from typing import List
from mcp.server.fastmcp import FastMCP

WiKI_DIR = "/Users/chaeeunryu/Desktop/MCP Study/ToyProject/MCP-Project/Wikis"

# Initialize the MCP server
mcp = FastMCP("Demo Server")


@mcp.prompt
def generate_wiki_related_prompt(topic: str, ticket_id: int=5) -> str:
    """
    Generate a prompt for the client to find the solution referring to the wikis
    on a specific problem.
    """
    
    prompt_str = """
    
    """
    return prompt_str