# This file is part of the Microsoft 365 Security API code samples (https://aka.ms/m365secapi)
# Description: This module provides a class to manage secrets for Graph API applications.
#!/usr/bin/env python3
# file: workflows/common/graphapi/module_generator.py
"""Generator for Graph API modules"""
import json
from pathlib import Path
from datetime import datetime

from workflows.common import log_utils

class ModuleGenerator:
    """Generates API modules for app registrations"""
    
    def __init__(self, config, use_key_vault=False, dry_run=False):
        """Initialize module generator with configuration"""
        self.config = config
        self.use_key_vault = use_key_vault
        self.dry_run = dry_run

    def _sanitize_name(self, name):
        """Convert a name to a valid Python identifier"""
        # Replace hyphens with underscores
        name = name.replace('-', '_')
        # Split by underscores and capitalize each part
        parts = [part.capitalize() for part in name.split('_')]
        # Join parts back together
        return ''.join(parts)
        
    def generate_module(self, app_name, scopes=None):
        """Generate a Python module for an app registration"""
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Would generate API module for: {app_name}")
            print(f"✅ [DRY RUN] Would generate API module in ./api_modules/{app_name}/")
            return True
        
        # Find the app in the configuration
        app_info = None
        for app in self.config.get("app_registrations", []):
            if app["name"] == f"Automation-{app_name}":
                app_info = app
                break
                
        if not app_info:
            log_utils.error(f"App registration not found: {app_name}")
            return False
        
        # Default scopes
        if not scopes:
            scopes = ["https://graph.microsoft.com/.default"]
        
        # Create modules directory if it doesn't exist
        modules_dir = Path("./api_modules")
        modules_dir.mkdir(exist_ok=True)
        
        # Create app module directory
        app_module_dir = modules_dir / app_name
        app_module_dir.mkdir(exist_ok=True)
        
        # Create __init__.py
        with open(app_module_dir / "__init__.py", "w") as f:
            f.write(f'"""API module for {app_name} operations"""\n')
            f.write(f'from .{app_name}_api import get_client, get_access_token\n')
        
        # Create the module file
        module_path = app_module_dir / f"{app_name}_api.py"
        
        # Add Key Vault support in the module
        key_vault_import = ""
        key_vault_code = ""
        
        if self.use_key_vault:
            key_vault_import = """
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient"""
            
            key_vault_code = f"""
    def _load_credentials_from_key_vault(self):
        \"\"\"Load credentials from Azure Key Vault\"\"\"
        # Try to get Key Vault URL
        vault_url = os.getenv("AZURE_KEYVAULT_URL")
        if not vault_url:
            log_utils.warning("Azure Key Vault URL not set, skipping Key Vault credential retrieval")
            return None, None, None
                
        try:
            # Get credentials using DefaultAzureCredential
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
                
            # Convert app name to valid Key Vault secret name (replace underscores with hyphens)
            safe_app_name = "{app_name}".replace('_', '-')
                
            # Get secrets using app name
            client_id = client.get_secret(f"{{safe_app_name}}-client-id").value
            client_secret = client.get_secret(f"{{safe_app_name}}-client-secret").value
            tenant_id = client.get_secret("tenant-id").value
                
            log_utils.info("Retrieved credentials from Azure Key Vault")
            return client_id, client_secret, tenant_id
        except Exception as e:
            log_utils.error(f"Failed to get credentials from Key Vault: {{e}}")
            return None, None, None"""
        
        # Modify the _load_credentials method to try Key Vault
        load_credentials_method = f"""
    def _load_credentials(self):
        \"\"\"Load credentials from various sources\"\"\"
        # First try environment variables
        env_prefix = "{app_name.replace('-', '_').upper()}"  # Changed from PURVIEW-API to PURVIEW_API
        client_id = os.getenv(f"{{env_prefix}}_CLIENT_ID")
        client_secret = os.getenv(f"{{env_prefix}}_CLIENT_SECRET")
        tenant_id = os.getenv("TENANT_ID")
            
        # Try Key Vault if environment variables not set
        if not all([client_id, client_secret, tenant_id]) and hasattr(self, '_load_credentials_from_key_vault'):
            key_vault_id, key_vault_secret, key_vault_tenant = self._load_credentials_from_key_vault()
            if all([key_vault_id, key_vault_secret, key_vault_tenant]):
                return key_vault_id, key_vault_secret, key_vault_tenant
            
        # If not available, try the secret file
        if not all([client_id, client_secret, tenant_id]):
            secret_file = f".env.{app_name}.secret"
            if os.path.exists(secret_file):
                with open(secret_file, "r") as f:
                    env_content = f.read()
                    
                # Parse environment variables
                for line in env_content.split('\\n'):
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if key == f"{{env_prefix}}_CLIENT_ID":  # Changed from PURVIEW-API_CLIENT_ID
                            client_id = value
                        elif key == f"{{env_prefix}}_CLIENT_SECRET":  # Changed from PURVIEW-API_CLIENT_SECRET
                            client_secret = value
                        elif key == "TENANT_ID":
                            tenant_id = value
            
        if not all([client_id, client_secret, tenant_id]):
            log_utils.error("Missing credentials for {app_name} API")
            raise ValueError(
                f"Missing credentials for {app_name} API. "
                "Please ensure environment variables, Key Vault, or secret file are properly set."
            )
            
        return client_id, client_secret, tenant_id"""
        
        # Fix the template string issue by properly escaping curly braces
        scopes_json = json.dumps(scopes)
        
        # Create a valid Python class name from app_name
        class_name = self._sanitize_name(app_name)
        
        # Generate module content
        module_content = f'''"""
{app_name.upper()} API Module
Auto-generated secure access module for {app_name} operations
Generated: {datetime.now().isoformat()}
"""
import os
import json
from pathlib import Path
from msal import ConfidentialClientApplication
from datetime import datetime, timedelta
{key_vault_import}

# Import logging
from workflows.common import log_utils

# API endpoints
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

class {self._sanitize_name(app_name)}Client:
    """Client for {app_name} API operations"""
    
    def __init__(self):
        """Initialize the {app_name} API client"""
        self.token = None
        self.token_expiry = None
        self.client = None
        
        # Load credentials
        client_id, client_secret, tenant_id = self._load_credentials()
        
        # Initialize the MSAL app
        self.app = ConfidentialClientApplication(
            client_id=client_id,
            authority=f"https://login.microsoftonline.com/{{tenant_id}}",
            client_credential=client_secret
        )
    {key_vault_code}
{load_credentials_method}
    
    def get_access_token(self):
        """Get an access token for the API"""
        # Check if we have a valid token
        if self.token and self.token_expiry and self.token_expiry > datetime.now():
            return self.token
        
        # Get a new token
        scopes = {scopes_json}
        result = self.app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            self.token = result["access_token"]
            # Set expiry time (token typically valid for 1 hour)
            self.token_expiry = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
            log_utils.debug("Obtained access token for {app_name} API")
            return self.token
        else:
            error = result.get("error", "unknown")
            error_desc = result.get("error_description", "")
            log_utils.error("Failed to get access token: {{}} - {{}}", error, error_desc)
            raise Exception(f"Failed to get access token: {{error}} - {{error_desc}}")
    
    def get_headers(self):
        """Get authorization headers for API requests"""
        token = self.get_access_token()
        return {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
    
    # Add specialized methods for {app_name} operations below
    # For example:
    
    def make_api_request(self, method, endpoint, data=None, params=None):
        """Make a request to the API"""
        import requests
        
        headers = self.get_headers()
        url = f"{{GRAPH_API_ENDPOINT}}{{endpoint}}"
        
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, json=data, params=params)
        elif method.lower() == 'patch':
            response = requests.patch(url, headers=headers, json=data)
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            log_utils.error("Unsupported HTTP method: {{}}", method)
            raise ValueError(f"Unsupported HTTP method: {{method}}")
        
        if response.status_code >= 400:
            log_utils.error("API request failed: {{}} - {{}}", response.status_code, response.text)
            raise Exception(f"API request failed: {{response.status_code}} - {{response.text}}")
        
        log_utils.debug("{app_name} API request successful: {{}}", endpoint)
        return response.json() if response.content else None

# Create a client instance
_client = None

def get_client():
    """Get the {app_name} API client"""
    global _client
    if _client is None:
        _client = {class_name}()
    return _client

def get_access_token():
    """Get an access token for {app_name} API operations"""
    return get_client().get_access_token()

# Example usage:
# client = get_client()
# result = client.make_api_request('get', '/me')
'''
        
        # Write the module file
        with open(module_path, "w") as f:
            f.write(module_content)
        
        log_utils.info(f"Generated API module: {module_path}")
        
        # Create a README.md file for the module
        readme_content = f"""# {app_name.capitalize()} API Module

Auto-generated secure access module for {app_name} operations.

## Usage

```python
from api_modules.{app_name} import get_client

# Get a client
client = get_client()

# Use the client
response = client.make_api_request('get', '/me')

## Available Methods
- get_client(): Get the API client
- get_access_token(): Get an access token for API operations
- client.make_api_request(method, endpoint, data=None, params=None): Make an API request

## Configuration

This module requires the following environment variables:

- `{app_name.upper()}_CLIENT_ID`: The client ID of the app registration
- `{app_name.upper()}_CLIENT_SECRET`: The client secret of the app registration
- `TENANT_ID`: The Entry ID of the tenant

Alternatively, you can create a .env.{app_name}.secret file with these variables."""        
        readme_path = app_module_dir / "README.md"
        with open(readme_path, "w") as f:
            f.write(readme_content)
        
        log_utils.info(f"Generated README: {readme_path}")
        
        return True
