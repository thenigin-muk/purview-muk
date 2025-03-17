<!-- description: Documentation about Environment Setup & Prerequisites for Your Organization. -->
# Environment Setup & Prerequisites

### Site Navigation

## Overview
This section provides a detailed guide on **Environment Setup & Prerequisites**, including setup steps and best practices.

## Prerequisites
- Windows Subsystem for Linux (WSL) or a virtual environment
- Git installed and configured
- Visual Studio Code (recommended) with necessary extensions

## Installation Steps
1. Install WSL: [Microsoft WSL Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Install Git: [Git Download](https://git-scm.com/downloads)
3. Install VS Code: [VS Code Download](https://code.visualstudio.com/)
4. Configure SSH keys for GitHub:
```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
```

## Next Steps
- Follow the step-by-step instructions provided.
- Ensure all dependencies and configurations are in place.
- If encountering issues, refer to the [Troubleshooting Guide](10-troubleshooting.md).

---

[⬅ Previous: 0 Setup Guide](0-setup-guide.md) | [Next: 10 Troubleshooting ➡](10-troubleshooting.md)