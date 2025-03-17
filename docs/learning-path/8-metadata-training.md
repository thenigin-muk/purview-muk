<!-- description: Documentation about Metadata Training and Reference Guide for Your Organization. -->

# Metadata Training and Reference Guide

### Site Navigation
[🏠 Home](../README.md) > [Learning Path](README.md) | [⬅ Back to Learning Path](../README.md)

### **What is Metadata?**

Metadata describes documents, making them easier to organize, find, and manage. Proper metadata helps you quickly find the right document.

### **How to Access and Apply Metadata**

1. Verify your access to SharePoint libraries.
2. If you don't have access, contact your supervisor.

#### **Creating a Document Set**

- Navigate to the correct SharePoint library.
- Click **New → Document Set**.
- Enter Document Set metadata clearly.
- Save the Document Set.

#### **Uploading Documents**

- Open the Document Set.
- Drag and drop files or click **Upload**.
- Fill in Document-level metadata carefully.

#### **Linking Documents**

- Link related Agenda Bills and Contracts if matches exist.

### **Actions When Unsure About Metadata**

#### 🔍 For City Council Meetings

- Agenda Bill Number: Open the document and look at the top. Usually labeled clearly as 'Agenda Bill ####'.
- Agenda Item Name: If folder name is unclear, open the PDF and use the 'Subject Title' at the top of the first page.
- Staff Lead: Check the document header or top sections for a clearly stated staff member's name.
- Example: Folder name unclear? Open the PDF file and use the clearly stated 'Subject Title' and 'Meeting Date' at the top.

#### 📑 For Contracts

- Contract/Agreement: Standard terms with signatures for purchase or services.
- MOU (Memorandum of Understanding): Usually informal, describes an understanding or roles. Often involves no financial terms.
- Interlocal Agreement (ILA): Agreement clearly between government entities (cities, counties).
- Franchise Agreement: Related to utilities, cable, or other services provided by private companies.
- Grant: Clearly about receiving funding or financial assistance.
- If Unsure: Ask your supervisor or contact the City Clerk's Office.

### **Section 2: Metadata Quick Reference Tables**

#### 🏛️ City Council Meetings Library

📁 Document Set-Level Metadata

| **Column Name** | **Type** | **Purpose/Examples** |
| --- | --- | --- |
| Meeting Date | Date | Date the City Council Meeting occurred |
| Meeting Type | Choice | Regular, Special, Work Session, Executive Session |
| Year | Calculated | Automatically extracted from "Meeting Date" |

📄 Document-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Agenda Bill Number | Single Line | Unique identifier, e.g., AB25-018 |
| Title | Single Line | Descriptive title of agenda item/document |
| Agenda Item Number | Number | Official agenda sequence number |
| Department | Choice | Finance, Public Works, Fire, etc. |
| Sponsor/Staff Lead | Person | Responsible staff member or sponsor |
| Document Type | Choice | Agenda Bill, Agenda, Minutes, Resolution, Ordinance, Exhibit, Presentation, ILA |
| Status | Choice | Draft, Submitted, Approved, Rejected, Withdrawn |
| Voting Outcome | Choice | Passed, Failed, Deferred, Discussion Only |
| Linked Contract | Hyperlink | Links to related contract(s) in Contract library |
| Budget Reference | Single Line | Budget GL code |
| Amount Budgeted | Currency | Amount allocated in budget |
| Amount Required | Currency | Amount required by this agenda item |
| Additional Appropriation Required | Yes/No | Flag if more funds need approval |
| Remarks/Notes | Multiple lines | Additional details |

#### 📑 Contracts Library

📁 Document Set-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Contract Number | Single Line | Unique contract identifier |
| Contract Title | Single Line | Brief descriptive contract title |
| Vendor/Party Name | Single Line | Name of contracted vendor |
| Department | Choice | Finance, Public Works, Fire, etc. |
| Contract Type | Choice | Service, Purchase, Lease, ILA, Grant, MOU |
| Effective Date | Date | Start date |
| Expiration Date | Date | End date |
| Contract Status | Choice | Active, Pending, Expired, Closed |
| Financial GL Code | Single Line | Budget tracking code |
| Total Contract Amount | Currency | Budgeted total for contract |
| Linked Agenda Bill | Hyperlink | Links directly to City Council Agenda Bill |
| Notification Trigger | Date | For future automation |

📄 Document-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Document Title | Single Line | Title of individual document |
| Document Type | Choice | Contract, Amendment, Exhibit, Supporting Document, Correspondence, Form |
| Document Status | Choice | Draft, Routed, Approved, Signed, Final, Archived |
| Date Routed | Date | Document routed date |
| Approval Status | Choice | Pending, Routed, Approved, Returned, Signed |
| Reviewer/Approver | Person | Reviewing or approving staff |
| Signature Method | Choice | Electronic, Wet Signature |
| Returned to City Clerk | Yes/No | Executed copies returned |
| Scanned | Yes/No | Digitally archived |
| Finance Amount | Currency | Specific financial amount |
| Notes/Remarks | Multiple lines | Additional context |

#### 📋 Policies Library

📁 Document Set-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Policy Title | Single Line | Official policy title |
| Policy Number | Single Line | Unique identifier |
| Policy Category | Choice | Financial, Operational, HR, IT, Safety |
| Responsible Department | Choice | Finance, HR, IT, etc. |
| Policy Status | Choice | Active, Archived, Superseded, Under Review |
| Effective Date | Date | Policy effective date |
| Last Reviewed Date | Date | Most recent review |
| Next Review Due | Date | Scheduled review |
| Approval Body | Choice | City Council, Mayor, Committee |

📄 Document-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Document Title | Single Line | Specific document title |
| Document Type | Choice | Policy, Procedure, Form, Instructions, Resolution |
| Document Date | Date | Document creation/approval date |
| Document Status | Choice | Draft, Final, Approved, Superseded, Archived |
| Form Indicator | Yes/No | Identifies forms for automation |
| Author/Owner | Person | Document responsible individual |
| Linked Agenda Bill | Hyperlink | Optional link to related Agenda Bill |
| Remarks/Notes | Multiple lines | Additional context |

🗃️ Boards & Commissions Library

📁 Document Set-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Commission Name | Choice | DEI, Parks & Arts, Planning, Salary |
| Meeting Date | Date | Official meeting date |

📄 Document-Level Metadata

| Column Name | Type | Purpose/Examples |
| --- | --- | --- |
| Document Title | Single Line | Title of individual document |
| Document Type | Choice | Agenda, Minutes, Resolution, Supporting Document |
| Document Status | Choice | Draft, Final, Approved |
| Staff Lead | Person | Responsible staff |
| Remarks/Notes | Multiple lines | Further context |

🔗 **Cross-Linking & Automation**

- Easily cross-reference documents via hyperlinks.
- Future automation opportunities include notifications and financial updates via Power Automate.

**Next** [That's everything (for now), head to the Users folder to find training for your new workflows](../users/users.md)

---

[⬅ Previous: 7 Next Steps](7-next-steps.md)