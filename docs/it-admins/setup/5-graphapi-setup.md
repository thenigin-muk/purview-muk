# Microsoft Graph API Security Orchestration

This system provides a secure, modular approach to Microsoft Graph API access following the principle of least privilege.

## Getting Started

### 1. Initial Setup

**This step you will**
- Set up a master app registration in Entra ID
- Creating specialized app registrations with specific permissions
- Generating Python modules for these app registrations


**What to Expect During Setup**
When you run the setup command, the orchestrator will:

1. Welcome you to the setup process with a brief explanation
2. Guide you through creating an app registration in Entra ID:
- You'll be instructed to go to the Microsoft Entra Admin Center
- Create a new app registration named "Security-Orchestrator-Master" or similar
- Note down the client ID
- Add the required API permissions
- Create a client secret and note its value
3. Collect information about the registration:
- Tenant ID
- Client ID
- Client Secret
4. Test the credentials to verify they work
5. Store the configuration for future use

**You will require**
- Global Admin Permission to Grant Consent
- If you do not have Global Admin permission to Grant consent, follow the above steps above, and ask your Global Admin to grant the permissions. Then, start the script when you have the IDs and Secret.

**To setup the master app registration, in your shell .venv**

Enter venv if you're not there, and make sure you're at the root project folder.

You can check if your source folder with

```bash
pwd
```

If you're unsure, copy and paste the follow bash:

```bash
#!/bin/bash

# Ensure the script is run from the correct project directory
if [[ ! -f "setup_graphapi.py" ]]; then
    echo "Error: You are not in the correct project folder."
    echo "Navigate to the project folder first:"
    echo "   cd /path/to/your/project"
    return 1 2>/dev/null || exit 1
fi

# Check if a virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Error: Virtual environment is not activated."

    # Detect OS type for correct activation command
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "Run: venv\\Scripts\\activate (Windows)"
    else
        echo "Run: source venv/bin/activate (Mac/Linux)"
    fi

    return 1 2>/dev/null || exit 1
fi

echo "Environment check passed. You can proceed."

```

Once you've confirmed your enviroment, start with:

```bash
python setup_graphapi.py --setup
```
This will:

- Guide you through creating a master app registration in Azure AD
- Ask for necessary information (tenant ID, etc.)
- Store credentials securely

**This master app registration will have the permissions needed to create other app registrations**

### 2. Create Specialized App Registrations

This step creates purpose-specific app registrations in Microsoft Entra ID, each with only the minimum permissions required for their function.

**What This Step Does:**
- Creates a new app registration in your Entra ID tenant
- Assigns specific API permissions according to your requirements
- Creates a client secret for authentication
- Stores the credentials securely in a `.env.[app-name].secret` file
- Updates the security configuration with the new app details



**Command Format:**

```bash
python setup_graphapi.py --create-app sharepoint --description "SharePoint operations" --permissions Sites.Read.All Sites.ReadWrite.All
```
```bash
python setup_graphapi.py --create-app teams --description "Teams operations" --permissions Team.ReadBasic.All Channel.ReadBasic.All
```

**Required Parameters:**

--create-app [APP_NAME]: Name of the app (e.g., sharepoint, teams, mail)
--permissions [PERMISSIONS]: **Space-separated list** of Microsoft Graph permissions

For a list of permissions:

https://learn.microsoft.com/en-us/graph/permissions-reference

**Optional Parameters:**

--description "[DESCRIPTION]": Human-readable description of the app's purpose

**Examples:**

1. Create a SharePoint Operations App

```bash
python setup_graphapi.py --create-app sharepoint --description "SharePoint operations" --permissions Sites.Read.All Sites.ReadWrite.All
```
2. Create a Teams management app:

```bash
python setup_graphapi.py --create-app teams --description "Teams operations" --permissions Team.ReadBasic.All Channel.ReadBasic.All
```
3. Create a maill Processing app:
```bash
python setup_graphapi.py --create-app mail --description "Email processing" --permissions Mail.Read Mail.Send
```

### 3. Generate API Modules
Generate Python modules for the app registrations:


```bash
python setup_graphapi.py --generate-module sharepoint
```

### Generated API Modules

The `api_modules/` directory created by the orchestrator contains organization-specific 
code that should NOT be committed to version control. These are added to `.gitignore` 
by default.

Each developer or organization should:
1. Run the setup process locally
2. Generate their own modules
3. Keep the secret files secure

or

set your branch to private and invite IT Admins

or 

Clone the repository and run in a private repo

## Security Best Practices
- Least Privilege: Each app registration has only the permissions it needs
- Secret Management: Secrets are stored in environment variables or secure files
- Audit Trail: All app registrations are documented in configuration files
- Secret Rotation: Implement regular secret rotation


## Key Benefits of This Approach

1. **Programmatic Setup**: You automate the creation of properly secured app registrations
2. **Consistent Security**: Every new project follows the same secure pattern
3. **Modular Access**: Each module has only the permissions it needs
4. **Separation of Concerns**: Authentication is handled by the module, not your business logic
5. **Documentation**: Self-documenting approach with READMEs for each module

This orchestration system will significantly enhance your security posture while making it easier to build new applications that interact with Microsoft Graph API. The modular approach ensures you follow best practices from day one of any new project.

