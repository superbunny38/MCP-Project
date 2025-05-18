import os
import json
import arxiv   
from typing import List
from mcp.server.fastmcp import FastMCP
import glob
from utils import get_topic
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
    return

@mcp.tool()
def search_wikis(topic: str) -> List[str]:
    """
    Search for wikis related to a specific topic.
    
    This tool searches through the wikis directory and returns a list of
    wiki filenames that contain the specified topic.
    """
    
    wiki_files = []
    for filename in os.listdir(WiKI_DIR):
        if os.path.isfile(os.path.join(WiKI_DIR, filename)) and topic in filename:
            wiki_files.append(filename)
    
    return wiki_files

@mcp.prompt()
def generate_wiki_related_prompt(ticket_id: int=5) -> str:
    """
    Generate a prompt for the client to find the solution referring to the wikis
    on a specific problem.
    """
    
    topic = get_topic(ticket_id)
    prompt_str = """
    Search for the solution about {topic} in the wikis using the search_wikis tool.
    
    1. First search for wikis using search_wikis(topic) tool.
    2. Then, read the wikis and find the solution.
    3. Finally, summarize the solution in a structured format and bullet points for easy readibility. Make sure to give a step-by-step action plan for the client.
    
    """
    return prompt_str

@mcp.prompt()
def generate_code_related_prompt(ticket_id: int, problem = str) -> str:
    """
    Generate a prompt for the client to find the solution referring to the code
    on a specific problem.
    """
    topic = get_topic(ticket_id)
    prompt_str = """
    
    This is a direct message from the client about the problem related to existing codes about the topic {topic}.
    
    {problem}
    
    Follow these instructions:
    1. Inspect all the codes in the CodeBase (path: {CODE_DIR}) and see if there's any error.
    2. If you find any errors, prepare for a new code file named '{original_code_name}_fiixed' and write the code in the folder.
    3. Explain to the client what the error is and how you fixed it.
    
    """
    return prompt_str

@mcp.prompt()
def generate_data_related_prompt(ticket_id: int=5) -> str:
    """
    Generate a prompt for the client to find the solution referring to the data
    on a specific problem.
    """
    topic = get_topic(ticket_id)
    prompt_str = """
    
    Generate a prompt for Claude to see if the data is
    
    """
    return prompt_str