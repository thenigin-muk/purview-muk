# PCard Workflow - Metadata Schema

This document outlines the metadata structure for managing PCard statement records.

## **Metadata Fields**
| **Field**               | **Type**           | **Column Group** | **Description** |
|-------------------------|-------------------|-----------------|----------------|
| Billing Cycle Close Date | Date | PCard Columns | Date when the PCard statement cycle ends. |
| Cardholder Name | Person or Group | PCard Columns | The name of the person assigned the PCard. |
| Supervisor Name | Person or Group | PCard Columns | The designated supervisor for approval. |
| Submission Status | Choice (Pending, Submitted, Approved, Rejected) | PCard Columns | Status of the PCard statement submission. |
| File Uploaded? | Yes/No | PCard Columns | Indicates whether the required file has been uploaded. |
| Signed Copy Received? | Yes/No | PCard Columns | Confirms if the final signed copy has been received. |
| Date Submitted | Date | PCard Columns | The date when the PCard statement was submitted. |
| Statement Year | Number | PCard Columns | The fiscal year associated with the statement. |
| Active? | Yes/No | PCard Columns | Indicates whether the record is still active. |

## **Lists & Libraries Using These Fields**
| **Name**                 | **Type**            | **Purpose** |
|-------------------------|-------------------|----------------|
| PCard Statements | Document Library | Stores user-submitted PCard statements. |
| PCard Holders | SharePoint List | Tracks details of authorized PCard users. |
| PCard Statement Dates | SharePoint List | Maintains a record of valid statement periods. |
| PCard Submissions | SharePoint List | Manages tracking of submissions per user per cycle. |

## **Power Automate Integration**
- These metadata fields will be **automatically applied** when document sets are created.
- The **Submission Status** field will be used in **reminder notifications** for incomplete statements.
- The **File Uploaded?** and **Signed Copy Received?** fields will **trigger compliance workflows**.

