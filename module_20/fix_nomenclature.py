import re

with open('generate_module20_report_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Cover Page Boxes
old_cover = '<div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">11 Patterns</div></div>'
new_cover = '<div class="cover-box"><div class="cover-box-label">Classifications</div><div class="cover-box-val">5 Areas</div></div>\\n    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">6 Patterns</div></div>'
code = code.replace(old_cover, new_cover)

# 2. Update Summary Table (Part A - Classifications)
code = code.replace('<td><b>Pattern 1</b></td>', '<td><b>Classif. 1</b></td>')
code = code.replace('<td><b>Pattern 2</b></td>', '<td><b>Classif. 2</b></td>')
code = code.replace('<td><b>Pattern 3</b></td>', '<td><b>Classif. 3</b></td>')
code = code.replace('<td><b>Pattern 4</b></td>', '<td><b>Classif. 4</b></td>')
code = code.replace('<td><b>Pattern 5</b></td>', '<td><b>Classif. 5</b></td>')

# Update Summary Table (Part B - Patterns)
code = code.replace('<td><b>Pattern 6</b></td>', '<td><b>Pattern 1</b></td>')
code = code.replace('<td><b>Pattern 7</b></td>', '<td><b>Pattern 2</b></td>')
code = code.replace('<td><b>Pattern 8</b></td>', '<td><b>Pattern 3</b></td>')
code = code.replace('<td><b>Pattern 9</b></td>', '<td><b>Pattern 4</b></td>')
code = code.replace('<td><b>Pattern 10</b></td>', '<td><b>Pattern 5</b></td>')
code = code.replace('<td><b>Pattern 11</b></td>', '<td><b>Pattern 6</b></td>')

# 3. Update the Headers for the Blocks
# Classifications
code = code.replace('<div class="ph-label">PATTERN 1</div>', '<div class="ph-label">CLASSIFICATION 1</div>')
code = code.replace('<div class="ph-label">PATTERN 2</div>', '<div class="ph-label">CLASSIFICATION 2</div>')
code = code.replace('<div class="ph-label">PATTERN 3</div>', '<div class="ph-label">CLASSIFICATION 3</div>')
code = code.replace('<div class="ph-label">PATTERN 4</div>', '<div class="ph-label">CLASSIFICATION 4</div>')
code = code.replace('<div class="ph-label">PATTERN 5</div>', '<div class="ph-label">CLASSIFICATION 5</div>')

# Patterns
code = code.replace('<div class="ph-label">PATTERN 6</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 1 (BEHAVIORAL)</div>')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 2 (BEHAVIORAL)</div>')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 3 (BEHAVIORAL)</div>')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 9 (BEHAVIORAL)</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 4 (BEHAVIORAL)</div>')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 10 (BEHAVIORAL)</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 5 (BEHAVIORAL)</div>')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 11 (BEHAVIORAL)</div>', '<div class="ph-label" style="color:#c0392b">PATTERN 6 (BEHAVIORAL)</div>')

# 4. Update the Table Titles (Table 6.1 -> Table P1.1, etc.)
code = code.replace('Table 1.1', 'Table C1')
code = code.replace('Table 2.1', 'Table C2')
code = code.replace('Table 3.1', 'Table C3')
code = code.replace('Table 4.1', 'Table C4')
code = code.replace('Table 5.1', 'Table C5')

code = code.replace('Pattern 6.1:', 'Pattern 1.1:')
code = code.replace('Pattern 6.2:', 'Pattern 1.2:')
code = code.replace('Pattern 6.3:', 'Pattern 1.3:')

code = code.replace('Table 7.1', 'Table P2')
code = code.replace('Table 8.1', 'Table P3')
code = code.replace('Table 9.1', 'Table P4')
code = code.replace('Table 10.1', 'Table P5')
code = code.replace('Table 11.1', 'Table P6')

with open('generate_module20_report_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Nomenclature fixed successfully.")
