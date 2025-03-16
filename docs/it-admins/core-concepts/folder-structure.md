# Folder Structure Overview
The project is organized into several key directories to streamline access to documentation and ensure clarity in roles and responsibilities. Below is an outline of the folder structure:

Root Directory
README.md: The main file providing an overview of the project, instructions, and links to other key documentation.
docs/: Contains all the documentation related to workflows, administrative guides, and training materials.
workflows/: Contains metadata schemas, workflow-specific application files, and setup documentation.
docs/ Folder
The docs/ directory holds all of the project's documentation, organized by user roles and workflows:

it-admins/: This folder contains administrative guides and setup documentation specific to the workflows. It includes:

{workflow}/setup/: Contains metadata schemas and any setup instructions for each workflow (e.g., metadata-schema.md).
{workflow}/admin-guide.md: Administrative guides for managing each workflow.
users/: This folder is dedicated to user-facing documentation. It is further divided into subfolders for each workflow:

{workflow}/task-guides/: Contains user-specific task guides (e.g., "how-to" documents for specific processes in the workflow).
{workflow}/training/: Contains long-term training materials and reference guides for users to review at any time.
{workflow}/supervisors/: Contains supervisor-specific documentation. Supervisors can reference these materials for additional instructions and their responsibilities within the workflow.
Example structure for the docs/ folder:

pgsql
Copy
Edit
docs/
├── it-admins/
│   ├── contracts/
│   │   ├── setup/
│   │   │   └── metadata-schema.md
│   │   └── admin-guide.md
│   ├── purchase-cards/
│   │   ├── setup/
│   │   └── admin-guide.md
│   └── purview/
│       ├── setup/
│       └── admin-guide.md
├── users/
│   ├── contracts/
│   │   ├── task-guides/
│   │   ├── training/
│   │   └── supervisors/
│   ├── purchase-cards/
│   │   ├── task-guides/
│   │   ├── training/
│   │   └── supervisors/
│   ├── ediscovery/
│   │   ├── task-guides/
│   │   ├── training/
│   │   └── supervisors/
│   └── purview/
│       ├── task-guides/
│       ├── training/
│       └── supervisors/
workflows/ Folder
The workflows/ directory contains files specific to each workflow, including metadata schemas and application-related files. These are typically used by IT administrators during setup and configuration.

{workflow}/metadata-schema.md: Contains the metadata schema for the workflow, detailing the structure and fields needed for each record in the workflow.
{workflow}/metadata-schema.json: A JSON version of the metadata schema, often used for integration or automation processes.
{workflow}/app/: Contains application-related files or configuration scripts for each workflow (e.g., API integration scripts, app configuration files).
Example structure for the workflows/ folder:

graphql
Copy
Edit
workflows/
├── contracts/
│   ├── metadata-schema.md
│   └── app/
├── purchase-cards/
│   ├── metadata-schema.md
│   └── app/
└── purview/
    ├── metadata-schema.md
    └── app/
Summary
This folder structure is designed to maintain clarity between user documentation, supervisor-specific materials, and IT/admin setup resources. It ensures that each role has easy access to the right level of information, and provides a straightforward way to organize and scale the project’s documentation over time.