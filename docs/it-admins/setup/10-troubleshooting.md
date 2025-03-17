<!-- description: Documentation about Troubleshooting & Common Issues for Your Organization. -->

# Troubleshooting & Common Issues

### Site Navigation
[🏠 Home](../../README.md) > [It Admins](../README.md) > [Setup](README.md) | [⬅ Back to Setup](README.md)

## Common Issues & Fixes
| Issue | Cause | Solution |
|-------|--------|----------|
| Git authentication error | SSH key missing or incorrect | Ensure SSH key is generated and added to the SSH agent. Verify the SSH key is added to your GitHub account. |
| Repository not found | Incorrect repository URL | Verify the repository URL and update the remote URL using `git remote set-url origin git@github.com:username/repo.git`. |
| API permission denied | Missing API permissions in Azure AD | Verify role assignments and ensure the necessary permissions are granted. |
| pip not installed | pip is required but not installed | Install pip using `sudo apt install python3-pip`. |
| Python script failing | Missing dependencies | Create a virtual environment and install the required dependencies using the following steps: |
| | | 1. Create a virtual environment: `python3 -m venv path/to/venv` |
| | | 2. Activate the virtual environment: `source path/to/venv/bin/activate` |
| | | 3. Install dependencies: `pip install -r requirements.txt` |

## Next Steps
- Follow the step-by-step instructions provided.
- Ensure all dependencies and configurations are in place.
- If encountering issues, refer to the [Troubleshooting Guide](10-troubleshooting.md).

---

[⬅ Previous: 1 Environment Setup](1-environment-setup.md) | [Next: 2 Git Version Control ➡](2-git-version-control.md)