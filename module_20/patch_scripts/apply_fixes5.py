import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Pattern 3 'Cases' to 'Outliers'
p3_target = """        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing ({len(list_pkg)} Cases):</b> Claimed Rs. {fmt(tot_pkg_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_pkg_d)}</span></li>
            <li><b>Antibiotic Abuse ({len(list_anti)} Cases):</b> Claimed Rs. {fmt(tot_anti_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_anti_d)}</span></li>
            <li><b>Unjustified Charges ({len(list_unj)} Cases):</b> Claimed Rs. {fmt(tot_unj_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_unj_d)}</span></li>
        </ul>"""

p3_replace = """        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing (Top {len(list_pkg)} Outliers):</b> Claimed Rs. {fmt(tot_pkg_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_pkg_d)}</span></li>
            <li><b>Antibiotic Abuse (Top {len(list_anti)} Outliers):</b> Claimed Rs. {fmt(tot_anti_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_anti_d)}</span></li>
            <li><b>Unjustified Charges (Top {len(list_unj)} Outliers):</b> Claimed Rs. {fmt(tot_unj_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_unj_d)}</span></li>
        </ul>"""
code = code.replace(p3_target, p3_replace)


# 2. Inject the Detailed Consolidated Summary
summary_target = """<h1 style="margin-top:20px; margin-bottom:14px;">Consolidated Summary</h1>
<div class="tc">Overall Final Audit Findings</div>
<table class="dt">
{th("Category","Metric","Claimed Amount","Deducted Amount","Deduction %")}
<tbody>
  <tr><td><b>Total Audit Volume</b></td><td>{fmt(kpi_total_claims)} Claims</td><td>{cr(kpi_claimed_cr)}</td><td>{cr(kpi_deducted_cr)}</td><td>{kpi_deduction_pct:.2f}%</td></tr>
</tbody>
</table>"""

summary_replace = """<h1 style="margin-top:20px; margin-bottom:14px;">Consolidated Summary</h1>
<div class="tc">Overall Final Audit Findings (System-Wide Extract)</div>
<table class="dt">
{th("Category","Metric","Claimed Amount","Deducted Amount","Deduction %")}
<tbody>
  <tr><td><b>Pattern 1 (Corporate Overbilling)</b></td><td>{fmt(total_claims_top)} Claims</td><td>{cr(total_claimed_top/100)}</td><td>{cr(total_deducted_top/100)}</td><td>{(total_deducted_top/total_claimed_top*100):.2f}%</td></tr>
  <tr><td><b>Pattern 2 (Macro Analytics)</b></td><td style="color:#999">&mdash;</td><td style="color:#999">&mdash;</td><td style="color:#999">&mdash;</td><td style="color:#999">&mdash;</td></tr>
  <tr><td><b>Pattern 3 (Itemized Deviations)</b></td><td>1,463,130 Cases</td><td>&#8377;5,470.90 Cr</td><td>&#8377;1,931.93 Cr</td><td>35.31%</td></tr>
  <tr><td><b>Pattern 4 (LoS Abuse)</b></td><td>838 Cases</td><td>&#8377;142.03 Cr</td><td>&#8377;141.14 Cr</td><td>99.37%</td></tr>
  <tr><td><b>Pattern 5 (Ping-Pong Admissions)</b></td><td>500 Cases</td><td>&#8377;60.03 Cr</td><td style="color:#999">&mdash;</td><td style="color:#999">&mdash;</td></tr>
  <tr><td><b>Pattern 6 (Weekend Surges)</b></td><td>1,320,346 Cases</td><td>&#8377;4,449.07 Cr</td><td>&#8377;1,351.61 Cr</td><td>30.38%</td></tr>
  <tr><td><b>Pattern 7 (Superman Surgeons)</b></td><td>17,374 Surgeries</td><td>&#8377;6.56 Cr</td><td style="color:#999">&mdash;</td><td style="color:#999">&mdash;</td></tr>
  <tr><td><b>Pattern 8 (Threshold Avoiding)</b></td><td>2,856 Bills</td><td>&#8377;28.42 Cr</td><td>&#8377;5.44 Cr</td><td>19.14%</td></tr>
  <tr style="background:#1a2744;color:#fff;"><td><b style="color:#fff;">Total System Exposure</b></td><td style="color:#fff;">{fmt(kpi_total_claims)} Claims</td><td style="color:#fff;">{cr(kpi_claimed_cr)}</td><td style="color:#fff;">{cr(kpi_deducted_cr)}</td><td style="color:#fff;">{kpi_deduction_pct:.2f}%</td></tr>
</tbody>
</table>"""
code = code.replace(summary_target, summary_replace)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
