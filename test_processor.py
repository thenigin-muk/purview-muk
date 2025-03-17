#!/usr/bin/env python3

import yaml
from jinja2 import Template

print("Testing YAML module...")
data = yaml.safe_load('{"test": "success"}')
print(f"YAML test: {data}")

print("Testing Jinja2 module...")
template = Template("Hello, {{name}}!")
result = template.render(name="world")
print(f"Jinja2 test: {result}")

print("All tests passed!")
