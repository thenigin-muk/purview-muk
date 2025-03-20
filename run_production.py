#!/usr/bin/env python3
# file: run_production.py
"""
Run the Microsoft Graph API Orchestrator in production mode
Uses service principal authentication with Key Vault
"""
import os
import argparse
import sys
import logging
from dotenv import load_dotenv
from workflows.common.graphapi.cli import main as orchestrator_main

def setup_logging(debug=False):
    """Configure logging with appropriate level and format"""
    level = logging.DEBUG if debug else logging.INFO
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    if debug:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        formatter = logging.Formatter('%(message)s')
    
    # Add formatter to handler
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

def main():
    parser = argparse.ArgumentParser(description="Run Graph API Orchestrator in production mode")
    parser.add_argument("--env-file", default=".env.production", help="Production environment file")
    
    # Add all the original orchestrator arguments
    parser.add_argument("--setup", action="store_true", help="Set up the master app registration")
    parser.add_argument("--create-app", help="Create a new app registration")
    parser.add_argument("--description", help="Description for the app registration")
    parser.add_argument("--permissions", nargs="+", help="Required API permissions")
    parser.add_argument("--generate-module", help="Generate a Python module for an app")
    parser.add_argument("--list-apps", action="store_true", help="List registered applications")
    parser.add_argument("--rotate-secret", help="Rotate the client secret for an app")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args, unknown_args = parser.parse_known_args()
    
    # Setup logging
    logger = setup_logging(args.debug)
    
    # Load environment variables from production file
    if os.path.exists(args.env_file):
        print(f"Loading production environment from {args.env_file}")
        load_dotenv(args.env_file)
    else:
        print(f"⚠️ Production environment file not found: {args.env_file}")
        print("Run setup_production.py first to create the production environment.")
        return 1
    
    # Ensure Key Vault is being used
    if not os.getenv("AZURE_KEYVAULT_URL"):
        print("⚠️ Key Vault URL not found in environment variables")
        return 1
    
    # Convert namespace to a list of args for the orchestrator
    orchestrator_args = []
    
    # Always use Key Vault in production
    orchestrator_args.extend(["--use-key-vault"])
    
    # Add the command arguments
    if args.setup:
        orchestrator_args.extend(["--setup"])
    if args.create_app:
        orchestrator_args.extend(["--create-app", args.create_app])
    if args.description:
        orchestrator_args.extend(["--description", args.description])
    if args.permissions:
        orchestrator_args.extend(["--permissions"] + args.permissions)
    if args.generate_module:
        orchestrator_args.extend(["--generate-module", args.generate_module])
    if args.list_apps:
        orchestrator_args.extend(["--list-apps"])
    if args.rotate_secret:
        orchestrator_args.extend(["--rotate-secret", args.rotate_secret])
    
    # Add any unknown args
    orchestrator_args.extend(unknown_args)
    
    # Replace sys.argv for the orchestrator
    sys.argv = [sys.argv[0]] + orchestrator_args
    
    # Run the orchestrator with the production settings
    return orchestrator_main()

if __name__ == "__main__":
    exit(main())