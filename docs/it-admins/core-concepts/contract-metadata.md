# Contract Management Metadata and Automation Guide

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
