# SharePoint & Microsoft Purview for Records Management & Compliance
### Future Forward: Structuring for Effective Digital Records Management

## Purpose & Audience

This document serves as a guide for **records managers, IT administrators, and departmental staff** responsible for implementing SharePoint-based document management. It outlines best practices for **structuring document libraries, applying metadata, and automating retention policies** using SharePoint and Microsoft Purview.

### Scope of This Document

This initiative focuses **solely on the management of stored documents** within our organization’s **Windows File Server and SharePoint libraries**. It **does not** address records management for data stored inside applications, such as SmartGov, GovQA, Eden, and many other places where data resides. The key distinction is if that file is accessible today using WIndows File Explorer it probably applies to this documentation. **Application-based records remain managed within their respective systems.**

### Approach & Expectations

Our goal is to create **new workspaces based on organizational workflows** to improve records management. Departments and staff responsible for these records will be expected to **migrate documents into newly created SharePoint spaces.**

This is a **long-term, collaborative effort** between IT and designated department staff to ensure proper **document library structures are built** within SharePoint. IT will work **closely with each department or workflow owner** to establish relevant document libraries and retention policies.

By following this guide, organizations can streamline records retention, enhance searchability, and ensure compliance with regulatory requirements while maintaining a structured and manageable document repository.

## Introduction

Effective records management is crucial for compliance, efficiency, and accessibility. This document provides a structured approach to transitioning from traditional **Windows File Servers** to a **modern digital records management system using SharePoint and Microsoft Purview**.

Key topics covered:

- **Why SharePoint?** Advantages over traditional file storage.
- **Metadata & Auto-Labeling** for better organization.
- **Automated Retention & Compliance** to streamline recordkeeping.
- **Email Retention & Public Records Requests** to ensure accountability and legal compliance.
- **Compliance Manager for audits and legal holds** to support transparency and governance.

This guide will help organizations move toward a more **structured, automated, and efficient** records management system by leveraging metadata, auto labeling, and automated disposition workflows. The implementation is **incremental**, ensuring that each department and workflow is introduced in a manageable way, allowing for continuous evaluation and improvement without overwhelming staff.

---

## 📌 Where Should You Start?
🔹 **New Users & Employees** → Start with the [Learning Path](docs/learning-path/0-tableofcontents.md).  
🔹 **Users Managing Documents in Workflows** → Select your [Workflow Guide](docs/users/).
🔹 **IT Administrators** → Go to the [Admin Folder](docs/it-admins/).  

---

### **User Guides for each Workflow**
These sections provide **step-by-step guides** for **users managing workflows** in SharePoint.

- [Contracts Management](docs/users/contracts/)
- [Council Meetings](docs/users/council-meetings/)
- [eDiscovery Cases](docs/users/purview/ediscovery/)
- [Records Management](docs/users/purview/records-management/)
- [Email Retention](docs/users/email-retention/)
- [Purchase Cards (P-Cards)](docs/users/purchase-cards/)

---

## 📂 Folder Structure & Organization
This repository is structured to **separate user guides, workflows, and IT administration**.

### 📁 **docs/**
- **users/** → Guides for end users, organized by workflow.
  - **learning-path/** → Structured training on SharePoint & Purview.
  - **[Workflow Name]/** → User guides for specific workflows (e.g., contracts, meetings, records).
- **it-admins/** → Documentation for IT administrators.
  - **core-concepts/** → Technical guides (Graph API, REST API, metadata).
  - **solutions/** → Configuration guides for Microsoft 365 admin centers (Purview, Exchange, SharePoint).
  - **workflows/** → IT-specific workflow configurations (contracts, meetings, email retention).

### 📁 **workflows/**
- Stores JSON schemas, metadata configurations, and automation scripts for workflows.