# Description: Centralized logging utilities for the Purview-MUK project.
#!/usr/bin/env python3
# file: workflows/common/log_utils.py

"""
Centralized logging utilities for the Purview-MUK project.
This module provides a consistent logging approach across the entire project.
"""

import os
import logging
from datetime import datetime

# Store the initialized logger to avoid multiple initializations
_logger = None

def setup_logging(log_file=None, level=logging.INFO, name="purview-muk"):
    """
    Configure logging with consistent formatting and multiple outputs.
    
    Args:
        log_file: Path to log file (default: logs/purview-muk_YYYYMMDD.log)
        level: Logging level (default: INFO)
        name: Logger name (default: purview-muk)
        
    Returns:
        Configured logger object
    """
    global _logger
    
    # If logger is already set up, return it
    if _logger is not None:
        return _logger
    
    # Create logs directory if needed
    if not log_file:
        os.makedirs('./logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = f"./logs/purview-muk_{timestamp}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Store logger for reuse
    _logger = logger
    
    logger.debug(f"Logging initialized: {log_file}")
    return logger

# Message catalog for common log messages
class Messages:
    """Centralized repository of log messages to ensure consistency."""
    
    class Auth:
        """Authentication-related messages."""
        TOKEN_SUCCESS = "Successfully obtained access token"
        TOKEN_FAILURE = "Failed to get access token"
        ENV_MISSING = "Missing required environment variables"
        ENV_LOAD_ERROR = "Error loading .env file: {}"
        DOTENV_MISSING = "dotenv module not found, skipping .env file loading"
        TOKEN_ERROR = "Error: {}"
        TOKEN_ERROR_DESC = "Description: {}"
        
    class Site:
        """SharePoint site-related messages."""
        SITE_ID_SUCCESS = "Successfully resolved site ID: {}"
        SITE_ID_FAILURE = "Failed to get site ID for {}"
        SITE_URL_PARSED = "Parsed URL: hostname={}, path={}"
        SITE_API_URL = "Using API URL: {}"
        SITE_NAME = "Success! Site name: {}"
        SITE_ERROR = "Error retrieving site: Status {}"
        
    class Lists:
        """Lists and library related messages."""
        LISTS_FOUND = "Found {} lists"
        LISTS_NONE = "No lists found in the site"
        LISTS_ERROR = "Error retrieving lists: Status {}"
        LIST_NOT_FOUND = "List '{}' not found. Available lists:"
        LIST_AVAILABLE = "  - {}"
        LIBRARIES_FOUND = "Found {} document libraries:"
        LIBRARIES_NONE = "No document libraries found"
        PROCESSING_LIST = "Processing list: {}"
        
    class Columns:
        """Column-related messages."""
        COLUMNS_ERROR = "Error retrieving columns: Status {}"
        SITE_COLUMNS_RETRIEVING = "Getting site columns..."
        SITE_COLUMNS_FOUND = "Found {} site columns"
        SITE_COLUMNS_ERROR = "Error retrieving site columns: Status {}"
        
    class ContentTypes:
        """Content types and features messages."""
        TYPES_RETRIEVING = "Extracting content types..."
        TYPES_ERROR = "Error retrieving content types: Status {}"
        TYPES_FOUND = "Found {} content types"
        FEATURES_RETRIEVING = "Extracting site features..."
        FEATURES_ERROR = "Error retrieving site features: Status {}"
        FEATURES_FOUND = "Found {} site features/properties"
        LIST_SETTINGS_ERROR = "Error retrieving list settings: Status {}"
        
    class Schema:
        """Schema extraction and comparison messages."""
        EXTRACT_START = "Extracting metadata schema from {}"
        EXTRACT_COMPREHENSIVE = "Extracting comprehensive information from {}"
        EXTRACT_SUCCESS = "Successfully extracted {} metadata fields"
        EXTRACT_FAILURE = "Failed to extract schema from SharePoint"
        SCHEMA_SAVED = "Saved extracted schema to {}"
        
        COMPARE_START = "Comparing with target schema: {}"
        COMPARE_TARGET_LOADED = "Loaded target schema: {} fields defined"
        COMPARE_ERROR = "Error loading schema file: {}"
        COMPARE_FILE_PATH = "Looking for file at: {}"
        
        CHANGES_SUMMARY = "Changes Required:"
        CHANGES_ADD = "  • {} fields to add"
        CHANGES_UPDATE = "  • {} fields to update"
        CHANGES_REMOVE = "  • {} fields to remove"
        
        FIELDS_TO_ADD = "Fields to Add:"
        FIELD_ADD_ITEM = "  • {} ({}): {}"
        FIELDS_TO_UPDATE = "Fields to Update:"
        FIELD_UPDATE_ITEM = "  • {}:"
        FIELD_UPDATE_TYPE = "    - Type: {} ➡ {}"
        FIELD_UPDATE_DESC = "    - Description: {} ➡ {}"
        FIELD_UPDATE_OPTIONS = "    - Options changed"
        FIELDS_TO_REMOVE = "Fields to Remove:"
        FIELD_REMOVE_ITEM = "  • {} ({})"
        
    class Tool:
        """Messages specific to the SP metadata tool."""
        TOOL_HEADER = "\nSharePoint Metadata Tool"
        TOOL_SEPARATOR = "========================="
        SITE_URL = "Site URL: {}"
        LIST_NAME = "List/Library: {}"
        COMPREHENSIVE_MODE = "Mode: Comprehensive Site Extraction"
        SUCCESS = "Operation completed successfully!"
        ARG_ERROR = "Either specify a list/library with --list/--library, use --list-libraries to see available libraries, or use --comprehensive for site-wide extraction"
        SCHEMA_REQUIRED = "Error: --schema is required when using --analyze"
        LIST_REQUIRED = "Error: --list or --library parameter is required for metadata extraction"
        LIST_HINT = "Use --list-libraries to see available document libraries"
        COMPREHENSIVE_HINT = "Use --comprehensive for site-wide extraction"

# Get the default logger
def get_logger():
    """Get the configured logger, initializing if needed."""
    if _logger is None:
        return setup_logging()
    return _logger

# Convenience methods
def debug(message, *args):
    """Log a debug message, formatting if args provided."""
    logger = get_logger()
    if args:
        message = message.format(*args)
    logger.debug(message)

def info(message, *args):
    """Log an info message, formatting if args provided."""
    logger = get_logger()
    if args:
        message = message.format(*args)
    logger.info(message)

def warning(message, *args):
    """Log a warning message, formatting if args provided."""
    logger = get_logger()
    if args:
        message = message.format(*args)
    logger.warning(message)

def error(message, *args):
    """Log an error message, formatting if args provided."""
    logger = get_logger()
    if args:
        message = message.format(*args)
    logger.error(message)

def critical(message, *args):
    """Log a critical message, formatting if args provided."""
    logger = get_logger()
    if args:
        message = message.format(*args)
    logger.critical(message)