# Description: Test script for Graph API Orchestrator
# file: examples-tests/api_modules_template/workflows/common/graphapi/test_api.py
"""
Test script for Graph API Orchestrator
This runs in dry-run mode to verify functionality without writing to Azure
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
# This finds the project root by going up until it finds the 'purview-muk' directory
def find_project_root():
    """Find the project root directory"""
    current_path = Path(__file__).resolve()
    while current_path.name != 'purview-muk' and current_path != current_path.parent:
        current_path = current_path.parent
    return current_path

# Add the project root to sys.path
project_root = find_project_root()
sys.path.insert(0, str(project_root))

# Now imports should work
from workflows.common.graphapi.orchestrator import GraphAPIOrchestrator
from workflows.common import log_utils

def main():
    """Run tests for the GraphAPI orchestrator"""
    # Initialize orchestrator in dry-run mode
    print("🧪 Initializing GraphAPI Orchestrator in dry-run mode...")
    orchestrator = GraphAPIOrchestrator(dry_run=True)
    
    # Test creating an app
    print("\n📋 Testing app creation...")
    orchestrator.create_app(
        "test-app", 
        "This is a test app", 
        ["User.Read", "Directory.Read.All"]
    )
    
    # Test listing apps
    print("\n📋 Testing app listing...")
    orchestrator.list_apps()
    
    # Test generating a module
    print("\n📋 Testing module generation...")
    orchestrator.generate_module("test-app")
    
    # Test rotating a secret
    print("\n📋 Testing secret rotation...")
    orchestrator.rotate_secret("test-app")
    
    print("\n✅ All tests completed successfully in dry-run mode!")
    return 0

if __name__ == "__main__":
    sys.exit(main())