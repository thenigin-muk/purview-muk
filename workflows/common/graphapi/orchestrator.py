#!/usr/bin/env python3
# file: workflows/common/graphapi/orchestrator.py
"""
Microsoft Graph API Orchestrator
Creates and manages specialized app registrations with least-privilege permissions
"""
import json
from pathlib import Path

from workflows.common import log_utils
from workflows.common.graphapi.auth import GraphAuth
from workflows.common.graphapi.app_manager import AppManager
from workflows.common.graphapi.secret_manager import SecretManager
from workflows.common.graphapi.module_generator import ModuleGenerator

class GraphAPIOrchestrator:
    """
    Orchestrates the creation and management of secure app registrations
    """
    
    def __init__(self, config_path=None, use_key_vault=False, dry_run=False):
        """Initialize the GraphAPI orchestrator"""
        log_utils.setup_logging()
        
        self.config_path = config_path or Path("./GraphAPI_config.json")
        self.use_key_vault = use_key_vault
        self.dry_run = dry_run  # Add this line
        self.config = self._load_config()
        
        # Pass dry_run to all components
        self.auth = GraphAuth(use_key_vault=use_key_vault, dry_run=dry_run)
        self.secret_manager = SecretManager(use_key_vault=use_key_vault, dry_run=dry_run)
        self.app_manager = AppManager(self.config, use_key_vault=use_key_vault, dry_run=dry_run)
        self.module_generator = ModuleGenerator(self.config, use_key_vault=use_key_vault, dry_run=dry_run)
        
    def _load_config(self):
        """Load the configuration file"""
        if not self.config_path.exists():
            log_utils.info(f"Configuration file not found, creating: {self.config_path}")
            return {"app_registrations": []}
            
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_utils.error(f"Invalid JSON in configuration file: {self.config_path}")
            return {"app_registrations": []}
            
    def _save_config(self):
        """Save the configuration to the file"""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
            
        log_utils.info(f"Configuration saved to {self.config_path}")
        
    def setup_master_app(self):
        """Guide the user through setting up the master app registration"""
        log_utils.info("Starting master app registration setup")
        
        print("\n====== MASTER APP REGISTRATION SETUP ======")
        print("This will guide you through setting up a master app registration")
        print("that will be used to create and manage other app registrations.")
        print("\n1. Go to Entra Admin Center > Applications > App Registrations")
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
        
        tenant_id = input("\nEnter your Azure AD tenant ID: ")
        client_id = input("Enter the Application (client) ID: ")
        client_secret = input("Enter the client secret value: ")
        
        # Save in config
        self.config["tenant_id"] = tenant_id
        self._save_config()
        
        # Save master secrets
        self.secret_manager.save_master_secrets(tenant_id, client_id, client_secret)
        
        print("\n✅ Master app registration setup completed")
        log_utils.info("Master app registration setup completed")
        
        return True
        
    def create_app(self, app_name, description=None, permissions=None):
        """Create a new app registration"""
        result = self.app_manager.create_app_registration(app_name, description, permissions)
        
        if result:
            self._save_config()
            log_utils.info(f"App registration created: {app_name}")
            return True
        else:
            log_utils.error(f"Failed to create app registration: {app_name}")
            return False
            
    def list_apps(self):
        """List all app registrations"""
        apps = self.app_manager.list_app_registrations()
        
        if not apps:
            print("\nNo app registrations found.")
            return False
            
        print("\n==== APP REGISTRATIONS ====")
        for i, app in enumerate(apps, 1):
            print(f"\n{i}. {app['name'].replace('Automation-', '')}")
            print(f"   ID: {app['id']}")
            print(f"   Client ID: {app['client_id']}")
            print(f"   Description: {app['description']}")
            print(f"   Created: {app['created']}")
            print(f"   Permissions: {', '.join(app['permissions']) if app['permissions'] else 'None'}")
            
        return True
        
    def generate_module(self, app_name, scopes=None):
        """Generate an API module for an app"""
        result = self.module_generator.generate_module(app_name, scopes)  # Change from generate_api_module to generate_module
        
        if result:
            log_utils.info(f"API module generated: {app_name}")
            return True
        else:
            log_utils.error(f"Failed to generate API module: {app_name}")
            return False
            
    def rotate_secret(self, app_name):
        """Rotate the client secret for an app"""
        result = self.app_manager.rotate_client_secret(app_name)
        
        if result:
            log_utils.info(f"Client secret rotated: {app_name}")
            return True
        else:
            log_utils.error(f"Failed to rotate client secret: {app_name}")
            return False

    def generate_api_module(self, app_name, scopes=None):
        """Generate a Python module for an app registration"""
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Would generate API module for: {app_name}")
            print(f"✅ [DRY RUN] Would generate API module in ./api_modules/{app_name}/")
            return True
            
        # Original implementation for non-dry-run mode
        # Find the app in the configuration...