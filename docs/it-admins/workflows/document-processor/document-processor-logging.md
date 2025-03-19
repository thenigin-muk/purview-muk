<!-- description: Documentation about Config related messages for Your Organization. -->
# Document Processing Logging

### Site Navigation
[🏠 Home](../../../README.md) > [It Admins](../../README.md) > [Workflows](../README.md) > [Document Processor](README.md) | [⬅ Back to Document Processor](README.md)

# Config related messages

The document processor component uses the centralized logging system for all operations related to markdown processing, navigation generation, and HTML conversion.

### Document Processing Message Categories

Document processing messages are organized under the `Messages.Doc` namespace:

```python
from workflows.common.log_utils import Messages


log_utils.info(Messages.Doc.CONFIG_LOADED) 

# Navigation related messages
log_utils.info(Messages.Doc.NAV_UPDATED, file_path)

# README processing messages
log_utils.info(Messages.Doc.README_CREATED, readme_path)

```

### Common Document Processing Logging Patterns
When processing markdown files:

# Start of processing
log_utils.info(Messages.Doc.PROCESS_START)

# File operations
log_utils.debug("Processing {} markdown files", file_count)

# Error handling
```python
try:
    # Template rendering
    template.render(**config)
except Exception as e:
    log_utils.warning(Messages.Doc.TEMPLATE_ERROR, file_path, str(e))

# Completion
log_utils.info(Messages.Doc.PROCESS_COMPLETE)

```

## Testing the Integration

Once you've implemented all these changes, test your document processor with different log levels:

# Normal logging
./document_processor_modular.py

# Debug logging for more details
log_utils.setup_logging(level=logging.DEBUG)
./document_processor_modular.py --config

# Create a log file
log_utils.setup_logging(log_file="./logs/document_processor.log")
./document_processor_modular.py