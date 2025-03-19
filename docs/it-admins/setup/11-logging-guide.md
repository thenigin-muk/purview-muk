<!-- description: Documentation about the centralized logging system and how to use it effectively in your automation projects. -->

# Logging Guide & Best Practices

### Site Navigation
[🏠 Home](../../README.md) > [It Admins](../README.md) > [Setup](README.md) | [⬅ Back to Setup](README.md)

## Overview

This guide explains the centralized logging system implemented across the project. Proper logging is essential for troubleshooting, monitoring, and maintaining your SharePoint and Purview automation workflows. By following this guide, you can ensure all project components use consistent, well-structured logs.

## The Logging Architecture

The project uses a centralized logging approach with these key components:

1. **`log_utils.py`** - The core logging module that provides:
   - Consistent log formatting
   - Multi-destination logging (console and files)
   - Centralized message catalog
   - Helper functions for logging at different levels

2. **Message Catalog** - A structured class hierarchy in `Messages` that:
   - Organizes messages by component/function
   - Provides standardized formatting and wording
   - Makes messages easy to discover and maintain

3. **Convenience Functions** - Simple wrapper functions (`debug`, `info`, `warning`, etc.) that:
   - Handle string formatting automatically
   - Ensure consistent log output
   - Simplify common logging tasks

## Using the Logging System

### Basic Usage

***To use logging in any module:***

```python
# Import the logging utilities
from workflows.common import log_utils
from workflows.common.log_utils import Messages

# Initialize logging (only needed once per script)
log_utils.setup_logging()

# Log at different levels
log_utils.info("Processing started")
log_utils.debug("Found {} items to process", len(items))
log_utils.warning("Missing optional parameter: {}", param_name)
log_utils.error("Failed to connect to {}", service_name)

# Use predefined messages from the catalog
log_utils.info(Messages.Auth.TOKEN_SUCCESS)
log_utils.error(Messages.Site.SITE_ID_FAILURE, site_url)
```
Log Levels
The system supports standard Python logging levels (in order of increasing severity):

Level	Function	When to Use
DEBUG	log_utils.debug()	Detailed diagnostic information, useful during development
INFO	log_utils.info()	Confirmation that things are working as expected
WARNING	log_utils.warning()	Indication that something unexpected happened, but the script can continue
ERROR	log_utils.error()	Due to a more serious problem, the script couldn't perform a specific function
CRITICAL	log_utils.critical()	A very serious error, indicating the script may be unable to continue
String Formatting
The helper functions automatically handle string formatting using Python's str.format() method:

```python
# Instead of:
log_utils.info("Processing item {} of {}".format(i, total))

# You can use:
log_utils.info("Processing item {} of {}", i, total)
```
The Message Catalog
Structure and Organization
Messages are organized by component or function area:

```text
Messages
├── Auth - Authentication-related messages
├── Site - SharePoint site-related messages
├── Lists - Lists and library related messages
├── Columns - Column-related messages
├── ContentTypes - Content types and features messages
├── Schema - Schema extraction and comparison messages
└── Tool - Messages specific to the SP metadata tool
```
Each area contains constants for specific message types:

```python
class Messages:
    class Auth:
        TOKEN_SUCCESS = "Successfully obtained access token"
        TOKEN_FAILURE = "Failed to get access token"
        # ...
```
### Adding New Message Categories

To add a new category of messages:

Open log_utils.py
Locate the Messages class
Add a new nested class for your category:

```python
class Messages:
    # Existing classes...
    
    class Purview:
        """Purview-specific messages."""
        CONNECTION_SUCCESS = "Successfully connected to Purview API"
        CONNECTION_FAILURE = "Failed to connect to Purview API: {}"
        ENTITY_CREATED = "Successfully created entity: {}"
        ENTITY_UPDATED = "Successfully updated entity: {}"
        ENTITY_DELETED = "Successfully deleted entity: {}"
```
Adding New Messages to Existing Categories
To add new messages to an existing category:

Open log_utils.py
Locate the appropriate category class inside Messages
Add your new message constants:

```python
class Lists:
    # Existing messages...
    LIST_CREATED = "Created new list: {}"
    LIST_DELETED = "Deleted list: {}"
    LIST_UPDATED = "Updated list configuration: {}"
```

### Best Practices for Logging

**DO:**

1. **Use appropriate log levels:**
   - `debug` for detailed diagnostic information
   - `info` for general operational information
   - `warning` for unexpected but non-critical issues
   - `error` for failures that prevent specific operations
   - `critical` for system-wide failures

2. **Include contextual information:**
   - File names, record IDs, and operation types
   - Before/after state for important changes
   - Specific error codes and messages from external systems

3. **Be consistent:**
   - Use similar wording for similar operations
   - Follow the same format for similar events
   - Use the message catalog for common messages

4. **Log the complete lifecycle:**
   - Start of significant operations
   - Completion of operations with results
   - Major decision points in the code
   - Authentication and connection events

**DON'T:**

- **Don't log sensitive information:**
  - Passwords or credentials
  - Personal identifiable information (PII)
  - Full authentication tokens
  - Unredacted sensitive business data

- **Avoid excessive logging:**
  - Don't log inside tight loops (use counters instead)
  - Don't duplicate logs for the same event
  - Don't log obvious or redundant information

- **Don't include raw exception details in user-facing logs:**
  - Log technical details at `debug` level
  - Provide user-friendly messages at `info/warning` level

### Adding Logging to New Scripts

When creating a new automation script for the project:

1. **Import the logging utilities**:

```python
from workflows.common import log_utils
from workflows.common.log_utils import Messages
```

2. Initialize logging (once at the start of execution)

```python
log_utils.setup_logging()
```

3. Add message definitions (if needed):

```python
# Add to log_utils.py if these messages will be reused
class Messages:
    class YourNewComponent:
        OPERATION_START = "Starting operation: {}"
        OPERATION_COMPLETE = "Operation completed successfully: {}"
```

4. Use logging throughout your script:

```python
def main():
    log_utils.info("Script starting")
    try:
        # Your code here
        log_utils.info("Processing {} files", len(files))
        
        for file in files:
            try:
                # Process file
                log_utils.debug("Processing file: {}", file)
                # ...
            except Exception as e:
                log_utils.error("Failed to process file {}: {}", file, str(e))
                
    except Exception as e:
        log_utils.critical("Script failed: {}", str(e))
        return 1
        
    log_utils.info("Script completed successfully")
    return 0
```
## Advanced Logging Features
Custom Log File Location
You can specify a custom log file location:

```python
log_utils.setup_logging(log_file="/path/to/custom/logfile.log")
```

### Changing Log Levels
For more detailed output during development or troubleshooting:

```python
import logging
log_utils.setup_logging(level=logging.DEBUG)
```

For less verbose output in production:

```python
import logging
log_utils.setup_logging(level=logging.WARNING)
```

### Multiple Logger Support

If you need separate loggers for different components:

```python
purview_logger = log_utils.setup_logging(
    log_file="./logs/purview.log", 
    name="purview-component"
)
```

## Troubleshooting Logging Issues

### Common Problems and Solutions

#### 1. Duplicate log entries
- Ensure `setup_logging()` is called only once.
- Check if multiple handlers are being created accidentally.

#### 2. Missing log entries
- Verify the log level is appropriate (e.g., `DEBUG` messages won't appear with `INFO` level).
- Ensure the log file is being written to an accessible location.

#### 3. Format string errors
- If you see `KeyError` or `IndexError` exceptions, check your format strings.
- Ensure the number of placeholders `{}` matches the number of arguments.

```python
#!/usr/bin/env python3
"""
Script to synchronize SharePoint lists with Purview metadata.
"""
import sys
from workflows.common import log_utils
from workflows.common.log_utils import Messages

def connect_to_sharepoint(site_url):
    """Connect to SharePoint site."""
    log_utils.info("Connecting to SharePoint site: {}", site_url)
    try:
        # Connection code...
        log_utils.debug("Connection established")
        return True
    except Exception as e:
        log_utils.error("Failed to connect to SharePoint: {}", str(e))
        return False

def sync_metadata(site_url, list_name):
    """Synchronize metadata between SharePoint and Purview."""
    log_utils.info("Starting metadata synchronization")
    
    # Connect to services
    if not connect_to_sharepoint(site_url):
        return False
        
    try:
        # Sync operation code...
        items_processed = 42
        items_updated = 7
        
        log_utils.info("Processed {} items, updated {}", 
                     items_processed, items_updated)
        return True
    except Exception as e:
        log_utils.error("Synchronization failed: {}", str(e))
        return False

def main():
    """Main entry point."""
    log_utils.setup_logging()
    log_utils.info("Starting metadata synchronization script")
    
    # Script parameters
    site_url = "https://contoso.sharepoint.com/sites/Records"
    list_name = "Contracts"
    
    # Execute main functionality
    success = sync_metadata(site_url, list_name)
    
    if success:
        log_utils.info("Script completed successfully")
        return 0
    else:
        log_utils.error("Script failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

[⬅ Previous: 10 Troubleshooting](10-troubleshooting.md) | [Next: 2 Git Version Control ➡](2-git-version-control.md)