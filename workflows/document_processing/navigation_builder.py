#!/usr/bin/env python3
# filepath: workflows/document_processing/navigation_builder.py
import re
from pathlib import Path
from jinja2 import Template

from workflows.common import log_utils
from workflows.document_processing.utils import get_relative_path
from workflows.common.log_utils import Messages

def generate_navigation(file_path, config):
    """Generate navigation for a markdown file"""
    file_path = Path(file_path)
    
    # Read content
    try:
        content = file_path.read_text()
    except Exception as e:
        log_utils.error("Failed to read file {}: {}", file_path, str(e))
        return False
    original_content = content
    
    # Skip navigation generation if skip marker exists
    if '<!-- skip-navigation -->' in content:
        print(f"ℹ️ Skipping navigation generation for: {file_path}")
        return
    
    # Get title from first heading or filename
    title_match = re.search(r'^# (.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()
    
    # Create top navigation with breadcrumbs
    top_nav = f"### Site Navigation\n"
    top_nav += generate_breadcrumb_navigation(file_path)
    
    # Add common links
    #workflows_path = get_relative_path("users/users.md", file_path)
    #admin_path = get_relative_path("it-admins/README.md", file_path)
    #top_nav += f" | [📂 All Workflows]({workflows_path}) | [⚙ IT Admin Docs]({admin_path})"
    
    # Add back link to parent folder for non-README files
    if file_path.name.lower() != "readme.md":
        back_path = "README.md"
        parent_folder = file_path.parent.name.replace('-', ' ').title()
        top_nav += f" | [⬅ Back to {parent_folder}]({back_path})"
    
    # Completely remove any existing site navigation section
    content = re.sub(r'### Site Navigation\n.*?\n\n', '', content, flags=re.DOTALL)
    
    # Insert navigation after title
    if title_match:
        # Get the position of the title match
        title_pos = content.find(f"# {title}")
        title_end = title_pos + len(f"# {title}\n")
        
        # Insert navigation after title
        content = content[:title_end] + f"\n{top_nav}\n\n" + content[title_end:]
    else:
        # If no title found, add one with navigation
        content = f"# {title}\n\n{top_nav}\n\n" + content
    
    # Clean up any bottom navigation
    content = re.sub(r'\n\n---\n\n\[.*?\].*?(\n|$)', '\n', content)
    
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
        
        nav_bottom = []
        if prev_file:
            prev_title = prev_file.stem.replace('-', ' ').title()
            nav_bottom.append(f"[⬅ Previous: {prev_title}]({prev_file.name})")
        if next_file:
            next_title = next_file.stem.replace('-', ' ').title()
            nav_bottom.append(f"[Next: {next_title} ➡]({next_file.name})")
        
        # Only add bottom navigation if there's something to add
        if nav_bottom:
            content += f"\n\n---\n\n{' | '.join(nav_bottom)}"
    
    # Process templates with error handling
    try:
        template = Template(content)
        final_content = template.render(**config)
    except Exception as e:
        log_utils.warning(Messages.Doc.TEMPLATE_ERROR, file_path, str(e))
        log_utils.debug(Messages.Doc.TEMPLATE_FALLBACK)
        final_content = content
    
    # Final clean up of multiple blank lines
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
    # Write back to file only if changed
    if final_content != original_content:
        file_path.write_text(final_content)
        print(f"✅ Updated navigation in: {file_path}")
    else:
        print(f"ℹ️ No changes needed for: {file_path}")

def generate_breadcrumb_navigation(file_path):
    """Generate a breadcrumb navigation for a file showing the full path hierarchy"""
    file_path = Path(file_path)
    docs_dir = Path("docs")
    
    # Get the relative path from docs directory
    try:
        rel_path = file_path.parent.relative_to(docs_dir)
        path_parts = rel_path.parts
    except ValueError:
        # File is not in docs directory
        return f"[🏠 Home](README.md)"
    
    # Calculate home path - go up to docs root
    home_path = "../" * len(path_parts) + "README.md"
    
    # Start with home link
    breadcrumbs = [f"[🏠 Home]({home_path})"]
    
    # Build the path incrementally
    current_path = ""
    for i, part in enumerate(path_parts):
        current_path += part + "/"
        display_name = part.replace('-', ' ').title()
        
        # Calculate relative link - go up to remaining depth then to target
        link_path = "../" * (len(path_parts) - i - 1) + "README.md"
        
        # Add to breadcrumbs
        breadcrumbs.append(f"[{display_name}]({link_path})")
    
    # Connect all parts with separator
    return " > ".join(breadcrumbs)

def verify_workflow_table():
    """Verify and fix the workflow table in users.md"""
    workflows_file = Path("docs/users/users.md")
    if (not workflows_file.exists()):
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
        if (name in existing_rows):
            path, desc = existing_rows[name]
            # Update path if needed
            if (path != f"{d.name}/"):
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
    if (new_content != content):
        workflows_file.write_text(new_content)
        print(f"✅ Updated workflow table in: {workflows_file}")

def process_setup_guide():
    """Special processing for the setup guide to sort by step number"""
    setup_guide = Path("docs/it-admins/setup/0-setup-guide.md")
    if (not setup_guide.exists()):
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