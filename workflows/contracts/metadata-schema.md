# Contracts Workflow - Metadata Schema

This document outlines the metadata structure for managing Contracts records.

## **Metadata Fields**
| **Field**               | **Type**           | **Description** |
|-------------------------|-------------------|----------------|
| Primary Contract Type | Managed Metadata | High-level classification of contract |
| Contract Type | Managed Metadata | Specific sub-category under the Primary Contract Type |
| Contract Number | Text | Unique contract identifier |
| Effective Date | Date | Start date of the contract |
| Expiration Date | Date | End date of the contract |
| Vendor/Party Name | Text | Name of the vendor or involved party |
| Approval Status | Choice | Current status of contract approval |
| Linked Agenda Bill | Hyperlink | Link to related council agenda bill |
| Retention Label | Managed Metadata | Applied retention label based on compliance requirements |

