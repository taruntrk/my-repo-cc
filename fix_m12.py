import re

with open('/home/aman/Desktop/echs_analysis/module_12/generate_module12_report.py', 'r') as f:
    content = f.read()

# Fix the escaping in the HTML f-strings
# Anything like {{variable}} should become {variable}
content = re.sub(r'\{\{([^\}]+)\}\}', r'{\1}', content)

# But wait, in CSS_STR we do want {{ and }} for literal CSS braces.
# We need to make sure we don't un-escape the CSS block.
# Let's just fix it properly by rewriting the file entirely with proper f-strings.
