# Description: Management of app registrations for Graph API
#!/usr/bin/env python3
# file: workflows/common/graphapi/app_manager.py
"""Management of app registrations for Graph API"""
import uuid
from datetime import datetime, timedelta

from workflows.common import log_utils
from workflows.common.graphapi.auth import GraphAuth
from workflows.common.graphapi.secret_manager import SecretManager

class AppManager:
    """Manages app registrations in Azure AD"""
    
    def __init__(self, config, use_key_vault=False, dry_run=False):
        """Initialize app manager with configuration"""
        self.config = config
        self.use_key_vault = use_key_vault
        self.dry_run = dry_run
        self.auth = GraphAuth(use_key_vault=use_key_vault, dry_run=dry_run)
        self.secret_manager = SecretManager(use_key_vault=use_key_vault, dry_run=dry_run)
        
    def create_app_registration(self, app_name, description=None, permissions=None):
        """Create a new app registration"""
        app_display_name = f"Automation-{app_name}"
        
        # Check if app already exists in config
        for app in self.config.get("app_registrations", []):
            if app["name"] == app_display_name:
                log_utils.info(f"App registration already exists: {app_display_name}")
                print(f"ℹ️ App registration already exists: {app_display_name}")
                return True
        
        # Handle dry run mode
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Would create app registration: {app_name}")
            
            # Create mock app data for dry run
            app_config = {
                "name": app_display_name,
                "id": f"dry-run-app-id-{app_name}",
                "client_id": f"dry-run-client-id-{app_name}",
                "description": description or f"Automation app for {app_name}",
                "created": datetime.now().isoformat(),
                "permissions": permissions or []
            }
            
            # Add to config without saving
            self.config.setdefault("app_registrations", []).append(app_config)
            
            print(f"\n✅ [DRY RUN] App registration would be created: {app_display_name}")
            print(f"   Application (client) ID would be: {app_config['client_id']}")
            
            return True
            
        # Original implementation for non-dry-run mode
        # Get token with master app
        token = self.auth.get_master_token()
        if not token:
            log_utils.error("Failed to get master token for app creation")
            return False
            
        # Prepare app registration data
        display_name = f"Automation-{app_name}"
        app_data = {
            "displayName": display_name,
            "signInAudience": "AzureADMyOrg",
            "api": {
                "requestedAccessTokenVersion": 2
            },
            "tags": ["Automation", "GraphAPI"]
        }
        
        if description:
            app_data["notes"] = description
            
        # Create app registration
        log_utils.info(f"Creating app registration: {display_name}")
        result = self.auth.make_graph_request('post', '/applications', data=app_data, token=token)
        
        if not result:
            log_utils.error(f"Failed to create app registration: {display_name}")
            return False
            
        app_id = result.get("id")
        client_id = result.get("appId")
        
        if not app_id or not client_id:
            log_utils.error("Missing app ID or client ID in response")
            return False
            
        log_utils.info(f"App registration created: {display_name} (ID: {app_id})")
        
        # Create client secret
        client_secret = self._create_client_secret(app_id, token)
        if not client_secret:
            log_utils.error(f"Failed to create client secret for {display_name}")
            return False
            
        # Add permissions if specified
        if permissions:
            for permission in permissions:
                self._add_permission(app_id, permission, token)
                
        # Store in config
        if "app_registrations" not in self.config:
            self.config["app_registrations"] = []
            
        app_info = {
            "name": display_name,
            "id": app_id,
            "client_id": client_id,
            "description": description or "",
            "created": datetime.now().isoformat(),
            "permissions": permissions or []
        }
        
        self.config["app_registrations"].append(app_info)
        
        # Save app secrets
        self.secret_manager.save_app_secrets(
            app_name,
            client_id,
            client_secret,
            self.config.get("tenant_id", "")
        )
        
        return True
        
    def _create_client_secret(self, app_id, token):
        """Create a client secret for an app registration"""
        # Prepare secret data
        secret_data = {
            "passwordCredential": {
                "displayName": f"Secret-{datetime.now().strftime('%Y%m%d')}",
                "endDateTime": (datetime.now() + timedelta(days=365)).isoformat()
            }
        }
        
        # Create secret
        result = self.auth.make_graph_request(
            'post',
            f'/applications/{app_id}/addPassword',
            data=secret_data,
            token=token
        )
        
        if not result or "secretText" not in result:
            log_utils.error("Failed to create client secret")
            return None
            
        return result["secretText"]
        
    def _add_permission(self, app_id, permission, token):
        """Add a permission to an app registration"""
        # Get Microsoft Graph resource ID
        graph_id = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph
        
        # Find permission ID
        permission_id = self._get_permission_id(permission, token)
        if not permission_id:
            log_utils.error(f"Permission not found: {permission}")
            return False
            
        # Get current permissions
        app_info = self.auth.make_graph_request('get', f'/applications/{app_id}', token=token)
        if not app_info:
            log_utils.error(f"Failed to get app info for {app_id}")
            return False
            
        # Check if permission already exists
        required_resource_access = app_info.get("requiredResourceAccess", [])
        graph_resource = None
        
        for resource in required_resource_access:
            if resource.get("resourceAppId") == graph_id:
                graph_resource = resource
                break
                
        if graph_resource:
            # Check if permission already exists
            for res_access in graph_resource.get("resourceAccess", []):
                if res_access.get("id") == permission_id and res_access.get("type") == "Role":
                    log_utils.info(f"Permission already exists: {permission}")
                    return True
                    
            # Add permission to existing resource
            graph_resource["resourceAccess"].append({
                "id": permission_id,
                "type": "Role"
            })
        else:
            # Add new resource with permission
            required_resource_access.append({
                "resourceAppId": graph_id,
                "resourceAccess": [
                    {
                        "id": permission_id,
                        "type": "Role"
                    }
                ]
            })
            
        # Update app registration
        update_data = {
            "requiredResourceAccess": required_resource_access
        }
        
        result = self.auth.make_graph_request(
            'patch',
            f'/applications/{app_id}',
            data=update_data,
            token=token
        )
        
        if not result:
            log_utils.error(f"Failed to add permission: {permission}")
            return False
            
        log_utils.info(f"Added permission: {permission}")
        return True
        
    def _get_permission_id(self, permission_name, token):
        """Get the ID for a permission name"""
        # Get Microsoft Graph service principal
        graph_id = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph
        
        result = self.auth.make_graph_request(
            'get',
            f'/servicePrincipals?$filter=appId eq \'{graph_id}\'',
            token=token
        )
        
        if not result or "value" not in result or not result["value"]:
            log_utils.error("Failed to get Microsoft Graph service principal")
            return None
            
        sp = result["value"][0]
        
        # Find permission in app roles
        for role in sp.get("appRoles", []):
            if role.get("value") == permission_name:
                return role.get("id")
                
        log_utils.error(f"Permission not found: {permission_name}")
        return None
        
    def list_app_registrations(self):
        """List all app registrations in the config"""
        if "app_registrations" not in self.config or not self.config["app_registrations"]:
            log_utils.info("No app registrations found in config")
            return []
            
        return self.config["app_registrations"]
        
    def rotate_client_secret(self, app_name):
        """Rotate the client secret for an app"""
        # Handle dry run mode
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Would rotate client secret for: {app_name}")
            print(f"✅ [DRY RUN] Would rotate client secret for app: {app_name}")
            return True
            
        # Original implementation
        # Get token
        token = self.auth.get_master_token()
        if not token:
            log_utils.error("Failed to get master token for secret rotation")
            return False
            
        # Find app in config
        display_name = f"Automation-{app_name}"
        app_info = None
        
        for app in self.config.get("app_registrations", []):
            if app.get("name") == display_name:
                app_info = app
                break
                
        if not app_info:
            log_utils.error(f"App registration not found: {display_name}")
            return False
            
        app_id = app_info.get("id")
        client_id = app_info.get("client_id")
        
        # Create new client secret
        client_secret = self._create_client_secret(app_id, token)
        if not client_secret:
            log_utils.error(f"Failed to create client secret for {display_name}")
            return False
            
        # Save app secrets
        self.secret_manager.save_app_secrets(
            app_name,
            client_id,
            client_secret,
            self.config.get("tenant_id", "")
        )
        
        log_utils.info(f"Rotated client secret for {display_name}")
        return True