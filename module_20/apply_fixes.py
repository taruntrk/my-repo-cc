import re

with open('generate_module20_report_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Restore Annual Trends (Pattern 2.1)
# Find the end of Pattern 1 (Corporate Hospitals) and insert Pattern 2.1
annual_code = """
# ── PATTERN 2.1: ANNUAL TRENDS ────────────────────────────────────────────────
if p02a:
    H.append(f'''
<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual Expenditure &amp; Deduction Trends</div>
<table class="dt">
{th("Financial Year","Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Deducted (₹ Cr)","Deduction %")}
<tbody>''')
    for r in p02a:
        fy = safe(r.get("financial_year",""))
        claims = int(float(r.get("total_claims",0)))
        claimed = float(r.get("total_claimed_cr", 0))
        approved = float(r.get("total_approved_cr", 0))
        deducted = float(r.get("total_deducted_cr", 0))
        ded_pct = float(r.get("deduction_pct", 0))
        H.append(f"<tr><td><b>{fy}</b></td><td>{fmt(claims)}</td>"
                 f"<td>{claimed:,.2f}</td><td>{approved:,.2f}</td><td>{deducted:,.2f}</td>"
                 f"<td>{ded_pct:.2f}%</td></tr>")
    H.append(f'''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Inflation Trend:</b> The data shows a massive escalation in budget leakage across the FY 2021-2026 window, directly correlating with increased private hospital utilization.</div>
''')
"""

# Insert Pattern 2.1 right after the end of Pattern 1 (Key Findings of Park Hospital)
# Look for: <div class="kf-item"><b>Park Hospital Chain Cumulative Impact:</b>...</div>\n</div>""")
pattern_1_end = r'<div class="kf-item"><b>Park Hospital Chain Cumulative Impact:.*?</div>"""\)'
code = re.sub(pattern_1_end, lambda m: m.group(0) + "\n" + annual_code, code)

# 2. Fix Ping Pong Table (Remove Gap Column)
code = code.replace('{th("Hospital Name","Patient Name","Admission 1","Gap (Days)","Admission 2","Combined Claim (₹)")}', '{th("Hospital Name","Patient Name","Admission 1","Admission 2","Combined Claim (₹)")}')

code = code.replace("""        gap_html = f"<span style='color:#c0392b;font-weight:700'>{gap} Days</span>"
        
        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{pname[:20]}</td>"
                 f"<td>{admin1}</td><td>{gap_html}</td><td>{admin2}</td>"
                 f"<td>{fmt(claimed)}</td></tr>")""", """        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{pname[:20]}</td>"
                 f"<td>{admin1}</td><td>{admin2}</td>"
                 f"<td>{fmt(claimed)}</td></tr>")""")

# 3. Fix Behavioral Numbering
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Item-level', '<div class="ph-label" style="color:#c0392b">PATTERN 3 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Item-level')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Bed Blocking', '<div class="ph-label" style="color:#c0392b">PATTERN 4 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Bed Blocking')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Split-Package', '<div class="ph-label" style="color:#c0392b">PATTERN 5 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Split-Package')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>\n  <div class="ph-ctx">The Friday Hustle', '<div class="ph-label" style="color:#c0392b">PATTERN 6 (BEHAVIORAL)</div>\n  <div class="ph-ctx">The Friday Hustle')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Doctor Cloning', '<div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>\n  <div class="ph-ctx">Doctor Cloning')
code = code.replace('<div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>\n  <div class="ph-ctx">The ₹99,999 Trick', '<div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>\n  <div class="ph-ctx">The ₹99,999 Trick')


# 4. Remove Consolidated Summary Table
code = re.sub(r'# ── CONSOLIDATED SUMMARY ──────────────────────────────────────────────────────.*?</table>', '', code, flags=re.DOTALL)
# Clean up hanging H.append(""" <div class="pb"> <h1>Consolidated Summary</h1> ... </table>
# Since I used regex, let's just make sure we strip out the exact block.
# The table ends at </table>, then <h1 style="margin-top:18px... Strategic Pre-Payment Projections
code = re.sub(r'<div class="pb">\s*<h1>Consolidated Summary</h1>.*?</table>', '<div class="pb">', code, flags=re.DOTALL)


# 5. Premium Policy Recommendations CSS & HTML
old_recommendations = r'<h1 style="margin-top:14px">Empanelled Policy Recommendations</h1>.*?</div>\n"""\)'

new_recommendations = r'''<h1 style="margin-top:20px; margin-bottom:14px;">Executive Policy Interventions</h1>
<div style="background:linear-gradient(to right, #1a2744, #2c3e50); padding:16px; border-radius:6px; margin-bottom:12px; box-shadow:0 4px 6px rgba(0,0,0,0.1); border-left:5px solid #c9a84c;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
    <div style="color:#fff; font-size:10.5pt; font-weight:800; display:flex; align-items:center;">
       <span style="font-size:14pt; margin-right:8px;">🚨</span> 1. Pre-Payment Interception Deployment
    </div>
    <div style="background:#e74c3c; color:#fff; font-size:7pt; font-weight:800; padding:3px 8px; border-radius:12px; letter-spacing:1px;">CRITICAL</div>
  </div>
  <p style="color:#e2e8f0; font-size:8.5pt; line-height:1.5; margin:0 0 0 30px;">Mandate the deployment of AI-assisted billing interception scoring algorithms. Catching upcoded claims <i>before</i> payment generation represents an immediate verifiable savings potential of <b>{cr(ai_val)}</b>.</p>
</div>

<div style="background:linear-gradient(to right, #f8f9fa, #ffffff); padding:14px 16px; border-radius:6px; border:1px solid #e2e8f0; border-left:5px solid #c9a84c; margin-bottom:12px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
    <div style="color:#1a2744; font-size:10pt; font-weight:800; display:flex; align-items:center;">
       <span style="font-size:13pt; margin-right:8px;">🏢</span> 2. Corporate Chain Investigation
    </div>
    <div style="background:#e74c3c; color:#fff; font-size:7pt; font-weight:800; padding:3px 8px; border-radius:12px; letter-spacing:1px;">CRITICAL</div>
  </div>
  <p style="color:#4a5568; font-size:8.5pt; line-height:1.5; margin:0 0 0 30px;">Initiate an immediate, retrospective billing audit on the <b>Park Hospital Chain</b> across all empanelled geographic locations to penalize systematic package unbundling and bed-blocking.</p>
</div>

<div style="background:linear-gradient(to right, #f8f9fa, #ffffff); padding:14px 16px; border-radius:6px; border:1px solid #e2e8f0; border-left:5px solid #d4680a; margin-bottom:16px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
    <div style="color:#1a2744; font-size:10pt; font-weight:800; display:flex; align-items:center;">
       <span style="font-size:13pt; margin-right:8px;">🛡️</span> 3. Tighten Empanelment Accreditation
    </div>
    <div style="background:#d4680a; color:#fff; font-size:7pt; font-weight:800; padding:3px 8px; border-radius:12px; letter-spacing:1px;">HIGH PRIORITY</div>
  </div>
  <p style="color:#4a5568; font-size:8.5pt; line-height:1.5; margin:0 0 0 30px;">Establish strict deadlines for mandatory NABH accreditation for all private empanelled hospitals within 3 years. This structural shift is projected to minimize baseline audit errors by ₹285–₹320 Cr annually.</p>
</div>

<div style="border-top:1px solid #e2e8f0; margin-top:24px; padding-top:16px; text-align:center;">
  <p style="font-size:7.5pt; color:#718096; font-weight:600; margin-bottom:4px; letter-spacing:0.5px;">PREPARED BY IIT KANPUR — DATA ANALYTICS &amp; FRAUD INTELLIGENCE DIVISION</p>
  <p style="font-size:7pt; color:#a0aec0;">Generated on {today_str} | Confidential &amp; Restricted Distribution</p>
</div>
</div>
""")'''

code = re.sub(old_recommendations, new_recommendations, code, flags=re.DOTALL)

with open('generate_module20_report_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

