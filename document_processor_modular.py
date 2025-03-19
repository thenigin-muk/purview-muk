#!/usr/bin/env python3
# file: document_processor_modular.py

"""
Document processor for municipality records management - Modular Version
"""
try:
    print("Starting document processor...")
    
    # Import logging first to initialize
    from workflows.common import log_utils
    print("Logging module imported")
    
    # Import log messages
    from workflows.document_processing.log_messages import DocMessages
    print("DocMessages imported")
    
    # Set up logging (using only supported parameters)
    # Without any parameters, this should use default settings
    log_utils.setup_logging()
    print("Logging initialized")
    
    # Test the logging directly
    log_utils.info("Document processor starting")
    
    # Import main entry point after log setup
    from workflows.document_processing.processor import main
    print("Main function imported")
    
    if __name__ == "__main__":
        print("Executing main function...")
        exit_code = main()
        print(f"Main function completed with exit code: {exit_code}")
        exit(exit_code)
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)