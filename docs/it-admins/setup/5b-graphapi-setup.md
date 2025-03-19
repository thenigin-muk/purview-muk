# Microsoft Graph API Setup Guide

## Overview

This system automates the creation of **secure** Microsoft Graph API app registrations. It follows **the principle of least privilege**, ensuring each app registration **only has the permissions it needs**.

## Impact & Considerations

- **Automates Entra ID app registration** to avoid manual errors.
- **Requires admin consent** for granting API permissions.
- **Stores credentials securely** in `.env.[app-name].secret` files.
- **Not suitable for environments with strict manual approval workflows.**

## Requirements

| Requirement            | Details |
|------------------------|---------|
| **Azure Role**         | Global Admin, Privileged Role Admin, or Application Admin |
| **Python Version**     | 3.8+ |
| **Graph API Permissions** | `Application.ReadWrite.All`, `Directory.ReadWrite.All` |
| **Storage**            | Credentials stored in `.env.master` and `.env.[app-name].secret` |
| **Secret Rotation**    | Requires manual or automated rotation |

---

# 📌 **1. Initial Setup**
## Step 1: Run the Setup Command
Run this in your project root folder:

```bash
python setup_graphapi.py --setup
```

This will:
1. **Guide you through creating a master app registration** in Entra ID.
2. **Prompt for your tenant ID, client ID, and client secret.**
3. **Verify your credentials** by acquiring an access token.
4. **Store credentials securely** in `.env.master`.

### How to Verify Setup?
After running the command, check the config:

```bash
cat GraphAPI_config.json
```

Example output:
```json
{
  "tenant_id": "your-tenant-id",
  "master_app": {
    "name": "GraphAPI-Orchestrator-Master",
    "client_id": "your-client-id",
    "object_id": "your-object-id",
    "creation_date": "2025-03-19T14:23:45"
  },
  "app_registrations": []
}
```

If you encounter errors, check:
```bash
cat logs/graphapi_setup.log
```

---

# 📌 **2. Adding Operators**
Operators are **additional users** who can manage Graph API app registrations.

### **Adding an Operator**
1. **Ensure the operator has the correct role** (`Application Administrator` or `Privileged Role Administrator`).
2. **Share the `.env.master` file securely** (never via email or public channels).
3. **Ensure they run the setup script** in their environment:

```bash
python setup_graphapi.py --setup
```

If an operator needs to create app registrations but **cannot grant admin consent**, they must request a **global admin** to approve permissions.

---

# 📌 **3. Adding API Modules**
Modules are **auto-generated Python clients** for Microsoft Graph API.

### **Creating a New App Registration**
Run:
```bash
python setup_graphapi.py --create-app sharepoint --description "SharePoint operations" --permissions Sites.Read.All Sites.ReadWrite.All
```

To list all registered apps:
```bash
python setup_graphapi.py --list-apps
```

### **Generating an API Module**
Once an app is registered, generate its module:
```bash
python setup_graphapi.py --generate-module sharepoint
```
This will:
- Create `api_modules/sharepoint/`
- Generate `sharepoint_api.py`
- Store credentials in `.env.sharepoint.secret`

For **usage details**, see the [Graph API Usage Guide](docs/it-admins/workflows/common/graphapi_usage.md).
