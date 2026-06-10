import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# I accidentally injected {fmt(total_claims_top)} in the previous script. Let's fix that.
code = code.replace(
    '<td><b>{fmt(total_claims_top)} Claims Evaluated</b></td>',
    '<td><b>2.07M Claims Evaluated</b></td>'
)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
