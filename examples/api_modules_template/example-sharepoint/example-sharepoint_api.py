#!/usr/bin/env python3
# filepath: examples/api_modules_template/example-sharepoint/example-sharepoint_api.py
"""
SHAREPOINT API Module
Auto-generated secure access module for sharepoint operations
Generated: 2025-03-19T14:48:02.720309
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

class SharepointClient:
    """Client for sharepoint API operations"""
    
    def __init__(self):
        """Initialize the sharepoint API client"""
        self.token = None
        self.token_expiry = None
        self.client = None
        
        # Load credentials
        client_id, client_secret, tenant_id = self._load_credentials()
        
        # Initialize the MSAL app
        self.app = ConfidentialClientApplication(
            client_id=client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            client_credential=client_secret
        )
    
    def _load_credentials(self):
        """Load credentials from the environment or secret file"""
        # First try environment variables
        client_id = os.getenv("SHAREPOINT_CLIENT_ID")
        client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
        tenant_id = os.getenv("TENANT_ID")
        
        # If not available, try the secret file
        if not all([client_id, client_secret, tenant_id]):
            secret_file = f".env.sharepoint.secret"
            if os.path.exists(secret_file):
                with open(secret_file, "r") as f:
                    env_content = f.read()
                
                # Parse environment variables
                for line in env_content.split('\n'):
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if key == "SHAREPOINT_CLIENT_ID":
                            client_id = value
                        elif key == "SHAREPOINT_CLIENT_SECRET":
                            client_secret = value
                        elif key == "TENANT_ID":
                            tenant_id = value
        
        if not all([client_id, client_secret, tenant_id]):
            log_utils.error("Missing credentials for sharepoint API")
            raise ValueError(
                f"Missing credentials for sharepoint API. "
                "Please ensure environment variables or secret file are properly set."
            )
        
        return client_id, client_secret, tenant_id
    
    def get_access_token(self):
        """Get an access token for the API"""
        # Check if we have a valid token
        if self.token and self.token_expiry and self.token_expiry > datetime.now():
            return self.token
        
        # Get a new token
        scopes = ["https://graph.microsoft.com/.default"]
        result = self.app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            self.token = result["access_token"]
            # Set expiry time (token typically valid for 1 hour)
            self.token_expiry = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
            log_utils.debug("Obtained access token for sharepoint API")
            return self.token
        else:
            error = result.get("error", "unknown")
            error_desc = result.get("error_description", "")
            log_utils.error("Failed to get access token: {} - {}", error, error_desc)
            raise Exception(f"Failed to get access token: {error} - {error_desc}")
    
    def get_headers(self):
        """Get authorization headers for API requests"""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    # Add specialized methods for sharepoint operations below
    # For example:
    
    def make_api_request(self, method, endpoint, data=None, params=None):
        """Make a request to the API"""
        import requests
        
        headers = self.get_headers()
        url = f"{GRAPH_API_ENDPOINT}{endpoint}"
        
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, json=data, params=params)
        elif method.lower() == 'patch':
            response = requests.patch(url, headers=headers, json=data)
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            log_utils.error("Unsupported HTTP method: {}", method)
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code >= 400:
            log_utils.error("API request failed: {} - {}", response.status_code, response.text)
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        log_utils.debug("sharepoint API request successful: {}", endpoint)
        return response.json() if response.content else None

# Create a client instance
_client = None

def get_client():
    """Get the sharepoint API client"""
    global _client
    if _client is None:
        _client = SharepointClient()
    return _client

def get_access_token():
    """Get an access token for sharepoint API operations"""
    return get_client().get_access_token()

# Example usage:
# client = get_client()
# result = client.make_api_request('get', '/me')
