<!-- description: Documentation about Managed Metadata & Term Sets in SharePoint for Your Organization. -->
# Managed Metadata & Term Sets in SharePoint

### Site Navigation

## Why Managed Metadata Matters
Managed Metadata allows organizations to standardize classification across SharePoint libraries. Instead of manually entering values, predefined **Term Sets** ensure consistency, reduce errors, and improve searchability.

## How Term Sets Work
- Term Sets are **centrally managed** in the **SharePoint Term Store**.
- They provide **consistent categories** across different document libraries.
- Changes made to a term **update all connected sites & columns automatically**.

## Planning Your Term Sets
Before implementing workflows, organizations **must decide** on the **term sets** they will use. Common term sets include:
- **Contract Types** (e.g., Capital Project, Grant, ILA)
- **Departments & Divisions** (e.g., IT, Finance, Public Works)
- **Policy Categories** (e.g., HR Policy, IT Security, Records Management)
- **Document Types** (e.g., Invoice, Report, Agreement)

## Example: Contract Type Term Set
| **Term** | **Description** |
|----------|---------------|
| Capital Project | Major infrastructure or facility contract |
| Grant Agreement | Government or agency-provided funding |
| Interlocal Agreement | Shared services between government entities |

## How This Integrates into Workflows
1. **Define the Term Sets** in SharePoint Admin Center.
2. **Ensure Each Term Set Has a GUID** for automation.
3. **Use Managed Metadata Columns** to reference these terms.
4. **Sync Metadata with Automation Scripts** to enforce consistency.

## Next Steps
- **Set up Term Sets** before configuring workflows.
- **Document all Term Sets** in \`managed-metadata.json\` for automation.
- **Use Power Automate or Graph API** to integrate term sets into metadata.

---

[Next: Retention Policies ➡](retention-policies.md)