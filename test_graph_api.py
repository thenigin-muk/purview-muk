#!/usr/bin/env python3
# file: test_graph_api.py
"""
Test script for the Graph API module
"""
import logging
import sys

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_purview_api():
    """Test the purview API module"""
    print("\n=== Testing Purview API Module ===")
    
    try:
        # Import the module
        from api_modules.purview import get_client
        print("✅ Successfully imported the module")
        
        # Get a client
        client = get_client()
        print("✅ Successfully created a client")
        
        # Test getting an access token
        token = client.get_access_token()
        if token and len(token) > 100:  # Simple validation that it looks like a token
            print(f"✅ Successfully obtained an access token: {token[:10]}...{token[-10:]}")
        else:
            print("❌ Failed to get a valid access token")
            return False
        
        # Test a simple API call
        print("\nMaking a test API call to /me...")
        response = client.make_api_request('get', '/me')
        print(f"✅ API call successful! Response:")
        print(f"  - Display Name: {response.get('displayName')}")
        print(f"  - User Principal Name: {response.get('userPrincipalName')}")
        print(f"  - ID: {response.get('id')}")
        
        # Test a more specific API call related to Purview if needed
        # For example, if you're working with retention labels:
        try:
            print("\nTrying to access retention labels...")
            labels = client.make_api_request('get', '/informationprotection/policy/labels')
            print(f"✅ Successfully retrieved {len(labels.get('value', []))} retention labels")
            
            # Display the first few labels
            for i, label in enumerate(labels.get('value', [])[:3]):
                print(f"  {i+1}. {label.get('name')} ({label.get('id')})")
            
        except Exception as e:
            print(f"❌ Retention label API call failed: {str(e)}")
            print("  This might be expected if the app doesn't have the required permissions.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests for Graph API modules"""
    success = test_purview_api()
    
    if success:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())