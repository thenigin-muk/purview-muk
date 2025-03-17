<!-- description: Documentation about Environment Setup & Prerequisites for Your Organization. -->

# Environment Setup & Prerequisites

### Site Navigation
[🏠 Home](../../README.md) | [📂 All Workflows](../../users/users.md) | [⚙ IT Admin Docs](../../it-admins/README.md) | [⬅ Back to Setup](../README.md)

## Prerequisites
- Windows Subsystem for Linux (WSL) or a virtual environment
- Git installed and configured
- Visual Studio Code (recommended) with necessary extensions

## Installation Steps
1. Install WSL: [Microsoft WSL Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Install Git: [Git Download](https://git-scm.com/downloads)
3. Install VS Code: [VS Code Download](https://code.visualstudio.com/)
4. Configure SSH keys for GitHub:

From your WSL Environment

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

5. **Add the SSH key to your GitHub account**:
    - Copy the SSH key to your clipboard:
    ```sh
    cat ~/.ssh/id_rsa.pub
    ```
    - Go to your GitHub account settings, navigate to "SSH and GPG keys", and add a new SSH key. Paste the key from your clipboard.

6. **Connect to the repository**:
    - Navigate to your project folder:
    ```sh
    cd ~/git-projects/purview-muk
    ```
    - Initialize a new Git repository if you haven't already:
    ```sh
    git init
    ```
    - Add the remote repository using the SSH URL. Replace `git@github.com:username/repo.git` with your repository's SSH URL:
    ```sh
    git remote add origin git@github.com:username/repo.git
    ```
    - Verify the remote repository has been added:
    ```sh
    git remote -v
    ```
    - Fetch the latest changes from the remote repository:
    ```sh
    git fetch origin
    ```
    - Pull the latest changes from the remote repository:
    ```sh
    git pull origin main
    ```

7. **Create a new branch**:
    - Create and switch to a new branch:
    ```sh
    git checkout -b your-branch-name
    ```

8. **Run the setup script**:
    - Make the setup script executable:
    ```sh
    chmod +x setup.sh
    ```
    - Run the setup script:
    ```sh
    ./setup.sh
    ```

## Next Steps
- Follow the step-by-step instructions provided.
- Ensure all dependencies and configurations are in place.
- If encountering issues, refer to the [Troubleshooting Guide](10-troubleshooting.md).

---

[⬅ Previous: 0 Setup Guide](0-setup-guide.md) | [Next: 10 Troubleshooting ➡](10-troubleshooting.md)