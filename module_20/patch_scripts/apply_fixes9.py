import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fixes in generate_module20_report_html.py
code = code.replace(
    "(> 15 Surgeries / Day)",
    "(> 15 Procedures / Day)"
)

code = code.replace(
    "abnormally high number of surgeries or admissions (e.g., >15)",
    "abnormally high number of procedures or admissions (e.g., >15)"
)

code = code.replace(
    '{th("Hospital Name","City","Treating Doctor","Date","Surgeries In 1 Day","Claimed (₹ Lakhs)")}',
    '{th("Hospital Name","City","Treating Doctor","Date","Procedures In 1 Day","Claimed (₹ Lakhs)")}'
)

code = code.replace(
    'Pattern 7 (High-Volume Provider (Superman Pattern)s)</td><td>17,374 Surgeries',
    'Pattern 7 (High-Volume Provider (Superman Pattern))</td><td>17,374 Procedures'
)

code = code.replace(
    "Pattern 7 (Superman Surgeons)</td><td>17,374 Surgeries",
    "Pattern 7 (High-Volume Provider (Superman Pattern))</td><td>17,374 Procedures"
)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
