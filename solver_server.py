import os
import json
import arxiv   
from typing import List
from mcp.server.fastmcp import FastMCP
import glob

WiKI_DIR = "/Users/chaeeunryu/Desktop/MCP Study/ToyProject/MCP-Project/Wikis"
CODE_DIR = "/Users/chaeeunryu/Desktop/MCP Study/ToyProject/MCP-Project/CodeBase"

# Initialize the MCP server
mcp = FastMCP("Demo Server")

@mcp.resource("CodeBase://folders")
def get_available_codes() -> str:
    """
    List all available codes in the CodeBase.
    
    This resource provides a simple list of all codes.
    """
    
    codes = []
    for folder in os.listdir(CODE_DIR):
        if os.path.isdir(os.path.join(CODE_DIR, folder)):
            codes.append(folder)
    return json.dumps(codes)
    
    

@mcp.tool()
def extract_info_about_code(code_name: str) -> str:
    """
    
    """

@mcp.prompt()
def generate_wiki_related_prompt(topic: str, ticket_id: int=5) -> str:
    """
    Generate a prompt for the client to find the solution referring to the wikis
    on a specific problem.
    """
    
    prompt_str = """
    
    """
    return prompt_str

@mcp.prompt()
def generate_data_related_prompt(topic: str, ticket_id: int=5) -> str:
    """
    Generate a prompt for the client to find the solution referring to the data
    on a specific problem.
    """
    
    prompt_str = """
    
    Generate a prompt for Claude to see if the data is
    
    """
    return prompt_str