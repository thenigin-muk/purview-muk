# Description: This script lists all document libraries in a SharePoint site.
#!/usr/bin/env python3
# file: workflows/common/find_libraries.py
import sys
import os
import argparse

# Add the common directory to the path so we can import the module
sys.path.append(os.path.dirname(__file__))

import sp_metadata_utils as sp

def main():
    """List all document libraries in a SharePoint site."""
    parser = argparse.ArgumentParser(
        description='SharePoint Library Finder - List all document libraries in a site'
    )
    
    parser.add_argument('--site', required=True, help='SharePoint site URL')
    
    args = parser.parse_args()
    
    print(f"\n📚 SharePoint Library Finder")
    print("=========================")
    print(f"Site URL: {args.site}")
    
    token = sp.get_access_token()
    if not token:
        print("❌ Failed to get access token")
        return 1
        
    site_id = sp.get_site_id(token, args.site)
    if not site_id:
        print(f"❌ Failed to get site ID for {args.site}")
        return 1
        
    libraries = sp.list_document_libraries(token, site_id)
    
    if libraries:
        print(f"\nFound {len(libraries)} document libraries:")
        print("\nName                          | URL Path")
        print("------------------------------|--------------------------------")
        for lib in libraries:
            name = lib.get('displayName', '')
            path = lib.get('webUrl', '').split('/sites/')[-1] if 'webUrl' in lib else ''
            print(f"{name[:30]:<30} | sites/{path}")
            
        print("\n✅ To extract metadata from a library, use:")
        print(f"python workflows/common/sp_metadata_tool.py --site \"{args.site}\" --library \"LIBRARY_NAME\"")
    else:
        print("❌ No document libraries found")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())