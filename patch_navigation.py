from pathlib import Path
import re

def patch_file():
    file_path = Path("docs/it-admins/core-concepts/graph-api-security.md")
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
        
    content = file_path.read_text()
    
    # Replace any template references with escaped versions
    new_content = re.sub(r'{{(\s*secrets\.[^}]+)}}', r'{{\1 | default("PLACEHOLDER")}}', content)
    
    # Or completely escape template syntax
    # new_content = re.sub(r'{{(.*?)}}', r'{% raw %}{{{\1}}{% endraw %}', content)
    
    # Write back to file
    file_path.write_text(new_content)
    print(f"✅ Fixed template references in: {file_path}")

if __name__ == "__main__":
    patch_file()
