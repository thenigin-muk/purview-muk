#!/usr/bin/env python3
"""
List all Microsoft Teams SharePoint sites using Microsoft Graph API
"""

import sys
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

# Ensure the script finds the `api_modules` directory
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent.parent  # Adjust to point to purview-muk root
sys.path.insert(0, str(ROOT_DIR))  # Add root to Python path

# Import the SharePoint API client
from api_modules.sharepoint import get_client

# Initialize the SharePoint API client
client = get_client()

# Make API request to list Teams-related SharePoint sites
response = client.make_api_request("get", "/sites?search=Teams")

# Print formatted output
if response and "value" in response:
    print("\n📌 Microsoft Teams SharePoint Sites Found:\n")
    for site in response["value"]:
        print(f"- {site['displayName']} ({site['webUrl']})")
else:
    print("\n⚠️ No Teams SharePoint sites found or insufficient permissions.")
