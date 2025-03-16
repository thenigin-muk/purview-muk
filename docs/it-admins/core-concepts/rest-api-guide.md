# Using the REST API to Collect JSON from State Archives

### Overview

The Washington State Secretary of State (WA SOS) Records Office provides an open REST API for querying and retrieving records retention schedules, historical data, and compliance documents. This appendix outlines how to interact with this API, retrieve JSON data, and prepare it for integration with Microsoft Purview and SharePoint without requiring authentication tokens.

### API Endpoint and Access**

The Washington State Secretary of State (WA SOS) Records Office provides an open REST API that does not require authentication tokens. This API allows direct access to records retention schedules.

**Example API Request**

```http
GET https://api.digitalarchives.wa.gov/api/retention-schedules/3
```
**Parsing JSON Response**

The JSON response will contain multiple records. Below is an example response structure:

```json
{
    "validationErrors": {},
    "isValid": true,
    "returnValue": {
      "scheduleID": 3,
      "scheduleName": "CORE (Local Government Common Records Retention Schedule)",
      "isActive": true,
      "localSchedules": [
        {
          "seriesID": 7153,
          "dispositionAuthorityNumber": "GS2010-001",
          "seriesTitleDescription": "Communications – Non-Executive",
          "primaryCopyRetention": "Retain for 2 years after communication received or provided, whichever is later then Destroy.",
          "archival": "Non-Archival",
          "category": {
            "categoryName": "Agency Mgmt - Administration (General)"
          }
        }
      ]
    }
  }
```
### Storing API Data**

To store the retrieved JSON in SharePoint, you can:

- Save the JSON as a file in a SharePoint document library.
- Process the data and insert relevant fields into a SharePoint list.

## Appendix D: Python Script for Cleaning Up and Formatting JSON for Graph API
