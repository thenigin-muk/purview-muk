#!/usr/bin/env python3

import os
import re
import argparse
from pathlib import Path
import yaml
from jinja2 import Template

# Load configuration
def load_config():
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            # Ensure 'paths' key exists in the configuration
            if 'paths' not in config:
                config['paths'] = {
                    "docs_dir": "docs",
                    "workflows_dir": "docs/users",
                    "admin_dir": "docs/it-admins"
                }
            return config
    return {
        "organization_name": "{{ORGANIZATION_NAME}}",
        "state_name": "{{STATE_NAME}}",
        "department": "{{DEPARTMENT}}",
        "contact_email": "{{CONTACT_EMAIL}}",
        "paths": {
            "docs_dir": "docs",
            "workflows_dir": "docs/users",
            "admin_dir": "docs/it-admins"
        }
    }

# Create a configuration file if it doesn't exist
def ensure_config():
    config_path = Path("config.yaml")
    if not config_path.exists():
        default_config = {
            "organization_name": "Your Organization",
            "state_name": "Your State",
            "department": "Records Management",
            "contact_email": "records@example.gov",
            "paths": {
                "docs_dir": "docs",
                "workflows_dir": "docs/users",
                "admin_dir": "docs/it-admins"
            }
        }
        with open(config_path, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
        print(f"✅ Created configuration file: {config_path}")
        print("⚠️ Please edit the config.yaml file with your organization's information")
        return default_config
    return load_config()

# Calculate relative path between files
def get_relative_path(target, source_file):
    source_dir = Path(source_file).parent
    docs_dir = Path("docs")
    try:
        depth = len(source_dir.relative_to(docs_dir).parts)
    except ValueError:
        depth = 0
        
    if depth == 0:
        return f"./{target}"
    return "../" * depth + target

# Update the generate_navigation function to add breadcrumbs to all files
def generate_navigation(file_path, config):
    """Generate navigation for a markdown file"""
    file_path = Path(file_path)
    
    # Skip the root README as it's the starting point
    if file_path == Path("docs/README.md"):
        print(f"🛑 Skipping root README.md")
        return
        
    # Read content
    content = file_path.read_text()
    
    # First clean up any existing navigation to prevent duplication
    # Remove duplicate Site Navigation sections
    pattern = r'(### Site Navigation\n.*?\n\n)### Site Navigation\n.*?\n\n'
    content = re.sub(pattern, r'\1', content, flags=re.DOTALL)
    
    # Remove existing Site Navigation (we'll add a fresh one)
    pattern = r'### Site Navigation\n.*?\n\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove existing bottom navigation links
    pattern = r'\n\n---\n\n\[.*?\].*?(\n|$)'
    content = re.sub(pattern, '\n', content)
    
    # Get title from first heading or filename
    title_match = re.search(r'^# (.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()
    
    # Calculate relative paths
    home_path = get_relative_path("README.md", file_path)
    workflows_path = get_relative_path("users/users.md", file_path)
    admin_path = get_relative_path("it-admins/README.md", file_path)
    
    # Create top navigation - add to ALL files now, including README files
    top_nav = f"### Site Navigation\n"
    top_nav += f"[🏠 Home]({home_path}) | [📂 All Workflows]({workflows_path}) | [⚙ IT Admin Docs]({admin_path})\n"
    
    # If inside workflow, add back link
    folder_path = file_path.parent
    workflow_match = re.search(r'users/([^/]+)', str(folder_path))
    if workflow_match:
        workflow_name = workflow_match.group(1)
        top_nav += f"[⬅ Back to {workflow_name}](../README.md)\n"

    # If in a learning path, add link back to table of contents
    if "learning-path" in str(file_path) and file_path.name != "0-tableofcontents.md":
        toc_path = get_relative_path("learning-path/0-tableofcontents.md", file_path)
        top_nav += f"[📚 Back to Table of Contents]({toc_path})\n"
    
    # Replace content - add navigation after title
    if title_match:
        new_content = re.sub(r'^# .*', f"# {title}\n\n{top_nav}", content, count=1)
    else:
        # If no title found, add one with navigation
        new_content = f"# {title}\n\n{top_nav}\n\n{content}"
        
    content = new_content
    
    # Add previous/next navigation at the bottom for non-README files
    if file_path.name != "README.md":
        folder = file_path.parent
        files = sorted([f for f in folder.glob("*.md") if f.name != "README.md"])
        
        prev_file = None
        next_file = None
        
        for i, f in enumerate(files):
            if f.name == file_path.name:
                if i > 0:
                    prev_file = files[i-1]
                if i < len(files) - 1:
                    next_file = files[i+1]
                break
        
        nav_bottom = ""
        if prev_file:
            prev_title = prev_file.stem.replace('-', ' ').title()
            nav_bottom += f"[⬅ Previous: {prev_title}]({prev_file.name}) | "
        if next_file:
            next_title = next_file.stem.replace('-', ' ').title()
            nav_bottom += f"[Next: {next_title} ➡]({next_file.name})"
        
        # Only add bottom navigation if there's something to add
        if nav_bottom:
            content += f"\n\n---\n\n{nav_bottom}"
    
    # Process templates with error handling
    try:
        # Process templates
        template = Template(content)
        final_content = template.render(**config)
    except Exception as e:
        print(f"⚠️ Template error in {file_path}: {str(e)}")
        print("   Using content without template processing")
        final_content = content
    
    # Write back to file
    file_path.write_text(final_content)
    print(f"✅ Updated navigation in: {file_path}")

# Ensure README exists in workflow folders
def ensure_readme(folder, config):
    folder = Path(folder)
    readme_path = folder / "README.md"
    
    if not readme_path.exists():
        title = folder.name
        content = f"""# {title}

This folder contains workflow-specific documentation for {{{{ organization_name }}}} in {{{{ state_name }}}}.

## Overview
This workflow includes processes for managing {title} records according to retention schedules.

---
[⬅ Back to Workflows](../users.md)
"""
        
        # Process template
        template = Template(content)
        final_content = template.render(**config)
        
        # Write to file
        readme_path.write_text(final_content)
        print(f"✅ Created: {readme_path}")

def process_setup_guide():
    """Special processing for the setup guide to sort by step number"""
    setup_guide = Path("docs/it-admins/setup/0-setup-guide.md")
    if not setup_guide.exists():
        return
        
    content = setup_guide.read_text()
    
    # Extract the table rows
    table_pattern = r"\| (.+?) \| (.+?) \| \[Link\]\((.+?)\) \|"
    matches = re.findall(table_pattern, content)
    
    # Sort by the filename number prefix
    def get_sort_key(match):
        filename = match[2]
        match_num = re.search(r'(\d+)', filename)
        return int(match_num.group(1)) if match_num else 999
        
    sorted_rows = sorted(matches, key=get_sort_key)
    
    # Rebuild the table
    new_table = "| Step | Topic | Description | Link |\n|------|-------|-------------|------|\n"
    for i, (topic, description, link) in enumerate(sorted_rows):
        # Fix link path - remove 'setup/' prefix if it exists
        fixed_link = re.sub(r'^setup/', '', link)
        new_table += f"| {i+1} | {topic} | {description} | [Link]({fixed_link}) |\n"
    
    # Replace the old table with the new one
    new_content = re.sub(r"\| Topic \| Description \| Link \|.*?\n\|.+?\|.+?\|.+?\|", new_table, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    setup_guide.write_text(new_content)
    print(f"✅ Updated setup guide with sorted table.")

def ensure_navigation_tables():
    """Create navigation tables for all major directories"""
    
    # Define fixed navigation tables with specific structures
    fixed_nav_tables = {
    "docs": {
        "title": "Records Management Documentation",
        "desc": "Welcome to the Records Management Documentation for your organization.",
        "columns": ["Section", "Description", "Link"],
        "data": [
            ["IT Administration", "Setup and administration guides", "it-admins/"],
            ["User Workflows", "End-user documentation for records workflows", "users/users.md"],
            ["Learning Path", "Step-by-step tutorial for new users", "learning-path/0-tableofcontents.md"]
        ]
    },
    "docs/it-admins": {
        "title": "IT Administrator Documentation",
        "desc": "Resources for IT Administrators implementing and maintaining Records Management solutions.",
        "columns": ["Section", "Description", "Link"],
        "data": [
            ["Setup Guides", "Step-by-step setup instructions", "setup/0-setup-guide.md"],
            ["Core Concepts", "Fundamental concepts for administrators", "core-concepts/"],
            ["Contracts", "Contract workflow configuration", "contracts/setup/"],
            ["Purview", "Microsoft Purview configuration", "purview/setup/"],
            ["Purchase Cards", "Purchase cards system setup", "purchase-cards/setup/"]
        ]
    },
    "docs/learning-path": {
        "title": "Learning Path",
        "desc": "Start here if you're new to SharePoint Records Management.",
        "columns": ["Step", "Topic", "Description", "Link"],
        "data": [
            ["1", "Introduction", "Overview of the system", "1-introduction.md"],
            ["2", "Core Concepts", "Key concepts to understand", "2-core-concepts.md"],
            ["3", "Basic Usage", "Getting started with the system", "3-basic-usage.md"]
                ]
            }
        }
        
    # Process predefined navigation tables
    for dir_path, table_info in fixed_nav_tables.items():
        create_navigation_table(dir_path, table_info)
    
    # Find all root directories in docs folder to generate dynamic navigation tables
    docs_dir = Path("docs")
    root_dirs = [d for d in docs_dir.iterdir() 
                if d.is_dir() 
                and d.name not in ["__pycache__"]
                and not d.name.startswith('.')]
    
    # Process each root directory
    for root_dir in root_dirs:
        # Skip directories with manually defined tables
        if str(root_dir) in fixed_nav_tables:
            continue
        
        # Create README if it doesn't exist
        index_file = root_dir / "README.md"
        if index_file.exists():
            continue
            
        # Get subdirectories and files to include in navigation
        subdirs = [d for d in root_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        md_files = [f for f in root_dir.glob("*.md") if f.name != "README.md"]
        
        # Create navigation table data
        data = []
        
        # Add directories first
        for i, subdir in enumerate(sorted(subdirs)):
            name = subdir.name.replace('-', ' ').title()
            data.append([str(i+1), name, f"Documentation for {name}", f"{subdir.name}/"])
        
        # Then add files
        for i, md_file in enumerate(sorted(md_files)):
            name = md_file.stem.replace('-', ' ').title()
            # Try to extract a better description from the file
            try:
                content = md_file.read_text()
                desc_pattern = r'^<!--\s*description:\s*(.+?)\s*-->'
                desc_match = re.search(desc_pattern, content, re.MULTILINE)
                
                if desc_match:
                    desc = desc_match.group(1)
                else:
                    # Fall back to first paragraph if no description comment
                    first_paragraph = re.search(r'# .+?\n\n(.+?)(?=\n\n|\Z)', content)
                    desc = first_paragraph.group(1) if first_paragraph else f"Documentation about {name}"
            except:
                desc = f"Documentation about {name}"
            
            data.append([str(len(subdirs) + i + 1), name, desc, md_file.name])
        
        # Create the navigation table info
        table_info = {
            "title": root_dir.name.replace('-', ' ').title(),
            "desc": f"Documentation resources for {root_dir.name.replace('-', ' ')}.",
            "columns": ["Step", "Topic", "Description", "Link"],
            "data": data
        }
        
        # Create the navigation table
        create_navigation_table(str(root_dir), table_info)
    

def create_navigation_table(dir_path, table_info):
    """Create or update a navigation table README in the specified directory"""
    index_file = Path(f"{dir_path}/README.md")
    
    # Create directory if it doesn't exist
    index_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate table header
    headers = " | ".join([f"**{col}**" for col in table_info["columns"]])
    separator = "|".join(["---"] * len(table_info["columns"]))
    
    # Generate table rows
    rows = []
    for row_data in table_info["data"]:
        # Format the link column specially
        link_column = f"[Link]({row_data[-1]})"
        formatted_row = " | ".join(row_data[:-1] + [link_column])
        rows.append(f"| {formatted_row} |")
    
    # Assemble the content
    content = f"# {table_info['title']}\n\n{table_info['desc']}\n\n"
    content += f"| {headers} |\n|{separator}|\n"
    content += "\n".join(rows)
    
    # Check if README exists
    if index_file.exists():
        # Preserve any content after the table
        existing_content = index_file.read_text()
        # Find any content after the navigation table
        after_table_match = re.search(r'\n\n---\n\n(.*)', existing_content, re.DOTALL)
        if after_table_match:
            content += f"\n\n---\n\n{after_table_match.group(1)}"
        print(f"📊 Updated navigation table: {index_file}")
    else:
        print(f"✅ Created navigation table: {index_file}")
    
    # Write to file
    index_file.write_text(content)

def verify_workflow_table():
    """Verify and fix the workflow table in users.md"""
    workflows_file = Path("docs/users/users.md")
    if not workflows_file.exists():
        return
        
    content = workflows_file.read_text()
    
    # Get list of actual workflow directories
    workflow_dirs = [d for d in Path("docs/users").iterdir() 
                    if d.is_dir() and d.name != "__pycache__" and not d.name.startswith('.')]
    
    # Extract existing table rows to preserve descriptions
    table_pattern = r"\| \[([^]]+)\]\(([^)]+)\) \| ([^|]+) \|"
    existing_rows = {name: (path, desc) for name, path, desc in re.findall(table_pattern, content)}
    
    # Build new table rows ensuring all directories are included
    rows = []
    for d in sorted(workflow_dirs):
        name = d.name.replace('-', ' ').title()
        
        # Use existing description if available or create a default one
        if name in existing_rows:
            path, desc = existing_rows[name]
            # Update path if needed
            if path != f"{d.name}/":
                path = f"{d.name}/"
        else:
            path = f"{d.name}/"
            desc = f" Manage {name.lower()} in SharePoint. "
        
        task_path = f"{d.name}/task-guides/"
        training_path = f"{d.name}/training/"
        supervisor_path = f"{d.name}/supervisors/"
        
        row = f"| [{name}]({path}) | {desc} | [Task Guides]({task_path}) | [Training]({training_path}) | [Supervisor Guide]({supervisor_path}) |"
        rows.append(row)
    
    # Create the new table
    table_header = "| **Workflow** | **Description** | **Task Guides** | **Training** | **Supervisor Guides** |\n|-------------|----------------|-----------------|--------------|----------------------|"
    new_table = table_header + "\n" + "\n".join(rows)
    
    # Replace the old table with the new one
    table_pattern = r"\| \*\*Workflow\*\* \|.*?\n\|.*?\n(.*?)(?=\n\n|\n#|\Z)"
    new_content = re.sub(table_pattern, new_table, content, flags=re.DOTALL)
    
    # Write back if changed
    if new_content != content:
        workflows_file.write_text(new_content)
        print(f"✅ Updated workflow table in: {workflows_file}")

def ensure_file_descriptions(file_path, config):
    """Ensure every markdown file has a proper description for navigation tables"""
    file_path = Path(file_path)
    
    # Skip README files as they're typically navigation tables
    if file_path.name == "README.md":
        return
        
    content = file_path.read_text()
    
    # Check if the file already has a description
    desc_pattern = r'^<!--\s*description:\s*(.+?)\s*-->'
    desc_match = re.search(desc_pattern, content, re.MULTILINE)
    
    if not desc_match:
        # No description found, add one
        title_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()
        
        # Create a default description based on the title
        default_desc = f"Documentation about {title} for {{{{ organization_name }}}}."
        
        # Add the description comment at the top of the file
        new_content = f"<!-- description: {default_desc} -->\n{content}"
        
        # Process template in the description
        template = Template(default_desc)
        rendered_desc = template.render(**config)
        
        # Write back to file
        file_path.write_text(new_content)
        print(f"✅ Added description to: {file_path}")
        return rendered_desc
    else:
        # Description exists, render it with template variables
        desc = desc_match.group(1)
        template = Template(desc)
        rendered_desc = template.render(**config)
        return rendered_desc

def check_unresolved_templates():
    """Check for any unresolved template variables in rendered files"""
    docs_dir = Path("docs")
    unresolved = []
    
    for file_path in docs_dir.glob("**/*.md"):
        content = file_path.read_text()
        if re.search(r'\{\{\s*\w+\s*\}\}', content):
            unresolved.append(str(file_path))
    
    if unresolved:
        print("\n⚠️ Unresolved template variables found in:")
        for file in unresolved:
            print(f"  - {file}")
        print("Please check your config.yaml file.")

def cleanup_file_for_processing(file_path):
    """Clean up a file before processing to remove duplicate navigation"""
    file_path = Path(file_path)
    content = file_path.read_text()
    
    # Remove duplicate bottom navigation
    cleaned = re.sub(r'(\n\n---\n\n\[⬅ Previous:.*?\].*?\n)\n\n---\n\n\[⬅ Previous:.*?\].*?\n', r'\1', content)
    
    # Remove duplicate top navigation
    cleaned = re.sub(r'(### Site Navigation\n.*?\n\n)### Site Navigation\n.*?\n', r'\1', cleaned)
    
    # Write back if changed
    if cleaned != content:
        file_path.write_text(cleaned)
        print(f"🧹 Cleaned up duplicate navigation in: {file_path}")
    
    return cleaned

# Fixed main function
def main():
    parser = argparse.ArgumentParser(description="Documentation processor for municipality records management")
    parser.add_argument("--html", action="store_true", help="Generate HTML files for SharePoint")
    parser.add_argument("--config", action="store_true", help="Create or update configuration")
    parser.add_argument("--branch", help="Create a new organization branch")
    args = parser.parse_args()
    
    # Ensure we're in the project root
    if not os.path.isdir("docs") or not os.path.isfile("README.md"):
        print("❌ Error: This script must be run from the project root directory.")
        return 1
    
    # Handle config
    if args.config:
        ensure_config()
        return 0
    
    # Load configuration
    config = load_config()
    
    # Process all markdown files
    docs_dir = Path("docs")
    print("🔍 Starting documentation navigation update...")
    
    for file_path in docs_dir.glob("**/*.md"):
        # First clean up any duplicate navigation
        cleanup_file_for_processing(file_path)
        # Then ensure descriptions are in place
        ensure_file_descriptions(file_path, config)
        # Finally generate navigation
        generate_navigation(file_path, config)
    
    # Ensure READMEs exist in workflow folders
    users_dir = Path("docs/users")
    if users_dir.exists():  # Added check
        for folder in [d for d in users_dir.iterdir() if d.is_dir()]:
            ensure_readme(folder, config)
    
    # Process special tables
    process_setup_guide()
    verify_workflow_table()
    ensure_navigation_tables()
    check_unresolved_templates()
    
    # Generate HTML if requested
    if args.html:
        try:
            import markdown
            print("\n📄 Generating HTML files for SharePoint...")
            
            for md_file in docs_dir.glob("**/*.md"):
                html_file = md_file.with_suffix(".html")
                with open(md_file) as f:
                    md_content = f.read()
                
                html_content = markdown.markdown(
                    md_content,
                    extensions=['tables', 'fenced_code', 'codehilite']
                )
                
                # Add basic styling
                styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{md_file.stem}</title>
    <style>
        body {{ font-family: Segoe UI, Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }}
        code {{ background-color: #f5f5f5; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f0f0f0; }}
        a {{ color: #0078d4; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
                
                with open(html_file, 'w') as f:
                    f.write(styled_html)
                
                print(f"✅ Generated HTML: {html_file}")
        except ImportError:
            print("⚠️ Python markdown module not found. Run 'pip install markdown' to generate HTML.")
    
    if args.branch:
        import subprocess
        branch_name = f"organization/{args.branch}"
        subprocess.run(["git", "checkout", "-b", branch_name])
        print(f"✅ Created organization branch: {branch_name}")
    
    print("\n🎯 All documentation files now have auto-generated navigation, and workflows have README.md files.")
    print("💡 Tip: Run with --html to generate SharePoint-ready HTML files.")
    
    return 0

if __name__ == "__main__":
    exit(main())