#!/usr/bin/env python3
# file: workflows/common/sp_metadata_utils.py
import requests
import os
import json
from msal import ConfidentialClientApplication
from datetime import datetime

# Import our custom logging utilities
from workflows.common import log_utils
from workflows.common.log_utils import Messages

# Initialize logging
log_utils.setup_logging()

# Try to import dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    log_utils.warning(Messages.Auth.DOTENV_MISSING)

def get_access_token():
    """Get Microsoft Graph API access token."""
    # Load environment variables from .env file if available
    try:
        load_dotenv()
    except Exception as e:
        log_utils.warning(Messages.Auth.ENV_LOAD_ERROR, e)
    
    client_id = os.getenv("SHAREPOINT_CLIENT_ID")
    client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")
    
    # Verify environment variables
    if not all([client_id, client_secret, tenant_id]):
        log_utils.error(Messages.Auth.ENV_MISSING)
        return None
        
    # Initialize the MSAL confidential client application
    app = ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret
    )
    
    # Get token for SharePoint Online scope
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    
    if "access_token" in result:
        log_utils.debug(Messages.Auth.TOKEN_SUCCESS)
        return result["access_token"]
    else:
        log_utils.error(Messages.Auth.TOKEN_ERROR, result.get('error'))
        log_utils.error(Messages.Auth.TOKEN_ERROR_DESC, result.get('error_description'))
        return None

def get_site_id(token, site_url, verbose=False):
    """Get SharePoint site ID from URL."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Extract hostname and relative path from URL
    from urllib.parse import urlparse
    parsed_url = urlparse(site_url)
    hostname = parsed_url.netloc
    site_path = parsed_url.path
    
    if verbose:
        log_utils.info("Parsed URL: hostname={}, path={}", hostname, site_path)
    api_url = None
    
    # Case 1: Root site
    if site_path == "/":
        api_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/"
    
    # Case 2: Site collection (/sites/sitename)
    elif site_path.startswith("/sites/"):
        parts = site_path.split("/")
        if len(parts) >= 3:  # "/sites/name" has 3 parts when split
            site_name = parts[2]
            
            # Case 2a: Just the site collection
            if len(parts) == 3 or (len(parts) == 4 and parts[3] == ""):
                api_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{site_name}:"
            
            # Case 2b: Site collection with subsite(s)
            else:
                # Build the full path including all subsites
                full_path = "/sites/" + "/".join(parts[2:])
                if full_path.endswith("/"):
                    full_path = full_path[:-1]  # Remove trailing slash
                api_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:{full_path}"
    
    # Case 3: Other paths
    else:
        api_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:{site_path}"
    
    if verbose:
        log_utils.info("Using API URL: {}", api_url)
    
    # Make the API request to get site information
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        site_data = response.json()
        if verbose:
            log_utils.info("Success! Site name: {}", site_data.get('displayName'))
        return site_data.get('id')
    else:
        log_utils.error("Error retrieving site: Status {} - {}", response.status_code, response.text)
        return None

def get_lists(token, site_id):
    """Get all lists in the SharePoint site."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        lists_data = response.json()
        return lists_data.get('value', [])
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving lists: Status {} - {}", response.status_code, response.text)

def get_list_columns(token, site_id, list_id):
    """Get all columns (fields) for a specific list."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        columns_data = response.json()
        return columns_data.get('value', [])
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving columns: Status {} - {}", response.status_code, response.text)

def map_sp_type_to_schema(column):
    """Map SharePoint column type to our schema format."""
    # Different places where type information might be stored
    lookup_keys = ['text', 'dateTime', 'boolean', 'number', 'choice', 'lookup', 'personOrGroup', 'hyperlink', 'calculated']
    
    # Determine column type
    column_type = "Text"  # Default
    
    # Check if it's a managed metadata field
    if column.get('termSetId') or "taxonomy" in str(column).lower():
        return "Managed Metadata"
    
    # Check for other types
    for key in lookup_keys:
        if column.get(key):
            if key == 'dateTime':
                return "Date"
            elif key == 'choice':
                return "Choice"
            elif key == 'lookup':
                return "Lookup"
            elif key == 'hyperlink':
                return "Hyperlink"
            elif key == 'personOrGroup':
                return "Person"
            else:
                return key.capitalize()
    
    return column_type

def get_site_columns(token, site_id):
    """Get all site columns defined at the site level."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/columns"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        columns_data = response.json()
        return columns_data.get('value', [])
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving site columns: Status {} - {}", response.status_code, response.text)

def extract_metadata_schema(site_url, list_name=None, verbose=False, detailed=False):
    """
    Extract metadata schema from a SharePoint site and list.
    
    Args:
        site_url: URL of the SharePoint site
        list_name: Name of the list/library (optional)
        verbose: log detailed progress information
        detailed: Include extended column details and site columns
    
    Returns:
        Dict containing extracted schema or None if failed
    """
    if verbose:
        log_utils.info("Extracting metadata schema from {}", site_url)
    
    token = get_access_token()
    if not token:
        log_utils.error("Failed to get access token")
        return None
    
    site_id = get_site_id(token, site_url, verbose)
    if not site_id:
        log_utils.error("Failed to get site ID for {}", site_url)
        return None
    
    # Get site columns if detailed info is requested
    site_columns_dict = {}
    if detailed:
        if verbose:
            log_utils.info("Getting site columns...")
        site_columns = get_site_columns(token, site_id)
        site_columns_dict = {col.get('name'): col for col in site_columns}
        if verbose:
            log_utils.info("Found {} site columns", len(site_columns))
    
    lists = get_lists(token, site_id)
    if not lists:
        log_utils.error("No lists found in the site")
        return None
    
    # Process all lists or just the specified one
    target_lists = [l for l in lists if not list_name or l.get('displayName') == list_name]
    
    if list_name and not target_lists:
        if verbose:
            log_utils.error("List '{}' not found. Available lists:", list_name)
            for l in lists:
                log_utils.error("  - {}", l.get('displayName'))
        return None
    
    all_schemas = []
    
    for lst in target_lists:
        list_id = lst.get('id')
        list_display_name = lst.get('displayName')
        
        if verbose:
            log_utils.info("Processing list: {}", list_display_name)
        
        # Get list columns
        columns = get_list_columns(token, site_id, list_id)
        
        workflow_name = list_display_name.lower().replace(" ", "_")
        schema = {
            "workflow": workflow_name,
            "metadata": []
        }
        
        # Skip system columns
        system_columns = ["ContentType", "ID", "Created", "Modified", "Author", "Editor", "_UIVersionString", 
                         "Attachments", "Edit", "LinkTitleNoMenu", "LinkTitle", "LinkTitle2", 
                         "DocIcon", "ItemChildCount", "FolderChildCount", "FileLeafRef", "_HasCopyDestinations",
                         "_CopySource", "owshiddenversion", "WorkflowVersion", "_UIVersion", "ParentLeafName"]
        
        for column in columns:
            name = column.get('name')
            if name in system_columns or name.startswith('_'):
                continue
            
            # Basic field info
            field = {
                "name": column.get('displayName'),
                "type": map_sp_type_to_schema(column),
                "description": column.get('description', "")
            }
            
            # Add options for choice fields
            if field["type"] == "Choice" and column.get('choice', {}).get('choices'):
                field["options"] = column.get('choice', {}).get('choices', [])
            
            # Add additional details if requested
            if detailed:
                # Include the raw column data for reference
                field["raw_column_data"] = column
                
                # Add column name (internal name)
                field["internal_name"] = name
                
                # Check if this is a site column
                is_site_column = name in site_columns_dict
                field["is_site_column"] = is_site_column
                
                # Add column ID
                if "id" in column:
                    field["id"] = column.get('id')
                
                # Add source if it's a site column
                if is_site_column:
                    field["source"] = "Site Column"
                    # Include site column definition
                    field["site_column_data"] = site_columns_dict[name]
                else:
                    field["source"] = "List Column"
                
                # Add common attributes
                for attr in ["enforceUniqueValues", "indexed", "required", "readOnly", "hidden"]:
                    if attr in column and column.get(attr):
                        field[attr] = column.get(attr)
                
                # Add format information for Date fields
                if field["type"] == "Date" and "dateTime" in column:
                    if "format" in column["dateTime"]:
                        field["dateFormat"] = column["dateTime"]["format"]
                    if "displayAs" in column["dateTime"]:
                        field["dateDisplayAs"] = column["dateTime"]["displayAs"]
                
                # Add text field properties
                if field["type"] == "Text" and "text" in column:
                    for text_attr in ["maxLength", "allowMultipleLines", "appendChanges", "linesForEditing"]:
                        if text_attr in column["text"] and column["text"][text_attr]:
                            field[text_attr] = column["text"][text_attr]
                
                # Add term set ID for managed metadata
                if field["type"] == "Managed Metadata" and "termSet" in column:
                    field["termSet"] = column["termSet"]
                
                # Add lookup information
                if field["type"] == "Lookup" and "lookup" in column:
                    field["lookup"] = column["lookup"]
            
            schema["metadata"].append(field)
        
        all_schemas.append(schema)
    
    return all_schemas[0] if list_name and len(all_schemas) == 1 else all_schemas

def compare_schemas(current_schema, target_schema):
    """
    Compare current SharePoint schema with target schema to identify changes needed.
    
    Args:
        current_schema: Schema extracted from SharePoint
        target_schema: Schema defined in metadata-schema.json
        
    Returns:
        Dict with fields to add, update, and remove
    """
    # Extract fields by name for easier comparison
    current_fields = {field["name"]: field for field in current_schema["metadata"]}
    target_fields = {field["name"]: field for field in target_schema["metadata"]}
    
    # Fields to add (in target but not in current)
    to_add = []
    for name, field in target_fields.items():
        if name not in current_fields:
            to_add.append(field)
    
    # Fields to update (in both but different)
    to_update = []
    for name, target_field in target_fields.items():
        if name in current_fields:
            current_field = current_fields[name]
            # Check if any property is different
            if target_field["type"] != current_field["type"] or \
               target_field.get("description") != current_field.get("description") or \
               (target_field.get("options") != current_field.get("options") and "options" in target_field):
                to_update.append(target_field)
    
    # Fields to remove (in current but not in target)
    to_remove = []
    for name, field in current_fields.items():
        if name not in target_fields:
            to_remove.append(field)
    
    return {
        "to_add": to_add,
        "to_update": to_update,
        "to_remove": to_remove
    }

def save_schema_to_file(schema, filename=None):
    """Save schema to JSON file with optional filename."""
    if not filename:
        workflow_name = schema.get("workflow", "generic")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./extracted_schemas/{workflow_name}_schema_{timestamp}.json"
        
        # Create directory if it doesn't exist
        os.makedirs("./extracted_schemas", exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(schema, f, indent=2)
        
    return filename

def list_document_libraries(token, site_id):
    """Get all document libraries in the SharePoint site."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        lists_data = response.json()
        # Filter to only show document libraries
        libraries = []
        for list_item in lists_data.get('value', []):
            # Check for documentLibrary template
            if list_item.get('list', {}).get('template') == 'documentLibrary':
                libraries.append(list_item)
        return libraries
    else:
        log_utils.error("Error retrieving lists: Status {} - {}", response.status_code, response.text)
        return []

def get_content_types(token, site_id):
    """Get all content types in the site."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/contentTypes"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('value', [])
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving content types: Status {} - {}", response.status_code, response.text)

def get_site_features(token, site_id):
    """Get site features information."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Note: Direct feature access is limited in Graph API
    # This is a simplified implementation that doesn't fully
    # expose all SharePoint features but gives some site properties
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Return available properties as "features"
        features = []
        if 'sharepointIds' in data:
            features.append({
                "name": "SharePoint IDs",
                "data": data['sharepointIds']
            })
        if 'siteCollection' in data:
            features.append({
                "name": "Site Collection",
                "data": data['siteCollection']
            })
        if 'templates' in data:
            features.append({
                "name": "Site Template", 
                "data": data['templates']
            })
        return features
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving site features: Status {} - {}", response.status_code, response.text)

def get_list_settings(token, site_id, list_id):
    """Get detailed list settings."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get list properties
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        list_data = response.json()
        
        # Get list content types
        content_types_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/contentTypes"
        ct_response = requests.get(content_types_url, headers=headers)
        
        if ct_response.status_code == 200:
            list_data['contentTypes'] = ct_response.json().get('value', [])
        
        return list_data
    else:
        from workflows.common import log_utils
        log_utils.error("Error retrieving list settings: Status {} - {}", response.status_code, response.text)

def extract_comprehensive_site_schema(site_url, specific_list=None, verbose=False, detailed=False):
    """
    Extract comprehensive site information including columns, content types, features, and lists.
    
    Args:
        site_url: URL of the SharePoint site
        specific_list: Name of a specific list to focus on (optional)
        verbose: log detailed progress information
        detailed: Include raw SharePoint API data
    
    Returns:
        Dict containing comprehensive site schema or None if failed
    """
    if verbose:
        log_utils.info("Extracting comprehensive information from {}", site_url)
    
    token = get_access_token()
    if not token:
        log_utils.error("Failed to get access token")
        return None
    
    site_id = get_site_id(token, site_url, verbose)
    if not site_id:
        log_utils.error("Failed to get site ID for {}", site_url)
        return None
    
    # Prepare the comprehensive schema
    comprehensive_schema = {
        "site_url": site_url,
        "site_id": site_id,
        "extraction_date": datetime.now().isoformat(),
        "site_columns": [],
        "content_types": [],
        "features": [],
        "lists": []
    }
    
    # 1. Get site columns
    if verbose:
        log_utils.info("Extracting site columns...")
    site_columns = get_site_columns(token, site_id)
    comprehensive_schema["site_columns"] = site_columns
    if verbose:
        log_utils.info("Found {} site columns", len(site_columns))
    
    # 2. Get content types
    if verbose:
        log_utils.info("Extracting content types...")
    content_types = get_content_types(token, site_id)
    comprehensive_schema["content_types"] = content_types
    if verbose:
        log_utils.info("Found {} content types", len(content_types))
    
    # 3. Get site features
    if verbose:
        log_utils.info("Extracting site features...")
    features = get_site_features(token, site_id)
    comprehensive_schema["features"] = features
    if verbose:
        log_utils.info("Found {} site features/properties", len(features))
    
    # 4. Get lists and their settings
    if verbose:
        log_utils.info("Extracting lists and libraries...")
    
    lists = get_lists(token, site_id)
    
    # If specific list is provided, filter to just that list
    if specific_list:
        filtered_lists = [l for l in lists if l.get('displayName') == specific_list]
        if not filtered_lists:
            if verbose:
                log_utils.error("List '{}' not found", specific_list)
                log_utils.info("Available lists:")
                for lst in lists:
                    log_utils.info("  - {}", lst.get('displayName'))
            return None
        lists = filtered_lists
    
    processed_lists = []
    for lst in lists:
        list_id = lst.get('id')
        list_name = lst.get('displayName')
        
        if verbose:
            log_utils.info("Processing list: {}", list_name)
        
        # Get detailed list settings
        list_settings = get_list_settings(token, site_id, list_id)
        
        # Get list columns
        columns = get_list_columns(token, site_id, list_id)
        
        # Process columns to match our schema format
        processed_columns = []
        
        # Skip system columns
        system_columns = ["ContentType", "ID", "Created", "Modified", "Author", "Editor", "_UIVersionString", 
                         "Attachments", "Edit", "LinkTitleNoMenu", "LinkTitle", "LinkTitle2", 
                         "DocIcon", "ItemChildCount", "FolderChildCount", "FileLeafRef", "_HasCopyDestinations",
                         "_CopySource", "owshiddenversion", "WorkflowVersion", "_UIVersion", "ParentLeafName"]
        
        for column in columns:
            name = column.get('name')
            if name in system_columns or name.startswith('_'):
                continue
                
            field = {
                "name": column.get('displayName'),
                "type": map_sp_type_to_schema(column),
                "description": column.get('description', "")
            }
            
            # Add options for choice fields
            if field["type"] == "Choice" and column.get('choice', {}).get('choices'):
                field["options"] = column.get('choice', {}).get('choices', [])
            
            # Add detailed metadata if requested
            if detailed:
                field["raw_column_data"] = column
                field["internal_name"] = name
                field["id"] = column.get('id')
                
                # Identify if this is a site column
                is_site_column = any(sc.get('name') == name for sc in site_columns)
                field["is_site_column"] = is_site_column
                
                # Add source information
                if is_site_column:
                    field["source"] = "Site Column"
                else:
                    field["source"] = "List Column"
            
            processed_columns.append(field)
        
        # Create processed list entry
        list_entry = {
            "name": list_name,
            "id": list_id,
            "columns": processed_columns
        }
        
        # Add list settings and details if requested
        if detailed:
            list_entry["settings"] = list_settings
            
            # Check if document library
            is_document_library = lst.get('list', {}).get('template') == 'documentLibrary'
            list_entry["is_document_library"] = is_document_library
            
            # Add content types used by this list
            if 'contentTypes' in list_settings:
                list_entry["content_types"] = list_settings['contentTypes']
        
        processed_lists.append(list_entry)
    
    comprehensive_schema["lists"] = processed_lists
    
    return comprehensive_schema