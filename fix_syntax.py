import re

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

content = content.replace('\n═', '\n# ═')
content = content.replace('═\n', '═\n')

# there are also block sections like "── PatternBanner matching Module 20 ──────────────────────────────────────────"
# I should just make sure any line starting with ─ or ═ is commented.
lines = content.split('\n')
for i in range(len(lines)):
    if lines[i].startswith('═') or lines[i].startswith('─'):
        lines[i] = '# ' + lines[i]

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write('\n'.join(lines))
