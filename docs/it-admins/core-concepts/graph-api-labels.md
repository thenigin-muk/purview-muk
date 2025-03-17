<!-- description: Documentation about Microsoft Graph API Endpoints for Label Management for Your Organization. -->

# Microsoft Graph API Endpoints for Label Management

### Site Navigation
[🏠 Home](../../README.md) > [It Admins](../README.md) > [Core Concepts](README.md) | [⬅ Back to Core Concepts](README.md)

## Overview
For the most up-to-date and comprehensive details on managing retention labels through Graph API, refer to Microsoft's official documentation:

- [Microsoft Graph API: Retention Labels](https://learn.microsoft.com/en-us/graph/api/resources/security-retentionlabel?view=graph-rest-1.0)
- [Create and Manage Retention Labels](https://learn.microsoft.com/en-us/microsoft-365/compliance/create-retention-labels?view=o365-worldwide)

### API Reference Table

| **Action** | **HTTP Method** | **Endpoint** |
| --- | --- | --- |
| Get all retention labels | GET | <https://graph.microsoft.com/v1.0/security/labels/retentionLabels> |
| Get a specific label | GET | <https://graph.microsoft.com/v1.0/security/labels/retentionLabels/{labelId}> |
| Create a new label | POST | <https://graph.microsoft.com/v1.0/security/labels/retentionLabels> |
| Update an existing label | PATCH | <https://graph.microsoft.com/v1.0/security/labels/retentionLabels/{labelId}> |
| Delete a label | DELETE | <https://graph.microsoft.com/v1.0/security/labels/retentionLabels/{labelId}> |

**Example Request: Creating a New Label**
```python
import requests

url = "https://graph.microsoft.com/v1.0/security/labels/retentionLabels"
headers = {
	"Content-Type": "application/json",
	"Authorization": "Bearer {access_token}"
}
data = {
	"displayName": "Communications - Non-Executive",
	"retentionTrigger": "dateCreated",
	"retentionDuration": {
		"@odata.type": "#microsoft.graph.security.retentionDurationInDays",
		"days": 730
	},
	"actionAfterRetentionPeriod": "delete",
	"isRecordLabel": False
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
```
### Summary

This script provides a structured approach for selecting retention policies before pushing them to Purview, ensuring compliance and automation in records management.

---

[⬅ Previous: Graph Api Guide](graph-api-guide.md) | [Next: Graph Api Security ➡](graph-api-security.md)