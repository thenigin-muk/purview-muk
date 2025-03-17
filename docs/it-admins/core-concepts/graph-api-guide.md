<!-- description: Documentation about Graph API Access & Security Guide for Your Organization. -->

# Graph API Access & Security Guide

### Site Navigation
[🏠 Home](../../README.md) > [It Admins](../README.md) > [Core Concepts](README.md) | [⬅ Back to Core Concepts](README.md)

### Site Navigiation

## Overview
This guide explains how to securely authenticate and interact with Microsoft Graph API using **client credentials** in Azure, safely store secrets, and execute API calls using **Python and Bash**.

## 1. Register an App in Azure AD

To use Graph API, you must first register an application in **Azure Active Directory (AAD)**.

### Steps:
1. Go to **[Azure Portal](https://portal.azure.com/)** and navigate to **Azure Active Directory**.
2. Select **App Registrations** → Click **New Registration**.
3. Set the app name (e.g., `GraphAPI_Automation`).
4. Choose **Accounts in this organizational directory only** (Default for internal use).
5. Click **Register**.

## 2. Configure API Permissions

1. In the registered app, go to **API Permissions**.
2. Click **Add a permission** → Select **Microsoft Graph**.
3. Choose **Application Permissions** (for backend automation, not user delegation).
4. Select required permissions, e.g.:
   - `Sites.Manage.All` (Manage SharePoint sites)
   - `Sites.ReadWrite.All` (Modify site contents)
   - `TermStore.Read.All` (Read managed metadata term sets)
   - `TermStore.ReadWrite.All` (Modify term sets)
   - `Directory.Read.All` (View directory data)
5. Click **Add permissions**.
6. Click **Grant admin consent** to approve permissions.

## 3. Generate Client Secret (App Password)

1. Go to **Certificates & Secrets**.
2. Click **New client secret** → Set expiration to **24 months**.
3. Copy the **Secret Value** immediately (it won’t be shown again).
4. Store the secret in a safe location.

## 4. Securely Store Secrets in GitHub

Never store secrets in your code. Instead, use **GitHub Secrets**:

1. In your GitHub repo, go to **Settings** → **Secrets and Variables** → **Actions**.
2. Click **New repository secret**.
3. Add the following secrets:
   - `AZURE_CLIENT_ID` → Copy from **App Registration → Application (client) ID**
   - `AZURE_TENANT_ID` → Copy from **Directory (tenant) ID**
   - `AZURE_CLIENT_SECRET` → Copy from **Certificates & Secrets**

## 5. Make a Graph API Call Using Python

### Install Required Libraries
```bash
pip install requests msal
```

### Python Script
```python
import os
import requests
from msal import ConfidentialClientApplication

# Load secrets from environment variables
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# Get OAuth Token
def get_token():
    app = ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=f"https://login.microsoftonline.com/{TENANT_ID}")
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token["access_token"]

# Make API Call
def get_sites():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/sites", headers=headers)
    print(response.json())

get_sites()
```

## 6. Make a Graph API Call Using Bash

### Install cURL and jq (if not installed)
```bash
sudo apt update && sudo apt install curl jq -y
```

### Bash Script
```bash
#!/bin/bash
CLIENT_ID="your-client-id"
TENANT_ID="your-tenant-id"
CLIENT_SECRET="your-client-secret"

TOKEN=$(curl -s -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID" \
  -d "scope=https://graph.microsoft.com/.default" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "grant_type=client_credentials" | jq -r '.access_token')

curl -s -X GET "https://graph.microsoft.com/v1.0/sites" -H "Authorization: Bearer $TOKEN"
```

## 7. Security Best Practices
- **NEVER** commit credentials to source code.
- Use **GitHub Secrets** or environment variables for storage.
- Rotate secrets **regularly** and update deployments accordingly.
- Restrict API permissions to **minimum necessary access**.
- Enable **audit logging** in Azure for API access tracking.

## 8. Next Steps
- Automate **retrieving term sets** from SharePoint.
- Develop **Graph API-based workflows** for SharePoint automation.
- Securely **deploy API automation** using GitHub Actions.

---

This guide provides a **secure foundation** for working with **Microsoft Graph API**, setting up authentication, and making API requests using **Python and Bash** while ensuring **best security practices**.

---

[⬅ Previous: Example Graph Json](example-graph-json.md) | [Next: Graph Api Labels ➡](graph-api-labels.md)