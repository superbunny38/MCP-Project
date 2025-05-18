# Updated version of solver_server.py

import os
import json
from typing import List, Dict, Any
import glob # For file searching, useful for code files
import requests # For making HTTP requests to your internal APIs
import subprocess # For running external scripts/C# tools if needed
import PyPDF2 # For reading PDF wikis

# Assuming utils.py is in the same directory or accessible in PYTHONPATH
from utils import get_topic # You need to ensure this function exists and works as expected

from mcp.server.fastmcp import FastMCP