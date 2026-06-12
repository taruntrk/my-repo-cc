"""
ECHS Module 20: Budget Impact & Leakage Analysis — Forensic Edition
HTML + WeasyPrint approach matching ECHS Identity Fraud Report layout.
Navy + Gold theme, IIT Kanpur branding, pattern headers with left gold bar.
"""

import os, csv, glob, re, time
from datetime import date

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint")
    exit(1)

BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE, "new_data")
# Fallback to old data folder if new_data is missing
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(BASE, "data")
REPORTS_DIR = os.path.join(BASE, "final_report")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(REPORTS_DIR, f"ECHS_Module20_Leakage_Report_{ts}.pdf")

NAV  = "#1a2744"
GOLD = "#c9a84c"

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

def cr(n):
    """Format amount in Crores."""
    try:
        v = float(n)
        return f"₹{v:,.2f} Cr"
    except:
        return str(n)

def lk(n):
    """Format amount in Lakhs."""
    try:
        v = float(n)
        return f"₹{v:,.2f} L"
    except:
        return str(n)

def safe(v, d="—"):
    return str(v).strip() if v and str(v).strip() not in ("", "nan", "None", "0", "0.0") else d

def risk_txt(r):
    r = str(r).upper()
    if "CRITICAL" in r: return f'<span style="color:#c0392b;font-weight:700">CRITICAL</span>'
    if "HIGH"     in r: return f'<span style="color:#d4680a;font-weight:700">HIGH</span>'
    if "MEDIUM"   in r: return f'<span style="color:#7f8c8d;font-weight:600">MEDIUM</span>'
    return f'<span style="color:#27ae60;font-weight:600">LOW</span>'

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

# ── Load CSVs ─────────────────────────────────────────────────────────────────

def load_latest(pattern, max_rows=None):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        # Check parent data directory just in case
        files = glob.glob(os.path.join(BASE, "data", pattern))
        if not files:
            return []
    files.sort(key=os.path.getmtime, reverse=True)
    rows = []
    with open(files[0], encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            rows.append(row)
            if max_rows and i + 1 >= max_rows:
                break
    return rows

# Load aggregated data
p01a = load_latest("new_01a_overall_leakage_summary*.csv")
p04a = load_latest("new_04a_hospital_leakage_summary*.csv", max_rows=15)
p09_pingpong = load_latest("new_09_ping_pong_admissions*.csv", max_rows=15)
p10_weekend = load_latest("new_10_weekend_surge_abuse*.csv", max_rows=15)
p11_superman = load_latest("new_11_superman_surgeon*.csv", max_rows=15)
p12_threshold = load_latest("new_12_threshold_avoiding*.csv", max_rows=15)
p13_cardsharing = load_latest("new_13_card_sharing*.csv", max_rows=15)
p14_familysharing = load_latest("new_14_family_sharing*.csv", max_rows=15)
p15_demographic = load_latest("new_15_demographic_mismatch*.csv", max_rows=15)

# Extract KPIs with fallback values matching historic context
kpi_total_claims = 19845384
kpi_claimed_cr = 36261.44
kpi_approved_cr = 32649.03
kpi_deducted_cr = 3612.41
kpi_deduction_pct = 9.96

if p01a:
    try:
        row = p01a[0]
        kpi_total_claims = int(float(row.get("total_claims", kpi_total_claims)))
        kpi_claimed_cr = float(row.get("total_claimed_cr", kpi_claimed_cr))
        kpi_approved_cr = float(row.get("total_approved_cr", kpi_approved_cr))
        kpi_deducted_cr = float(row.get("total_deducted_cr", kpi_deducted_cr))
        kpi_deduction_pct = float(row.get("overall_deduction_pct", kpi_deduction_pct))
    except Exception as e:
        print(f"Error parsing overall summary: {e}")

# Projections calculation
cons_val = kpi_deducted_cr * 0.30
mod_val = kpi_deducted_cr * 0.50
agg_val = kpi_deducted_cr * 0.75
ai_val = kpi_deducted_cr * 0.60

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4;
    margin:20mm 15mm 20mm 15mm;
    @top-left {{
        content: "ECHS FORENSIC LEAKAGE SYSTEM — REPORT";
        font-family: Arial; font-size:7.5pt; font-weight:700; color:#4a5568;
        border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; vertical-align: bottom;
    }}
    @top-right {{
        content: "IIT Kanpur | Page " counter(page);
        font-family: Arial; font-size:7.5pt; color:#4a5568;
        border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; vertical-align: bottom;
    }}
    @bottom-left {{
        content: "RESTRICTED — For Internal Presentation & Executive Review Only.";
        font-family: Arial; font-size:6.5pt; color:#718096; border-top: 1px solid #e2e8f0; padding-top: 4px;
    }}
    @bottom-right {{
        content: "Generated: {today_str}";
        font-family: Arial; font-size:6.5pt; color:#718096; border-top: 1px solid #e2e8f0; padding-top: 4px;
    }}
}}

/* Cover Page styling */
.cover {{
    page-break-after: always;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 30px 10px;
    border: 2px solid {NAV};
    margin-top: -5mm;
}}
.cover-topbar {{ height: 5px; background: {NAV}; margin-bottom: 40px; }}
.cover-botbar {{ height: 5px; background: {NAV}; margin-top: 40px; }}
.cover-title {{ font-size: 38pt; font-weight: 900; color: {NAV}; text-align: center; line-height: 1.1; margin-bottom: 5px; }}
.cover-mod {{ font-size: 14pt; font-weight: 700; color: {GOLD}; text-align: center; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 40px; }}
.cover-sub {{ font-size: 12pt; text-align: center; color: #4a5568; font-style: italic; margin-bottom: 50px; }}

.cover-boxes {{ display: flex; justify-content: space-between; margin: 40px 0; gap: 10px; }}
.cover-box {{ flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-top: 3px solid {NAV}; padding: 12px 8px; text-align: center; }}
.cover-box-label {{ font-size: 6.5pt; text-transform: uppercase; font-weight: bold; color: #718096; margin-bottom: 4px; }}
.cover-box-val {{ font-size: 10.5pt; font-weight: 800; color: {NAV}; }}

.cover-org {{ font-size: 10pt; font-weight: 700; text-align: center; color: {NAV}; margin-top: auto; padding-top: 60px; }}
.cover-date {{ font-size: 8pt; text-align: center; color: #718096; margin-bottom: 20px; }}

/* Headings */
h1 {{ font-size: 18pt; font-weight: 900; color: {NAV}; margin-bottom: 12px; border-bottom: 2px solid {GOLD}; padding-bottom: 4px; text-transform: uppercase; page-break-after: avoid; }}
h2 {{ font-size: 12pt; font-weight: 800; color: {NAV}; margin-top: 15px; margin-bottom: 8px; page-break-after: avoid; }}
p {{ margin-bottom: 12px; text-align: justify; }}

.pb {{ page-break-after: always; }}
.nob {{ page-break-inside: avoid; }}

/* Metric Dashboard */
.metric-row {{ display: flex; justify-content: space-between; gap: 12px; margin: 15px 0 20px 0; }}
.mbox {{ flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid {NAV}; padding: 12px; }}
.mbox-label {{ font-size: 7.5pt; font-weight: 700; color: #4a5568; margin-bottom: 4px; text-transform: uppercase; }}
.mbox-val {{ font-size: 15pt; font-weight: 900; color: {NAV}; }}
.mbox-sub {{ font-size: 7pt; color: #718096; margin-top: 2px; }}

/* Tables */
table.dt {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 8.5pt; }}
table.dt th {{ background: {NAV}; color: #fff; font-weight: 700; text-align: left; padding: 6px 8px; border: 1px solid #2d3748; font-size: 7.5pt; text-transform: uppercase; }}
table.dt td {{ padding: 5px 8px; border: 1px solid #e2e8f0; vertical-align: middle; }}
table.dt tr:nth-child(even) {{ background: #f8fafc; }}
.tc {{ font-size: 8pt; font-weight: 700; color: #4a5568; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; font-style: italic; page-break-after: avoid; }}

/* Pattern Header */
.ph {{ border-left: 5px solid {GOLD}; padding-left: 12px; margin-bottom: 12px; margin-top: 5px; }}
.ph-label {{ font-size: 7pt; font-weight: 800; color: {GOLD}; letter-spacing: 0.5px; text-transform: uppercase; }}
.ph-title {{ font-size: 14pt; font-weight: 900; color: {NAV}; line-height: 1.15; }}
.ph-ctx {{ font-size: 8pt; color: #718096; font-style: italic; margin-top: 1px; }}

/* Action items & Key findings */
.action-item {{ background: #fffaf0; border-left: 4px solid {GOLD}; padding: 10px 12px; margin-bottom: 10px; border-radius: 0 4px 4px 0; }}
.action-num {{ font-weight: bold; color: {GOLD}; font-size: 11pt; }}
.kf-head {{ font-weight: 800; color: {NAV}; font-size: 9.5pt; margin: 15px 0 6px 0; text-transform: uppercase; letter-spacing: 0.5px; }}
.kf-item {{ margin-bottom: 6px; padding-left: 12px; border-left: 2px solid {GOLD}; font-size: 8.5pt; text-align: justify; }}

/* Badges */
.badge {{ display:inline-block; padding:1px 4px; font-size:6.5pt; font-weight:700; border-radius:2px; text-transform:uppercase; margin-bottom:2px; }}
.badge-abuse {{ background:#fde8e8; color:#9b1c1c; }}
.badge-package {{ background:#e1effe; color:#1e429f; }}
.badge-unjust {{ background:#f3f4f6; color:#374151; }}

/* Projection Section */
.proj-container {{ display: flex; flex-direction: column; gap: 10px; margin: 15px 0; }}
.proj-row {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 15px; background: #f8fafc; border-left: 4px solid #718096; border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }}
.proj-details {{ flex: 1; }}
.proj-title {{ font-size: 9.5pt; font-weight: 800; color: {NAV}; }}
.proj-desc {{ font-size: 7.5pt; color: #718096; margin-top: 2px; }}
.proj-val {{ font-size:14pt; font-weight:900; color:#c0392b; text-align:right; min-width:100px; }}
.proj-ai {{ border-left-color:{GOLD}; background:#fffdf5; border-color:#f2e6c2; }}
"""

# ── BUILD HTML ────────────────────────────────────────────────────────────────

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYSIS</div>
  <div class="cover-mod">BUDGET IMPACT &amp; LEAKAGE ANALYSIS</div>
  <div class="cover-sub">Financial Audit &amp; Deductions Analysis Report</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">{fmt(kpi_total_claims)}</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">8 Forensic Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">1,358,281</div></div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>
""")

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Executive Summary</h1>
<p>This report quantifies the total financial leakage and budget impact across the ECHS claims ecosystem. 
Using database-wide extraction of settlement statistics, we analyze expenditure trends, corporate hospital overbilling, and critical behavioral fraud patterns.
The core objective is to shift reporting from general administrative savings to a dual framework distinguishing between prevented losses and approved slippages.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Claims Scanned</div><div class="mbox-val">{fmt(kpi_total_claims)}</div><div class="mbox-sub">Database Population</div></div>
  <div class="mbox"><div class="mbox-label">Prevented Leakage</div><div class="mbox-val" style="color:#27ae60">{cr(kpi_deducted_cr)}</div><div class="mbox-sub">Audit Savings (Deducted)</div></div>
  <div class="mbox"><div class="mbox-label">Realized Leakage</div><div class="mbox-val" style="color:#c0392b">&#8377;3,225.01 Cr</div><div class="mbox-sub">Approved Fraud (Slipped)</div></div>
  <div class="mbox"><div class="mbox-label">Realized Slippage %</div><div class="mbox-val">9.88%</div><div class="mbox-sub">Of Approved Budget</div></div>
</div>

<h1 style="margin-top:14px">Fraud Forensics — 8 Core Leakage Patterns</h1>
<table class="dt">
<thead>
  <tr>
    <th style="width:6%">#</th>
    <th style="width:30%">Forensic Pattern</th>
    <th style="width:49%">Methodology / Focus</th>
    <th style="width:15%">Realized Loss</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>1</td>
    <td><b>Corporate Overbilling</b></td>
    <td>Targeted audit of multi-specialty private chains inflating standard tariff limits.</td>
    <td style="color:#c0392b;font-weight:700">₹22.25 Cr</td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Ping-Pong Admissions</b></td>
    <td>Split-package tracking: patient readmitted within 48 hours for package threshold evasion.</td>
    <td style="color:#c0392b;font-weight:700">₹60.03 Cr</td>
  </tr>
  <tr>
    <td>3</td>
    <td><b>Weekend Surge Admissions</b></td>
    <td>Elective surgeries admitted on weekends via emergency route to bypass checks.</td>
    <td style="color:#c0392b;font-weight:700">₹3,097.47 Cr</td>
  </tr>
  <tr>
    <td>4</td>
    <td><b>Doctor Cloning (Superman)</b></td>
    <td>Clinically impossible doctor volume (>15 major surgeries billed under single doctor per day).</td>
    <td style="color:#c0392b;font-weight:700">₹6.56 Cr</td>
  </tr>
  <tr>
    <td>5</td>
    <td><b>Threshold Avoiding (₹99k Trick)</b></td>
    <td>Bills deliberately priced between ₹99,000 and ₹99,999 to bypass CFA approval limit.</td>
    <td style="color:#c0392b;font-weight:700">₹22.97 Cr</td>
  </tr>
  <tr>
    <td>6</td>
    <td><b>Individual Card-Sharing</b></td>
    <td>Same-day admissions of a single card ID at different hospital locations.</td>
    <td style="color:#c0392b;font-weight:700">₹4.82 Cr</td>
  </tr>
  <tr>
    <td>7</td>
    <td><b>Family Card-Sharing</b></td>
    <td>Simultaneous same-day admissions of multiple family members at different hospitals.</td>
    <td style="color:#c0392b;font-weight:700">₹8.44 Cr</td>
  </tr>
  <tr>
    <td>8</td>
    <td><b>Demographic Mismatch</b></td>
    <td>Impossible patient profiles (gender-relationship conflicts like Male Wife/Mother).</td>
    <td style="color:#c0392b;font-weight:700">₹37.99 Cr</td>
  </tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Targeted Audits on Top Overbilling Facilities:</b> Prioritize physical audits and billing reviews at Vijay Hospital (ID 3149) and Park Hospital Gurgaon (ID 367) to stop immediate leakage.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Implement Real-Time Temporal Bundling Checks:</b> Overhaul the billing portal to block sequential claims for the same patient within a 48-hour window (Pattern 2).</div>
<div class="action-item"><span class="action-num">3.</span> <b>Enforce Pre-Payment Volume Blocks:</b> Set a hard database block that rejects claim packages where a single treating specialist is linked to more than 15 surgeries in a single day (Pattern 4).</div>
<div class="action-item"><span class="action-num">4.</span> <b>Mandatory Audit Vetting for ₹99k Cluster Bills:</b> Enforce medical auditing for any hospital showing an anomalous cluster of bills priced exactly at ₹99,000–₹99,999 (Pattern 5).</div>
</div>
""")

# ── PATTERN 1: CORPORATE LEAKAGE ──────────────────────────────────────────────
if p04a:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 1 (CORPORATE LEAKAGE)</div>
  <div class="ph-ctx">Top Absolute Leakage Facilities</div>
  <div class="ph-title">Corporate Hospital Overbilling</div>
</div></div>
<p><b>Description:</b> Empanelled private hospital chains or specific high-volume single hospitals system abuse standard rates by systematically overbilling ECHS. They submit bills where surgeries, procedures, medicines, and packages exceed agreed limits. Pre-payment auditing caught <b>₹11.20 Cr</b>, but ECHS approved and paid out <b>₹22.25 Cr</b> across the top 15 list, resulting in realized leakage.</p>
<div class="tc">Table 1.1 — Top Private Hospitals by Deduction Volume (Top 15)</div>
<table class="dt">
{th("Rank","Hospital Name &amp; ECHS ID","Type","NABH","Claims","Claimed (₹ Cr)","Prevented (₹ Cr)","Realized (₹ Cr)","Loss %")}
<tbody>""")
    total_claims_top = 0
    total_claimed_top = 0.0
    total_approved_top = 0.0
    total_deducted_top = 0.0
    for idx, r in enumerate(p04a):
        name = r.get('hospital_name', 'Unknown')
        hosp_id = r.get('hospital_id', '')
        t_code = r.get('hosp_type_code', '1')
        nabh = r.get('nabh_status', 'N')
        claims = int(float(r.get('total_claims', 0)))
        claimed = float(r.get('total_claimed_lakh', 0))
        approved = float(r.get('total_approved_lakh', 0))
        deducted = float(r.get('total_deducted_lakh', 0))
        ded_pct = float(r.get('deduction_pct', 0))
        
        pct_label = f"{ded_pct:.2f}%"
        if ded_pct >= 20.0:
            pct_label = f'<span style="color:#c0392b;font-weight:700">{pct_label}</span>'
        elif ded_pct >= 12.0:
            pct_label = f'<span style="color:#d4680a;font-weight:700">{pct_label}</span>'
            
        full_name = f"<b>{name[:50]}</b>"
        if hosp_id:
            full_name += f" [ID {hosp_id}]"
            
        H.append(f"<tr><td>{idx+1}</td>"
                 f"<td style='font-size:7.5pt'>{full_name}</td>"
                 f"<td>{t_code}</td>"
                 f"<td>{nabh}</td>"
                 f"<td>{fmt(claims)}</td>"
                 f"<td>{claimed/100:,.2f}</td>"
                 f"<td>{deducted/100:,.2f}</td>"
                 f"<td><b style='color:#c0392b'>{approved/100:,.2f}</b></td>"
                 f"<td>{100 - ded_pct:.1f}%</td></tr>")
        total_claims_top += claims
        total_claimed_top += claimed
        total_approved_top += approved
        total_deducted_top += deducted
        
    overall_top_pct = (total_deducted_top * 100.0 / total_claimed_top) if total_claimed_top > 0 else 0
    H.append(f"""<tr style="background:#e8ecf5;font-weight:700">"
             <td>—</td>
             <td>TOP 15 TOTAL</td>
             <td>—</td>
             <td>—</td>
             <td>{fmt(total_claims_top)}</td>
             <td>{total_claimed_top/100:,.2f}</td>
             <td>{total_deducted_top/100:,.2f}</td>
             <td>{total_approved_top/100:,.2f}</td>
             <td>{100 - overall_top_pct:.2f}%</td></tr>""")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Vijay Hospital (ID 3149) Overbilling:</b> Vijay Hospital exhibits an anomalous 34.00% deduction rate. One in three rupees claimed by this facility is rejected. However, the approved portion (₹22.25 Cr) slipped through without clinical verification, indicating high realized leakage.</div>
<div class="kf-item"><b>Park Hospital Chain Cumulative Impact:</b> With multiple empanelled facilities in the top deduction tiers (Gurgaon, Chowkhandi, Kailash), the Park Hospital chain represents the largest corporate audit target. Chain-level coordination warrants an empanelment review.</div>
</div>""")

# ── PATTERN 2: PING-PONG ADMISSIONS ───────────────────────────────────────────
if p09_pingpong:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 2 (BEHAVIORAL)</div>
  <div class="ph-ctx">Split-Package Anomalies<br/>(Readmission &lt; 48 Hours)</div>
  <div class="ph-title">Ping-Pong Admissions</div>
</div></div>
<p><b>Description:</b> This highly critical pattern flags "Ping-Ponging"—where a hospital discharges a patient only to readmit them within 48 hours for the same or related condition to bypass package cost boundaries. ECHS approved <b>₹60.03 Cr</b> on these readmissions due to lack of a temporal bundling check, resulting in 100% realized leakage.</p>
<div class="tc">Table 2.1 — Top Cases of Split-Package Readmissions (Within 48 Hrs)</div>
<table class="dt">
{th("Hospital Name","Patient Name","Admission 1","Discharge 1","Readmission (Adm 2)","Combined Claim (₹)")}
<tbody>''')
    for r in p09_pingpong[:15]:
        hname = safe(r.get("hospital_name",""))
        pname = safe(r.get("patient_name",""))
        admin1 = safe(r.get("admission_1",""))[:10]
        disch1 = safe(r.get("discharge_1",""))[:10]
        admin2 = safe(r.get("admission_2",""))[:10]
        claimed = float(r.get("claim_amt",0))
        
        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{pname[:20]}</td>"
                 f"<td>{admin1}</td><td>{disch1}</td><td><span style='color:#c0392b;font-weight:700'>{admin2}</span></td>"
                 f"<td>{fmt(claimed)}</td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Direct Evasion of Package Rules:</b> The 0-2 day gap signifies that patients were likely never physically discharged from the ward; only their paperwork was closed and reopened to trigger new package rates.</div>
</div>''')

# ── PATTERN 3: WEEKEND SURGE ABUSE ────────────────────────────────────────────
if p10_weekend:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 3 (BEHAVIORAL)</div>
  <div class="ph-ctx">The Friday Hustle<br/>(Abnormal Weekend Admissions)</div>
  <div class="ph-title">Weekend / Holiday Surge Admissions</div>
</div></div>
<p><b>Description:</b> Planned / elective procedures are deliberately admitted on Friday night or weekends when referral checks are closed, utilizing emergency bypass routes to skip vetting. ECHS successfully deducted <b>₹1,351.61 Cr</b> from weekend claims, but approved <b>₹3,097.47 Cr</b>, representing a massive realized leakage footprint.</p>
<div class="tc">Table 3.1 — Hospitals with Suspicious Weekend Admission Spikes</div>
<table class="dt">
{th("Hospital Name","City","Weekend Admissions","Total Claimed (₹ Cr)","Prevented (₹ Cr)","Realized (₹ Cr)")}
<tbody>''')
    for r in p10_weekend[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        admissions = safe(r.get("weekend_admissions",""))
        claimed = float(r.get("total_claimed_lakhs",0))/100
        deducted = float(r.get("total_deducted_lakhs",0))/100
        approved = claimed - deducted
        
        H.append(f"<tr><td><b>{hname[:40]}</b></td><td>{city}</td>"
                 f"<td><span style='color:#d4680a;font-weight:700'>{admissions}</span></td>"
                 f"<td>{claimed:.2f} Cr</td><td>{deducted:.2f} Cr</td><td><b style='color:#c0392b'>{approved:.2f} Cr</b></td></tr>")
    H.append('''</tbody></table>
</div>''')

# ── PATTERN 4: SUPERMAN SURGEON ──────────────────────────────────────────────
if p11_superman:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 4 (BEHAVIORAL)</div>
  <div class="ph-ctx">Doctor Cloning Fraud<br/>(> 15 Procedures / Day)</div>
  <div class="ph-title">Doctor Cloning (Superman Surgeon)</div>
</div></div>
<p><b>Description:</b> Physical impossibility. Hospitals bill for multiple surgical procedures under a single treating doctor's ID that exceeds 15 surgeries in a single 24-hour window. ECHS approved <b>₹5.66 Cr</b> on these impossible days, indicating surgeon name cloning.</p>
<div class="tc">Table 4.1 — Impossible Daily Surgical Volumes</div>
<table class="dt">
{th("Hospital Name","City","Treating Doctor","Date","Procedures In 1 Day","Claimed/Approved (₹ Lakhs)")}
<tbody>''')
    for r in p11_superman[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        doc = safe(r.get("doctor_name",""))
        date = safe(r.get("claim_date",""))
        surgeries = safe(r.get("surgeries_in_one_day",""))
        claimed = float(r.get("total_claimed_lakhs",0))
        
        H.append(f"<tr><td><b>{hname[:35]}</b></td><td>{city}</td><td>{doc[:25]}</td>"
                 f"<td>{date}</td><td><span style='color:#c0392b;font-weight:700'>{surgeries} Procedures</span></td>"
                 f"<td>{claimed:.2f} L</td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Doctor Identity Abuse:</b> Multiple hospitals used credentials of senior consultants to bill surgeries performed by junior staff or not performed at all. Pre-payment doctor volume limits would block this leakage.</div>
</div>''')

# ── PATTERN 5: THRESHOLD AVOIDING ────────────────────────────────────────────
if p12_threshold:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 5 (BEHAVIORAL)</div>
  <div class="ph-ctx">The ₹99,999 Trick<br/>(CFA Approval Evasion)</div>
  <div class="ph-title">Threshold Avoiding</div>
</div></div>
<p><b>Description:</b> Hospitals systematically submit bills priced exactly between ₹99,000 and ₹99,999. This allows them to bypass the strict Competent Financial Authority (CFA) manual vetting protocol which triggers at ₹1,00,000. ECHS approved <b>₹22.97 Cr</b> on these bypass claims.</p>
<div class="tc">Table 5.1 — Top Hospitals Exploiting the ₹99k Threshold</div>
<table class="dt">
{th("Hospital Name","City","Trick Bills Count","Total Claimed (₹ Lakhs)","Total Deducted (₹ Lakhs)","Realized Leakage (₹ Lakhs)")}
<tbody>''')
    for r in p12_threshold[:15]:
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        bills = safe(r.get("trick_bills_count",""))
        claimed = float(r.get("total_claimed_lakhs",0))
        deducted = float(r.get("total_deducted_lakhs",0))
        approved = claimed - deducted
        
        H.append(f"<tr><td><b>{hname[:40]}</b></td><td>{city}</td>"
                 f"<td><span style='color:#d4680a;font-weight:700'>{bills} Bills</span></td>"
                 f"<td>{claimed:.2f} L</td><td>{deducted:.2f} L</td><td><b style='color:#c0392b'>{approved:.2f} L</b></td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Systematic Split Billing:</b> The concentration of bills at exactly ₹99k identifies systematic procedural manipulation to avoid auditing checkpoints, leading to ₹22.97 Cr in slipped leakage.</div>
</div>''')

# ── PATTERN 6: BENEFICIARY CARD SHARING ───────────────────────────────────────
if p13_cardsharing:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 6 (IDENTITY)</div>
  <div class="ph-ctx">Same-Day Multi-Hospital Admission<br/>(Single Card ID)</div>
  <div class="ph-title">Individual Card Sharing</div>
</div></div>
<p><b>Description:</b> This flags cases where the exact same beneficiary card was used to admit patients at two different, geographically distant hospitals on the same day. ECHS approved <b>₹4.82 Cr</b> on these claims without detecting that a single card was physically present in two locations simultaneously, resulting in 100% realized leakage.</p>
<div class="tc">Table 6.1 — Same-Day Card Sharing Across Different Hospitals</div>
<table class="dt">
{th("Card ID","Beneficiary Name","Admission Date","Hospital 1","Hospital 2","Appr Amt 1 (₹)","Appr Amt 2 (₹)","Total Approved (₹)")}
<tbody>''')
    for r in p13_cardsharing[:15]:
        card = safe(r.get("card_id",""))
        name = safe(r.get("beneficiary_name",""))
        date = safe(r.get("admission_date",""))[:10]
        h1 = safe(r.get("hospital_1",""))
        h2 = safe(r.get("hospital_2",""))
        amt1 = float(r.get("approved_amt_1",0))
        amt2 = float(r.get("approved_amt_2",0))
        tot = float(r.get("total_approved",0))
        
        H.append(f"<tr><td><b>{card}</b></td><td>{name[:20]}</td><td>{date}</td>"
                 f"<td>{h1[:25]}</td><td>{h2[:25]}</td>"
                 f"<td>{fmt(amt1)}</td><td>{fmt(amt2)}</td>"
                 f"<td><b style='color:#c0392b'>{fmt(tot)}</b></td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Identity Theft & Impersonation:</b> These records prove that cards were shared among non-eligible friends/relatives or cloned by hospitals to bill for dummy patients. Implementing real-time card validation would prevent this leakage.</div>
</div>''')

# ── PATTERN 7: FAMILY CARD SHARING ──────────────────────────────────────────
if p14_familysharing:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 7 (IDENTITY)</div>
  <div class="ph-ctx">Simultaneous Dependant Abuse<br/>(Same Service No, Different Cards)</div>
  <div class="ph-title">Family Card Sharing</div>
</div></div>
<p><b>Description:</b> This flags cases where multiple family members under the same Service Number were admitted to different hospitals on the exact same day for high-value treatments. ECHS approved <b>₹8.44 Cr</b> on these simultaneous family admissions.</p>
<div class="tc">Table 7.1 — Same-Day Family Admissions Across Different Hospitals</div>
<table class="dt">
{th("Service No","Member 1 &amp; Relation","Member 2 &amp; Relation","Admission Date","Hospital 1","Hospital 2","Approved 1 (₹)","Approved 2 (₹)","Total Approved (₹)")}
<tbody>''')
    for r in p14_familysharing[:15]:
        sno = safe(r.get("service_no",""))
        m1 = f"{safe(r.get('member_1',''))[:15]} ({safe(r.get('relation_1',''))})"
        m2 = f"{safe(r.get('member_2',''))[:15]} ({safe(r.get('relation_2',''))})"
        date = safe(r.get("admission_date",""))[:10]
        h1 = safe(r.get("hospital_1",""))
        h2 = safe(r.get("hospital_2",""))
        amt1 = float(r.get("approved_amt_1",0))
        amt2 = float(r.get("approved_amt_2",0))
        tot = float(r.get("total_approved",0))
        
        H.append(f"<tr><td><b>{sno}</b></td><td>{m1}</td><td>{m2}</td><td>{date}</td>"
                 f"<td>{h1[:20]}</td><td>{h2[:20]}</td>"
                 f"<td>{fmt(amt1)}</td><td>{fmt(amt2)}</td>"
                 f"<td><b style='color:#c0392b'>{fmt(tot)}</b></td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Collusive Family Abuse:</b> Simultaneous admission of multiple dependants at distant hospitals indicates organized card sharing or collusive billing by local healthcare providers.</div>
</div>''')

# ── PATTERN 8: DEMOGRAPHIC & RELATION MISMATCH ────────────────────────────────
if p15_demographic:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 8 (IDENTITY)</div>
  <div class="ph-ctx">Gender &amp; Relation Conflicts<br/>(e.g., Male registered as Wife)</div>
  <div class="ph-title">Demographic &amp; Relationship Mismatch</div>
</div></div>
<p><b>Description:</b> This identifies claims containing direct, impossible conflicts between the patient's gender and their registered relationship to the primary beneficiary (e.g. patients marked Male but with relationship 'Wife' or 'Mother'). ECHS approved <b>₹37.99 Cr</b> across 17,205 claims of this type.</p>
<div class="tc">Table 8.1 — Top High-Value Claims with Gender-Relationship Conflicts</div>
<table class="dt">
{th("Gender","Relationship","Hospital Name","City","Patient Name","Adm Date","Claimed (₹)","Approved (₹)","Deducted (₹)")}
<tbody>''')
    for r in p15_demographic[:15]:
        g = safe(r.get("gender",""))
        rel = safe(r.get("relationship",""))
        hname = safe(r.get("hospital_name",""))
        city = safe(r.get("city",""))
        pname = safe(r.get("patient_name",""))
        date = safe(r.get("admission_date",""))[:10]
        claimed = float(r.get("claimed_amount",0))
        approved = float(r.get("approved_amount",0))
        deducted = float(r.get("deducted_amount",0))
        
        H.append(f"<tr><td><b>{g}</b></td><td>{rel}</td><td>{hname[:25]}</td><td>{city}</td>"
                 f"<td>{pname[:15]}</td><td>{date}</td>"
                 f"<td>{fmt(claimed)}</td><td><b style='color:#c0392b'>{fmt(approved)}</b></td><td>{fmt(deducted)}</td></tr>")
    H.append('''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Falsified Profiles &amp; Lax Auditing:</b> These claims were processed and approved despite obvious data contradictions, pointing to a severe loophole in both pre-auth verification and claim processing workflows.</div>
</div>''')

H.append(f"""
<div class="pb">
<h1 style="margin-top:20px; margin-bottom:14px;">Consolidated Summary</h1>
<div class="tc">Overall Final Audit Findings (System-Wide Extract)</div>
<table class="dt">
{th("Category / Forensic Pattern","Flagged Cases","Claimed Amount","Prevented Leakage (Deductions)","Realized Leakage (Approved)","Realized Leakage %")}
<tbody>
  <tr><td><b>Pattern 1 (Corporate Overbilling)</b></td><td>{fmt(total_claims_top)} Claims</td><td>{cr(total_claimed_top/100)}</td><td>{cr(total_deducted_top/100)}</td><td>{cr(total_approved_top/100)}</td><td>{(total_approved_top/total_claimed_top*100):.2f}%</td></tr>
  <tr><td><b>Pattern 2 (Ping-Pong Admissions)</b></td><td>500 Cases</td><td>&#8377;60.03 Cr</td><td>&#8377;0.00 Cr</td><td>&#8377;60.03 Cr</td><td>100.00%</td></tr>
  <tr><td><b>Pattern 3 (Weekend Surges)</b></td><td>1,320,346 Cases</td><td>&#8377;4,449.07 Cr</td><td>&#8377;1,351.61 Cr</td><td>&#8377;3,097.47 Cr</td><td>69.62%</td></tr>
  <tr><td><b>Pattern 4 (Superman Surgeon)</b></td><td>17,374 Surgeries</td><td>&#8377;6.56 Cr</td><td>&#8377;0.00 Cr</td><td>&#8377;6.56 Cr</td><td>100.00%</td></tr>
  <tr><td><b>Pattern 5 (Threshold Avoiding)</b></td><td>2,856 Bills</td><td>&#8377;28.42 Cr</td><td>&#8377;5.44 Cr</td><td>&#8377;22.97 Cr</td><td>80.82%</td></tr>
  <tr><td><b>Pattern 6 (Individual Card-Sharing)</b></td><td>284 Cases</td><td>&#8377;4.82 Cr</td><td>&#8377;0.00 Cr</td><td>&#8377;4.82 Cr</td><td>100.00%</td></tr>
  <tr><td><b>Pattern 7 (Family Card-Sharing)</b></td><td>125 Cases</td><td>&#8377;8.44 Cr</td><td>&#8377;0.00 Cr</td><td>&#8377;8.44 Cr</td><td>100.00%</td></tr>
  <tr><td><b>Pattern 8 (Demographic Mismatch)</b></td><td>17,205 Claims</td><td>&#8377;37.99 Cr</td><td>&#8377;0.00 Cr</td><td>&#8377;37.99 Cr</td><td>100.00%</td></tr>
  <tr style="background:#1a2744;color:#fff;">
    <td><b style="color:#fff;">Total Classified Realized Leakage</b></td>
    <td style="color:#fff;">1,358,281 Cases</td>
    <td style="color:#fff;">&#8377;4,617.58 Cr</td>
    <td style="color:#fff;">&#8377;1,392.57 Cr</td>
    <td style="color:#fff;">&#8377;3,225.01 Cr</td>
    <td style="color:#fff;">9.88% (Slippage Rate)</td>
  </tr>
</tbody>
</table>
<div style="border-top:1px solid #e2e8f0; margin-top:24px; padding-top:16px; text-align:center;">
  <p style="font-size:7.5pt; color:#718096; font-weight:600; margin-bottom:4px; letter-spacing:0.5px;">Note: Dataset contains synthetic/shifted dates extending into FY2026 for predictive modeling purposes.<br/>PREPARED BY IIT KANPUR — DATA ANALYTICS &amp; BILLING FORENSICS DIVISION</p>
  <p style="font-size:7pt; color:#a0aec0;">Generated on {today_str} | Confidential &amp; Restricted Distribution</p>
</div>
</div>
""")

H.append("</body></html>")

# ── RENDER ────────────────────────────────────────────────────────────────────
full_html = "\n".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Saved → {PDF_OUT}")
print(f"   Total cases: {fmt(kpi_total_claims)}")
print(f"   Exposure   : {cr(kpi_deducted_cr)}")
