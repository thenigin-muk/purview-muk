# Microsoft Graph API Security Orchestration

This system provides a **secure, modular** approach to Microsoft Graph API access, following the principle of **least privilege**.

## Getting Started

### 1. Initialize Setup

#### What This Step Does
- Sets up a **master app registration** in Microsoft Entra ID.
- Allows the creation of specialized **app registrations** with specific permissions.
- Generates Python **API modules** for authentication and interaction.

#### What You'll Need
- **Global Administrator** permissions (or have an admin approve your registration).
- Access to **Microsoft Entra ID**.
- A local Python environment with `venv` installed.

#### How the Setup Works
When you run the setup command, the orchestrator will:
1. **Guide you through app registration** in the Microsoft Entra Admin Center.
2. **Ask for required information:**
   - Tenant ID
   - Client ID
   - Client Secret
3. **Validate credentials** by attempting authentication.
4. **Store the configuration** securely for future use.

#### Step 1: Verify Your Environment
Before running the script, make sure:
- You’re in the correct **project directory**.
- Your **virtual environment is activated**.

Use:
```bash
pwd  # Print current directory
```

Or copy and paste the following to verify and correct it:
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

#### Step 2: Run the Setup Script
Once your environment is set up, start the master app registration:

```bash
python setup_graphapi.py --setup
```

This will:
- **Walk you through the app registration** process.
- **Validate credentials** before storing them.
- **Prepare your environment** for further registrations.

> **Important:** The master app will have the permissions required to create other **app registrations**.

---

### 2. Creating Specialized App Registrations
This step creates **purpose-specific app registrations** in Microsoft Entra ID.

#### What This Step Does
- **Registers a new app** in Entra ID.
- **Assigns minimum necessary permissions**.
- **Creates and securely stores credentials**.
- **Updates configuration** for tracking.

#### Command Format
```bash
python setup_graphapi.py --create-app [APP_NAME] --description "[DESCRIPTION]" --permissions [PERMISSIONS]
```

#### Required Parameters
| Parameter | Description |
|-----------|------------|
| `--create-app [APP_NAME]` | Name of the new app (e.g., `sharepoint`, `teams`, `mail`). |
| `--permissions [PERMISSIONS]` | **Space-separated list** of required Microsoft Graph permissions. |

For a **full list of permissions**, see:  
[Microsoft Graph API Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)

#### Optional Parameters
| Parameter | Description |
|-----------|------------|
| `--description "[DESCRIPTION]"` | (Optional) Description of the app’s purpose. |

#### Examples
##### 1. Create a SharePoint App
```bash
python setup_graphapi.py --create-app sharepoint --description "SharePoint operations" --permissions Sites.Read.All Sites.ReadWrite.All
```
##### 2. Create a Teams Management App
```bash
python setup_graphapi.py --create-app teams --description "Teams operations" --permissions Team.ReadBasic.All Channel.ReadBasic.All
```
##### 3. Create an Email Processing App
```bash
python setup_graphapi.py --create-app mail --description "Email processing" --permissions Mail.Read Mail.Send
```

---

### 3. Generating API Modules
Once the app registration is created, generate its **Python module**:

```bash
python setup_graphapi.py --generate-module [APP_NAME]
```

#### Example
```bash
python setup_graphapi.py --generate-module sharepoint
```

### Generated API Modules

The `api_modules/` directory created by the orchestrator contains organization-specific  
code that should **NOT** be committed to version control. These are added to `.gitignore`  
by default.

Each developer or organization should:
1. Run the setup process locally
2. Generate their own modules
3. Keep the secret files secure

or

set your branch to private and invite IT Admins

or 

Clone the repository and run in a private repo

---

## Security Best Practices
- **Least Privilege:** Each app gets only the permissions it needs.
- **Secret Management:** Credentials stored in environment variables or secure `.env` files.
- **Audit Trail:** App registrations and permissions documented automatically.
- **Secret Rotation:** Implement regular secret rotations.

---

## Key Benefits
1. **Automated Security** – Ensures all app registrations follow best practices.
2. **Consistent Configuration** – Every project uses the same secure framework.
3. **Minimal Permissions** – Only required permissions are assigned.
4. **Separation of Concerns** – Authentication is handled outside application logic.
5. **Self-Documenting** – Modules include generated README files.

This system significantly **improves security** while making Microsoft Graph API integration **easier and repeatable**.

---

## Summary of Commands
| **Task** | **Command** |
|----------|------------|
| **Set up the master app** | `python setup_graphapi.py --setup` |
| **Create an app registration** | `python setup_graphapi.py --create-app [APP_NAME] --description "[DESC]" --permissions [PERMISSIONS]` |
| **Generate API module** | `python setup_graphapi.py --generate-module [APP_NAME]` |

---

## Final Thoughts
This **orchestration system** improves security **while simplifying API access**.  
By following **best practices from the start**, you ensure every new project is **secure, modular, and compliant**.
