<!-- description: Documentation about Example JSON Ready for Graph API for Your Organization. -->

# Example JSON Ready for Graph API

### Site Navigation
[🏠 Home](../../README.md) > [It Admins](../README.md) > [Core Concepts](README.md) | [⬅ Back to Core Concepts](README.md)

To properly integrate the cleaned retention data into Microsoft Purview, the JSON must be formatted according to Graph API requirements. Below is an example of how the structured JSON should look before being sent via a PATCH or PUT request to Graph API.

**Example JSON Payload for Graph API**
```json
{
    "displayName": "Communications - Non-Executive",
    "descriptionForUsers": "Records of internal and external communications.",
    "descriptionForAdmins": "Retain for 2 years after communication received or provided, then Destroy.",
    "retentionTrigger": "dateCreated",
    "retentionDuration": {
        "@odata.type": "#microsoft.graph.security.retentionDurationInDays",
        "days": 730
    },
    "actionAfterRetentionPeriod": "delete",
    "isRecordLabel": false,
    "behaviorDuringRetentionPeriod": "retain",
    "filePlanDescriptors": {
        "category": {
            "name": "Agency Mgmt - Administration (General)"
        },
        "citation": {
            "name": "CORE (Local Government Common Records Retention Schedule)",
            "url": "https://www.sos.wa.gov/archives/recordsmanagement/local-government-records-retention-schedules---alphabetical-list.aspx"
        }
    }
}
```

---

[⬅ Previous: Contract Metadata](contract-metadata.md) | [Next: Graph Api Guide ➡](graph-api-guide.md)