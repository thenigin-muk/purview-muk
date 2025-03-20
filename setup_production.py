#!/usr/bin/env python3
# file: setup_production.py
"""
Production setup script for Microsoft Graph API Orchestrator
Creates necessary resources and configurations for production use
"""
import os
import argparse
import subprocess
import json
import logging
import sys
from pathlib import Path
import uuid

# Configure logging
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

def run_command(cmd, check=True):
    """Run a shell command"""
    logging.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        logging.error(f"Command failed with exit code {result.returncode}")
        logging.error(f"Error: {result.stderr}")
        if check:
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    else:
        logging.debug(f"Command output: {result.stdout}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Production setup for Graph API Orchestrator")
    parser.add_argument("--subscription", required=True, help="Azure subscription ID")
    parser.add_argument("--resource-group", required=True, help="Azure resource group name")
    parser.add_argument("--location", default="eastus", help="Azure location")
    parser.add_argument("--keyvault-name", required=False, help="Key Vault name (generated if not provided)")
    parser.add_argument("--prefix", default="purview-kv", help="Prefix for auto-generated Key Vault name")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Setup logging with appropriate level
    logger = setup_logging(args.debug)
    
    # Generate a unique Key Vault name if not provided
    if not args.keyvault_name:
        # Generate a short unique ID (first 8 chars of a UUID)
        unique_id = str(uuid.uuid4())[:8]
        # Key Vault names must start with a letter, be 3-24 chars, and use only letters, numbers, and hyphens
        args.keyvault_name = f"{args.prefix}-{unique_id}"
        logging.info(f"\n=== Generated unique Key Vault name: {args.keyvault_name} ===")
    
    try:
        # 1. Ensure resource group exists
        logging.info("\n=== Creating Resource Group (if needed) ===")
        run_command([
            "az", "group", "create",
            "--name", args.resource_group,
            "--location", args.location
        ])
        
        # 2. Create Key Vault with RBAC authorization
        logging.info("\n=== Creating Key Vault (with RBAC) ===")
        try:
            run_command([
                "az", "keyvault", "create",
                "--name", args.keyvault_name,
                "--resource-group", args.resource_group,
                "--location", args.location,
                "--sku", "standard",
                "--enable-rbac-authorization", "true"  # Explicitly enable RBAC
            ])
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                logging.warning(f"Key Vault '{args.keyvault_name}' already exists. Continuing...")
            else:
                raise
        
        # 3. Create service principal for the application
        logging.info("\n=== Creating Service Principal ===")
        result = run_command([
            "az", "ad", "sp", "create-for-rbac",
            "--name", "purview-muk-app",
            "--role", "contributor", 
            "--scopes", f"/subscriptions/{args.subscription}"
        ])
        
        # Parse the service principal details
        sp_details = json.loads(result.stdout)
        client_id = sp_details["appId"]
        client_secret = sp_details["password"]
        tenant_id = sp_details["tenant"]
        
        # 4. Grant the service principal access to Key Vault using RBAC
        logging.info("\n=== Granting Service Principal Access to Key Vault using RBAC ===")
    
        # Get resource ID for the Key Vault
        key_vault_id_result = run_command([
            "az", "keyvault", "show",
            "--name", args.keyvault_name,
            "--resource-group", args.resource_group,
            "--query", "id",
            "-o", "tsv"
        ])
        key_vault_id = key_vault_id_result.stdout.strip()
    
        # Assign Key Vault Secrets Officer role to the service principal
        run_command([
            "az", "role", "assignment", "create",
            "--assignee", client_id,
            "--role", "Key Vault Secrets Officer",
            "--scope", key_vault_id
        ], check=False)  # Don't fail if assignment already exists
    
        # Also assign Reader role to ensure the SP can see the Key Vault
        run_command([
            "az", "role", "assignment", "create",
            "--assignee", client_id,
            "--role", "Reader",
            "--scope", key_vault_id
        ], check=False)  # Don't fail if assignment already exists
        
        # 5. Save the service principal credentials to a secure file
        logging.info("\n=== Saving Service Principal Credentials ===")
        
        credentials_file = Path(".env.production")
        with open(credentials_file, "w") as f:
            f.write("# Production credentials - KEEP SECURE\n")
            f.write(f"AZURE_CLIENT_ID={client_id}\n")
            f.write(f"AZURE_CLIENT_SECRET={client_secret}\n")
            f.write(f"AZURE_TENANT_ID={tenant_id}\n")
            f.write(f"AZURE_KEYVAULT_URL=https://{args.keyvault_name}.vault.azure.net/\n")
        
        logging.info(f"\n✅ Production environment set up successfully!")
        logging.info(f"✅ Credentials saved to {credentials_file}")
        logging.warning("\n⚠️ IMPORTANT: Keep these credentials secure and never commit them to source control!")
        logging.info("   Add .env.production to your .gitignore file.")
        
        # Add to .gitignore if not already there
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if ".env.production" not in content:
                with open(gitignore_path, "a") as f:
                    f.write("\n# Production credentials\n.env.production\n")
        
        return 0
        
    except Exception as e:
        logging.error(f"Setup failed: {str(e)}")
        if args.debug:
            logging.exception("Detailed error information:")
        return 1

if __name__ == "__main__":
    sys.exit(main())