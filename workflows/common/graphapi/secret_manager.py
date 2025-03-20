# Description: This module provides a class to manage secrets for Graph API applications.
#!/usr/bin/env python3
#file: workflows/common/graphapi/secret_manager.py
"""Secret management for Graph API applications"""
import os
from pathlib import Path
from datetime import datetime

from workflows.common import log_utils

class SecretManager:
    """Manages secrets for Graph API applications"""
    
    def __init__(self, use_key_vault=False, dry_run=False):
        self.use_key_vault = use_key_vault
        self.key_vault_client = None
        self.dry_run = dry_run  # Add this line
        
        if use_key_vault and not dry_run:
            self._init_key_vault()
    
    def _init_key_vault(self):
        """Initialize Key Vault client"""
        try:
            # Import Azure modules only if needed
            from azure.identity import DefaultAzureCredential, ClientSecretCredential
            from azure.keyvault.secrets import SecretClient
            
            vault_url = os.getenv("AZURE_KEYVAULT_URL")
            if not vault_url:
                log_utils.warning("Key Vault URL not provided, Key Vault storage disabled")
                return
            
            # Try to use DefaultAzureCredential first (good for development)
            try:
                credential = DefaultAzureCredential()
                self.key_vault_client = SecretClient(vault_url=vault_url, credential=credential)
                log_utils.info("Connected to Key Vault using DefaultAzureCredential")
            except Exception as e:
                log_utils.warning(f"DefaultAzureCredential failed: {str(e)}")
                
                # Fall back to ClientSecretCredential if environment variables are set
                client_id = os.getenv("AZURE_CLIENT_ID")
                client_secret = os.getenv("AZURE_CLIENT_SECRET")
                tenant_id = os.getenv("AZURE_TENANT_ID")
                
                if all([client_id, client_secret, tenant_id]):
                    try:
                        credential = ClientSecretCredential(
                            tenant_id=tenant_id,
                            client_id=client_id,
                            client_secret=client_secret
                        )
                        self.key_vault_client = SecretClient(vault_url=vault_url, credential=credential)
                        log_utils.info("Connected to Key Vault using ClientSecretCredential")
                    except Exception as e:
                        log_utils.error(f"Failed to connect to Key Vault: {str(e)}")
                else:
                    log_utils.error("Azure credentials not found for Key Vault access")
                    
        except Exception as e:
            log_utils.error(f"Failed to initialize Key Vault client: {str(e)}")
    
    def save_master_secrets(self, tenant_id, client_id, client_secret):
        """Save master app secrets"""
        # Save to local file
        self._save_to_env_file(".env.master", {
            "MASTER_TENANT_ID": tenant_id,
            "MASTER_CLIENT_ID": client_id,
            "MASTER_CLIENT_SECRET": client_secret
        })
        
        # Save to Key Vault if available
        if self.key_vault_client:
            self._save_to_key_vault("master-tenant-id", tenant_id)
            self._save_to_key_vault("master-client-id", client_id)
            self._save_to_key_vault("master-client-secret", client_secret)
    
    def save_app_secrets(self, app_name, client_id, client_secret, tenant_id):
        """Save app secrets"""
        # Save to local file
        self._save_to_env_file(f".env.{app_name}.secret", {
            f"{app_name.upper()}_CLIENT_ID": client_id,
            f"{app_name.upper()}_CLIENT_SECRET": client_secret,
            "TENANT_ID": tenant_id
        })
        
        # Save to Key Vault if available
        if self.key_vault_client:
            self._save_to_key_vault(f"{app_name}-client-id", client_id)
            self._save_to_key_vault(f"{app_name}-client-secret", client_secret)
            self._save_to_key_vault("tenant-id", tenant_id)
    
    def _save_to_env_file(self, file_name, secrets):
        """Save secrets to an environment file"""
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Would save secrets to {file_name}")
            for key in secrets:
                log_utils.info(f"[DRY RUN] - {key}")
            return True
        
        content = f"# Generated: {datetime.now().isoformat()}\n"
        content += "# DO NOT COMMIT THIS FILE\n\n"
        
        for key, value in secrets.items():
            content += f"{key}={value}\n"
        
        with open(file_name, "w") as f:
            f.write(content)
        
        log_utils.info(f"Secrets saved to {file_name}")
        
        # Update .gitignore
        self._update_gitignore(file_name)
    
    def _save_to_key_vault(self, name, value):
        """Save a secret to Key Vault"""
        if not self.key_vault_client:
            return False
            
        try:
            self.key_vault_client.set_secret(name, value)
            log_utils.info(f"Secret '{name}' saved to Key Vault")
            return True
        except Exception as e:
            log_utils.error(f"Failed to save secret to Key Vault: {str(e)}")
            return False
    
    def _update_gitignore(self, file_pattern):
        """Update .gitignore file"""
        gitignore_path = Path(".gitignore")
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if file_pattern not in content:
                with open(gitignore_path, "a") as f:
                    f.write(f"\n# GraphAPI secret files\n{file_pattern}\n")
        else:
            with open(gitignore_path, "w") as f:
                f.write(f"# GraphAPI secret files\n{file_pattern}\n")
    
    def get_master_secrets(self):
        """
        Retrieve master app secrets from Key Vault or local file
        
        Returns:
            tuple: (tenant_id, client_id, client_secret) or (None, None, None) if not found
        """
        tenant_id = None
        client_id = None
        client_secret = None
        
        # Try Key Vault first if available
        if self.key_vault_client:
            try:
                tenant_id = self.key_vault_client.get_secret("master-tenant-id").value
                client_id = self.key_vault_client.get_secret("master-client-id").value
                client_secret = self.key_vault_client.get_secret("master-client-secret").value
                
                if all([tenant_id, client_id, client_secret]):
                    log_utils.info("Retrieved master app secrets from Key Vault")
                    return tenant_id, client_id, client_secret
            except Exception as e:
                log_utils.warning(f"Failed to retrieve master secrets from Key Vault: {str(e)}")
        
        # Fall back to .env.master file
        env_file = Path(".env.master")
        if not env_file.exists():
            log_utils.warning("Master app secrets not found (.env.master)")
            return None, None, None
            
        # Load credentials from .env.master
        try:
            content = env_file.read_text()
            for line in content.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == "MASTER_TENANT_ID":
                        tenant_id = value
                    elif key == "MASTER_CLIENT_ID":
                        client_id = value
                    elif key == "MASTER_CLIENT_SECRET":
                        client_secret = value
                        
            if all([tenant_id, client_id, client_secret]):
                log_utils.info("Retrieved master app secrets from .env.master")
                return tenant_id, client_id, client_secret
            else:
                log_utils.warning("Incomplete master app secrets in .env.master")
                return None, None, None
        except Exception as e:
            log_utils.error(f"Error reading master app secrets from file: {str(e)}")
            return None, None, None
            
    def get_app_secrets(self, app_name):
        """
        Retrieve app secrets from Key Vault or local file
        
        Args:
            app_name (str): Name of the app
            
        Returns:
            tuple: (client_id, client_secret, tenant_id) or (None, None, None) if not found
        """
        client_id = None
        client_secret = None
        tenant_id = None
        
        # Try Key Vault first if available
        if self.key_vault_client:
            try:
                client_id = self.key_vault_client.get_secret(f"{app_name}-client-id").value
                client_secret = self.key_vault_client.get_secret(f"{app_name}-client-secret").value
                tenant_id = self.key_vault_client.get_secret("tenant-id").value
                
                if all([client_id, client_secret, tenant_id]):
                    log_utils.info(f"Retrieved {app_name} app secrets from Key Vault")
                    return client_id, client_secret, tenant_id
            except Exception as e:
                log_utils.warning(f"Failed to retrieve {app_name} secrets from Key Vault: {str(e)}")
        
        # Fall back to .env.[app_name].secret file
        env_file = Path(f".env.{app_name}.secret")
        if not env_file.exists():
            log_utils.warning(f"{app_name} app secrets not found ({env_file})")
            return None, None, None
            
        # Load credentials from file
        try:
            content = env_file.read_text()
            for line in content.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == f"{app_name.upper()}_CLIENT_ID":
                        client_id = value
                    elif key == f"{app_name.upper()}_CLIENT_SECRET":
                        client_secret = value
                    elif key == "TENANT_ID":
                        tenant_id = value
                        
            if all([client_id, client_secret, tenant_id]):
                log_utils.info(f"Retrieved {app_name} app secrets from {env_file}")
                return client_id, client_secret, tenant_id
            else:
                log_utils.warning(f"Incomplete {app_name} app secrets in {env_file}")
                return None, None, None
        except Exception as e:
            log_utils.error(f"Error reading {app_name} app secrets from file: {str(e)}")
            return None, None, None
            
    def get_secret_from_key_vault(self, secret_name):
        """
        Retrieve a specific secret from Key Vault
        
        Args:
            secret_name (str): Name of the secret
            
        Returns:
            str: Secret value or None if not found
        """
        if not self.key_vault_client:
            return None
            
        try:
            secret = self.key_vault_client.get_secret(secret_name).value
            log_utils.info(f"Secret '{secret_name}' retrieved from Key Vault")
            return secret
        except Exception as e:
            log_utils.error(f"Failed to retrieve secret '{secret_name}' from Key Vault: {str(e)}")
            return None