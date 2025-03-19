#!/usr/bin/env python3
# filepath: workflows/document_processing/processor.py
import os
import argparse
from pathlib import Path

# Import logging first
from workflows.common import log_utils
from workflows.common.log_utils import Messages

# Import document processing modules
from workflows.document_processing.config_manager import load_config, ensure_config
from workflows.document_processing.utils import check_unresolved_templates, cleanup_file_for_processing
from workflows.document_processing.readme_processor import (
    ensure_readme_has_description, 
    ensure_file_descriptions,
    ensure_readme,
    ensure_all_readmes,
    ensure_navigation_tables
)
from workflows.document_processing.navigation_builder import (
    generate_navigation,
    process_setup_guide,
    verify_workflow_table
)
from workflows.document_processing.html_generator import generate_html_files

# Import document message extensions
from workflows.document_processing.log_messages import DocMessages

def process_markdown_files(config):
    """Process all markdown files to ensure descriptions and navigation"""
    docs_dir = Path("docs")
    log_utils.info(Messages.Doc.PROCESS_START)
    
    file_count = 0
    updated_count = 0
    
    # First ensure all README files have proper descriptions
    readme_count = 0
    for readme_path in docs_dir.glob("**/README.md"):
        ensure_readme_has_description(readme_path)
        readme_count += 1
    
    log_utils.debug("Processed {} README files for descriptions", readme_count)
    
    for file_path in docs_dir.glob("**/*.md"):
        file_count += 1
        # First clean up any duplicate navigation
        cleanup_file_for_processing(file_path)
        # Then ensure descriptions are in place
        ensure_file_descriptions(file_path, config)
        # Finally generate navigation
        if generate_navigation(file_path, config):
            updated_count += 1
    
    log_utils.info("Processed {} markdown files, updated {} with navigation", 
                  file_count, updated_count)
    
    # Ensure READMEs exist in workflow folders
    users_dir = Path("docs/users")
    if (users_dir.exists()):
        for folder in [d for d in users_dir.iterdir() if d.is_dir()]:
            ensure_readme(folder, config)
    
    # Add READMEs to all directories
    ensure_all_readmes()
    
    # Process special tables
    process_setup_guide()
    verify_workflow_table()
    ensure_navigation_tables()
    check_unresolved_templates()

def create_branch(branch_name):
    """Create a new organization branch"""
    import subprocess
    branch_name = f"organization/{branch_name}"
    subprocess.run(["git", "checkout", "-b", branch_name])
    log_utils.info("Created organization branch: {}", branch_name)

def main():
    """Main entry point for document processor"""
    # Initialize logging
    log_utils.setup_logging(log_file="./logs/document_processor.log")
    
    parser = argparse.ArgumentParser(description="Documentation processor for municipality records management")
    parser.add_argument("--html", action="store_true", help="Generate HTML files for SharePoint")
    parser.add_argument("--config", action="store_true", help="Create or update configuration")
    parser.add_argument("--branch", help="Create a new organization branch")
    args = parser.parse_args()
    
    # Ensure we're in the project root
    if (not os.path.isdir("docs") or not os.path.isfile("README.md")):
        log_utils.error(Messages.Doc.ERROR_NOT_ROOT)
        return 1
    
    # Handle config
    if (args.config):
        ensure_config()
        return 0
    
    # Load configuration
    config = load_config()
    
    # Process all markdown files
    process_markdown_files(config)
    
    # Generate HTML if requested
    if (args.html):
        generate_html_files()
    
    if (args.branch):
        create_branch(args.branch)
    
    log_utils.info(Messages.Doc.PROCESS_COMPLETE)
    log_utils.info(Messages.Doc.TIP_HTML)
    
    return 0

if __name__ == "__main__":
    exit(main())