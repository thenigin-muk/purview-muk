#!/usr/bin/env python3
# filepath: workflows/document_processing/utils.py
import re
from pathlib import Path

def get_relative_path(target, source_file):
    """Calculate relative path from source to target, both relative to docs/"""
    source_dir = Path(source_file).parent
    docs_dir = Path("docs")
    
    # Calculate relative depth from docs directory
    try:
        rel_path = source_dir.relative_to(docs_dir)
        depth = len(rel_path.parts)
    except ValueError:
        # If source is not within docs directory
        depth = 0
        
    # Create path with proper number of "../" elements
    if depth == 0:
        return target
    else:
        return "../" * depth + target

def extract_description(file_path):
    """Extract description from markdown file"""
    content = Path(file_path).read_text()
    
    # First try to extract from description comment
    desc_pattern = r'<!--\s*description:\s*(.+?)\s*-->'
    desc_match = re.search(desc_pattern, content, re.MULTILINE)
    
    if desc_match:
        # If we have a description comment, use that directly
        return desc_match.group(1).strip()
    
    # For README files, look for a Description section, but avoid including table content
    if file_path.name.lower() == "readme.md":
        # Look for a Description section but stop before any table or next heading
        desc_section = re.search(r'## Description\s*\n(.*?)(?=\n##|\n\||\Z)', content, re.DOTALL)
        if desc_section:
            return desc_section.group(1).strip()
    
    # Fallback: Use first paragraph after title but SKIP navigation and table sections
    content_without_nav = re.sub(r'### Site Navigation\n.*?\n\n', '\n\n', content, flags=re.DOTALL)
    content_without_nav = re.sub(r'\|.*\|.*\|.*\|', '', content_without_nav, flags=re.MULTILINE)  # Remove table rows
    first_para = re.search(r'# .+?\n\n(.+?)(?=\n\n|\Z)', content_without_nav, re.DOTALL)
    if first_para:
        clean_para = first_para.group(1).replace('\n', ' ').strip()
        if '|' not in clean_para and '---' not in clean_para:  # Extra check to avoid table fragments
            return clean_para[:100] + "..." if len(clean_para) > 100 else clean_para
    
    # Last resort: generic description
    return f"Documentation about {Path(file_path).stem.replace('-', ' ').title()}"

def cleanup_file_for_processing(file_path):
    """Clean up a file before processing to remove duplicate navigation"""
    file_path = Path(file_path)
    content = file_path.read_text()
    
    # Remove duplicate bottom navigation
    cleaned = re.sub(r'(\n\n---\n\n\[⬅ Previous:.*?\].*?\n)\n\n---\n\n\[⬅ Previous:.*?\].*?\n', r'\1', content)
    
    # Remove duplicate top navigation
    cleaned = re.sub(r'(### Site Navigation\n.*?\n\n)### Site Navigation\n.*?\n', r'\1', cleaned)
    
    # Write back if changed
    if (cleaned != content):
        file_path.write_text(cleaned)
        print(f"🧹 Cleaned up duplicate navigation in: {file_path}")
    
    return cleaned

def clean_duplicate_navigation(content):
    """Clean up duplicate navigation sections in the content"""
    # Remove duplicate bottom navigation
    cleaned = re.sub(r'(\n\n---\n\n\[⬅ Previous:.*?\].*?\n)\n\n---\n\n\[⬅ Previous:.*?\].*?\n', r'\1', content)
    
    # Remove duplicate top navigation
    cleaned = re.sub(r'(### Site Navigation\n.*?\n\n)### Site Navigation\n.*?\n', r'\1', cleaned)
    
    return cleaned

def check_unresolved_templates():
    """Check for any unresolved template variables in rendered files"""
    docs_dir = Path("docs")
    unresolved = []
    
    for file_path in docs_dir.glob("**/*.md"):
        content = file_path.read_text()
        if (re.search(r'\{\{\s*\w+\s*\}\}', content)):
            unresolved.append(str(file_path))
    
    if (unresolved):
        print("\n⚠️ Unresolved template variables found in:")
        for file in unresolved:
            print(f"  - {file}")
        print("Please check your config.yaml file.")