#!/usr/bin/env python3
# filepath: workflows/document_processing/html_generator.py

from pathlib import Path

# Import logging
from workflows.common import log_utils
from workflows.common.log_utils import Messages

def generate_html_files():
    """Generate HTML files for SharePoint"""
    try:
        import markdown
        log_utils.info(Messages.Doc.HTML_GENERATING)
        
        docs_dir = Path("docs")
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
            
            log_utils.info(Messages.Doc.HTML_GENERATED, html_file)
    except ImportError:
        log_utils.warning(Messages.Doc.HTML_MODULE_MISSING)