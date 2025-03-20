# Microsoft Graph API Orchestrator

A modular system for creating and managing specialized app registrations in Microsoft Graph API.

## Features

- Create app registrations with least-privilege permissions
- Generate ready-to-use Python API modules
- Securely manage app credentials
- Support for Azure Key Vault integration
- Dry-run mode for testing

## Requirements

- Python 3.8+
- Azure subscription with admin access
- Following Python packages:
  - msal
  - requests
  - azure-identity (for Key Vault support)
  - azure-keyvault-secrets (for Key Vault support)

## Usage

### Initial Setup

```bash
# Set up the master app registration
python graphapi_orchestrator.py --setup
```
### Creating App Registrations

```bash
# Create a new app with specific permissions
python graphapi_orchestrator.py --create-app my-app --description "My API App" --permissions User.Read Directory.Read.All
```

### Generating API Modules

```bash
# Generate a Python module for accessing the API
python graphapi_orchestrator.py --generate-module my-app
```

### Managing Secrets
```bash
# Rotate a client secret
python graphapi_orchestrator.py --rotate-secret my-app
```

### Using Azure Key Vault

```bash
# Store secrets in Azure Key Vault
python graphapi_orchestrator.py --create-app secure-app --use-key-vault --key-vault-url https://your-vault.vault.azure.net/
```

### Testing with Dry Run

```bash
# Test without making any changes
python graphapi_orchestrator.py --create-app test-app --dry-run
```