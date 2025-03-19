#!/usr/bin/env python3
# filepath: workflows/document_processing/readme_processor.py
import re
from pathlib import Path
from jinja2 import Template

from workflows.document_processing.config_manager import load_config
from workflows.document_processing.utils import extract_description
from workflows.document_processing.navigation_builder import generate_breadcrumb_navigation

def ensure_readme(folder, config):
    """Create README.md file if it doesn't exist in the given folder"""
    folder = Path(folder)
    readme_path = folder / "README.md"
    
    if (not readme_path.exists()):
        title = folder.name
        content = f"""<!-- description: Documentation for {title} workflow -->

# {title}

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

def ensure_file_descriptions(file_path, config):
    """Ensure every markdown file has a proper description for navigation tables"""
    file_path = Path(file_path)
    
    # Skip README files as they're typically navigation tables
    if (file_path.name == "README.md"):
        return
        
    content = file_path.read_text()
    
    # Check if the file already has a description
    desc_pattern = r'^<!--\s*description:\s*(.+?)\s*-->'
    desc_match = re.search(desc_pattern, content, re.MULTILINE)
    
    if (not desc_match):
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

def ensure_readme_has_description(readme_path):
    """Ensure README file has a description section"""
    content = readme_path.read_text()
    
    # Check if file already has description comment
    desc_pattern = r'<!--\s*description:\s*(.+?)\s*-->'
    if not re.search(desc_pattern, content, re.MULTILINE):
        # No description found, create one
        title = readme_path.parent.name.replace('-', ' ').title()
        desc = f"Documentation about {title}"
        
        # Add description comment to top of file
        new_content = f"<!-- description: {desc} -->\n{content}"
        readme_path.write_text(new_content)
        print(f"✅ Added description to README: {readme_path}")
    
    return True

def ensure_readme_has_table(readme_path):
    """Ensure an existing README file has a proper navigation table"""
    content = readme_path.read_text()
    
    # Check if the README already has a table
    if not re.search(r'\|\s*\*\*#\*\*\s*\|\s*\*\*Topic\*\*', content):
        # No table found, add one
        dir_path = readme_path.parent
        title = dir_path.name.replace('-', ' ').title()
        
        # Get description from file
        desc_pattern = r'<!--\s*description:\s*(.+?)\s*-->'
        desc_match = re.search(desc_pattern, content, re.MULTILINE)
        description = desc_match.group(1) if desc_match else f"Documentation about {title}"
        
        # Build table info
        table_info = {
            "title": title,
            "desc": description,
            "columns": ["#", "Topic", "Description", "Link"],
            "data": []
        }
        
        # Scan directory for markdown files and subfolders
        md_files = sorted([f for f in dir_path.glob("*.md") if f.name.lower() != "readme.md"])
        subdirs = sorted([d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
        
        # Add directories first
        for i, subdir in enumerate(subdirs):
            name = subdir.name.replace('-', ' ').title()
            sub_readme = next((f for f in subdir.glob("*") if f.name.lower() == "readme.md"), None)
            
            # Get description from README if it exists
            if sub_readme:
                desc = extract_description(sub_readme)
            else:
                desc = f"Documentation for {name}"
                
            table_info["data"].append([i + 1, name, desc, f"{subdir.name}/"])
        
        # Then add files
        for i, md_file in enumerate(md_files):
            name = md_file.stem.replace('-', ' ').title()
            desc = extract_description(md_file)
            table_info["data"].append([len(subdirs) + i + 1, name, desc, md_file.name])
        
        # Create the table content
        table_header = "| **#** | **Topic** | **Description** | **Link** |\n|---|---|---|---|"
        table_rows = []
        
        for row in table_info["data"]:
            # Format link column differently based on data structure
            if len(row) >= 4:  # If row has at least 4 elements
                num = row[0]
                name = row[1]
                desc = row[2]
                link = row[3]
                table_rows.append(f"| {num} | {name} | {desc} | [{name}]({link}) |")
        
        table_content = table_header + "\n" + "\n".join(table_rows)
        
        # Add table to README if description section exists
        if "## Description" in content:
            # Add after description section
            new_content = re.sub(r'(## Description.*?)(\n##|\Z)', f'\\1\n\n## Contents\n\n{table_content}\\2', content, flags=re.DOTALL)
        else:
            # Add at the end
            new_content = content + f"\n\n## Contents\n\n{table_content}"
        
        # Write updated content
        readme_path.write_text(new_content)
        print(f"✅ Added navigation table to: {readme_path}")

def create_navigation_table(dir_path, table_info):
    """Create or update a navigation table README in the specified directory"""
    index_file = Path(f"{dir_path}/README.md")
    
    # Check if file exists - if so, read it to preserve any custom content
    if index_file.exists():
        existing_content = index_file.read_text()
        
        # Extract everything before any existing tables or content sections
        # This preserves title, description, and navigation
        content_before_tables = re.split(r'## (Contents|Folders|Documents)', existing_content)[0]
        
        # Clean up any trailing separators or extra whitespace
        content_before_tables = re.sub(r'---+\s*$', '', content_before_tables).rstrip() + "\n\n"
        
        # Start with this existing content
        content = content_before_tables
    else:
        # Create directory if it doesn't exist
        index_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Get folder name for title
        title = Path(dir_path).name.replace('-', ' ').title()
        if dir_path == "docs":
            title = "Records Management Documentation"
        
        # Create standard description if not provided
        description = table_info.get('desc', f"Documentation about {title}")
        
        # Create new content with consistent structure
        content = f"<!-- description: {description} -->\n\n# {title}\n\n"
        
        # Generate navigation
        config = load_config()
        
        # For non-root directories, add breadcrumb navigation
        if dir_path != "docs":
            # Create top navigation with breadcrumbs
            top_nav = f"### Site Navigation\n" + generate_breadcrumb_navigation(index_file)
            content += f"{top_nav}\n\n"
        
        # Add description section
        content += f"## Description\n{description}\n\n"
    
    # Scan directory for subfolders and markdown files
    md_files = sorted([f for f in Path(dir_path).glob("*.md") if f.name.lower() != "readme.md"])
    subdirs = sorted([d for d in Path(dir_path).iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    # Only add a Folders section if there are subdirectories
    if subdirs:
        content += "## Folders\n\n"
        
        # Build table for subdirectories
        folder_table = "| **Folder** | **Description** |\n|-----------|---------------|\n"
        
        for subdir in subdirs:
            name = subdir.name.replace('-', ' ').title()
            sub_readme = next((f for f in subdir.glob("*") if f.name.lower() == "readme.md"), None)
            
            # Get description from README if it exists
            if sub_readme:
                # Extract only the description comment, not content
                sub_content = sub_readme.read_text()
                desc_pattern = r'<!--\s*description:\s*(.+?)\s*-->'
                desc_match = re.search(desc_pattern, sub_content, re.MULTILINE)
                
                if desc_match:
                    desc = desc_match.group(1)
                else:
                    desc = f"Documentation for {name}"
            else:
                desc = f"Documentation for {name}"
            
            # Add row to table with folder name linked
            folder_table += f"| [{name}]({subdir.name}/) | {desc} |\n"
        
        content += folder_table + "\n"
    
    # Only add a Documents section if there are markdown files
    if md_files:
        content += "## Documents\n\n"
        
        # Build table for documents
        doc_table = "| **Document** | **Description** |\n|-------------|---------------|\n"
        
        for md_file in md_files:
            name = md_file.stem.replace('-', ' ').title()
            desc = extract_description(md_file)
            
            # Add row to table with document name linked
            doc_table += f"| [{name}]({md_file.name}) | {desc} |\n"
        
        content += doc_table
    
    # Write to file
    index_file.write_text(content)
    print(f"✅ Updated navigation in: {index_file}")

def ensure_navigation_tables():
    """Create navigation tables for all major directories"""
    
    # Define fixed navigation tables with specific structures
    fixed_nav_tables = {
        "docs": {
            "title": "Records Management Documentation",
            "desc": "Welcome to the Records Management Documentation. Select a section below to get started.",
            "columns": ["#", "Topic", "Description", "Link"],
            "data": [
                [1, "Users", "End-user documentation and workflows", "users/"],
                [2, "IT Administrators", "Setup and configuration guides", "it-admins/"],
                [3, "Learning Path", "Step-by-step training guide for new users", "learning-path/"]
            ]
        },
        "docs/users": {
            "title": "User Documentation",
            "desc": "End-user documentation for records management workflows.",
            "columns": ["#", "Topic", "Description", "Link"],
            "data": []  # Will be populated dynamically
        },
        "docs/it-admins": {
            "title": "IT Administration",
            "desc": "Technical documentation for IT administrators.",
            "columns": ["#", "Topic", "Description", "Link"],
            "data": []  # Will be populated dynamically
        },
        "docs/learning-path": {
            "title": "Learning Path",
            "desc": "Step-by-step training guide for new users.",
            "columns": ["#", "Topic", "Description", "Link"],
            "data": []  # Will be populated dynamically
        }
    }
    
    # Process each fixed table
    for dir_path, table_info in fixed_nav_tables.items():
        # Create or update the navigation table
        create_navigation_table(dir_path, table_info)

def ensure_all_readmes():
    """Ensure all folders within docs have proper README.md files with navigation tables"""
    docs_dir = Path("docs")
    
    # Find all directories recursively
    for dir_path in [p for p in docs_dir.glob("**/*") if p.is_dir()]:
        # Skip hidden directories
        if any(part.startswith('.') for part in dir_path.parts):
            continue
            
        # Check for README.md (case insensitive)
        readme_exists = False
        readme_path = None
        for file in dir_path.glob("*"):
            if file.name.lower() == "readme.md":
                readme_exists = True
                readme_path = file
                break
        
        if not readme_exists:
            # Create standard README with empty table
            table_info = {
                "title": dir_path.name.replace('-', ' ').title(),
                "desc": f"Documentation about {dir_path.name.replace('-', ' ')}",
                "columns": ["#", "Topic", "Description", "Link"],
                "data": []
            }
            create_navigation_table(str(dir_path), table_info)
        else:
            # Update existing README with navigation table
            ensure_readme_has_table(readme_path)