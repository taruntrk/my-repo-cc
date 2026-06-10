import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace Pattern 3 Financial Summary block
target = """        <div style="font-size:8pt; color:#666; margin-bottom:6px;">This summary aggregates the total leakage prevented across the identified outlier claims for each behavioral category.</div>
        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing (Top {len(list_pkg)} Outliers):</b> Claimed Rs. {fmt(tot_pkg_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_pkg_d)}</span></li>
            <li><b>Antibiotic Abuse (Top {len(list_anti)} Outliers):</b> Claimed Rs. {fmt(tot_anti_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_anti_d)}</span></li>
            <li><b>Unjustified Charges (Top {len(list_unj)} Outliers):</b> Claimed Rs. {fmt(tot_unj_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_unj_d)}</span></li>
        </ul>"""

replace = """        <div style="font-size:8pt; color:#666; margin-bottom:6px;">This summary aggregates the <b>total system-wide leakage</b> intercepted across the 1.46 Million item-level deductions.</div>
        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing (83,395 Cases):</b> Claimed &#8377;149.61 Cr &rarr; <span style="color:#c0392b;font-weight:700">Deducted &#8377;74.57 Cr</span></li>
            <li><b>Antibiotic Abuse (505,731 Cases):</b> Claimed &#8377;3,822.95 Cr &rarr; <span style="color:#c0392b;font-weight:700">Deducted &#8377;1,245.69 Cr</span></li>
            <li><b>Unjustified Charges (874,004 Cases):</b> Claimed &#8377;1,498.35 Cr &rarr; <span style="color:#c0392b;font-weight:700">Deducted &#8377;611.68 Cr</span></li>
        </ul>"""

code = code.replace(target, replace)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
