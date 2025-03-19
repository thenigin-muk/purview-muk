#!/usr/bin/env python3
# file: setup_graphapi.py
"""
Security Setup Script
--------------------
Entry point for setting up Microsoft Graph API security.

This script calls the security orchestrator module to:
1. Set up master app registration
2. Create specialized app registrations 
3. Generate API modules
"""

import os
import sys
from pathlib import Path
from workflows.common.graphapi_orchestrator import main

if __name__ == "__main__":
    # Print banner
    print("\n=== Microsoft Graph API Security Setup ===\n")
    
    # Run the main function from the orchestrator
    main()