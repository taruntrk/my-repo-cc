import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Pattern 2 Heading
p2_target = """if p02a:
    H.append(f'''
<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual Expenditure &amp; Deduction Trends</div>"""

p2_replace = """if p02a:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 2 (MACRO &amp; SYSTEMIC ANALYTICS)</div>
  <div class="ph-ctx">Systemic structural leakage</div>
  <div class="ph-title">Annual Trends, Regional &amp; Demographics</div>
</div></div>
<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual Expenditure &amp; Deduction Trends</div>"""
code = code.replace(p2_target, p2_replace)

# 2. Financial Summary Enhancement
p3_target = """    <div style="background:#fffdf5; border-left:4px solid {GOLD}; border-top:1px solid #f2e6c2; border-right:1px solid #f2e6c2; border-bottom:1px solid #f2e6c2; padding:10px; margin-bottom:14px;">
        <div style="font-weight:800; color:{NAV}; font-size:9.5pt; margin-bottom:6px;">Financial Impact Summary (Top 15 Outliers per Category)</div>
        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing:</b> Claimed Rs. {fmt(tot_pkg_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_pkg_d)}</span></li>
            <li><b>Antibiotic Abuse:</b> Claimed Rs. {fmt(tot_anti_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_anti_d)}</span></li>
            <li><b>Unjustified Charges:</b> Claimed Rs. {fmt(tot_unj_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_unj_d)}</span></li>
        </ul>
    </div>"""

p3_replace = """    <div style="background:#fffdf5; border-left:4px solid {GOLD}; border-top:1px solid #f2e6c2; border-right:1px solid #f2e6c2; border-bottom:1px solid #f2e6c2; padding:10px; margin-bottom:14px;">
        <div style="font-weight:800; color:{NAV}; font-size:9.5pt; margin-bottom:4px;">Financial Impact Summary (Top Outliers per Category)</div>
        <div style="font-size:8pt; color:#666; margin-bottom:6px;">This summary aggregates the total leakage prevented across the identified outlier claims for each behavioral category.</div>
        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing ({len(list_pkg)} Cases):</b> Claimed Rs. {fmt(tot_pkg_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_pkg_d)}</span></li>
            <li><b>Antibiotic Abuse ({len(list_anti)} Cases):</b> Claimed Rs. {fmt(tot_anti_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_anti_d)}</span></li>
            <li><b>Unjustified Charges ({len(list_unj)} Cases):</b> Claimed Rs. {fmt(tot_unj_c)} &rarr; <span style="color:#c0392b;font-weight:700">Deducted Rs. {fmt(tot_unj_d)}</span></li>
        </ul>
    </div>"""
code = code.replace(p3_target, p3_replace)

# 3. LoS Ailment Removal
p4_target1 = '{th("Hospital Name","City","Patient Name","Ailment","Admitted","Discharged","Stay","Claimed (₹)","Deducted (₹)")}'
p4_replace1 = '{th("Hospital Name","City","Patient Name","Admitted","Discharged","Stay","Claimed (₹)","Deducted (₹)")}'
code = code.replace(p4_target1, p4_replace1)

p4_target2 = """        H.append(f"<tr><td><b>{hname[:30]}</b></td><td>{city}</td><td>{pname[:15]}</td>"
                 f"<td style='font-size:7.5pt'>{ailment}</td><td>{admit}</td><td>{discharge}</td>"
                 f"<td><span style='color:#c0392b;font-weight:700'>{stay} d</span></td>"
                 f"<td>{fmt(claimed)}</td><td>{fmt(deducted)}</td></tr>")"""
p4_replace2 = """        H.append(f"<tr><td><b>{hname[:30]}</b></td><td>{city}</td><td>{pname[:15]}</td>"
                 f"<td>{admit}</td><td>{discharge}</td>"
                 f"<td><span style='color:#c0392b;font-weight:700'>{stay} d</span></td>"
                 f"<td>{fmt(claimed)}</td><td>{fmt(deducted)}</td></tr>")"""
code = code.replace(p4_target2, p4_replace2)

# 4 & 5. Replace Projections and Policy with Consolidated Summary
start_remove = '<h1 style="margin-top:18px; margin-bottom:12px;">Strategic Pre-Payment Projections</h1>'
end_remove = '<div style="border-top:1px solid #e2e8f0; margin-top:24px; padding-top:16px; text-align:center;">'

start_idx = code.find(start_remove)
end_idx = code.find(end_remove)

if start_idx != -1 and end_idx != -1:
    summary_code = """
<h1 style="margin-top:20px; margin-bottom:14px;">Consolidated Summary</h1>
<div class="tc">Overall Final Audit Findings</div>
<table class="dt">
{th("Category","Metric","Claimed Amount","Deducted Amount","Deduction %")}
<tbody>
  <tr><td><b>Total Audit Volume</b></td><td>{fmt(kpi_total_claims)} Claims</td><td>{cr(kpi_claimed_cr)}</td><td>{cr(kpi_deducted_cr)}</td><td>{kpi_deduction_pct:.2f}%</td></tr>
</tbody>
</table>
"""
    code = code[:start_idx] + summary_code + code[end_idx:]

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
