# Updated version of solver_server.py

import os
import json
from typing import List, Dict, Any
import glob # For file searching, useful for code files

import requests # For making HTTP requests to your internal APIs
import subprocess # For running external scripts/C# tools if needed
import PyPDF2 # For reading PDF wikis

# Assuming utils.py is in the same directory or accessible in PYTHONPATH
from utils import get_topic_from_db # You need to ensure this function exists and works as expected
# import sqlite3
from mcp.server.fastmcp import FastMCP


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
WIKI_DIR = os.path.join(PROJECT_ROOT, "Wikis")
CODE_BASE_DIR = os.path.join(PROJECT_ROOT, "CodeBase")

# Initialize the MCP server
mcp = FastMCP("AdsDiagnosticsServer")



@mcp.tool()
def get_ad_data(campaign_id: str = None, ad_group_id: str = None, ad_id: str = None) -> Dict[str, Any]:
    """
    Retrieves advertisement data for a given campaign, ad group, or ad ID from internal Ads APIs.
    (Placeholder: Needs actual API integration)
    Args:
        campaign_id: The ID of the campaign to query.
        ad_group_id: The ID of the ad group to query.
        ad_id: The ID of the ad to query.
    Returns:
        A dictionary containing the ad data, or an error message.
    """
    if not any([campaign_id, ad_group_id, ad_id]):
        return {"error": "At least one ID (campaign_id, ad_group_id, or ad_id) must be provided."}
    # --- Placeholder for API call ---
    # api_endpoint = "YOUR_ADS_DATA_API_ENDPOINT_HERE"
    # headers = {"Authorization": "Bearer YOUR_API_TOKEN_OR_AUTH_METHOD"}
    # params = {...}
    # try:
    #     response = requests.get(api_endpoint, headers=headers, params=params)
    #     response.raise_for_status()
    #     return response.json()
    # except Exception as e:
    #     return {"error": f"API request failed: {str(e)}"}
    return {"status": "placeholder", "message": "get_ad_data needs actual API implementation."}

@mcp.tool()
def get_customer_ticket_details(ticket_id: str) -> Dict[str, Any]:
    """
    Retrieves details for a given customer ticket ID from the internal ticketing system.
    (Placeholder: Needs actual API integration)
    Args:
        ticket_id: The ID of the customer ticket.
    Returns:
        A dictionary containing the ticket details, or an error message.
    """
    if not ticket_id:
        return {"error": "Ticket ID must be provided."}
    # --- Placeholder for API call ---
    # api_endpoint = f"YOUR_TICKETING_SYSTEM_API_ENDPOINT_HERE/{ticket_id}"
    # headers = {"Authorization": "Bearer YOUR_API_TOKEN_OR_AUTH_METHOD"}
    # try:
    #     response = requests.get(api_endpoint, headers=headers)
    #     response.raise_for_status()
    #     return response.json() # Example: {"ticket_id": "123", "description": "...", "customer_id": "..."}
    # except Exception as e:
    #     return {"error": f"API request failed: {str(e)}"}

    return {"status": "placeholder", "ticket_id": ticket_id, "message": "get_customer_ticket_details needs actual API implementation."}

@mcp.tool()
def get_selection_logs(complaint_id: str = None, request_id: str = None, user_id: str = None, num_logs: int = 100) -> Dict[str, Any]:
    """
    Retrieves selection logs related to a specific complaint, request, or user from internal log systems.
    (Placeholder: Needs actual API integration)
    Args:
        complaint_id: The complaint ID.
        request_id: The specific request ID.
        user_id: The user ID.
        num_logs: Max number of log entries.
    Returns:
        A dictionary containing the logs or an error message.
    """
    if not any([complaint_id, request_id, user_id]):
        return {"error": "At least one identifier (complaint_id, request_id, or user_id) must be provided."}
    # --- Placeholder for API call ---
    return {"status": "placeholder", "message": "get_selection_logs needs actual API implementation."}


# --- Wiki and Knowledge Base Tools ---

@mcp.tool()
def search_wikis(topic: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Searches for wiki PDF filenames in the Wikis directory that relate to a specific topic.
    The search is based on the topic string appearing in the filename.

    Args:
        topic: The topic to search for in wiki filenames. Case-insensitive.
        max_results: The maximum number of matching wiki filenames to return.

    Returns:
        A list of dictionaries, each containing 'filename' and 'path' of matching wiki PDFs.
    """
    found_wikis = []
    if not os.path.exists(WIKI_DIR):
        return [{"error": f"Wiki directory not found: {WIKI_DIR}"}] # Or return empty list

    for filename in os.listdir(WIKI_DIR):
        if filename.lower().endswith(".pdf") and topic.lower() in filename.lower():
            if os.path.isfile(os.path.join(WIKI_DIR, filename)):
                found_wikis.append({"filename": filename, "path": os.path.join(WIKI_DIR, filename)})
                if len(found_wikis) >= max_results:
                    break
    if not found_wikis:
        return [{"message": f"No wiki PDFs found matching topic '{topic}' in their filename."}]
    return found_wikis

@mcp.tool()
def extract_text_from_wiki_pdf(pdf_filename: str) -> Dict[str, str]:
    """
    Extracts text content from a specified PDF file in the Wikis directory.

    Args:
        pdf_filename: The name of the PDF file (e.g., "COMPLAINTS-HANDLING-PROCEDURE-1.pdf").

    Returns:
        A dictionary containing the extracted text or an error message.
    """
    if not pdf_filename.lower().endswith(".pdf"):
        return {"error": "Filename must be a .pdf file."}
    
    file_path = os.path.join(WIKI_DIR, pdf_filename)

    if not os.path.exists(file_path):
        return {"error": f"Wiki PDF '{pdf_filename}' not found in {WIKI_DIR}."}

    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                extracted_page_text = page.extract_text()
                if extracted_page_text: # Ensure text was extracted
                    text += extracted_page_text + "\n" # Add newline between pages
        if not text.strip(): # Check if any text was extracted at all
             return {"filename": pdf_filename, "content": "", "warning": "No text could be extracted from this PDF. It might be image-based or corrupted."}
        return {"filename": pdf_filename, "content": text}
    except Exception as e:
        return {"error": f"Failed to extract text from '{pdf_filename}': {str(e)}"}

# --- Code Interaction Tools ---

@mcp.tool()
def list_code_files_in_project_directory(project_subfolder: str, file_extension: str = ".cs") -> Dict[str, Any]:
    """
    Lists code files (e.g., .cs, .py) within a specific project subfolder in the CodeBase.

    Args:
        project_subfolder: The subfolder name within CodeBase (e.g., "customerfeedback-web").
        file_extension: The file extension to search for (default: ".cs").

    Returns:
        A dictionary containing a list of found file paths or an error message.
    """
    target_dir = os.path.join(CODE_BASE_DIR, project_subfolder)
    if not os.path.isdir(target_dir):
        return {"error": f"Project directory not found: {target_dir}"}

    found_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(file_extension):
                found_files.append(os.path.join(root, file))
    
    if not found_files:
        return {"message": f"No '{file_extension}' files found in '{target_dir}'." , "files": []}
    return {"project_subfolder": project_subfolder, "files": found_files}

@mcp.tool()
def read_code_file_content(file_path: str) -> Dict[str, str]:
    """
    Reads the content of a specific code file.
    Ensure the file_path is within the allowed CODE_BASE_DIR for security.

    Args:
        file_path: The full path to the code file.

    Returns:
        A dictionary containing the file content or an error message.
    """
    # Security check: Ensure the path is within CODE_BASE_DIR
    normalized_code_base_dir = os.path.abspath(CODE_BASE_DIR)
    normalized_file_path = os.path.abspath(file_path)

    if not normalized_file_path.startswith(normalized_code_base_dir):
        return {"error": "Access denied: File path is outside the allowed CodeBase directory."}
    
    if not os.path.isfile(normalized_file_path):
        return {"error": f"Code file not found: {file_path}"}
        
    try:
        with open(normalized_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"file_path": file_path, "content": content}
    except Exception as e:
        return {"error": f"Failed to read code file '{file_path}': {str(e)}"}

@mcp.tool()
def get_topic(ticket_id: int) -> str:
    """
    Retrieves the topic associated with a specific ticket ID.
    This is a placeholder for actual implementation, which should be replaced with a real database or API call.

    Args:
        ticket_id: The ID of the ticket.

    Returns:
        A string representing the topic or an error message.
    """
    topic = get_topic_from_db(ticket_id) # Assuming this function exists in utils.py
    return f"Topic for ticket {ticket_id}: {topic}"

@mcp.tool()
def analyze_code_snippet(code_snippet: str, language: str = "csharp") -> Dict[str, Any]:
    """
    Analyzes a code snippet for potential issues or to understand its behavior.
    (Placeholder: Needs integration with a code analysis service or GitHub Copilot API)

    Args:
        code_snippet: The snippet of code to analyze.
        language: The programming language of the snippet (default: "csharp").

    Returns:
        A dictionary with the analysis results or an error if integration is not set up.
    """
    # --- Placeholder for actual analysis API call ---
    
    return {
        "status": "placeholder_analysis",
        "message": "This tool needs integration with a real code analysis service (e.g., SonarLint API, GitHub Copilot API if suitable).",
        "analyzed_snippet_preview": code_snippet[:200] + "...",
        "language": language
    }

@mcp.tool()
def save_fixed_code_file(original_file_path: str, fixed_code_content: str, new_filename_suffix: str = "_fixed") -> Dict[str, str]:
    """
    Saves the provided code content to a new file, typically with a suffix like '_fixed'.
    WARNING: This tool writes to the filesystem. Use with extreme caution and robust security checks.
    It's highly recommended to restrict write paths and validate inputs thoroughly.

    Args:
        original_file_path: The path of the original code file (used to determine save directory and base name).
        fixed_code_content: The new code content to save.
        new_filename_suffix: Suffix to add to the original filename (before extension).

    Returns:
        A dictionary with the path to the new file or an error message.
    """
    # Security check: Ensure the original_file_path is within CODE_BASE_DIR
    normalized_code_base_dir = os.path.abspath(CODE_BASE_DIR)
    normalized_original_file_path = os.path.abspath(original_file_path)

    if not normalized_original_file_path.startswith(normalized_code_base_dir):
        return {"error": "Access denied: Original file path is outside the allowed CodeBase directory for writing."}
    if not os.path.isfile(normalized_original_file_path): # Check if original file exists to get its path info
         return {"error": f"Original code file not found: {original_file_path}, cannot determine save location."}


    try:
        directory, filename = os.path.split(normalized_original_file_path)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}{new_filename_suffix}{ext}"
        new_file_path = os.path.join(directory, new_filename)

        # Additional security: ensure new_file_path is also within an allowed writeable area.
        # For now, we assume writing to the same directory is okay if the original was.

        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_code_content)
        return {"status": "success", "saved_file_path": new_file_path}
    except Exception as e:
        return {"error": f"Failed to save fixed code file '{new_file_path}': {str(e)}"}


# --- Resources ---

@mcp.resource("Wikis://available")
def list_available_wiki_pdfs() -> str:
    """
    Lists all available PDF wiki files in the Wikis directory.
    Formatted as Markdown.
    """
    content = "# Available Wiki PDFs for Ads Diagnostics\n\n"
    found_wikis = False
    if os.path.exists(WIKI_DIR):
        for item in os.listdir(WIKI_DIR):
            if item.lower().endswith(".pdf") and os.path.isfile(os.path.join(WIKI_DIR, item)):
                content += f"- `{item}`\n" # Use backticks for filename
                found_wikis = True
    
    if not found_wikis:
        content += "No PDF wiki files found in the Wikis directory.\n"
    else:
        content += f"\nUse the `search_wikis` tool with a topic or `extract_text_from_wiki_pdf` with a specific filename from this list.\n"
    return content

@mcp.resource("CodeBase://projects") # Changed from CodeBase://files to be more descriptive
def get_available_code_projects() -> str:
    """
    Lists all available top-level project folders in the CodeBase directory.
    Formatted as Markdown.
    """
    content = "# Available Code Projects/Folders in CodeBase\n\n"
    projects = []
    if os.path.exists(CODE_BASE_DIR):
        for item in os.listdir(CODE_BASE_DIR):
            if os.path.isdir(os.path.join(CODE_BASE_DIR, item)):
                # Exclude .venv if it's inside CodeBase, or other non-project folders
                if item.startswith(".") or item == "__pycache__":
                    continue
                projects.append(item)
    
    if not projects:
        content += "No project folders found in the CodeBase directory.\n"
    else:
        for project in projects:
            content += f"- `{project}`\n"
        content += "\nUse `list_code_files_in_project_directory` with a project folder name to see specific code files.\n"
    return content


# --- Prompts ---

@mcp.prompt()
def generate_wiki_diagnostic_prompt(ticket_id: int) -> str: # Renamed from generate_wiki_related_prompt
    """
    Generates a prompt to guide the LLM in using wiki documents for diagnosing a problem based on a ticket ID.
    It uses utils.get_topic to determine the relevant topic.
    """
    # Assuming get_topic exists in utils.py and works as expected
    # You might need to handle potential errors from get_topic if ticket_id is not found
    try:
        topic = get_topic(ticket_id) # Example: ticket_id might be int or str depending on your system
    except Exception as e:
        # Fallback if get_topic fails or ticket_id is not valid for it
        print(f"Error calling get_topic for ticket_id {ticket_id}: {e}")
        topic = f"issue related to ticket {ticket_id}"


    prompt_str = f"""
    You are a diagnostic assistant. A customer has reported an issue related to '{topic}' (from ticket ID {ticket_id}).
    Your task is to consult the available wiki documents to find a solution or diagnostic steps.

    Follow these instructions carefully:
    1.  First, use the `search_wikis` tool with `topic="{topic}"` to find relevant wiki PDF filenames. Review the list of filenames returned.
    2.  If relevant wikis are found, select the most promising one(s). For each selected wiki, use the `extract_text_from_wiki_pdf` tool with its `pdf_filename` to get its content.
    3.  Read and analyze the extracted text from the wiki(s). Identify key diagnostic procedures, troubleshooting steps, or known solutions related to '{topic}'.
    4.  Synthesize the information into a clear, step-by-step action plan that an engineer can follow to resolve the issue.
    5.  If multiple wikis offer insights, consolidate them. If there are conflicting procedures, highlight them.
    6.  For each step in your action plan, cite the source wiki filename(s) if possible.
    7.  If no relevant wikis are found or the wikis do not provide a clear solution, state that and suggest alternative investigation paths (e.g., escalating, checking logs, or analyzing code if applicable).

    Present your findings in a structured format with clear headings and bullet points for readability.
    """
    return prompt_str


@mcp.prompt()
def generate_code_analysis_prompt(ticket_id: int, problem_description: str, project_subfolder: str, specific_file: str = None) -> str:
    """
    Generates a prompt to guide the LLM in analyzing code related to a problem.
    It leverages tools to list files, read file content, and then analyze it.
    """
    try:
        topic = get_topic(ticket_id)
    except Exception:
        topic = f"issue related to ticket {ticket_id}"

    initial_file_instruction = f"First, if you don't have a specific file in mind, use `list_code_files_in_project_directory` with `project_subfolder=\"{project_subfolder}\"` to see available code files (e.g., .cs files)."
    if specific_file:
        initial_file_instruction = f"The investigation points towards the file: `{specific_file}` in project subfolder `{project_subfolder}`."


    prompt_str = f"""
    You are a code analysis assistant for a problem related to '{topic}' (from ticket ID {ticket_id}).
    The problem description is: "{problem_description}"
    The relevant code is expected to be in the project subfolder: `{project_subfolder}`.

    Follow these instructions:
    1.  {initial_file_instruction}
    2.  Based on the problem description and the list of files (or the `specific_file` provided), identify the most relevant code file(s) to inspect.
    3.  For each relevant file, use the `read_code_file_content` tool with the correct `file_path` to get its source code.
    4.  Once you have the code content, use the `analyze_code_snippet` tool. Provide the `code_snippet` (the content you read) and the correct `language` (e.g., "csharp").
        In your request to `analyze_code_snippet` (which is a placeholder), you should ask it to:
            a. Explain the functionality of the code in relation to the problem: "{problem_description}".
            b. Identify any potential bugs, logical errors, or areas that might cause the described problem.
            c. Suggest specific lines of code or sections that are most relevant.
    5.  Based on the (simulated) analysis from `analyze_code_snippet`, summarize:
        a. What the code does.
        b. Any identified potential errors or suspicious patterns.
        c. How these relate to the customer's reported problem.
    6.  **IMPORTANT**: If the analysis suggests a fix:
        a. Clearly describe the proposed change(s) to the code.
        b. **Do NOT attempt to write the fixed code directly unless explicitly instructed to use a save tool in a separate step.**
        c. If you were to suggest using `save_fixed_code_file`, clearly state the `original_file_path` and provide the complete `fixed_code_content` that should be saved. Explain why the fix is necessary.
    
    If the `analyze_code_snippet` tool indicates it's a placeholder, acknowledge this and state what kind of analysis you *would* perform if it were fully functional.
    """
    return prompt_str

@mcp.prompt()
def generate_data_investigation_prompt(ticket_id: int, problem_description: str) -> str:
    """
    Generates a prompt to guide the LLM in investigating data-related aspects of a problem.
    This prompt will focus on using tools to fetch and interpret various data sources.
    """
    try:
        topic = get_topic(ticket_id) # Assumes utils.get_topic(ticket_id) exists
    except Exception:
        topic = f"issue related to ticket {ticket_id}"

    prompt_str = f"""
    You are a data investigation specialist for a problem related to '{topic}' (ticket ID: {ticket_id}).
    The customer's problem is: "{problem_description}"

    Your goal is to use available tools to fetch relevant data and determine if data issues are contributing to the problem.

    Follow these steps:
    1.  **Ticket Review & Initial Hypothesis:**
        * Use `get_customer_ticket_details` with `ticket_id="{ticket_id}"` to understand the specifics.
        * Based on the ticket, form an initial hypothesis about what data might be relevant (e.g., ad configurations, user activity logs, specific entity states).

    2.  **Ad Data Retrieval (if applicable):**
        * If the problem seems related to ad performance or configuration, determine if any specific `campaign_id`, `ad_group_id`, or `ad_id` are mentioned or inferable.
        * Use `get_ad_data` with the relevant ID(s) to fetch current ad settings.
        * Analyze the retrieved ad data: Are there misconfigurations? Is it active? Does it meet targeting criteria?

    3.  **Log Analysis (Selection/Activity Logs):**
        * If the problem involves system behavior, errors, or unexpected outcomes, consider fetching selection/activity logs.
        * Use `get_selection_logs` with relevant identifiers (e.g., `complaint_id="{ticket_id}"`, or a `user_id` or `request_id` if known from the ticket or ad data).
        * Examine the logs for errors, warnings, unexpected values, or missing entries that correlate with the problem description.

    4.  **Deep Log Analysis (Cloud Logs - if necessary):**
        * If initial logs are inconclusive and the problem is complex, detailed cloud logs might be needed.
        * Use `initiate_cloud_log_download` (e.g., with `customer_request_id` if known). Note the `job_id`.
        * Periodically use `check_cloud_log_download_status` with the `job_id`.
        * Once 'completed' (simulated), describe what kind of information you would look for in these detailed logs given the problem.

    5.  **Synthesize Data Findings:**
        * Combine insights from all retrieved data sources.
        * Does the data confirm or refute your initial hypothesis?
        * Are there any data inconsistencies, anomalies, or missing data points that could explain the customer's issue?
        * Clearly state your conclusions based on the data investigation. If the data is inconclusive, specify what additional data or checks are needed.

    Present your findings methodically, detailing which tools you used, the key data points retrieved, and your interpretation of that data in relation to the problem.
    """
    return prompt_str


# Comprehensive Diagnostic Prompt (from AI's previous version, slightly adapted)
@mcp.prompt()
def ads_comprehensive_diagnostic_prompt(ticket_id: str) -> str: # Ensure ticket_id type matches get_topic or ticket tool
    
    """
    Generates a comprehensive prompt for the LLM to diagnose a Ads customer escalation.
    This prompt guides the LLM to use available tools step-by-step.
    """
    
    # Assuming ticket_id is a string here for consistency with `get_customer_ticket_details`
    # If `get_topic` requires an int, you might need to cast or adjust.
    # For simplicity, I'm not calling get_topic here, but you could add it.

    return f"""
    You are an expert Ads Escalation Diagnostic Agent.
    Your goal is to investigate and find the root cause for customer ticket ID: {ticket_id}.

    Follow these steps methodically. Think step by step. For each step, state the tool you are using, the parameters, and summarize the tool's output.

    1.  **Understand the Problem:**
        * Use `get_customer_ticket_details` with `ticket_id="{ticket_id}"` to fetch the complaint.
        * Summarize the customer's problem, what they observed, and their expected outcome.

    2.  **Initial Data Gathering (based on ticket information):**
        * Based on the ticket details (e.g., if it mentions a `campaign_id`, `ad_group_id`, `ad_id`, or `user_id`), use the `get_ad_data` tool to fetch relevant ad configuration.
        * If applicable, use `get_selection_logs` to get an overview of recent activities related to the complaint. Note any obvious errors or warnings in the initial logs.

    3.  **Consult Knowledge Base (Wikis):**
        * Use the resource `Wikis://available` to see available diagnostic guides.
        * Identify a relevant wiki PDF based on the problem type (e.g., "no impressions", "low click-through rate", etc.). You can use `search_wikis` with a derived topic if needed.
        * Use `extract_text_from_wiki_pdf` with the chosen `pdf_filename` to get its content.
        * Based on the wiki content and the problem description, formulate a step-by-step diagnostic plan.

    4.  **Execute Diagnostic Plan (Using Data and Code Tools as needed):**
        * Follow the plan. This may involve further calls to `get_ad_data`, `get_selection_logs`.
        * If the plan suggests checking code:
            * Use `CodeBase/projects` to see available code projects.
            * Use `list_code_files_in_project_directory` to find relevant files in a project.
            * Use `read_code_file_content` to read specific files.
            * Use `analyze_code_snippet` with the code content to look for issues.

    5.  **Deep Dive Log Analysis (If Necessary):**
        * If initial logs are insufficient and the plan suggests deeper log analysis, consider using cloud logs.
        * Use `initiate_cloud_log_download` with a relevant `customer_request_id` (if known). Note the `job_id`.
        * Periodically use `check_cloud_log_download_status` with the `job_id` until "completed".
        * Describe what you would analyze in these detailed logs (as direct access isn't possible here).

    6.  **Synthesize Findings and Propose Root Cause:**
        * Combine all gathered information: ticket details, ad data, logs, wiki guidance, code analysis (if any).
        * Clearly state the suspected root cause(s).
        * If a code fix is identified and seems straightforward based on `analyze_code_snippet`'s simulated output, describe the fix. You can then, if confident, suggest using `save_fixed_code_file` with the `original_file_path` and the complete `fixed_code_content`.
        * If the root cause is unclear, identify ambiguities and suggest next steps for a human engineer.

    Provide a detailed report of your investigation, including tool outputs and your reasoning.
    """


# --- Main Execution ---


if __name__ == "__main__":
    print("Welcome to Chaeeun's Demo!")
    print(f"Starting AdsDiagnosticsServer...")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Wiki Directory: {WIKI_DIR}")
    print(f"CodeBase Directory: {CODE_BASE_DIR}")
    # print(f"Available tools: {[name for name, _ in mcp.list_tools()]}")
    # print(f"Available resources: {[uri for uri, _ in mcp.resources.items()]}")
    # print(f"Available prompts: {[name for name, _ in mcp.prompts.items()]}")
    
    # Run the server
    mcp.run(transport='stdio') # Or 'http' if you want to expose it over network e.g. mcp.run(transport='http', host='0.0.0.0', port=8080)