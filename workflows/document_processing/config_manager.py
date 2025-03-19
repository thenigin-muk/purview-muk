#!/usr/bin/env python3
# filepath: workflows/document_processing/config_manager.py
import os
import yaml
from pathlib import Path

# Import logging
from workflows.common import log_utils
from workflows.common.log_utils import Messages

def load_config():
    """Load configuration from config.yaml or return default config"""
    config_path = Path("config.yaml")
    if (config_path.exists()):
        with open(config_path) as f:
            config = yaml.safe_load(f)
            # Ensure 'paths' key exists in the configuration
            if ('paths' not in config):
                config['paths'] = {
                    "docs_dir": "docs",
                    "workflows_dir": "docs/users",
                    "admin_dir": "docs/it-admins"
                }
            log_utils.debug(Messages.Doc.CONFIG_LOADED)
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

def ensure_config():
    """Create default config file if it doesn't exist"""
    config_path = Path("config.yaml")
    if (not config_path.exists()):
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
        log_utils.info(Messages.Doc.CONFIG_CREATED, config_path)
        log_utils.warning(Messages.Doc.CONFIG_WARNING)
        return default_config
    return load_config()