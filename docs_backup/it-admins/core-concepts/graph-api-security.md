<!-- description: Documentation about Graph API Multi-App Security Guide for Your Organization. -->
# Graph API Multi-App Security Guide

### Site Navigation

## Overview

This document outlines the best practices for securely accessing Microsoft Graph API across multiple workflows. Instead of granting excessive permissions to a single application, this guide details how to create **separate** app registrations based on specific functionality.

---

## **1. Why Use Multiple App Registrations?**

### 🔹 Principle of Least Privilege

- **Avoid excessive permissions**: Each app should only have access to the APIs necessary for its function.
- **Minimize security risks**: If one app’s credentials are compromised, the impact is limited.
- **Compliance**: Helps with audit tracking and role-based security.

| **Application Name**      | **Purpose**                                        | **APIs Accessed**         | **Permissions Needed** (Least Privilege) |
| ------------------------- | -------------------------------------------------- | ------------------------- | ---------------------------------------- |
| **Purview API Access**    | Handles retention policies, labels, and compliance | Microsoft Purview API     | `RecordsManagement.ReadWrite.All`        |
| **SharePoint Automator**  | Reads/Writes data to SharePoint for workflows      | SharePoint Online API     | `Sites.ReadWrite.All`                    |
| **User Directory Reader** | Reads user profiles for automation workflows       | Microsoft Graph Users API | `User.Read.All`                          |
| **Exchange Email Reader** | Fetches emails for retention workflows             | Microsoft Exchange Online | `Mail.Read`                              |

Each **workflow** should only call the necessary **app registration** and use **only** the permissions it needs.

---

## **2. Creating Azure App Registrations**

To ensure proper security segmentation, follow these steps to create each required **Azure App Registration**:

### **List of Required App Registrations**

| **App Name**              | **Purpose**                                | **Permissions Needed**            |
| ------------------------- | ------------------------------------------ | --------------------------------- |
| **Purview API Access**    | Controls retention labels and records mgmt | `RecordsManagement.ReadWrite.All` |
| **SharePoint Automator**  | Reads/Writes SharePoint data               | `Sites.ReadWrite.All`             |
| **User Directory Reader** | Reads user profiles for automation         | `User.Read.All`                   |
| **Exchange Email Reader** | Fetches and processes emails for retention | `Mail.Read`                       |

### **Step 1: Register an App in Azure AD**

1. Navigate to [Azure Active Directory](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview).
2. Click **App registrations** → **New registration**.
3. Enter the App Name (e.g., `Purview API Access`).
4. Select **Accounts in this organizational directory only**.
5. Click **Register**.

### **Step 2: Configure API Permissions**

1. In the app settings, go to **API permissions** → **Add permission**.
2. Select **Microsoft Graph** → Choose the relevant API (e.g., `RecordsManagement.ReadWrite.All`).
3. If using background automation (Power Automate), select **Application Permissions**.
4. Click **Grant Admin Consent** (requires Global Admin approval).

### **Step 3: Generate Client Secret**

1. Navigate to **Certificates & secrets**.
2. Click **New client secret** → Set expiration (recommend `1 year`).
3. Copy and securely store the **Secret Value**.

---

## **3. Storing and Using API Credentials**

### **Option 1: GitHub Secrets (Recommended for Automation)**

1. In GitHub, navigate to **Settings** → **Secrets and variables**.
2. Add the following secrets:
   - `PURVIEW_CLIENT_ID` → Azure AD App Client ID
   - `PURVIEW_CLIENT_SECRET` → Azure AD App Secret Value
   - `TENANT_ID` → Your Azure AD Tenant ID
3. In workflows, access them securely:
   ```yaml
   env:
     CLIENT_ID: $PLACEHOLDER_SECRETS_PURVIEW_CLIENT_ID
     CLIENT_SECRET: $PLACEHOLDER_SECRETS_PURVIEW_CLIENT_SECRET
     TENANT_ID: $PLACEHOLDER_SECRETS_TENANT_ID
   ```

### **Option 2: Environment Variables (For Local Development)**

1. Edit your `.env` file and add:
   ```env
   PURVIEW_CLIENT_ID=your-client-id
   PURVIEW_CLIENT_SECRET=your-client-secret
   TENANT_ID=your-tenant-id
   ```
2. Load them securely in a script:
   ```bash
   source .env
   ```

---

## **4. Calling the Graph API Securely**

Each workflow should retrieve a token **specific to the API it needs**.

### **Python Example for Authentication**

```python
import requests
import os

def get_access_token():
    url = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token".format(tenant_id=os.getenv("TENANT_ID"))
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv("PURVIEW_CLIENT_ID"),
        'client_secret': os.getenv("PURVIEW_CLIENT_SECRET"),
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, data=payload)
    return response.json().get("access_token")
```

---

## **5. Best Practices for API Security**

✅ **Use Environment-Specific App Registrations**:

- **Dev**: Limited permissions for testing.
- **Prod**: Strict permissions with admin approval.
  ✅ **Rotate Client Secrets Regularly**: Prevent unauthorized access.
  ✅ **Use Role-Based Access Control (RBAC)**: Assign users/groups access based on necessity.
  ✅ **Monitor API Usage with Azure Logs**: Track API calls for security audits.
  ✅ **Never Hardcode API Keys**: Always use **environment variables or secure vaults**.

---

## **Final Notes**

Following this structured approach ensures that **each workflow only gets the access it requires**, reducing security risks while maintaining flexibility for automation.

This guide should be **referenced before implementing API-driven workflows** to ensure secure access to Graph API across different departments and automation workflows.

---

[⬅ Previous: Graph Api Labels](graph-api-labels.md) | [Next: Managed Metadata ➡](managed-metadata.md)