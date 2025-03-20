# Description: This script is used to extract metadata from SharePoint lists and libraries, compare against target schemas, and generate reports on differences.
#!/usr/bin/env python3
# file: workflows/common/sp_metadata_tool.py
"""
SharePoint Metadata Tool - Extract, analyze and compare SharePoint metadata schemas.

This tool can extract metadata from SharePoint lists and libraries,
compare against target schemas, and generate reports on differences.
"""

import os
import json
import sys
import argparse
from datetime import datetime

# Add the common directory to the path so we can import the modules
sys.path.append(os.path.dirname(__file__))

# Import our custom modules
import sp_metadata_utils as sp
from log_utils import setup_logging, Messages
import log_utils

# Initialize logging
setup_logging()

def main():
    """SharePoint metadata tool for extraction and analysis."""
    parser = argparse.ArgumentParser(
        description='SharePoint Metadata Tool - Extract and analyze SharePoint metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract metadata from a specific list/library
  python sp_metadata_tool.py --site "https://contoso.sharepoint.com/sites/ProjectX" --list "Documents" --output schema.json
  
  # List all document libraries in a site
  python sp_metadata_tool.py --site "https://contoso.sharepoint.com/sites/ProjectX" --list-libraries
  
  # Extract comprehensive site information (no specific list needed)
  python sp_metadata_tool.py --site "https://contoso.sharepoint.com/sites/ProjectX" --comprehensive --output site_inventory.json
  
  # Extract and analyze against target schema
  python sp_metadata_tool.py --site "https://contoso.sharepoint.com/sites/ProjectX" --list "Documents" --analyze --schema metadata-schema.json
        """
    )
    
    parser.add_argument('--site', required=True, help='SharePoint site URL')
    parser.add_argument('--output', help='Path to save extracted schema (default: auto-generated filename)')
    parser.add_argument('--analyze', action='store_true', help='Compare extracted schema with target schema')
    parser.add_argument('--schema', help='Path to target schema for analysis (required with --analyze)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed progress information')
    parser.add_argument('--list-libraries', action='store_true', 
                        help='List all document libraries in the site and exit')
    parser.add_argument('--detailed', action='store_true', 
                        help='Include extended column information and site columns')
    parser.add_argument('--comprehensive', action='store_true',
                        help='Extract comprehensive site information (columns, content types, features)')
    
    # List and library are now optional if using comprehensive mode
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', help='List or document library name (e.g., "Documents", "Tasks")')
    group.add_argument('--library', dest='list', help='Document library name (alias for --list)')
    
    args = parser.parse_args()
    
    # Make sure a list is provided or comprehensive mode is used or list-libraries is used
    if not (args.list or args.list_libraries or args.comprehensive):
        log_utils.error(Messages.Tool.ARG_ERROR)
        parser.print_help()
        return 1
    
    # List all libraries if requested
    if args.list_libraries:
        log_utils.info("Listing document libraries for: {}", args.site)
        token = sp.get_access_token()
        if not token:
            log_utils.error(Messages.Auth.TOKEN_FAILURE)
            return 1
            
        site_id = sp.get_site_id(token, args.site)
        if not site_id:
            log_utils.error(Messages.Site.SITE_ID_FAILURE, args.site)
            return 1
            
        libraries = sp.list_document_libraries(token, site_id)
        
        if libraries:
            log_utils.info(Messages.Lists.LIBRARIES_FOUND, len(libraries))
            for lib in libraries:
                log_utils.info("  • {}", lib.get('displayName'))
        else:
            log_utils.error(Messages.Lists.LIBRARIES_NONE)
        
        return 0
    
    # Validation: If analyze is specified, schema must be provided
    if args.analyze and not args.schema:
        log_utils.error(Messages.Tool.SCHEMA_REQUIRED)
        parser.print_help()
        return 1
    
    log_utils.info(Messages.Tool.TOOL_HEADER)
    log_utils.info(Messages.Tool.TOOL_SEPARATOR)
    log_utils.info(Messages.Tool.SITE_URL, args.site)
    if args.list:
        log_utils.info(Messages.Tool.LIST_NAME, args.list)
    elif args.comprehensive:
        log_utils.info(Messages.Tool.COMPREHENSIVE_MODE)
    
    # Handle comprehensive site extraction
    if args.comprehensive:
        log_utils.info(Messages.Schema.EXTRACT_COMPREHENSIVE, args.site)
        site_schema = sp.extract_comprehensive_site_schema(
            args.site, 
            specific_list=args.list,  # Optional list to focus on
            verbose=args.verbose, 
            detailed=args.detailed
        )
        
        if not site_schema:
            log_utils.error(Messages.Schema.EXTRACT_FAILURE)
            return 1
            
        log_utils.info("Successfully extracted site information:")
        log_utils.info("  • {} site columns", len(site_schema.get('site_columns', [])))
        log_utils.info("  • {} content types", len(site_schema.get('content_types', [])))
        log_utils.info("  • {} site features", len(site_schema.get('features', [])))
        log_utils.info("  • {} lists/libraries", len(site_schema.get('lists', [])))
        
        # Save comprehensive schema
        if args.output:
            output_path = args.output
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(site_schema, f, indent=2)
            log_utils.info(Messages.Schema.SCHEMA_SAVED, output_path)
        else:
            # Auto-generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            site_name = args.site.split('/')[-1] if '/' in args.site else 'site'
            output_path = f"./extracted_schemas/site_{site_name}_{timestamp}.json"
            os.makedirs("./extracted_schemas", exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(site_schema, f, indent=2)
            log_utils.info(Messages.Schema.SCHEMA_SAVED, output_path)
        
        return 0
    
    # Regular metadata extraction (requires list parameter)
    if not args.list:
        log_utils.error(Messages.Tool.LIST_REQUIRED)
        log_utils.error(Messages.Tool.LIST_HINT)
        log_utils.error(Messages.Tool.COMPREHENSIVE_HINT)
        return 1
    
    # Extract current schema
    log_utils.info(Messages.Schema.EXTRACT_START, args.site)
    current_schema = sp.extract_metadata_schema(args.site, args.list, verbose=args.verbose, detailed=args.detailed)
    
    if not current_schema:
        log_utils.error(Messages.Schema.EXTRACT_FAILURE)
        return 1
    
    log_utils.info(Messages.Schema.EXTRACT_SUCCESS, len(current_schema['metadata']))
    
    # Save extracted schema
    if args.output:
        output_path = args.output
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(current_schema, f, indent=2)
        log_utils.info(Messages.Schema.SCHEMA_SAVED, output_path)
    else:
        # Auto-generate filename if not specified
        output_path = sp.save_schema_to_file(current_schema)
        log_utils.info(Messages.Schema.SCHEMA_SAVED, output_path)
    
    # Analyze if requested
    if args.analyze:
        log_utils.info("\nAnalyzing schema...")
        log_utils.info(Messages.Schema.COMPARE_START, args.schema)
        
        # Load target schema
        try:
            with open(args.schema) as f:
                target_schema = json.load(f)
                log_utils.info(Messages.Schema.COMPARE_TARGET_LOADED, len(target_schema['metadata']))
        except Exception as e:
            log_utils.error(Messages.Schema.COMPARE_ERROR, e)
            log_utils.error(Messages.Schema.COMPARE_FILE_PATH, os.path.abspath(args.schema))
            return 1
        
        # Compare schemas
        comparison = sp.compare_schemas(current_schema, target_schema)
        
        # Display results summary
        log_utils.info("\n" + Messages.Schema.CHANGES_SUMMARY)
        log_utils.info(Messages.Schema.CHANGES_ADD, len(comparison['to_add']))
        log_utils.info(Messages.Schema.CHANGES_UPDATE, len(comparison['to_update']))
        log_utils.info(Messages.Schema.CHANGES_REMOVE, len(comparison['to_remove']))
        
        # Generate detailed report
        log_utils.info("\nDetailed Change Report:")
        
        if comparison['to_add']:
            log_utils.info("\n" + Messages.Schema.FIELDS_TO_ADD)
            for field in comparison['to_add']:
                log_utils.info(Messages.Schema.FIELD_ADD_ITEM, 
                              field['name'], field['type'], field.get('description', ''))
        
        if comparison['to_update']:
            log_utils.info("\n" + Messages.Schema.FIELDS_TO_UPDATE)
            for field in comparison['to_update']:
                current = next((f for f in current_schema['metadata'] if f['name'] == field['name']), {})
                log_utils.info(Messages.Schema.FIELD_UPDATE_ITEM, field['name'])
                if current.get('type') != field['type']:
                    log_utils.info(Messages.Schema.FIELD_UPDATE_TYPE, 
                                  current.get('type'), field['type'])
                if current.get('description') != field.get('description'):
                    log_utils.info(Messages.Schema.FIELD_UPDATE_DESC, 
                                  current.get('description'), field.get('description'))
                if current.get('options') != field.get('options') and 'options' in field:
                    log_utils.info(Messages.Schema.FIELD_UPDATE_OPTIONS)
        
        if comparison['to_remove']:
            log_utils.info("\n" + Messages.Schema.FIELDS_TO_REMOVE)
            for field in comparison['to_remove']:
                log_utils.info(Messages.Schema.FIELD_REMOVE_ITEM, field['name'], field['type'])
    
    log_utils.info("\n" + Messages.Tool.SUCCESS)
    return 0

if __name__ == "__main__":
    sys.exit(main())