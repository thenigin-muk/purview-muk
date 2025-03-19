#!/usr/bin/env python3
# filepath: workflows/document_processing/log_messages.py
"""
Document processing specific log messages that extend the common logging system.
"""
from workflows.common.log_utils import Messages

class DocMessages:
    """Document processing specific messages."""
    
    # Config related messages
    CONFIG_CREATED = "Created configuration file: {}"
    CONFIG_WARNING = "Please edit the config.yaml file with your organization's information"
    CONFIG_LOADED = "Configuration loaded successfully"
    
    # Navigation related messages
    NAV_UPDATED = "Updated navigation in: {}"
    NAV_SKIPPED = "Skipping navigation generation for: {}"
    NAV_NO_CHANGES = "No changes needed for: {}"
    
    # README related messages
    README_CREATED = "Created: {}"
    README_UPDATED = "Updated navigation table to: {}"
    README_DESC_ADDED = "Added description to README: {}"
    
    # File processing messages
    FILE_CLEANUP = "Cleaned up duplicate navigation in: {}"
    FILE_DESC_ADDED = "Added description to: {}"
    
    # Table related messages
    TABLE_WORKFLOW_UPDATED = "Updated workflow table in: {}"
    TABLE_SETUP_UPDATED = "Updated setup guide with sorted table."
    
    # Template related messages
    TEMPLATE_ERROR = "Template error in {}: {}"
    TEMPLATE_FALLBACK = "Using content without template processing"
    TEMPLATE_UNRESOLVED = "Unresolved template variables found in:"
    TEMPLATE_UNRESOLVED_FILE = "  - {}"
    
    # HTML generation messages
    HTML_GENERATING = "Generating HTML files for SharePoint..."
    HTML_GENERATED = "Generated HTML: {}"
    HTML_MODULE_MISSING = "Python markdown module not found. Run 'pip install markdown' to generate HTML."
    
    # Overall process messages
    PROCESS_START = "Starting documentation navigation update..."
    PROCESS_COMPLETE = "All documentation files now have auto-generated navigation, and all folders have README.md files."
    TIP_HTML = "Tip: Run with --html to generate SharePoint-ready HTML files."
    
    # Error messages
    ERROR_NOT_ROOT = "Error: This script must be run from the project root directory."

# Add to the base Messages class
setattr(Messages, 'Doc', DocMessages)