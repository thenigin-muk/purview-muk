<!-- description: Documentation about PCard Statement Workflow  for Your Organization. -->
# PCard Statement Workflow 

## Introduction

This project automates the creation, management, and tracking of Purchase Card (PCard) statements in SharePoint using Power Automate. It is specifically structured to ensure compliance with the Washington Public Records Act (PRA) by organizing data efficiently, applying detailed metadata, and leveraging Microsoft Purview’s advanced Records Management and eDiscovery capabilities.

## Purpose

- Ensure compliance with the Washington Public Records Act (PRA).
- Streamline and standardize the submission and management process of PCard statements.
- Automate document set creation and management with metadata.
- Facilitate transparency, accountability, and efficiency for public records requests.

## Project Components

### SharePoint Document Libraries

- **PCard Statements**: Stores user-submitted PCard statements.

### SharePoint Lists

- **PCard Holders**: Stores details of authorized PCard users.
- **PCard Statement Dates**: Tracks approved PCard statement dates.
- **PCard Submissions**: Manages tracking of submissions for each holder per statement date.

### Site Columns

| Column Name              | Type            | Applied To                                   | Column Group  |
| ------------------------ | --------------- | -------------------------------------------- | ------------- |
| Billing Cycle Close Date | Date            | Statement Dates List, Document Set           | PCard Columns |
| Cardholder Name          | Person or Group | Holders List, Submissions List, Document Set | PCard Columns |
| Supervisor Name          | Person or Group | Holders List, Submissions List               | PCard Columns |
| Submission Status        | Choice          | Submissions List                             | PCard Columns |
| File Uploaded?           | Yes/No          | Submissions List                             | PCard Columns |
| Signed Copy Received?    | Yes/No          | Submissions List                             | PCard Columns |
| Date Submitted           | Date            | Submissions List, Document Set               | PCard Columns |
| Statement Year           | Number          | Statement Dates List, Document Set           | PCard Columns |
| Active?                  | Yes/No          | Holders List, Statement Dates List           | PCard Columns |

## Power Automate Solution Structure

The automation is structured into clear, maintainable flows within one Power Automate solution.

### Environment Variables Setup

| Variable Name             | Type | Description                                                      |
| ------------------------- | ---- | ---------------------------------------------------------------- |
| `TargetSharePointSiteURL` | Text | The SharePoint site where the automation will be deployed.       |
| `TestSharePointSiteURL`   | Text | The test environment site URL for deployment testing.            |
| `BaselineSiteListJSON`    | JSON | Contains the definitions of all required SharePoint lists.       |
| `BaselineSiteColumnsJSON` | JSON | Stores all site column definitions, including metadata settings. |
| `DefaultAdminEmail`       | Text | Email address to receive error notifications.                    |

### Flow Overview & Setup Instructions

Each Power Automate flow is **fully detailed** below, including setup steps, actions, and best practices.

#### 1. Get Deployment Settings
**Purpose:** Retrieve environment variables and validate SharePoint URLs.

#### 2. Create SharePoint Lists and Document Library
**Purpose:** Verify and create necessary lists.

#### 3. Create Site Columns
**Purpose:** Ensure required site columns exist.

#### 4. Assign Columns to Lists and Libraries
**Purpose:** Attach created columns to the appropriate lists and document library.

#### 5. Batch Create Document Sets (Future Implementation)
**Purpose:** Automate document set creation for PCard statement submissions.

#### 6. Notification and Reminder Flows (Future Implementation)
**Purpose:** Send reminders to cardholders and supervisors.

## JSON Structure

### BaselineSiteColumnsJSON
```json
{
  "Columns": [
    {
      "Title": "Billing Cycle Close Date",
      "InternalName": "BillingCycleCloseDate",
      "Type": "DateTime",
      "Group": "PCard Columns"
    },
    {
      "Title": "Cardholder Name",
      "InternalName": "CardholderName",
      "Type": "Lookup",
      "LookupList": "PCard Holders",
      "LookupField": "Title",
      "Group": "PCard Columns"
    },
    {
      "Title": "Supervisor Name",
      "InternalName": "SupervisorName",
      "Type": "Lookup",
      "LookupList": "PCard Holders",
      "LookupField": "Supervisor Name",
      "Group": "PCard Columns"
    }
  ]
}
```

### BaselineSiteListsJSON
```json
{
  "Lists": [
    {
      "Title": "PCard Holders",
      "InternalName": "PCardHolders",
      "Description": "Contains details about registered PCard users.",
      "Columns": ["Cardholder Name", "Supervisor Name", "Active?"]
    }
  ]
}
```

## Future Steps and Enhancements

- Automated list view and document set configurations.
- Implement comprehensive notification flows for deadlines.
- Integrate with Power BI for detailed reporting and compliance monitoring.
- Continuous enhancement of JSON structures for more granular metadata control.

## Maintenance and Deployment

- Store all Power Automate flows within a single solution for centralized management.
- Document detailed instructions for updating Environment Variables and JSON configurations.
- Regularly review for alignment with evolving compliance requirements.

This document ensures complete transparency, accuracy, and clarity in executing and maintaining the automation of the PCard statement management workflow.



---

[Next: Submit Pcard ➡](submit-pcard.md)