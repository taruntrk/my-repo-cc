import re

with open('generate_module20_report_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove p01b loading
code = re.sub(r'p01b = load_latest\("new_01b_top_deduction_claims\*\.csv".*?\n', '', code)

# 2. Update cover page
code = code.replace('<div class="cover-box"><div class="cover-box-val">6 Patterns</div>', '<div class="cover-box"><div class="cover-box-val">8 Patterns</div>')
code = re.sub(r'<div class="cover-box"><div class="cover-box-label">Classifications.*?</div></div>', '', code, flags=re.DOTALL)
code = code.replace('6 Patterns', '8 Patterns')
code = code.replace('11 Patterns', '8 Patterns')

# 3. Update Summary Table
old_summary_table = r'<h1 style="margin-top:14px">Fraud Forensics.*?</tbody>\n</table>'
new_summary_table = """<h1 style="margin-top:14px">Fraud Forensics — Detection Patterns &amp; Methodologies</h1>
<table class="dt">
<thead>
  <tr>
    <th style="width:6%">#</th>
    <th style="width:30%">Detection Pattern</th>
    <th style="width:49%">Methodology / Focus</th>
    <th style="width:15%">Data Status</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td colspan="4" style="background:#f4f6f9; font-weight:800; color:#1a2744; text-align:center;">MACRO &amp; SYSTEMIC ANALYTICS</td>
  </tr>
  <tr>
    <td>1</td>
    <td><b>Corporate Hospital Overbilling</b></td>
    <td>Billing details for top 50 highest absolute leakage facilities</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Macro &amp; Systemic Frauds</b></td>
    <td>Combines Annual Trends, Regional Geography, and Demographics</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td colspan="4" style="background:#f4f6f9; font-weight:800; color:#c0392b; text-align:center;">BEHAVIORAL EXECUTION PATTERNS</td>
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

code = re.sub(old_summary_table, new_summary_table, code, flags=re.DOTALL)
code = re.sub(r'<div class="tc" style="font-weight:800; color:#c0392b; margin-top:16px;">PART B.*?</tbody>\n</table>', '', code, flags=re.DOTALL)

# 4. Delete Pattern 1 block
code = re.sub(r'# ── PATTERN 1: OVERALL BASELINE LEAKAGE ───────────────────────────────────────.*?</div>"""\)', '', code, flags=re.DOTALL)

# 5. Fix nomenclature and nesting
code = code.replace('CLASSIFICATION 3', 'PATTERN 1')
code = code.replace('Table C3', 'Table 1.1')
code = code.replace('Table C4', 'Table 2.2')
code = code.replace('CLASSIFICATION 4', 'PATTERN 2.2')
code = code.replace('Table C5', 'Table 2.3')
code = code.replace('CLASSIFICATION 5', 'PATTERN 2.3')

annual_start = """# ── PATTERN 2: ANNUAL TRENDS & INFLATION ──────────────────────────────────────
if p02a:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 2</div>"""
  
new_annual_start = """# ── PATTERN 2: MACRO & SYSTEMIC ANALYTICS ─────────────────────────────────────
if p02a or p05a or p08a:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Macro &amp; Systemic Frauds<br/>(System-wide Billing Inflation)</div>
  <div class="ph-title">Macro &amp; Systemic Analytics</div>
</div></div>
<p><b>Description:</b> This combined pattern analyzes systemic fraud vectors across the ECHS landscape, covering Year-on-Year inflation rates, geographical fraud hotspots, and demographic dependent abuse. Tracking these vectors is critical to deploying macro-level policy interventions.</p>
''')

if p02a:
    H.append(f'''<div class="tc" style="margin-top:14px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual YoY Inflation Trends</div>
<table class="dt" style="margin-bottom:12px;">"""

code = code.replace(annual_start, new_annual_start)

# Remove redundant lines from Annual
code = re.sub(r'<div class="ph-ctx">Annual YoY Inflation Trends.*?<tbody>', '<tbody>', code, flags=re.DOTALL)

# Remove pb and ph from Pattern 4 (now 2.2) and Pattern 5 (now 2.3)
code = re.sub(r'<div class="pb">\s*<div class="nob">\s*<div class="ph">\s*<div class="ph-label">PATTERN 2.2</div>.*?<p><b>Description:.*?<p><b>How the threshold.*?<div class="tc">Table 2\.2 —', '<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.2 —', code, flags=re.DOTALL)

code = re.sub(r'<div class="pb">\s*<div class="nob">\s*<div class="ph">\s*<div class="ph-label">PATTERN 2.3</div>.*?<p><b>Description:.*?<p><b>How the threshold.*?<div class="tc">Table 2\.3 —', '<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.3 —', code, flags=re.DOTALL)


# 6. Itemized (Pattern 3) - Financial summary & badge removal
itemized_setup = """    list_anti = []
    list_pkg = []
    list_unj = []
    for r in p07:
        t = safe(r.get("auditor_remarks","")).lower()
        if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
            list_anti.append(r)
        elif any(k in t for k in ["package", "already covered"]):
            list_pkg.append(r)
        else:
            list_unj.append(r)"""

new_itemized_setup = """    list_anti = []
    list_pkg = []
    list_unj = []
    tot_pkg_c, tot_pkg_d = 0.0, 0.0
    tot_anti_c, tot_anti_d = 0.0, 0.0
    tot_unj_c, tot_unj_d = 0.0, 0.0
    
    for r in p07:
        t = safe(r.get("auditor_remarks","")).lower()
        c = float(r.get("item_claimed_amount",0))
        d = float(r.get("item_deducted_amount",0))
        if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
            list_anti.append(r)
            tot_anti_c += c
            tot_anti_d += d
        elif any(k in t for k in ["package", "already covered"]):
            list_pkg.append(r)
            tot_pkg_c += c
            tot_pkg_d += d
        else:
            list_unj.append(r)
            tot_unj_c += c
            tot_unj_d += d
            
    H.append(f'''
    <div style="background:#fffdf5; border-left:4px solid {GOLD}; border-top:1px solid #f2e6c2; border-right:1px solid #f2e6c2; border-bottom:1px solid #f2e6c2; padding:10px; margin-bottom:14px;">
        <div style="font-weight:800; color:{NAV}; font-size:9.5pt; margin-bottom:6px;">Financial Impact Summary (Top 15 Outliers per Category)</div>
        <ul style="font-size:8.5pt; margin:0 0 0 16px;">
            <li><b>Package Double-Billing:</b> Claimed ₹{tot_pkg_c:,.2f} &rarr; <span style="color:#c0392b;font-weight:700">Deducted ₹{tot_pkg_d:,.2f}</span></li>
            <li><b>Antibiotic Abuse:</b> Claimed ₹{tot_anti_c:,.2f} &rarr; <span style="color:#c0392b;font-weight:700">Deducted ₹{tot_anti_d:,.2f}</span></li>
            <li><b>Unjustified Charges:</b> Claimed ₹{tot_unj_c:,.2f} &rarr; <span style="color:#c0392b;font-weight:700">Deducted ₹{tot_unj_d:,.2f}</span></li>
        </ul>
    </div>
    ''')"""
code = code.replace(itemized_setup, new_itemized_setup)

# Remove badge
code = code.replace('cat_badge = f\'<span class="badge {badge_class}">{badge_text}</span><br/>\'', 'cat_badge = ""')

code = code.replace('PATTERN 1 (BEHAVIORAL)', 'PATTERN 3 (BEHAVIORAL)')
code = code.replace('PATTERN 2 (BEHAVIORAL)', 'PATTERN 4 (BEHAVIORAL)')
code = code.replace('PATTERN 3 (BEHAVIORAL)', 'PATTERN 5 (BEHAVIORAL)')
code = code.replace('PATTERN 4 (BEHAVIORAL)', 'PATTERN 6 (BEHAVIORAL)')
code = code.replace('PATTERN 5 (BEHAVIORAL)', 'PATTERN 7 (BEHAVIORAL)')
code = code.replace('PATTERN 6 (BEHAVIORAL)', 'PATTERN 8 (BEHAVIORAL)')

# Update internal itemized numbers
code = code.replace('Pattern 1.1:', 'Pattern 3.1:')
code = code.replace('Pattern 1.2:', 'Pattern 3.2:')
code = code.replace('Pattern 1.3:', 'Pattern 3.3:')

# 7. Ping Pong Table
ping_pong_table_header = '{th("Hospital Name","Patient Name","Admission 1","Discharge 1","Admission 2","Gap (Days)","Combined Claim (₹)")}'
new_ping_pong_table_header = '{th("Hospital Name","Patient Name","Admission 1","Gap (Days)","Admission 2","Combined Claim (₹)")}'
code = code.replace(ping_pong_table_header, new_ping_pong_table_header)

ping_pong_row = 'f"<td>{admin1}</td><td>{disch1}</td><td>{admin2}</td>" \\\n                 f"<td>{gap_html}</td><td>{fmt(claimed)}</td></tr>"'
new_ping_pong_row = 'f"<td>{admin1}</td><td>{gap_html}</td><td>{admin2}</td>" \\\n                 f"<td>{fmt(claimed)}</td></tr>"'
code = code.replace(ping_pong_row, new_ping_pong_row)
code = code.replace('f"<td>{admin1}</td><td>{disch1}</td><td>{admin2}</td>"', 'f"<td>{admin1}</td><td>{gap_html}</td><td>{admin2}</td>"')
code = code.replace('f"<td>{gap_html}</td><td>{fmt(claimed)}</td></tr>"', 'f"<td>{fmt(claimed)}</td></tr>"')

# 8. Update Final Consolidated Summary
new_final_summary = """  <tr>
    <td colspan="4" style="background:#f4f6f9; font-weight:800; color:#1a2744; text-align:center;">8-PATTERN FORENSICS SNAPSHOT</td>
  </tr>
  <tr>
    <td><b>Pattern 1</b></td>
    <td>Corporate Hospital Overbilling (Top 50)</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td><b>Pattern 2</b></td>
    <td>Macro &amp; Systemic Analytics</td>
    <td>6,305,752</td>
    <td>{cr(45232.08)}</td>
  </tr>
  <tr>
    <td><b>Pattern 3</b></td>
    <td>Itemized Procedure Deviations (&ge; ₹50k)</td>
    <td>1,463,130</td>
    <td>{cr(1931.93)}</td>
  </tr>
  <tr>
    <td><b>Pattern 4</b></td>
    <td>Length of Stay (LoS) Abuse</td>
    <td>838 Active Cases</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 5</b></td>
    <td>Ping-Pong Admissions</td>
    <td>500 Active Cases</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 6</b></td>
    <td>Weekend Admission Surge</td>
    <td>200 High-Risk Hosps</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 7</b></td>
    <td>Doctor / Surgeon Cloning</td>
    <td>200 High-Risk Doctors</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 8</b></td>
    <td>Threshold Avoiding (₹99k Trick)</td>
    <td>146 High-Risk Hosps</td>
    <td>Behavioral</td>
  </tr>"""

code = re.sub(r'  <tr>\s*<td colspan="4" style="background:#f4f6f9; font-weight:800; color:#1a2744; text-align:center;">PART A: CLASSIFICATIONS</td>.*?</tr>', new_final_summary, code, flags=re.DOTALL)

with open('generate_module20_report_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

