#!/usr/bin/env python3
# file: workflows/common/graphapi/auth.py
"""Authentication handling for Graph API"""
import os
import msal
from datetime import datetime, timedelta

from workflows.common import log_utils
from workflows.common.graphapi.secret_manager import SecretManager

class GraphAuth:
    """Handles authentication with Microsoft Graph API"""
    
    def __init__(self, tenant_id=None, client_id=None, client_secret=None, use_key_vault=False, dry_run=False):
        """Initialize Graph API authentication helper"""
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = None
        self.use_key_vault = use_key_vault
        self.secret_manager = SecretManager(use_key_vault=use_key_vault, dry_run=dry_run)
        self.dry_run = dry_run
        
    def get_token(self, scopes=None, force_refresh=False):
        """Get an access token for Microsoft Graph API"""
        # Check if we have a valid token
        if not force_refresh and self.token and self.token_expiry and self.token_expiry > datetime.now():
            return self.token
            
        if not scopes:
            scopes = ["https://graph.microsoft.com/.default"]
            
        # Make sure we have the credentials
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            log_utils.error("Missing credentials for authentication")
            return None
            
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            self.token = result["access_token"]
            # Set expiry time (token typically valid for 1 hour)
            self.token_expiry = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
            log_utils.info("Acquired access token for Graph API")
            return self.token
        else:
            error = result.get('error', 'Unknown')
            error_desc = result.get('error_description', '')
            log_utils.error(f"Failed to get token: {error} - {error_desc}")
            return None
            
    def get_master_token(self):
        """Get an access token for the master app"""
        if self.dry_run:
            log_utils.info("[DRY RUN] Would get master token")
            return "dry-run-token-123456789"
            
        # Check if we have a valid token
        if self.token and self.token_expiry and self.token_expiry > datetime.now():
            return self.token
        
        # Try to load master secrets
        tenant_id, client_id, client_secret = self.secret_manager.get_master_secrets()
        
        if not all([tenant_id, client_id, client_secret]):
            log_utils.error("Missing master app credentials")
            return None
            
        # Set credentials and get token
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        
        return self.get_token(force_refresh=True)
        
    def get_app_token(self, app_name, scopes=None):
        """Get an access token for a specific app registration"""
        # Try to load app secrets
        client_id, client_secret, tenant_id = self.secret_manager.get_app_secrets(app_name)
        
        if not all([client_id, client_secret, tenant_id]):
            log_utils.error(f"Missing credentials for {app_name} app")
            return None
            
        # Set credentials and get token
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        
        return self.get_token(scopes=scopes, force_refresh=True)
        
    def make_graph_request(self, method, endpoint, data=None, params=None, token=None):
        """Make a request to Microsoft Graph API"""
        if self.dry_run:
            log_utils.info(f"[DRY RUN] Graph API {method.upper()} request to {endpoint}")
            # Return mock responses based on the endpoint
            if endpoint == '/applications':
                return {
                    "id": "dry-run-app-id-123",
                    "appId": "dry-run-client-id-123",
                    "displayName": data.get("displayName", "Dry Run App")
                }
            elif 'addPassword' in endpoint:
                return {
                    "secretText": "dry-run-secret-123456789"
                }
            elif 'servicePrincipals' in endpoint:
                return {
                    "value": [
                        {
                            "id": "sp-id-123",
                            "appRoles": [
                                {
                                    "id": "role-id-123",
                                    "value": "User.Read"
                                },
                                {
                                    "id": "role-id-456",
                                    "value": "Directory.Read.All"
                                }
                            ]
                        }
                    ]
                }
            else:
                # Generic mock response
                return {"status": "success", "message": f"Dry run successful for {endpoint}"}
                
        # Only proceed with real request if not in dry run mode
        import requests
        
        if not token:
            token = self.get_master_token()
            if not token:
                log_utils.error("Failed to get token for Graph API request")
                return None
                
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, params=params)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=data, params=params)
            elif method.lower() == 'patch':
                response = requests.patch(url, headers=headers, json=data)
            elif method.lower() == 'delete':
                response = requests.delete(url, headers=headers)
            else:
                log_utils.error(f"Unsupported HTTP method: {method}")
                return None
                
            if response.status_code >= 400:
                log_utils.error(f"Graph API request failed: {response.status_code} - {response.text}")
                return None
                
            return response.json() if response.content else {}
        except Exception as e:
            log_utils.error(f"Error making Graph API request: {str(e)}")
            return None