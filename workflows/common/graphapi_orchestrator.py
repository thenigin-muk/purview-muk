#!/usr/bin/env python3
# file: workflows/common/graphapi_orchestrator.py
"""
Microsoft Graph API Orchestrator
Creates and manages specialized app registrations with least-privilege permissions
"""

import os
import json
import argparse
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import requests
import msal

# Import your logging system
from workflows.common import log_utils
from workflows.common.log_utils import Messages

# Add message definitions for GraphAPI orchestrator
class GraphAPIMessages:
    """GraphAPI orchestration related messages."""
    MASTER_SETUP_START = "Starting master app registration setup"
    MASTER_SETUP_SUCCESS = "Master app registration setup successful"
    MASTER_SETUP_FAILURE = "Master app registration setup failed: {}"
    APP_CREATION_START = "Creating app registration: {}"
    APP_CREATION_SUCCESS = "Created app registration: {}"
    APP_CREATION_FAILURE = "Failed to create app registration: {} - {}"
    TOKEN_ACQUIRED = "Successfully acquired access token"
    TOKEN_FAILURE = "Failed to acquire access token: {}"
    PERMISSION_ADDED = "Added permission: {}"
    PERMISSION_FAILURE = "Failed to add permission {}: {}"
    MODULE_GENERATED = "Generated API module: {}"
    
# Register message class
if not hasattr(Messages, 'GraphAPI'):
    setattr(Messages, 'GraphAPI', GraphAPIMessages)

class GraphAPIOrchestrator:
    """
    Orchestrates the creation and management of secure app registrations
    """
    
    def __init__(self, config_path=None):
        """Initialize the GraphAPI orchestrator"""
        # Initialize logging
        log_utils.setup_logging()
        
        self.config_path = config_path or Path("./GraphAPI_config.json")
        self.config = self._load_config()
        self.token = None
        
    def _load_config(self):
        """Load the GraphAPI configuration file"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        else:
            # Return default empty config
            return {
                "tenant_id": "",
                "master_app": {
                    "name": "GraphAPI-Orchestrator-Master",
                    "client_id": "",
                    "object_id": "",
                    "creation_date": "",
                },
                "app_registrations": []
            }
    
    def _save_config(self):
        """Save the current configuration"""
        # Ensure the directory exists
        self.config_path.parent.mkdir(exist_ok=True)
        
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        
        log_utils.info("Configuration saved to {}", self.config_path)
    
    def setup_master_app(self):
        """
        Guide the user through setting up the master app registration
        """
        log_utils.info(Messages.GraphAPI.MASTER_SETUP_START)
        
        print("\n====== MASTER APP REGISTRATION SETUP ======")
        print("This will guide you through setting up a master app registration")
        print("that will be used to create and manage other app registrations.")
        print("\n1. Go to Azure Portal > Azure Active Directory > App Registrations")
        print("2. Click 'New registration'")
        print("3. Name it 'GraphAPI-Orchestrator-Master'")
        print("4. Select 'Accounts in this organizational directory only'")
        print("5. Click 'Register'")
        print("6. Note the Application (client) ID")
        print("7. Go to 'API permissions' and add these permissions:")
        print("   - Microsoft Graph > Application.ReadWrite.All")
        print("   - Microsoft Graph > Directory.ReadWrite.All")
        print("8. Click 'Grant admin consent'")
        print("9. Go to 'Certificates & secrets'")
        print("10. Create a new client secret and note its value")
        
        # Collect information from user
        tenant_id = input("\nEnter your tenant ID: ").strip()
        client_id = input("Enter the master app client ID: ").strip()
        client_secret = input("Enter the master app client secret: ").strip()
        
        # Verify the information by attempting to get a token
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=client_secret
        )
        
        # Get token for Microsoft Graph with Application.ReadWrite.All scope
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            log_utils.info(Messages.GraphAPI.MASTER_SETUP_SUCCESS)
            print("\n✅ Authentication successful! Master app is correctly configured.")
            
            # Store in config without saving the secret
            self.config["tenant_id"] = tenant_id
            self.config["master_app"]["client_id"] = client_id
            self.config["master_app"]["creation_date"] = datetime.now().isoformat()
            
            # Get the object ID of the app registration
            headers = {
                "Authorization": f"Bearer {result['access_token']}",
                "Content-Type": "application/json"
            }
            
            # Get app registration details
            response = requests.get(
                f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{client_id}'",
                headers=headers
            )
            
            if response.status_code == 200:
                app_info = response.json().get('value', [])[0]
                self.config["master_app"]["object_id"] = app_info.get('id')
                self.config["master_app"]["name"] = app_info.get('displayName')
            
            # Save config
            self._save_config()
            
            # Save secrets separately (never in git)
            self._save_master_secrets(tenant_id, client_id, client_secret)
            
            return True
        else:
            error = result.get('error', 'Unknown')
            log_utils.error(Messages.GraphAPI.MASTER_SETUP_FAILURE, error)
            print(f"\n❌ Authentication failed: {error}")
            print(f"Error description: {result.get('error_description')}")
            return False
    
    def _save_master_secrets(self, tenant_id, client_id, client_secret):
        """Save master secrets to .env file (not in git)"""
        env_content = f"""# Master app credentials - DO NOT COMMIT THIS FILE
# Created: {datetime.now().isoformat()}
MASTER_TENANT_ID={tenant_id}
MASTER_CLIENT_ID={client_id}
MASTER_CLIENT_SECRET={client_secret}
"""
        
        with open(".env.master", "w") as f:
            f.write(env_content)
        
        log_utils.info("Master secrets saved to .env.master file")
        print("\nMaster secrets saved to .env.master file")
        print("⚠️ IMPORTANT: Add .env.master to your .gitignore file")
        
        # Check if .gitignore exists and update it
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if ".env.master" not in content:
                with open(gitignore_path, "a") as f:
                    f.write("\n# GraphAPI orchestrator secrets\n.env.master\n.env.*.secret\n")
                log_utils.info("Added .env.master to .gitignore")
                print("✅ Added .env.master to .gitignore")
        else:
            with open(gitignore_path, "w") as f:
                f.write("# GraphAPI orchestrator secrets\n.env.master\n.env.*.secret\n")
            log_utils.info("Created .gitignore with .env.master entry")
            print("✅ Created .gitignore with .env.master entry")
    
    def get_master_token(self):
        """Get an access token for the master app"""
        # Load master secrets
        if not Path(".env.master").exists():
            log_utils.error("Master app secrets not found (.env.master)")
            print("❌ Master app secrets not found (.env.master)")
            print("Please run setup_master_app first")
            return None
        
        # Load credentials from .env.master
        with open(".env.master", "r") as f:
            env_content = f.read()
            
        # Parse environment variables
        env_vars = {}
        for line in env_content.split('\n'):
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
        
        tenant_id = env_vars.get("MASTER_TENANT_ID")
        client_id = env_vars.get("MASTER_CLIENT_ID")
        client_secret = env_vars.get("MASTER_CLIENT_SECRET")
        
        if not all([tenant_id, client_id, client_secret]):
            log_utils.error("Missing master app credentials in .env.master")
            print("❌ Missing master app credentials in .env.master")
            return None
        
        # Initialize MSAL app
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=client_secret
        )
        
        # Get token for Microsoft Graph
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            self.token = result["access_token"]
            log_utils.info(Messages.GraphAPI.TOKEN_ACQUIRED)
            return self.token
        else:
            error = result.get('error', 'Unknown')
            log_utils.error(Messages.GraphAPI.TOKEN_FAILURE, error)
            print(f"❌ Failed to get master token: {error}")
            print(f"Error description: {result.get('error_description')}")
            return None
    
    def create_app_registration(self, name, description=None, api_permissions=None):
        """
        Create a new app registration for a specific API surface area
        
        Args:
            name: Name of the app (e.g., sharepoint-reader)
            description: Description of the app's purpose
            api_permissions: List of required API permissions
        """
        log_utils.info(Messages.GraphAPI.APP_CREATION_START, name)
        
        # Ensure we have a valid token
        if not self.token and not self.get_master_token():
            return False
        
        # Prepare headers for Graph API
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Format the app name
        app_name = f"Automation-{name}"
        
        # Check if app already exists
        existing_app = next((app for app in self.config["app_registrations"] 
                            if app["name"] == app_name), None)
        
        if existing_app:
            log_utils.warning("App registration '{}' already exists", app_name)
            print(f"⚠️ App registration '{app_name}' already exists")
            return False
        
        # Prepare the app registration data
        app_data = {
            "displayName": app_name,
            "signInAudience": "AzureADMyOrg",
            "notes": description or f"App registration for {name} automation"
        }
        
        # Create the app registration
        log_utils.info("Creating app registration '{}'...", app_name)
        print(f"Creating app registration '{app_name}'...")
        response = requests.post(
            "https://graph.microsoft.com/v1.0/applications",
            headers=headers,
            json=app_data
        )
        
        if response.status_code >= 400:
            log_utils.error(Messages.GraphAPI.APP_CREATION_FAILURE, app_name, response.status_code)
            print(f"❌ Failed to create app registration: {response.status_code}")
            print(response.text)
            return False
        
        app_info = response.json()
        app_object_id = app_info["id"]
        app_client_id = app_info["appId"]
        
        log_utils.info(Messages.GraphAPI.APP_CREATION_SUCCESS, app_name)
        print(f"✅ Created app registration: {app_name}")
        print(f"   Object ID: {app_object_id}")
        print(f"   Client ID: {app_client_id}")
        
        # Add required permissions if specified
        if api_permissions:
            log_utils.info("Adding API permissions...")
            print("Adding API permissions...")
            for permission in api_permissions:
                self._add_permission(app_object_id, permission)
        
        # Create a client secret
        log_utils.info("Creating client secret...")
        print("Creating client secret...")
        secret_info = self._create_client_secret(app_object_id, "Initial-Secret")
        
        if not secret_info:
            log_utils.error("Failed to create client secret")
            print("❌ Failed to create client secret")
            return False
        
        # Update the configuration
        app_config = {
            "name": app_name,
            "client_id": app_client_id,
            "object_id": app_object_id,
            "description": description or f"App registration for {name} automation",
            "creation_date": datetime.now().isoformat(),
            "permissions": api_permissions or [],
            "secret_expiry": secret_info["end_date"]
        }
        
        self.config["app_registrations"].append(app_config)
        self._save_config()
        
        # Save the secret to a separate .env file
        self._save_app_secrets(name, app_client_id, secret_info["value"])
        
        # Notify about admin consent requirement
        log_utils.warning("API permissions require admin consent for app {}", app_client_id)
        print("\n⚠️ IMPORTANT: API permissions require admin consent")
        print(f"Please ask an admin to approve permissions at:")
        print(f"https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/CallAnAPI/appId/{app_client_id}")
        
        return {
            "name": app_name,
            "client_id": app_client_id,
            "object_id": app_object_id,
            "secret": secret_info["value"],
            "secret_expiry": secret_info["end_date"]
        }
    
    def _add_permission(self, app_object_id, permission):
        """Add a permission to the app registration"""
        if not self.token:
            return False
        
        # Prepare headers for Graph API
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Get the permission ID from Microsoft Graph
        # This is a simplified example - in reality you'd need to lookup the actual permission IDs
        resource_app_id = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph
        
        # Get the service principal to find permission IDs
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{resource_app_id}'",
            headers=headers
        )
        
        if response.status_code != 200:
            log_utils.error("Failed to get service principal: {}", response.status_code)
            print(f"❌ Failed to get service principal: {response.status_code}")
            return False
        
        graph_service_principal = response.json().get("value", [])[0]
        sp_id = graph_service_principal["id"]
        
        # Find the permission ID
        permission_id = None
        app_roles = graph_service_principal.get("appRoles", [])
        
        for role in app_roles:
            if role["value"] == permission:
                permission_id = role["id"]
                break
        
        if not permission_id:
            log_utils.error("Permission not found: {}", permission)
            print(f"❌ Permission not found: {permission}")
            return False
        
        # Add the permission
        permission_data = {
            "requiredResourceAccess": [
                {
                    "resourceAppId": resource_app_id,
                    "resourceAccess": [
                        {
                            "id": permission_id,
                            "type": "Role"
                        }
                    ]
                }
            ]
        }
        
        response = requests.patch(
            f"https://graph.microsoft.com/v1.0/applications/{app_object_id}",
            headers=headers,
            json=permission_data
        )
        
        if response.status_code >= 400:
            log_utils.error(Messages.GraphAPI.PERMISSION_FAILURE, permission, response.status_code)
            print(f"❌ Failed to add permission {permission}: {response.status_code}")
            print(response.text)
            return False
        
        log_utils.info(Messages.GraphAPI.PERMISSION_ADDED, permission)
        print(f"✅ Added permission: {permission}")
        return True
    
    def _create_client_secret(self, app_object_id, display_name, duration_years=1):
        """Create a client secret for the app registration"""
        if not self.token:
            return None
        
        # Prepare headers for Graph API
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Calculate expiration date
        end_date = (datetime.now() + timedelta(days=365*duration_years)).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Prepare secret data
        secret_data = {
            "passwordCredential": {
                "displayName": display_name,
                "endDateTime": end_date
            }
        }
        
        # Create the secret
        response = requests.post(
            f"https://graph.microsoft.com/v1.0/applications/{app_object_id}/addPassword",
            headers=headers,
            json=secret_data
        )
        
        if response.status_code >= 400:
            log_utils.error("Failed to create client secret: {}", response.status_code)
            print(f"❌ Failed to create client secret: {response.status_code}")
            print(response.text)
            return None
        
        secret_info = response.json()
        
        return {
            "value": secret_info["secretText"],
            "id": secret_info["keyId"],
            "end_date": end_date
        }
    
    def _save_app_secrets(self, app_name, client_id, client_secret):
        """Save app secrets to a separate .env file"""
        env_content = f"""# {app_name} app credentials - DO NOT COMMIT THIS FILE
# Created: {datetime.now().isoformat()}
{app_name.upper()}_CLIENT_ID={client_id}
{app_name.upper()}_CLIENT_SECRET={client_secret}
TENANT_ID={self.config["tenant_id"]}
"""
        
        # Create secrets directory if it doesn't exist
        os.makedirs("./.secrets", exist_ok=True)
        
        # Save to .env.[app_name].secret file
        env_file = f".env.{app_name}.secret"
        with open(env_file, "w") as f:
            f.write(env_content)
        
        log_utils.info("App secrets saved to {}", env_file)
        print(f"App secrets saved to {env_file}")
        print(f"⚠️ IMPORTANT: Keep this file secure and do not commit it to Git")
        
        return True
    
    def generate_api_module(self, app_name, scopes=None):
        """Generate a Python module for the app registration"""
        # Find the app in the configuration
        app_info = None
        for app in self.config["app_registrations"]:
            if app["name"] == f"Automation-{app_name}":
                app_info = app
                break
        
        if not app_info:
            log_utils.error("App registration not found: {}", app_name)
            print(f"❌ App registration not found: {app_name}")
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
        
        # Fix the template string issue by properly escaping curly braces
        scopes_json = json.dumps(scopes)
        
        #Start of module content
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

# Import logging
from workflows.common import log_utils

# API endpoints
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

class {app_name.capitalize()}Client:
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
    
    def _load_credentials(self):
        """Load credentials from the environment or secret file"""
        # First try environment variables
        client_id = os.getenv("{app_name.upper()}_CLIENT_ID")
        client_secret = os.getenv("{app_name.upper()}_CLIENT_SECRET")
        tenant_id = os.getenv("TENANT_ID")
        
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
                        if key == "{app_name.upper()}_CLIENT_ID":
                            client_id = value
                        elif key == "{app_name.upper()}_CLIENT_SECRET":
                            client_secret = value
                        elif key == "TENANT_ID":
                            tenant_id = value
        
        if not all([client_id, client_secret, tenant_id]):
            log_utils.error("Missing credentials for {app_name} API")
            raise ValueError(
                f"Missing credentials for {app_name} API. "
                "Please ensure environment variables or secret file are properly set."
            )
        
        return client_id, client_secret, tenant_id
    
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
        _client = {app_name.capitalize()}Client()
    return _client

def get_access_token():
    """Get an access token for {app_name} API operations"""
    return get_client().get_access_token()

# Example usage:
# client = get_client()
# result = client.make_api_request('get', '/me')
'''
    #End of of module content        
        with open(module_path, "w") as f:
            f.write(module_content)

        log_utils.info(Messages.GraphAPI.MODULE_GENERATED, module_path)
        print(f"✅ Generated API module: {module_path}")

        # Create a README.md file for the module
        # Start of readme_content
        readme_content = f"""# {app_name.capitalize()} API Module

Auto-generated secure access module for {app_name} operations.

## Usage

```python
from api_modules.{app_name} import get_client

# Get a client
client = get_client()

# Use the client
response = client.make_api_request('get', '/me')
```

## Available Methods

- `get_client()`: Get the API client
- `get_access_token()`: Get an access token for API operations
- `client.make_api_request(method, endpoint, data=None, params=None)`: Make an API request

## Configuration

This module requires the following environment variables:

- `{app_name.upper()}_CLIENT_ID`: The client ID of the app registration
- `{app_name.upper()}_CLIENT_SECRET`: The client secret of the app registration
- `TENANT_ID`: The Azure AD tenant ID

Alternatively, you can create a .env.{app_name}.secret file with these variables."""
        # End of readme_content
        readme_path = app_module_dir / "README.md"
        with open(readme_path, "w") as f: f.write(readme_content)
    
        log_utils.info("Generated README.md for {}", app_name)
        print(f"✅ Generated README.md for {app_name}")
    
        return True

# Main function to handle CLI arguments    

def main():
    """Main function for the GraphAPI orchestrator CLI"""
    parser = argparse.ArgumentParser(description="Microsoft Graph API Orchestrator")
    parser.add_argument("--setup", action="store_true", help="Set up the master app registration")
    parser.add_argument("--create-app", help="Create a new app registration")
    parser.add_argument("--description", help="Description for the app registration")
    parser.add_argument("--permissions", nargs="+", help="Required API permissions")
    parser.add_argument("--generate-module", help="Generate a Python module for an app")
    parser.add_argument("--list-apps", action="store_true", help="List registered applications")
    
    args = parser.parse_args()
    
    orchestrator = GraphAPIOrchestrator()
    
    if args.setup:
        orchestrator.setup_master_app()
    
    elif args.create_app:
        orchestrator.get_master_token()
        orchestrator.create_app_registration(
            args.create_app, 
            description=args.description,
            api_permissions=args.permissions
        )
    
    elif args.generate_module:
        orchestrator.generate_api_module(args.generate_module)
        
    elif args.list_apps:
        print("\n===== Registered Applications =====")
        for app in orchestrator.config["app_registrations"]:
            print(f"\nName: {app['name']}")
            print(f"Client ID: {app['client_id']}")
            print(f"Description: {app['description']}")
            print(f"Created: {app['creation_date']}")
            print(f"Secret Expires: {app['secret_expiry']}")
            print("Permissions:")
            for perm in app.get('permissions', []):
                print(f"  - {perm}")
            print("-" * 40)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()