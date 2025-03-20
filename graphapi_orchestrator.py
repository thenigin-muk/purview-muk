#!/usr/bin/env python3
# file: graphapi_orchestrator.py
"""
Microsoft Graph API Orchestrator Setup
Creates and manages specialized app registrations with least-privilege permissions
"""
from workflows.common.graphapi.cli import main

if __name__ == "__main__":
    exit(main())