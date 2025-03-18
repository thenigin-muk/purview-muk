<!-- description: Documentation about SharePoint API for Your Organization. -->
# SharePoint API Integration

### Site Navigation
[🏠 Home](../../../README.md) > [It Admins](../../README.md) > [Solutions](../README.md) > [Sharepoint](README.md) | [⬅ Back to Sharepoint](README.md)

## API App Registration

- **App Name**: SharePoint Online Manager
- **API Permissions**: Sites.Read.All, Sites.ReadWrite.All
- **Authentication**: Client credentials
- **Environment Variables**:
  - `SHAREPOINT_CLIENT_ID`: Azure AD app registration client ID
  - `SHAREPOINT_CLIENT_SECRET`: Client secret for authentication
  - `TENANT_ID`: Microsoft 365 tenant ID

## Features Implemented

- Authentication with Microsoft Graph API
- Reading SharePoint site information
- Applying metadata schemas to document libraries

## Integration Points

- GitHub Actions workflow: `.github/workflows/sharepoint-metadata.yml`
- API connection script: `workflows/contracts/sp-api-test.py`
- Metadata schema: `workflows/contracts/metadata-schema.json`

---

[Next: Readme ➡](readme.md)