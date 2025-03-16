# SharePoint & Microsoft Purview for Records Management & Compliance
### Future Forward: Structuring for Effective Digital Records Management

## Table of Contents

1. Purpose & Audience
2. Introduction
3. Understanding SharePoint Document Management
4. Metadata: The Key to Smarter Records Organization
5. Document Sets: A Smarter Alternative to Folders
6. Automating Records Retention & Compliance
7. The Advantages Over Windows File Server
8. Expanding Auto-Labeling to Emails
9. Disposition & Records Review Process
10. Next Steps & Implementation
11. Appendix
    1. Records Management Metadata Training and Reference Guide
    2. Contract Management Metadata and Automation Guide
    3. Using the REST API to Collect JSON from State Archives
    4. Python Script for Cleaning Up and Formatting JSON for Graph API
    5. Example JSON Ready for Graph API
    6. Microsoft Graph API Endpoints for Label Management
    7. SharePoint Step-by-Step Guide: Moving Contract Files

## 1 Purpose & Audience

This document serves as a guide for **records managers, IT administrators, and departmental staff** responsible for implementing SharePoint-based document management. It outlines best practices for **structuring document libraries, applying metadata, and automating retention policies** using SharePoint and Microsoft Purview.

### Scope of This Document

This initiative focuses **solely on the management of stored documents** within our organization’s **Windows File Server and SharePoint libraries**. It **does not** address records management for data stored inside applications, such as SmartGov, GovQA, Eden, and many other places where data resides. The key distinction is if that file is accessible today using WIndows File Explorer it probably applies to this documentation. **Application-based records remain managed within their respective systems.**

### Approach & Expectations

Our goal is to create **new workspaces based on organizational workflows** to improve records management. Departments and staff responsible for these records will be expected to **migrate documents into newly created SharePoint spaces.**

This is a **long-term, collaborative effort** between IT and designated department staff to ensure proper **document library structures are built** within SharePoint. IT will work **closely with each department or workflow owner** to establish relevant document libraries and retention policies.

By following this guide, organizations can streamline records retention, enhance searchability, and ensure compliance with regulatory requirements while maintaining a structured and manageable document repository.

## 2 Introduction

Effective records management is crucial for compliance, efficiency, and accessibility. This document provides a structured approach to transitioning from traditional **Windows File Servers** to a **modern digital records management system using SharePoint and Microsoft Purview**.

Key topics covered:

- **Why SharePoint?** Advantages over traditional file storage.
- **Metadata & Auto-Labeling** for better organization.
- **Automated Retention & Compliance** to streamline recordkeeping.
- **Email Retention & Public Records Requests** to ensure accountability and legal compliance.
- **Compliance Manager for audits and legal holds** to support transparency and governance.

This guide will help organizations move toward a more **structured, automated, and efficient** records management system by leveraging metadata, auto labeling, and automated disposition workflows. The implementation is **incremental**, ensuring that each department and workflow is introduced in a manageable way, allowing for continuous evaluation and improvement without overwhelming staff.

## 3 Understanding SharePoint Document Management

### What is SharePoint Document Management?

SharePoint is a **cloud-based collaboration platform** that enables teams to store, organize, and manage documents efficiently. Unlike traditional Windows File Servers, which rely on **lettered drives and deep folder structures**, SharePoint introduces a more flexible and metadata-driven approach to document organization.

SharePoint document management is built on three key components:

- **SharePoint Sites** – Workspaces where departments or projects can store related documents.
- **Document Libraries** – Storage locations within SharePoint Sites where documents are categorized and managed.
- **Metadata & Auto-Labeling** – A way to classify and organize documents dynamically instead of relying on folder structures.

This shift requires **understanding new terminology and concepts** that will improve how records are managed.

### SharePoint vs. Windows File Server

| Feature | Windows File Server | SharePoint |
| --- | --- | --- |
| Storage Structure | Folder-based, static | Metadata-driven, dynamic |
| Access & Security | Requires manual permission setup | Granular access controls per document/site |
| Collaboration | Limited file sharing | Real-time editing and versioning |
| Retention & Compliance | Manual processes | Automated policies with Microsoft Purview |

💡 **By shifting to SharePoint, departments no longer need to rely on deep folder structures or confusing drive mappings. Instead, they can leverage metadata and automation to streamline records management.**

### The Challenge: Unstructured Legacy Records

One of the biggest hurdles in transitioning to structured document management is dealing with historical records. Over time, employees created personal folders to store work, leading to:

- **Scattered legacy records** sitting in shared drives "just in case."
- **Named personal folders** (e.g., "Joe’s Folder") becoming an unofficial standard.
- **Siloed workspaces**, where employees saved files independently instead of collaborating.
- **Duplicate content** stored across multiple locations, making version control difficult.

To address these challenges, we must transition from **lettered drives** to SharePoint-based **Document Libraries** and adopt a more structured approach to storing, labeling, and retrieving records.

## 4 Metadata: The Key to Smarter Records Organization

### What is Metadata?

Metadata is **“data about data”**—it provides descriptive information about a document, allowing for better organization and searchability.

Instead of relying on folder names, metadata classifies files using standardized attributes like:

- 📅 **Date Created** – When the document was added
- 🏢 **Department** – Which group owns the document
- 📑 **Document Type** – Policy, contract, invoice, report, etc.
- 🔐 **Security Level** – Public, confidential, restricted
- 📌 **Retention Label** – How long the document must be kept

### Why Metadata Matters

Have you ever needed to find a specific policy document related to your department? Do you know exactly where to look for an IT policy or an HR policy, or would you need to send an email asking someone else? These situations create unnecessary delays and interruptions in workflow, reducing overall efficiency.

Metadata allows users to **filter, sort, and search for documents dynamically**, rather than navigating through complex folder structures.

💡 **Example:** Instead of storing separate copies of city-wide policies in different department folders, all policies can exist in a single **City Policies Document Library** where users can filter by:

- "Policy Type: HR Policy, IT Policy, Finance Policy, etc."
- "Year: 2024"
- "Department: Human Resources, IT, Finance, etc."

This method improves searchability, reduces duplication, and ensures that everyone in the organization is accessing **the most up-to-date version** of a document without confusion.


## 5 Document Sets: A Smarter Alternative to Folders

### What is a Document Set?

A **Document Set** in SharePoint is a specialized type of folder that groups related documents together while maintaining metadata consistency across all files within the set. Unlike traditional folders, Document Sets ensure that all associated documents share the same classification, retention policies, and search attributes.

### Why Document Sets Matter

Managing large numbers of contracts, policies, and agreements requires a structured approach to ensure that files are stored, accessed, and retained correctly. Instead of navigating multiple folders, Document Sets allow users to:

- Keep all related documents in **one logical container**.
- Automatically **inherit metadata** across all documents within the set.
- Improve **searchability** by filtering instead of manually sorting through folders.

💡 Example: City Contracts Document Library

Instead of each department storing contracts in separate locations, all city-wide contracts can be managed in a single **City Contracts Document Library**. Each contract would exist as a **Document Set**, containing all related files such as:

- The signed contract agreement.
- Amendments and modifications.
- Correspondence and approval documents.
- Supporting financial and legal documents.

Users can **filter contracts dynamically** without manually sorting through folders. For example, they can filter by:

- "Contracts where I am a key stakeholder."
- "Contracts expiring in the next 6 months."
- "Vendor name or contract type."

This method ensures that **all contracts remain in a single location**, and users can easily retrieve the documents most relevant to them at any given time.

A **Document Set** in SharePoint is similar to a folder but with key improvements:

- All documents in the set inherit the same metadata (classification, retention, etc.)
- Users can easily access related records in one place

## 6 Automating Records Retention & Compliance

### What is Microsoft Purview?

Microsoft Purview is a **compliance and data governance platform** that integrates with SharePoint to help organizations **automate records retention, classification, and security policies**. By leveraging metadata, Purview ensures that records are stored, retained, and disposed of in accordance with legal and organizational policies.

### Why Automating Retention Matters

Manual retention processes require employees to remember when to archive or delete records, leading to inconsistencies and compliance risks. By automating retention with Microsoft Purview, organizations can:

- **Ensure consistent retention policies** across all departments.
- **Classify records automatically** based on metadata and content.
- **Lock finalized records** to prevent unauthorized modifications.
- **Ensure legal compliance** without relying on manual processes.

### Example: Retention in the City Contracts Document Library

With Microsoft Purview, the **City Contracts Document Library** can automatically enforce retention policies. For example:

- Contracts tagged with **"Active"** status are retained for reference.
- Contracts tagged as **"Expired"** automatically enter a disposition process.
- Key documents are **locked from modifications** once signed to preserve their legal integrity.

Instead of manually tracking contract expiration dates, Microsoft Purview enables **automated disposition actions** based on predefined retention schedules. Disposition refers to the process of reviewing records at the end of their retention period to determine whether they should be archived, deleted, or retained further based on compliance requirements.

### Understanding Electronic Dispositions in Records Management

Just like physical records require periodic review, such as storing essential documents in **bankers' boxes** for long-term archival or discarding temporary notes and post-its, digital records also undergo **disposition actions** based on their record type.

Microsoft Purview acts as the **digital equivalent of a structured disposition process**, ensuring that:

- Essential records are **archived** properly.
- Time-sensitive documents are **reviewed and approved before deletion**.
- Non-essential or obsolete files are **automatically disposed of**, reducing clutter and compliance risks.

By using metadata-driven retention, organizations **eliminate the need for manual file cleanup** and ensure that records are retained as long as required—without extra administrative overhead. Additionally, when the State revises Disposition Authority Numbers (DANs), IT can update these retention schedules and disposition actions in Microsoft Purview, ensuring compliance without requiring staff to manually review and adjust each document.

By using metadata-driven auto-labeling and Microsoft Purview, SharePoint can:

- Automatically classify records based on metadata
- Apply retention rules consistently across all departments
- Lock finalized records to prevent accidental changes
- Ensure compliance with legal & regulatory requirements

## 7 Expanding Auto-Labeling to Emails

### Why Email Retention Matters

Email communication often contains critical business records, including contracts, approvals, and legal correspondences. However, managing email retention manually can lead to **accidental deletions, clutter, and compliance risks**. Microsoft Purview extends **auto-labeling and retention policies to Outlook**, ensuring that:

- **Important emails are automatically classified** based on metadata.
- **Retention labels are applied consistently** to match SharePoint records.
- **Emails are stored or deleted in accordance with compliance policies.**

### How Auto-Labeling Works in Outlook

Microsoft Purview scans emails for **keywords, metadata, and sender/recipient details** to determine retention needs. For example, in the **City Contracts Document Library**, related emails can be automatically:

- Tagged with a **"Contract Correspondence"** label.
- Retained for **a set period** based on regulatory requirements.
- Linked to the appropriate **contract files in SharePoint** for reference.

### Example: Managing Contracts-Related Emails

Instead of manually sorting and saving contract-related emails, Purview ensures that:

- Any email discussing **contract terms, amendments, or approvals** is retained for compliance.
- Expired contracts trigger **email disposition actions**, ensuring old correspondence is handled properly.

By automating email retention, organizations **eliminate human error** and ensure that important records remain available when needed, reducing the risk of **compliance violations or misplaced information**.

Microsoft Purview extends auto-labeling beyond SharePoint to Outlook, ensuring that emails are:

- Automatically classified based on metadata and keywords.
- Assigned retention labels that match corresponding SharePoint records.
- Retained or deleted according to compliance requirements.

## 8 Compliance Manager & Disposition Review

### Using Microsoft Purview Compliance Manager

In addition to managing retention and labeling, **Microsoft Purview Compliance Manager** provides tools for overseeing **public records requests, legal holds, and compliance audits**. This ensures that metadata-driven records management is **not just about retention but also about accessibility and legal accountability.**

When responding to a **public records request**, Purview allows users to:

- Identify all documents related to a **specific contract or policy**.
- Retrieve **all email correspondence** tied to a given project or agreement.
- Ensure that all associated files are reviewed, exported, or disclosed in a structured manner.

### Example: Public Records Requests & Legal Holds

Imagine a scenario where a **public records request** is submitted regarding a vendor contract. Instead of manually searching through disconnected folders and inboxes, Compliance Manager can:

- Aggregate **all related emails, documents, and approvals** into a single case.
- Apply **legal holds** to prevent deletion during the review process.
- Ensure **records remain intact** even if employees leave or change roles.

Microsoft Purview acts as the **banker’s box** of electronic records management—ensuring all documents are retained, discoverable, and **ready for audits or legal inquiries.**

## 9 Next Steps & Implementation

### Implementing SharePoint for Auto-Labeling & Retention

This implementation follows an **incremental approach**, where phases **1 through 3 are looped for each workflow within a department or division** rather than applied organization-wide all at once. This ensures staff are not overwhelmed with changes and can adapt as each workflow is introduced, refined, and optimized. Each workflow serves as a learning experience, making subsequent implementations smoother and more efficient.

### Phased Approach for Implementation

**Assessment & Planning**

- Identify record types within each department that require structured retention.
- Map existing file structures from the Windows File Server and SharePoint into logical Document Libraries.
- Define metadata fields that will drive organization, filtering, and retention policies.

**Creating Document Libraries & Metadata Structure**

- Work with departments to create Document Libraries aligned with workflows.
- Apply consistent metadata to enable structured filtering.
- Establish Document Sets where necessary to group related records logically.

**Configuring Retention Policies in Microsoft Purview**

- Define Retention Labels based on Disposition Authority Numbers (DANs).
- Implement auto-labeling rules to ensure records are classified automatically.
- Apply disposition workflows to trigger audits, approvals, and final actions on records.

**Training & Adoption**

- Train department leads and records managers on metadata usage, filtering, and retention policies.
- Conduct workshops on how email retention integrates with document management.
- Provide guidance on handling public records requests using Compliance Manager.

**Ongoing Management & Optimization**

- Regularly review retention policies and update DANs as regulations change.
- Ensure IT and Records Managers monitor compliance dashboards in Purview.
- Refine metadata and organization structures as new use cases emerge.

**By following these structured steps, the organization will transition seamlessly into a modern, automated records retention and compliance system, reducing administrative burden while ensuring compliance and accessibility.**

## Appendix A: Metadata Training and Reference Guide

### **Section 1: Training & How-to Instructions**

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

## Appendix B: Contract Management Metadata and Automation Guide

### 1 Document Set Structure & Metadata

- Primary Contract Type captures the highest-level classification of the contract (e.g., On-Call Consultant Agreement for multiple Task Orders).
- Managed Metadata is used for Contract Types instead of Choice fields to allow for future flexibility.
- The Managed Metadata Term Set for Contract Types was created in the **Term Store** under "Search Directories."
- Two Managed Metadata columns were created:
  - **Primary Contract Type** (stored at the Document Set level to categorize the contract at the highest level)
  - **Contract Type (Document Level)** (stored at the document level to allow classification for individual documents)
- These fields will be leveraged later in **Microsoft Purview** to support retention policies and compliance automation.

### **2 Managed Metadata Term Set for Contract Types**

| **Contract Type** | **Description** |
| --- | --- |
| Capital Project | A contract for the design, construction, or major improvement of public infrastructure, buildings, or facilities. |
| Grant Agreement | A formal agreement outlining the terms under which funding is provided by a government or organization for a specific project or purpose. |
| Interagency Agreement (IAA) | A contract between two government agencies outlining responsibilities, funding, and resource-sharing for a project or service. |
| Interlocal Agreement (ILA) | A legal agreement between two or more local governments to collaborate on shared services, infrastructure, or responsibilities. |
| Memorandum of Understanding (MOU) | A non-binding agreement that outlines the intentions and responsibilities of two or more parties in collaboration. |
| Consultant Agreement | A contract for hiring an external consultant to provide professional expertise or services for a project or initiative. |
| Professional Services | A contract for specialized professional services such as legal, financial, engineering, or IT services. |
| Contract | A general legal agreement between parties outlining obligations, deliverables, and terms. Use this category for contracts that do not fit other specific types. |
| Purchase Agreement | A contract for the purchase of goods, equipment, or materials from a vendor. |
| Franchise Agreement | A contract granting a company or entity the rights to operate a service (e.g., utilities, telecommunications) under a city's jurisdiction. |
| Task Order | A contract issued under a broader agreement that authorizes specific work or services for a particular scope and period. |
| On-Call Consultant Agreement | A contract that establishes a pool of pre-approved consultants who can be assigned projects as needed without a separate procurement process. |
| Other | For contracts that do not fit any of the predefined categories. Users should specify details in an additional field if possible. |

### **3 Contract Numbering System**

- Format: YYYY-XXX (Year + Sequential Number)
- The Contract Number is stored as a Number field but displayed as YYYY-XXX using JSON formatting.
- Users must enter numbers manually (e.g., 2024001), but formatting will display it as 2024-001.
- Sorting is preserved by keeping the underlying value as a number.
- If a contract number is reassigned, the system does not remember past numbers and will always assign the next highest available number when generating a new contract.

### JSON Formatting for Contract Number Display:**
```json
{  
"$schema": "https://developer.microsoft.com/json-schemas/sp/v2/column-formatting.schema.json",  
"elmType": "div",  
"attributes": {  
"isValidNumber": "=if(@currentField >= 1000000 && @currentField < 10000000, 1, 0)",  
"contractYear": "=toString(floor(@currentField / 1000))",  
"contractSeq": "=padStart(toString(@currentField % 1000), 3, '0')"  
},  
"txtContent": "=if(\[$isValidNumber\] == 1, \[$contractYear\] + '-' + \[$contractSeq\], 'No Contract Number Assigned')"  
}
```
### **4 Power Automate for Assigning Contract Numbers**

### Summary of Power Automate Flow:**

1. **Trigger**: Runs when a new Document Set is created.
2. **Condition**: Checks if the Contract Number is empty or invalid (less than 1000000).
3. **Action**:
    1. Finds the highest contract number for the current year in the document library.
    2. Determines the next available sequential number.
    3. Assigns the new contract number in the format YYYYXXX.
4. **Final Step**: Updates the Document Set metadata with the assigned contract number.

This automation ensures that contract numbers are always assigned in order without tracking past reassignments.

### **5 Future Considerations**

- Future improvements may include:
  - Integrating PowerApps as a front-end interface for browsing and managing contracts.
  - Enhancing compliance and retention automation in **Microsoft Purview** using the Managed Metadata fields.
  - Exploring additional automation options to streamline contract lifecycle management.

### **Next Steps**

1. Complete Power Automate for Contract Numbering.
2. Finalize and test JSON formatting for contract number display.
3. Confirm Managed Metadata Term Set structure.
4. Plan and develop PowerApps interface in the future.

## Appendix C: Using the REST API to Collect JSON from State Archives

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

### Overview

Once JSON data is retrieved, it needs to be cleaned and formatted before uploading it to SharePoint via Microsoft Graph API. The following Python script automates this process.

**Python Script**
```python
import requests
import json
import re

# Base API URL
API_BASE_URL = "https://api.digitalarchives.wa.gov/api/retention-schedules/"

# Function to determine which schedule to pull from
def get_schedule_id():
	"""Prompt user or determine which retention schedule ID to use."""
	schedules = {
		"CORE": 3,
		"Law Enforcement": 5,
		"Public Utilities": 7
	}
	print("Available Retention Schedules:")
	for name, id in schedules.items():
		print(f"{name}: {id}")
	choice = input("Enter the name of the retention schedule to pull: ").strip()
	return schedules.get(choice, 3) # Default to CORE if not found

SCHEDULE_ID = get_schedule_id()
API_URL = f"{API_BASE_URL}{SCHEDULE_ID}"
OUTPUT_FILE = "purview_retention_labels.json"

# Function to extract and format the display name
def extract_display_name(name):
	"""
	- Extracts only the first line from the name field
	- Removes leading/trailing whitespace
	- Removes invalid characters per Microsoft Purview requirements
	- Truncates to 64 characters max
	"""
	if not name:
		return "Default_Label"
	cleaned_name = name.split("\r\n")[0].strip()
	cleaned_name = re.sub(r"[\\%&<>|?:;/*,\x00\x08\x0B\x0C\x0E-\x1F]", "", cleaned_name) # Remove invalid characters
	return cleaned_name[:64] # Truncate to 64 characters

# Function to convert retention period from text to days
def convert_retention_to_days(retention_text):
	match = re.search(r"(\d+) year", retention_text)
	if match:
		return int(match.group(1)) * 365 # Convert years to days
	match = re.search(r"(\d+) month", retention_text)
	if match:
		return int(match.group(1)) * 30 # Convert months to days
	match = re.search(r"(\d+) day", retention_text)
	if match:
		return int(match.group(1)) # Keep as days
	return -1 # Default to indefinite retention

# Function to determine the disposition action
def determine_disposition_action(retention_text):
	if "Destroy" in retention_text:
		return "delete"
	if "Review" in retention_text:
		return "startDispositionReview"
	return "none" # Default if action is unclear

# Function to format multi-line descriptions
def format_description(text):
	"""Ensures multi-line formatting remains intact and replaces en dashes"""
	return text.replace("\u2013", "-").replace("\r", "").strip()

# Step 1: Fetch latest retention schedule JSON
response = requests.get(API_URL)
if response.status_code != 200:
	print(f"Failed to fetch data: {response.status_code}")
	exit()

data = response.json()

# Step 2: Extract retention schedule details
schedule = data.get("returnValue", {})
local_schedules = schedule.get("localSchedules", [])

# Step 3: Prepare transformed data for Microsoft Purview
purview_labels = []

for record in local_schedules:
	# Only process active retention labels
	if not record.get("isActive", False):
		continue

	# Extract category information
	category_name = record.get("category", {}).get("categoryName", "Uncategorized")

	# Extract citation details if available
	citation_text = record.get("citation", "")

	label = {
		"displayName": extract_display_name(record["seriesTitleDescription"]),
		"descriptionForUsers": format_description(record["seriesTitleDescription"]),
		"descriptionForAdmins": format_description(record["primaryCopyRetention"]),
		"retentionTrigger": "dateCreated",
		"retentionDuration": {"@odata.type": "#microsoft.graph.security.retentionDurationInDays", "days": convert_retention_to_days(record["primaryCopyRetention"])},
		"actionAfterRetentionPeriod": determine_disposition_action(record["primaryCopyRetention"]),
		"isRecordLabel": bool(record.get("archival", False)),
		"behaviorDuringRetentionPeriod": "retain", # Ensuring this is explicitly defined
		"filePlanDescriptors": {
			"category": {
				"name": category_name
			},
			"citation": {
				"name": schedule.get("scheduleName", "CORE (Local Government Common Records Retention Schedule)"),
				"url": "https://www.sos.wa.gov/archives/recordsmanagement/local-government-records-retention-schedules---alphabetical-list.aspx"
			}
		}
	}

	purview_labels.append(label)

# Step 4: Save transformed data to a new JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
	json.dump(purview_labels, outfile, indent=4)

print(f"Transformed data saved to {OUTPUT_FILE}")
```

### Updated Core Principles for Applying Retention Policies

1. **Selective Retention Policy Application**
    - Only apply the specific labels that are needed at a given time.
    - Implement a step to select which retention policy to push to Purview via Graph API.
2. **Structured Preparation Before Purview Integration**
    - Add items to Purview _only_ after establishing a Document Library.
    - Configure the Document Library with Document Sets and all relevant metadata required for Purview.
3. **Automated Labeling**
    - Utilize automation to auto-label documents based on predefined metadata and configurations.

## Appendix E: Example JSON Ready for Graph API

**Overview**

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

## Appendix F: Microsoft Graph API Endpoints for Label Management

**Microsoft Documentation Reference**

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

## Appendix G: SharePoint Step-by-Step Guide: Moving Contract Files

| **Step** | **Instructions** |
| --- | --- |
| **1** | Open SharePoint. Click **Contracts** from the left navigation, then click **Contract (Copy of Folder from Clerks Library)** and select the next working folder |
| **2** | Find your specific folder (ex. 2024, 2023, 2022). Locate the next contract.<br><br>**Click once in the white space next to the folder name** (do not click directly on the name). |
| **3** | After selecting the folder, click **Rename** from the toolbar at the top. |
| **4** | Highlight the folder name with the mouse-drag and right-click on the highlighted text and choose **Copy** then close the Rename window. |
| **5** | **\[Switch screens\]**<br><br>Click **\+ New** (top-left), then select **Contracts Document Set**. |
| **6** | **Name —** Right-click and choose **Paste**. Remove the numbers/dash, leaving only the contract name (e.g., _Snohomish County Conservation District ILA_). |
| **7** | **Contract Number —** type numbers only as **YYYYXXX** (e.g., **2024022**). |
| **8** | **Primary Contract Type —** Click the tag icon on the right to show all contract types and choose the appropriate type. This step may require reading the documents inside the original folder and gathering information from context. |
| **9** | **Department & Division —** Click the tag icon and select the appropriate option. Leave blank if unsure. |
| **10** | **Vendor/Party Name —** Type the most appropriate name, if unsure leave blank. If multiple, leave blank. |
| **11** | **Effective Date** and **Expiration Date —** Search contract documents. Leave blank if unsure. Close the preview window of the document you were searching for information. |
| **12** | **Click Save** and **Switch screens**<br><br>Return to the original folder on the other screen. |
| **13** | Click the circle next to each file to select all documents (blue checkmarks appear). |
| **14** | On the toolbar, click **Move to**. (“**...”** on the toolbar if Move to is not visible) |
| **15** | Click “**...”,** then **Contracts**, then select the _Document Set_ you created in step 5. |
| **16** | Click **Move Here**. Completed, move to the next folder |
