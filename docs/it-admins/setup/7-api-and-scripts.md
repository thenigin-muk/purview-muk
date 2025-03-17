<!-- description: Documentation about API Integration & Script Execution for Your Organization. -->
# API Integration & Script Execution

## Overview
This section provides a detailed guide on **API Integration & Script Execution**, including setup steps and best practices.

## Overview of API Usage
Microsoft Graph API and REST APIs enable advanced automation and data retrieval from SharePoint and Purview.

## Setting Up API Access
1. Register an Azure App in **Azure AD**.
2. Assign the required API permissions (Graph API, SharePoint API).
3. Generate a Client ID and Secret.
4. Store credentials securely in a  file.

### Example  File
```ini
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
TENANT_ID=your-tenant-id
```

## Example API Call (Python)
```python
import requests
headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
print(response.json())
```

## Next Steps
- Follow the step-by-step instructions provided.
- Ensure all dependencies and configurations are in place.
- If encountering issues, refer to the [Troubleshooting Guide](10-troubleshooting.md).

---

### Navigation
[← Microsoft Purview Compliance Configuration](6-purview-configuration.md) | [Power Automate & PowerApps Integration →](8-powerapps-powerautomate.md)



---

[⬅ Previous: 6 Purview Configuration](6-purview-configuration.md) | [Next: 8 Powerapps Powerautomate ➡](8-powerapps-powerautomate.md)