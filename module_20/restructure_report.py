import re

with open('generate_module20_report_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove loading of p01b (Overall Baseline Leakage)
code = re.sub(r'p01b = load_latest\("new_01b_top_deduction_claims\*\.csv".*\n', '', code)

# 2. Update the cover page Patterns Run to "8 Patterns" and remove classifications box
code = re.sub(r'<div class="cover-box"><div class="cover-box-label">Classifications.*?</div></div>\s*', '', code, flags=re.DOTALL)
code = code.replace('<div class="cover-box-val">6 Patterns</div>', '<div class="cover-box-val">8 Patterns</div>')

# 3. Update the summary table
old_summary_table_regex = r'<h1 style="margin-top:14px">Fraud Forensics.*?</tbody>\n</table>'
new_summary_table = """<h1 style="margin-top:14px">Fraud Forensics — Detection Patterns &amp; Methodologies</h1>
<table class="dt">
<thead>
  <tr>
    <th style="width:6%">#</th>
    <th style="width:30%">Behavioral Detection Pattern</th>
    <th style="width:49%">Methodology / Focus</th>
    <th style="width:15%">Data Status</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>1</td>
    <td><b>Corporate Hospital Overbilling</b></td>
    <td>Billing details for top 50 highest absolute leakage facilities</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Macro &amp; Systemic Analytics</b></td>
    <td>Combines Annual Trends, Regional Geography, and Demographics</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>3</td>
    <td><b>Itemized Procedure Deviations</b></td>
    <td>Unbundled packages, Antibiotic abuse, and Unjustified billing</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>4</td>
    <td><b>Length of Stay (LoS) Abuse</b></td>
    <td>Bed blocking: Keeping patients admitted > 10 days unnecessarily</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>5</td>
    <td><b>Ping-Pong Admissions</b></td>
    <td>Split-Package: Discharging and readmitting patient within 48 hours</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>6</td>
    <td><b>Weekend Admission Surge</b></td>
    <td>The Friday Hustle: Exploiting lack of physical verification on weekends</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>7</td>
    <td><b>Doctor / Surgeon Cloning</b></td>
    <td>The Superman Surgeon: Billing >15 procedures in a single day</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>8</td>
    <td><b>Threshold Avoiding</b></td>
    <td>The ₹99k Trick: Billing exactly ₹99,000 to avoid senior CFA approvals</td>
    <td><b>Extracted</b></td>
  </tr>
</tbody>
</table>"""
code = re.sub(old_summary_table_regex, new_summary_table, code, flags=re.DOTALL)

# 4. Completely remove Pattern 1 (Baseline Leakage)
code = re.sub(r'# ── PATTERN 1: OVERALL BASELINE LEAKAGE ───────────────────────────────────────.*?</div>"""\)', '', code, flags=re.DOTALL)

# 5. Modify Pattern 2 (Annual), Pattern 4 (Corporate), Pattern 5 (Regional)
# First, Pattern 4 (Corporate) becomes Pattern 1.
code = code.replace('CLASSIFICATION 3', 'PATTERN 1')
code = code.replace('Table C3', 'Table 1.1')

# 6. Group Annual, Regional, Demographics into Pattern 2: Macro Analytics
code = code.replace('# ── PATTERN 2: ANNUAL TRENDS & INFLATION ──────────────────────────────────────', """# ── PATTERN 2: MACRO & SYSTEMIC ANALYTICS ─────────────────────────────────────
if p02a or p05a or p08a:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Macro &amp; Systemic Frauds<br/>(System-wide Billing Inflation)</div>
  <div class="ph-title">Macro &amp; Systemic Analytics</div>
</div></div>
<p><b>Description:</b> This combined pattern analyzes the systemic fraud vectors across the ECHS landscape, covering Year-on-Year inflation rates, geographical fraud hotspots, and demographic dependent abuse. Tracking these vectors is critical to deploying macro-level policy interventions.</p>
''')

# ── PATTERN 2.1: ANNUAL TRENDS ──
if p02a:
    H.append(f'''<div class="tc" style="margin-top:14px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual YoY Inflation Trends</div>
<table class="dt" style="margin-bottom:12px;">''')
""")
# Adjust internal headers for Annual
code = code.replace('CLASSIFICATION 2', 'PATTERN 2.1')
code = code.replace('Table C2', 'Table 2.1')
# Remove redundant pb and ph blocks for Annual
code = re.sub(r'<div class="pb">\s*<div class="nob">\s*<div class="ph">.*?<p><b>Description:.*?<p><b>How the threshold.*?<div class="tc">Table 2\.1.*?</p>', '', code, flags=re.DOTALL)
# The regex above is tricky. Let's do exact string replacements instead.

with open('generate_module20_report_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

