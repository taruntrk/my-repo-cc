import re

with open('generate_module20_report_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update CSV loading
old_loads = """# Load aggregated data
p01a = load_latest("new_01a_overall_leakage_summary*.csv")
p01b = load_latest("new_01b_top_deduction_claims*.csv", max_rows=15)
p02a = load_latest("new_02a_annual_expenditure_trend*.csv")
p03a = load_latest("new_03a_hospital_type_nabh_summary*.csv")
p04a = load_latest("new_04a_hospital_leakage_summary*.csv", max_rows=15)
p05a = load_latest("new_05a_regional_deduction_breakdown*.csv")
p07  = load_latest("new_07_targeted_itemized_deductions*.csv", max_rows=15)
p08a = load_latest("new_08a_gender_relation_summary*.csv")"""

new_loads = """# Load aggregated data
p01a = load_latest("new_01a_overall_leakage_summary*.csv")
p01b = load_latest("new_01b_top_deduction_claims*.csv", max_rows=15)
p02a = load_latest("new_02a_annual_expenditure_trend*.csv")
p04a = load_latest("new_04a_hospital_leakage_summary*.csv", max_rows=15)
p05a = load_latest("new_05a_regional_deduction_breakdown*.csv")
p07  = load_latest("new_07_targeted_itemized_deductions*.csv", max_rows=15)
p08a = load_latest("new_08a_gender_relation_summary*.csv")
p08_los = load_latest("new_08_los_bed_blocking_abuse*.csv", max_rows=15)
p09_pingpong = load_latest("new_09_ping_pong_admissions*.csv", max_rows=15)
p10_weekend = load_latest("new_10_weekend_surge_abuse*.csv", max_rows=15)
p11_superman = load_latest("new_11_superman_surgeon*.csv", max_rows=15)
p12_threshold = load_latest("new_12_threshold_avoiding*.csv", max_rows=15)"""

code = code.replace(old_loads, new_loads)

# 2. Update cover page
code = code.replace(
    '<div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">7 Patterns</div></div>\n    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">9,557,089</div></div>',
    '<div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">11 Patterns</div></div>\n    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">1,982,562</div></div>'
)

# 3. Update the Summary Table
old_summary_table = """<h1 style="margin-top:14px">Seven Leakage Detection Patterns — Summary</h1>
<table class="dt">
<thead>
  <tr>
    <th style="width:6%">#</th>
    <th style="width:30%">Detection Pattern</th>
    <th style="width:34%">Targeted Anomaly / Focus</th>
    <th style="width:15%">Cases Flagged</th>
    <th style="width:15%">Exposure</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>1</td>
    <td><b>Overall Baseline Leakage</b></td>
    <td>National baseline audit &amp; outlier claims (Claim &ge; ₹25,000)</td>
    <td>659,564</td>
    <td>{cr(7380.72)}</td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Annual Trends &amp; Inflation</b></td>
    <td>YoY inflation rates &amp; billing growth (Claim &ge; ₹20,000)</td>
    <td>766,652</td>
    <td>{cr(7619.60)}</td>
  </tr>
  <tr>
    <td>3</td>
    <td><b>Hospital Type &amp; Accreditation</b></td>
    <td>Category-specific leakage &amp; NABH status (Claim &ge; ₹10,000)</td>
    <td>175,448</td>
    <td>{cr(1357.15)}</td>
  </tr>
  <tr>
    <td>4</td>
    <td><b>Corporate Hospital Overbilling</b></td>
    <td>Billing details for top 50 highest absolute leakage facilities</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td>5</td>
    <td><b>Regional Commands &amp; Geography</b></td>
    <td>Geographic hotspot commands &amp; local billing offices</td>
    <td>4,401,707</td>
    <td>{cr(29458.98)}</td>
  </tr>
  <tr>
    <td>6</td>
    <td><b>Itemized Procedure Deviations</b></td>
    <td>Item-level rejections &amp; pharmacy upcoding (Line &ge; ₹50,000)</td>
    <td>1,463,130</td>
    <td>{cr(1931.93)}</td>
  </tr>
  <tr>
    <td>7</td>
    <td><b>Demographic Claims Abuse</b></td>
    <td>Dependent card-sharing and gender anomalies (Deduction &ge; ₹10,000)</td>
    <td>1,137,393</td>
    <td>{cr(8153.50)}</td>
  </tr>
</tbody>
</table>"""

new_summary_table = """<h1 style="margin-top:14px">Fraud Forensics — Detection Patterns &amp; Methodologies</h1>

<div class="tc" style="font-weight:800; color:#1a2744; margin-top:10px;">PART A: Fraud Classifications (The "Where" &amp; "Who")</div>
<table class="dt">
<thead>
  <tr>
    <th style="width:6%">#</th>
    <th style="width:30%">Classification Axis</th>
    <th style="width:34%">Targeted Anomaly / Focus</th>
    <th style="width:15%">Cases Flagged</th>
    <th style="width:15%">Exposure</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>1</td>
    <td><b>Overall Baseline Leakage</b></td>
    <td>National baseline audit &amp; outlier claims (Claim &ge; ₹25,000)</td>
    <td>659,564</td>
    <td>{cr(7380.72)}</td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Annual Trends &amp; Inflation</b></td>
    <td>YoY inflation rates &amp; billing growth (Claim &ge; ₹20,000)</td>
    <td>766,652</td>
    <td>{cr(7619.60)}</td>
  </tr>
  <tr>
    <td>3</td>
    <td><b>Corporate Hospital Overbilling</b></td>
    <td>Billing details for top 50 highest absolute leakage facilities</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td>4</td>
    <td><b>Regional Commands &amp; Geography</b></td>
    <td>Geographic hotspot commands &amp; local billing offices</td>
    <td>4,401,707</td>
    <td>{cr(29458.98)}</td>
  </tr>
  <tr>
    <td>5</td>
    <td><b>Demographic Claims Abuse</b></td>
    <td>Dependent card-sharing and gender anomalies (Deduction &ge; ₹10,000)</td>
    <td>1,137,393</td>
    <td>{cr(8153.50)}</td>
  </tr>
</tbody>
</table>

<div class="tc" style="font-weight:800; color:#c0392b; margin-top:16px;">PART B: Leakage Execution Patterns (The "How" / Modus Operandi)</div>
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
    <td>6</td>
    <td><b>Itemized Procedure Deviations</b></td>
    <td>Unbundled packages, Antibiotic abuse, and Unjustified line-item billing</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>7</td>
    <td><b>Length of Stay (LoS) Abuse</b></td>
    <td>Bed blocking: Keeping patients admitted > 10 days unnecessarily</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>8</td>
    <td><b>Ping-Pong Admissions</b></td>
    <td>Split-Package: Discharging and readmitting patient within 48 hours</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>9</td>
    <td><b>Weekend Admission Surge</b></td>
    <td>The Friday Hustle: Exploiting lack of physical verification on weekends</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>10</td>
    <td><b>Doctor / Surgeon Cloning</b></td>
    <td>The Superman Surgeon: Billing >15 procedures in a single day</td>
    <td><b>Extracted</b></td>
  </tr>
  <tr>
    <td>11</td>
    <td><b>Threshold Avoiding</b></td>
    <td>The ₹99k Trick: Billing exactly ₹99,000 to avoid senior CFA approvals</td>
    <td><b>Extracted</b></td>
  </tr>
</tbody>
</table>"""

code = code.replace(old_summary_table, new_summary_table)

# 4. Remove Pattern 3 (Hospital Type & NABH Status)
import re
# Regex to remove Pattern 3 completely
code = re.sub(r'# ── PATTERN 3: HOSPITAL TYPE & ACCREDITATION ─────────────────────────────────.*?</div>"""\)', '', code, flags=re.DOTALL)

# 5. Fix Pattern numbering for Corporate, Regional, Demography
code = code.replace('PATTERN 4', 'PATTERN 3').replace('Pattern 4', 'Pattern 3').replace('Table 4.1', 'Table 3.1')
code = code.replace('PATTERN 5', 'PATTERN 4').replace('Pattern 5', 'Pattern 4').replace('Table 5.1', 'Table 4.1')
code = code.replace('PATTERN 7', 'PATTERN 5').replace('Pattern 7', 'Pattern 5').replace('Table 7.1', 'Table 5.1')

# 6. We keep Pattern 6 (Itemized) as PATTERN 6. So let's make sure its numbering is correct.
# Wait, old Pattern 6 was Itemized, new is 6. Old Pattern 7 was Demography, new is 5.
# Let's fix the Table 6.1 etc if needed, but it's fine.

# 7. Add new Patterns 7, 8, 9, 10, 11 at the end before Consolidated Summary
new_patterns_html = """
# ── PATTERN 7: LENGTH OF STAY (LOS) ABUSE ─────────────────────────────────────
if p08_los:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 7 (BEHAVIORAL)</div>
  <div class="ph-ctx">Bed Blocking &amp; Unjustified Admissions<br/>(Stay > 10 Days)</div>
  <div class="ph-title">Length of Stay (LoS) Abuse</div>
</div></div>
<p><b>Description:</b> This behavioral pattern detects "Bed Blocking"—hospitals deliberately keeping patients admitted for unnecessarily long durations (> 10 days) to inflate daily room rent and routine nursing charges, often without clear clinical progression.</p>
<div class="tc">Table 7.1 — Top Instances of Unjustified Extended Hospital Stays</div>
<table class="dt">
{th("Hospital Name","City","Patient Name","Ailment","Admitted","Discharged","Stay","Claimed (₹)","Deducted (₹)")}
<tbody>''')
    for r in p08_los[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        pname = safe(r.get("patient_name",""))
        ailment = safe(r.get("ailment",""))[:25]
        admit = safe(r.get("admission_date",""))[:10]
        discharge = safe(r.get("discharge_date",""))[:10]
        stay = safe(r.get("stay_days",""))
        claimed = float(r.get("claimed_amount",0))
        deducted = float(r.get("deducted_amount",0))
        
        H.append(f"<tr><td><b>{hname[:30]}</b></td><td>{city}</td><td>{pname[:15]}</td>"
                 f"<td style='font-size:7.5pt'>{ailment}</td><td>{admit}</td><td>{discharge}</td>"
                 f"<td><span style='color:#c0392b;font-weight:700'>{stay} d</span></td>"
                 f"<td>{fmt(claimed)}</td><td>{fmt(deducted)}</td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Intentional Delaying:</b> Cases with >15 days for routine ailments signify clear abuse of inpatient resources.</div>
</div>''')

# ── PATTERN 8: PING-PONG ADMISSIONS ───────────────────────────────────────────
if p09_pingpong:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 8 (BEHAVIORAL)</div>
  <div class="ph-ctx">Split-Package Fraud<br/>(Readmission &lt; 48 Hours)</div>
  <div class="ph-title">Ping-Pong Admissions</div>
</div></div>
<p><b>Description:</b> This highly critical pattern flags "Ping-Ponging"—where a hospital discharges a patient only to readmit them within 48 hours for the same or related condition. This is an explicit attempt to bypass package duration limits and bill two separate procedures instead of one continuous stay.</p>
<div class="tc">Table 8.1 — Top Cases of Split-Package Readmissions (Within 48 Hrs)</div>
<table class="dt">
{th("Hospital Name","Patient Name","Admission 1","Discharge 1","Admission 2","Gap (Days)","Combined Claim (₹)")}
<tbody>''')
    for r in p09_pingpong[:15]:
        hname = safe(r.get("hospital_name",""))
        pname = safe(r.get("patient_name",""))
        admin1 = safe(r.get("admission_1",""))[:10]
        disch1 = safe(r.get("discharge_1",""))[:10]
        admin2 = safe(r.get("admission_2",""))[:10]
        gap = safe(r.get("gap_days",""))
        claimed = float(r.get("claim_amt",0))
        
        gap_html = f"<span style='color:#c0392b;font-weight:700'>{gap} Days</span>"
        
        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{pname[:20]}</td>"
                 f"<td>{admin1}</td><td>{disch1}</td><td>{admin2}</td>"
                 f"<td>{gap_html}</td><td>{fmt(claimed)}</td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Direct Evasion of Package Rules:</b> The 0-2 day gap signifies that patients were likely never physically discharged from the ward; only their paperwork was closed and reopened to trigger new package rates.</div>
</div>''')

# ── PATTERN 9: WEEKEND SURGE ABUSE ────────────────────────────────────────────
if p10_weekend:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 9 (BEHAVIORAL)</div>
  <div class="ph-ctx">The Friday Hustle<br/>(Abnormal Weekend Admissions)</div>
  <div class="ph-title">Weekend / Holiday Surge Admissions</div>
</div></div>
<p><b>Description:</b> Analyzes the distribution of admissions across the days of the week. Hospitals that show a massive spike in admissions specifically on Fridays, Saturdays, and Sundays are likely exploiting the lack of physical ECHS verifiers on duty during the weekend.</p>
<div class="tc">Table 9.1 — Hospitals with Suspicious Weekend Admission Spikes</div>
<table class="dt">
{th("Hospital Name","City","Weekend Admissions","Total Claimed (₹ Cr)","Total Deducted (₹ Cr)")}
<tbody>''')
    for r in p10_weekend[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        admissions = safe(r.get("weekend_admissions",""))
        claimed = float(r.get("total_claimed_lakhs",0))/100
        deducted = float(r.get("total_deducted_lakhs",0))/100
        
        H.append(f"<tr><td><b>{hname[:40]}</b></td><td>{city}</td>"
                 f"<td><span style='color:#d4680a;font-weight:700'>{admissions}</span></td>"
                 f"<td>{claimed:.2f} Cr</td><td>{deducted:.2f} Cr</td></tr>")
    H.append('''</tbody></table>
</div>''')

# ── PATTERN 10: SUPERMAN SURGEON ──────────────────────────────────────────────
if p11_superman:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 10 (BEHAVIORAL)</div>
  <div class="ph-ctx">Doctor Cloning Fraud<br/>(> 15 Surgeries / Day)</div>
  <div class="ph-title">Doctor Cloning (The Superman Surgeon)</div>
</div></div>
<p><b>Description:</b> Detects physical impossibility. Flags instances where a single treating doctor's ID is attached to an abnormally high number of surgeries or admissions (e.g., >15) within a single 24-hour period.</p>
<div class="tc">Table 10.1 — Impossible Daily Surgical Volumes</div>
<table class="dt">
{th("Hospital Name","City","Treating Doctor","Date","Surgeries In 1 Day","Claimed (₹ Lakhs)")}
<tbody>''')
    for r in p11_superman[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        doc = safe(r.get("doctor_name",""))
        date = safe(r.get("claim_date",""))
        surgeries = safe(r.get("surgeries_in_one_day",""))
        claimed = float(r.get("total_claimed_lakhs",0))
        
        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{city}</td><td>{doc[:25]}</td>"
                 f"<td>{date}</td><td><span style='color:#c0392b;font-weight:700'>{surgeries} Surgeries</span></td>"
                 f"<td>{claimed:.2f} L</td></tr>")
    H.append('''</tbody></table>
</div>''')

# ── PATTERN 11: THRESHOLD AVOIDING ────────────────────────────────────────────
if p12_threshold:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 11 (BEHAVIORAL)</div>
  <div class="ph-ctx">The ₹99,999 Trick<br/>(CFA Approval Evasion)</div>
  <div class="ph-title">Threshold Avoiding</div>
</div></div>
<p><b>Description:</b> Hospitals intentionally billing exact amounts just beneath the special approval threshold (e.g., ₹1,00,000) to ensure the claim is automatically processed without requiring senior CFA officer scrutiny.</p>
<div class="tc">Table 11.1 — Top Hospitals Exploiting the ₹99k Threshold</div>
<table class="dt">
{th("Hospital Name","City","Trick Bills Count","Total Claimed (₹ Lakhs)","Total Deducted (₹ Lakhs)")}
<tbody>''')
    for r in p12_threshold[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        bills = safe(r.get("trick_bills_count",""))
        claimed = float(r.get("total_claimed_lakhs",0))
        deducted = float(r.get("total_deducted_lakhs",0))
        
        H.append(f"<tr><td><b>{hname[:40]}</b></td><td>{city}</td>"
                 f"<td><span style='color:#d4680a;font-weight:700'>{bills} Bills</span></td>"
                 f"<td>{claimed:.2f} L</td><td>{deducted:.2f} L</td></tr>")
    H.append('''</tbody></table>
</div>''')

# ── CONSOLIDATED SUMMARY ──────────────────────────────────────────────────────
"""

# Now we need to inject new_patterns_html before the Consolidated Summary
code = code.replace('# ── CONSOLIDATED SUMMARY ──────────────────────────────────────────────────────', new_patterns_html)

# Now, update the Consolidated summary table inside the code
old_cons_table = """<table class="dt">
<thead>
  <tr>
    <th style="width:12%">Pattern</th>
    <th style="width:40%">Fraud / Leakage Signal</th>
    <th style="width:24%">Cases Flagged</th>
    <th style="width:24%">Exposure (Deducted)</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><b>Pattern 1</b></td>
    <td>Overall Outlier Claims (&ge; ₹25k)</td>
    <td>659,564</td>
    <td>{cr(7380.72)}</td>
  </tr>
  <tr>
    <td><b>Pattern 2</b></td>
    <td>Annual Trends &amp; Inflation (&ge; ₹20k)</td>
    <td>766,652</td>
    <td>{cr(7619.60)}</td>
  </tr>
  <tr>
    <td><b>Pattern 3</b></td>
    <td>Hospital Type &amp; NABH status (&ge; ₹10k)</td>
    <td>175,448</td>
    <td>{cr(1357.15)}</td>
  </tr>
  <tr>
    <td><b>Pattern 4</b></td>
    <td>Corporate Hospital Overbilling (Top 50)</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td><b>Pattern 5</b></td>
    <td>Regional Commands (Top 10 regions)</td>
    <td>4,401,707</td>
    <td>{cr(29458.98)}</td>
  </tr>
  <tr>
    <td><b>Pattern 6</b></td>
    <td>Itemized Procedure Deviations (&ge; ₹50k)</td>
    <td>1,463,130</td>
    <td>{cr(1931.93)}</td>
  </tr>
  <tr>
    <td><b>Pattern 7</b></td>
    <td>Demographic Claims Abuse (&ge; ₹10k)</td>
    <td>1,137,393</td>
    <td>{cr(8153.50)}</td>
  </tr>
  <tr style="background:#e8ecf5;font-weight:700">
    <td><b>TOTAL</b></td>
    <td><b>ECHS Claims Forensics</b></td>
    <td><b>9,557,089</b></td>
    <td><b>{cr(kpi_deducted_cr)}</b></td>
  </tr>
</tbody>
</table>"""

new_cons_table = """<table class="dt">
<thead>
  <tr>
    <th style="width:12%">Pattern</th>
    <th style="width:40%">Fraud / Leakage Signal</th>
    <th style="width:24%">Cases Flagged</th>
    <th style="width:24%">Exposure / Impact</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td colspan="4" style="background:#f4f6f9; font-weight:800; color:#1a2744; text-align:center;">PART A: CLASSIFICATIONS</td>
  </tr>
  <tr>
    <td><b>Pattern 1</b></td>
    <td>Overall Outlier Claims (&ge; ₹25k)</td>
    <td>659,564</td>
    <td>{cr(7380.72)}</td>
  </tr>
  <tr>
    <td><b>Pattern 2</b></td>
    <td>Annual Trends &amp; Inflation (&ge; ₹20k)</td>
    <td>766,652</td>
    <td>{cr(7619.60)}</td>
  </tr>
  <tr>
    <td><b>Pattern 3</b></td>
    <td>Corporate Hospital Overbilling (Top 50)</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td><b>Pattern 4</b></td>
    <td>Regional Commands (Top 10 regions)</td>
    <td>4,401,707</td>
    <td>{cr(29458.98)}</td>
  </tr>
  <tr>
    <td><b>Pattern 5</b></td>
    <td>Demographic Claims Abuse (&ge; ₹10k)</td>
    <td>1,137,393</td>
    <td>{cr(8153.50)}</td>
  </tr>
  <tr>
    <td colspan="4" style="background:#f4f6f9; font-weight:800; color:#c0392b; text-align:center;">PART B: EXECUTION PATTERNS</td>
  </tr>
  <tr>
    <td><b>Pattern 6</b></td>
    <td>Itemized Procedure Deviations (&ge; ₹50k)</td>
    <td>1,463,130</td>
    <td>{cr(1931.93)}</td>
  </tr>
  <tr>
    <td><b>Pattern 7</b></td>
    <td>Length of Stay (LoS) Abuse</td>
    <td>838 Active Cases</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 8</b></td>
    <td>Ping-Pong Admissions</td>
    <td>500 Active Cases</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 9</b></td>
    <td>Weekend Admission Surge</td>
    <td>200 High-Risk Hosps</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 10</b></td>
    <td>Doctor / Surgeon Cloning</td>
    <td>200 High-Risk Doctors</td>
    <td>Behavioral</td>
  </tr>
  <tr>
    <td><b>Pattern 11</b></td>
    <td>Threshold Avoiding (₹99k Trick)</td>
    <td>146 High-Risk Hosps</td>
    <td>Behavioral</td>
  </tr>
  <tr style="background:#e8ecf5;font-weight:700">
    <td><b>TOTAL</b></td>
    <td><b>Unique Targetable Anomalies</b></td>
    <td><b>1,982,562</b></td>
    <td><b>{cr(kpi_deducted_cr)}</b></td>
  </tr>
</tbody>
</table>"""

code = code.replace(old_cons_table, new_cons_table)

with open('generate_module20_report_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Report generation script updated successfully.")
