# Description: Command-line interface for the Graph API Orchestrator
#!/usr/bin/env python3
# file: workflows/common/graphapi/cli.py
"""
Command-line interface for Graph API Orchestrator
"""
import os
import argparse
from pathlib import Path

from workflows.common import log_utils
from workflows.common.graphapi.orchestrator import GraphAPIOrchestrator

def main():
    """Main function for the GraphAPI orchestrator CLI"""
    parser = argparse.ArgumentParser(description="Microsoft Graph API Orchestrator")
    parser.add_argument("--setup", action="store_true", help="Set up the master app registration")
    parser.add_argument("--create-app", help="Create a new app registration")
    parser.add_argument("--description", help="Description for the app registration")
    parser.add_argument("--permissions", nargs="+", help="Required API permissions")
    parser.add_argument("--generate-module", help="Generate a Python module for an app")
    parser.add_argument("--list-apps", action="store_true", help="List registered applications")
    parser.add_argument("--rotate-secret", help="Rotate the client secret for an app")
    parser.add_argument("--use-key-vault", action="store_true", help="Use Azure Key Vault for secrets")
    parser.add_argument("--key-vault-url", help="URL for Azure Key Vault")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--client-id", help="Service principal client ID for Azure authentication")
    parser.add_argument("--client-secret", help="Service principal client secret for Azure authentication")
    parser.add_argument("--tenant-id", help="Tenant ID for Azure authentication")
    
    args = parser.parse_args()
    
    # Set Key Vault URL if provided
    if args.key_vault_url:
        os.environ["AZURE_KEYVAULT_URL"] = args.key_vault_url
    
    if args.client_id and args.client_secret and args.tenant_id:
        os.environ["AZURE_CLIENT_ID"] = args.client_id
        os.environ["AZURE_CLIENT_SECRET"] = args.client_secret
        os.environ["AZURE_TENANT_ID"] = args.tenant_id
        print("Using service principal authentication")
    
    orchestrator = GraphAPIOrchestrator(use_key_vault=args.use_key_vault)
    
    if args.setup:
        orchestrator.setup_master_app()
    
    elif args.create_app:
        if not orchestrator.create_app(args.create_app, args.description, args.permissions):
            return 1
    
    elif args.list_apps:
        if not orchestrator.list_apps():
            return 1
    
    elif args.rotate_secret:
        if not orchestrator.rotate_secret(args.rotate_secret):
            return 1
    
    elif args.generate_module:
        if not orchestrator.generate_module(args.generate_module):
            return 1
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)