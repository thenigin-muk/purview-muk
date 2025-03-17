#!/usr/bin/env python3

import os
import re
from pathlib import Path

def get_relative_path(target, source_file):
    """Calculate relative path from source_file to target"""
    source_dir = os.path.dirname(str(source_file))
    target_path = str(target)
    if not target_path.startswith("docs/"):
        target_path = f"docs/{target_path}"
    rel_path = os.path.relpath(target_path, source_dir)
    return rel_path.replace("\\", "/")  # Normalize for markdown

def extract_description(file_path):
    """Extract description from markdown file"""
    try:
        content = file_path.read_text()
        desc_pattern = r'<!--\s*description:\s*(.+?)\s*-->'
        desc_match = re.search(desc_pattern, content, re.MULTILINE)
        
        if desc_match:
            return desc_match.group(1)
        else:
            # Fallback to first paragraph
            first_para = re.search(r'# .+?\n\n(.+?)(?=\n\n|\Z)', content, re.DOTALL)
            if first_para:
                return first_para.group(1).replace('\n', ' ')[:100] + "..."
            else:
                return f"Documentation about {file_path.stem.replace('-', ' ').title()}"
    except Exception:
        return f"Documentation about {file_path.stem.replace('-', ' ').title()}"

def fix_tables_in_readme(readme_path):
    """Fix navigation sections that got into tables"""
    if not readme_path.exists():
        return False
        
    content = readme_path.read_text()
    changed = False
    
    # Fix table rows that contain navigation sections
    nav_in_table = re.search(r'\| \d+ \| .* \| ### Site Navigation.*?\| \[.*?\]\(.*?\) \|', content)
    if nav_in_table:
        # Extract all rows
        rows = re.findall(r'\| \d+ \| (.*?) \| (.*?) \| \[(.*?)\]\((.*?)\) \|', content)
        if rows:
            # Rebuild the table with clean data
            table = "| **#** | **Topic** | **Description** | **Link** |\n|---|---|---|---|\n"
            for i, row in enumerate(rows):
                topic, desc, link_text, link = row
                # Clean up description and remove any navigation text
                clean_desc = re.sub(r'### Site Navigation.*?((?=\|)|$)', '', desc).strip()
                if not clean_desc:
                    clean_desc = f"Documentation for {topic}"
                table += f"| {i+1} | {topic} | {clean_desc} | [{topic}]({link}) |\n"
            
            # Replace the old table with the clean one
            content = re.sub(r'\| \*\*#\*\* \|.*?\|\n\|[-\|]+\n(.*?)(?=\n\n|\n##|\Z)', table, content, flags=re.DOTALL)
            readme_path.write_text(content)
            changed = True
            print(f"🧹 Fixed table with embedded navigation in {readme_path}")
    
    return changed

def fix_navigation(file_path):
    """Fix navigation in a single file"""
    # Skip if doesn't exist or isn't a markdown file
    if not file_path.exists() or file_path.suffix != '.md':
        return False
    
    # Fix tables if this is a README file
    if file_path.name == "README.md":
        fix_tables_in_readme(file_path)
    
    content = file_path.read_text()
    original_content = content
    
    # Get title from first heading or filename
    title_match = re.search(r'^# (.*)', content, re.MULTILINE)
    if not title_match:
        title = file_path.stem.replace('-', ' ').title()
        content = f"# {title}\n\n{content}"
    else:
        title = title_match.group(1).strip()
    
    # Calculate relative paths
    home_path = get_relative_path("docs/README.md", file_path)
    workflows_path = get_relative_path("docs/users/users.md", file_path)
    admin_path = get_relative_path("docs/it-admins/README.md", file_path)
    
    # Create top navigation
    top_nav = f"### Site Navigation\n"
    top_nav += f"[🏠 Home]({home_path}) | [📂 All Workflows]({workflows_path}) | [⚙ IT Admin Docs]({admin_path})"
    
    # If inside workflow, add back link
    folder_path = file_path.parent
    workflow_match = re.search(r'users/([^/]+)', str(folder_path))
    if workflow_match and workflow_match.group(1) != "users":
        workflow_name = workflow_match.group(1)
        back_path = "../README.md"
        # Adjust path based on depth
        if "supervisors" in str(folder_path) or "task-guides" in str(folder_path) or "training" in str(folder_path):
            back_path = "../README.md"
        top_nav += f" | [⬅ Back to {workflow_name}]({back_path})"

    # If in learning path, add link back to table of contents
    if "learning-path" in str(file_path) and file_path.name != "0-tableofcontents.md" and file_path.name != "README.md":
        toc_path = get_relative_path("docs/learning-path/0-tableofcontents.md", file_path)
        top_nav += f" | [📚 Table of Contents]({toc_path})"
    
    # Split content into parts: title, potential existing navigation, and body
    parts = content.split("\n", 1)
    title_line = parts[0]
    body = parts[1].lstrip() if len(parts) > 1 else ""
    
    # Remove any existing Site Navigation section completely
    body = re.sub(r'### Site Navigation\n.*?(\n\n|\n#|\Z)', '\n\n', body, flags=re.DOTALL)
    body = body.lstrip('\n')
    
    # Rebuild content with correct navigation
    new_content = f"{title_line}\n\n{top_nav}\n\n{body}"
    
    # Fix bottom navigation for non-README files
    if file_path.name != "README.md":
        # Remove any existing bottom navigation
        new_content = re.sub(r'\n\n---\n\n\[.*?\].*?(\n|$)', '\n', new_content)
        
        # Check if file is in a sequence
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
        
        nav_bottom = []
        if prev_file:
            prev_title = prev_file.stem.replace('-', ' ').title()
            nav_bottom.append(f"[⬅ Previous: {prev_title}]({prev_file.name})")
        if next_file:
            next_title = next_file.stem.replace('-', ' ').title()
            nav_bottom.append(f"[Next: {next_title} ➡]({next_file.name})")
        
        # Only add bottom navigation if there's something to add
        if nav_bottom:
            new_content += f"\n\n---\n\n{' | '.join(nav_bottom)}"
    
    # Fix typos
    new_content = new_content.replace("## Descriotion", "## Description")
    
    # Clean up multiple blank lines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    # Write back if changed
    if new_content != original_content:
        file_path.write_text(new_content)
        print(f"✅ Fixed navigation in: {file_path}")
        return True
    
    return False

def update_navigation_tables(readme_path):
    """Update navigation tables in README files"""
    if not readme_path.exists() or readme_path.suffix != '.md':
        return False
    
    dir_path = readme_path.parent
    content = readme_path.read_text()
    original_content = content
    
    # Scan directory for markdown files and subfolders
    md_files = sorted([f for f in dir_path.glob("*.md") if f.name != "README.md"])
    subdirs = sorted([d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    # Only proceed if we have files or subdirs to list
    if md_files or subdirs:
        # Ensure title and navigation
        title_match = re.search(r'^# (.*)', content, re.MULTILINE)
        if not title_match:
            dir_name = dir_path.name.replace('-', ' ').title()
            content = f"# {dir_name}\n\n{content}"
        
        # Generate table content
        table_rows = []
        
        # Add directories first
        for i, subdir in enumerate(subdirs):
            name = subdir.name.replace('-', ' ').title()
            readme = subdir / "README.md"
            
            # Get description from README if it exists
            if readme.exists():
                desc = extract_description(readme)
            else:
                desc = f"Documentation for {name}"
                
            table_rows.append(f"| {i + 1} | {name} | {desc} | [{name}]({subdir.name}/) |")
        
        # Then add files
        for i, md_file in enumerate(md_files):
            name = md_file.stem.replace('-', ' ').title()
            desc = extract_description(md_file)
            table_rows.append(f"| {len(subdirs) + i + 1} | {name} | {desc} | [{name}]({md_file.name}) |")
        
        # Create the table
        table_header = "| **#** | **Topic** | **Description** | **Link** |\n|---|---|---|---|"
        table = table_header + "\n" + "\n".join(table_rows)
        
        # Check if table already exists
        if "| **#** |" in content or "| **Topic** |" in content:
            # Replace existing table
            content = re.sub(r'\|.*\*\*.*\*\*.*\|\n\|[-\|]+\n(.*?)(?=\n\n|\n##|\Z)', table, content, flags=re.DOTALL)
        else:
            # Add section header for the table if not present
            if "## Contents" not in content:
                content += "\n\n## Contents\n\n"
            # Add table
            content += f"{table}\n"
            
        # Clean up multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
            
        # Write back if changed
        if content != original_content:
            readme_path.write_text(content)
            print(f"📊 Updated navigation table in: {readme_path}")
            return True
    
    return False

def fix_all_navigation():
    """Fix navigation in all files"""
    docs_dir = Path("docs")
    files_fixed = 0
    tables_updated = 0
    
    # Special case for root README
    root_readme = docs_dir / "README.md"
    if root_readme.exists():
        content = root_readme.read_text()
        
        # Ensure title
        if "# Records Management Documentation" not in content:
            content = re.sub(r'^# .*\n', "# Records Management Documentation\n", content, count=1)
        
        # Fix root navigation
        nav = "### Site Navigation\n"
        nav += "[🏠 Home](./README.md) | [📂 All Workflows](./users/users.md) | [⚙ IT Admin Docs](./it-admins/README.md)"
        
        # Add navigation after title if needed
        if "### Site Navigation" not in content:
            content = re.sub(r'^# .*\n', f"# Records Management Documentation\n\n{nav}\n", content, count=1)
        else:
            # Replace existing navigation
            content = re.sub(r'### Site Navigation\n.*?(\n\n|\n#)', f"{nav}\n\n", content, flags=re.DOTALL)
        
        # Fix navigation table format
        table_section = """
## Contents

| **#** | **Topic** | **Description** | **Link** |
|---|---|---|---|
| 1 | Users | End-user documentation and workflows | [Users](users/) |
| 2 | IT Administrators | Setup and configuration guides | [IT Administrators](it-admins/) |
| 3 | Learning Path | Step-by-step training guide for new users | [Learning Path](learning-path/) |
"""
        
        # Check for existing table
        if "## Contents" in content:
            # Replace table section
            content = re.sub(r'## Contents\n\n.*?(?=\n\n|\Z)', table_section.strip(), content, flags=re.DOTALL)
        else:
            # Add table section
            content += table_section
        
        # Clean up multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Write back
        root_readme.write_text(content)
        print(f"✅ Fixed root README: {root_readme}")
        files_fixed += 1
    
    # First pass: fix navigation in all files
    for file_path in docs_dir.glob("**/*.md"):
        if fix_navigation(file_path):
            files_fixed += 1
    
    # Second pass: update navigation tables in README files
    for readme_path in docs_dir.glob("**/README.md"):
        if update_navigation_tables(readme_path):
            tables_updated += 1
    
    print(f"\n🎉 Fixed navigation in {files_fixed} files.")
    print(f"📊 Updated tables in {tables_updated} README files.")

if __name__ == "__main__":
    fix_all_navigation()