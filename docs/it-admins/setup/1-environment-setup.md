<!-- description: Documentation about Environment Setup & Prerequisites for Your Organization. -->

### Site Navigation
[🏠 Home](../../README.md) | [📂 All Workflows](../../users/users.md) | [⚙ IT Admin Docs](../README.md)

# Environment Setup & Prerequisites

## Prerequisites
- Windows Subsystem for Linux (WSL) or a virtual environment
- Git installed and configured
- Visual Studio Code (recommended) with necessary extensions

## Installation Steps
1. Install WSL: [Microsoft WSL Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Install Git: [Git Download](https://git-scm.com/downloads)
3. Install VS Code: [VS Code Download](https://code.visualstudio.com/)
4. Configure SSH keys for GitHub:

```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

  Follow the prompts to save the key to the default location (`~/.ssh/id_rsa`) and set a passphrase if desired.

  **Add the SSH key to the agent**:
  Once the SSH key is generated, you can add it to the SSH agent using the following command:
  
```sh
ssh-add ~/.ssh/id_rsa
```

  **Start the SSH agent**:
  If the SSH agent is not running, you can start it with the following command:
  
```sh
eval "$(ssh-agent -s)"
```

## Next Steps
- Follow the step-by-step instructions provided.
- Ensure all dependencies and configurations are in place.
- If encountering issues, refer to the [Troubleshooting Guide](10-troubleshooting.md).

---

[⬅ Previous: 0 Setup Guide](0-setup-guide.md) | [Next: 10 Troubleshooting ➡](10-troubleshooting.md)
