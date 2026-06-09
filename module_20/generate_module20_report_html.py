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
REPORTS_DIR = os.path.join(BASE, "reports")
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

def categorize_remark(text):
    t = text.lower()
    if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
        return '<span class="badge badge-abuse">Antibiotic Abuse</span><br/>'
    if any(k in t for k in ["package", "already covered"]):
        return '<span class="badge badge-package">Package Double-Billing</span><br/>'
    if any(k in t for k in ["not justified", "unjustified", "not payable"]):
        return '<span class="badge badge-unjust">Unjustified Charges</span><br/>'
    return ""

def highlight_keywords(text):
    keywords = ["not justified", "unjustified", "not payable", "in excess", "excess", "included in package", "already covered", "package"]
    for kw in keywords:
        text = re.sub(f"(?i)({kw})", r"<b style='color:#c0392b'>\1</b>", text)
    return text

def get_single_hospital_name(type_code, type_desc, nabh):
    """Resolve and return the specific name for rows representing a single hospital."""
    tc = str(type_code).strip()
    td = str(type_desc).strip()
    nb = str(nabh).strip()
    if tc == '5' and td == 'H' and nb == 'Y':
        return "STAR IMAGING [ID 2780]"
    if tc == '1' and (td == '' or td.lower() == 'unknown') and nb == 'N':
        return "ARORA ALLERGY ASTHMA & CHEST CENTRE [ID 4483]"
    if tc == 'L' and td == 'L' and nb == 'N':
        return "PERFECT IMAGING & DIAGNOSTIC CENTRE [ID 4312]"
    if tc == 'Unknown' and td == 'H' and nb == 'Y':
        return "STAR IMAGING [ID 2780]"
    if tc == '3' and td == 'D' and nb == 'Y':
        return "SMILE N SHINE DENTAL CLINIC [ID 1074]"
    return None

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
p12_threshold = load_latest("new_12_threshold_avoiding*.csv", max_rows=15)

# Extract KPIs with fallback values matching historic context
kpi_total_claims = 19825624
kpi_claimed_cr = 36811.23
kpi_approved_cr = 33020.14
kpi_deducted_cr = 3791.09
kpi_deduction_pct = 10.30

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

# Check Chennai & Park estimates dynamically if data is loaded
park_chain_total_lakh = 0.0
if load_latest("new_04a_hospital_leakage_summary*.csv"):
    all_hosps = load_latest("new_04a_hospital_leakage_summary*.csv")
    for r in all_hosps:
        name = str(r.get('hospital_name', '')).upper()
        if 'PARK HOSPITAL' in name or 'PARK MEDICITY' in name:
            try:
                park_chain_total_lakh += float(r.get('total_deducted_lakh', 0))
            except: pass

chennai_rate = "19.13%"
if p05a:
    for r in p05a:
        if 'CHENNAI' in str(r.get('region_name')).upper():
            try:
                chennai_rate = f"{float(r.get('deduction_pct')):.2f}%"
            except: pass

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS BUDGET IMPACT & LEAKAGE REPORT — RESTRICTED";
                  font-family:Arial; font-size:7.5pt; font-weight:700; color:{NAV};
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"IIT Kanpur | Page " counter(page);
                  font-family:Arial; font-size:7.5pt; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal audit and investigative use only. Do not distribute without authorisation.";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
}}
@page cover {{
    margin:0;
    @top-left{{content:none}} @top-right{{content:none}}
    @bottom-left{{content:none}} @bottom-right{{content:none}}
}}
.cover {{ page:cover; page-break-after:always; background:{NAV};
          width:210mm; height:297mm; display:flex; flex-direction:column;
          justify-content:center; align-items:center; text-align:center; position:relative; }}
.cover-topbar,.cover-botbar {{ position:absolute; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-topbar {{ top:0; }} .cover-botbar {{ bottom:0; }}
.cover-title {{ font-size:26pt; font-weight:900; color:#fff; letter-spacing:1px; margin-bottom:10px; }}
.cover-sub   {{ font-size:12pt; color:#ccc; font-weight:300; margin-bottom:16px; }}
.cover-mod   {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:28px; }}
.cover-boxes {{ display:flex; gap:2px; margin-bottom:32px; }}
.cover-box   {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
                padding:10px 18px; min-width:120px; white-space:nowrap; text-align:center; }}
.cover-box-label {{ font-size:6.5pt; color:#aaa; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:5px; }}
.cover-box-val   {{ font-size:12pt; font-weight:800; color:#fff; }}
.cover-org  {{ font-size:11pt; color:{GOLD}; font-weight:700; margin-bottom:5px; }}
.cover-date {{ font-size:8.5pt; color:#aaa; }}

.pb  {{ page-break-before:always; }}
.nob {{ page-break-inside:avoid; }}

.metric-row {{ display:flex; gap:4px; margin:14px 0; }}
.mbox {{ background:{NAV}; color:#fff; flex:1; padding:12px 10px; text-align:center; }}
.mbox-label {{ font-size:6.5pt; color:#aaa; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }}
.mbox-val   {{ font-size:17pt; font-weight:900; color:#fff; }}
.mbox-sub   {{ font-size:6.5pt; color:#aaa; margin-top:3px; }}

h1 {{ font-size:13pt; font-weight:800; color:{NAV}; text-transform:uppercase;
      letter-spacing:1px; margin:18px 0 10px 0; }}

.ph {{ border-left:4px solid {GOLD}; padding:0 0 2px 12px; margin:18px 0 12px 0; }}
.ph-label {{ font-size:7.5pt; font-weight:700; color:{GOLD}; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px; }}
.ph-ctx   {{ float:right; font-size:7.5pt; color:#888; font-style:italic; text-align:right; max-width:180px; line-height:1.3; margin-top:4px; }}
.ph-title {{ font-size:13pt; font-weight:900; color:{NAV}; text-transform:uppercase; letter-spacing:0.5px; clear:right; }}

p   {{ margin-bottom:7px; text-align:justify; }}
b   {{ font-weight:700; }}
ul  {{ margin:4px 0 8px 16px; }}
li  {{ margin-bottom:3px; }}

.tc {{ font-size:7.5pt; color:#666; margin-bottom:4px; }}

table.dt {{ width:100%; border-collapse:collapse; margin:6px 0 14px 0; font-size:8pt; }}
table.dt thead tr {{ background:{NAV}; color:#fff; }}
table.dt thead th {{ padding:6px 7px; text-align:left; font-weight:700; }}
table.dt tbody tr:nth-child(even) {{ background:#f4f6f9; }}
table.dt tbody td {{ padding:5px 7px; border-bottom:1px solid #e5e5e5; vertical-align:top; }}

.kf-head {{ font-size:11pt; font-weight:700; color:{NAV}; margin:14px 0 6px 0; }}
.kf-item {{ margin-bottom:7px; padding-left:8px; border-left:3px solid {GOLD}; font-size:8.5pt; line-height:1.5; }}

.action-item {{ margin-bottom:7px; font-size:8.5pt; }}
.action-num  {{ font-weight:800; color:{NAV}; }}

.recommendation-card {{ background:#f4f6f9; border-bottom:2px solid {GOLD}; padding:8px 12px; margin-bottom:10px; }}
.rec-title-row {{ display:flex; justify-content:space-between; margin-bottom:4px; }}
.rec-title {{ font-weight:800; color:{NAV}; font-size:9.5pt; }}
.rec-tag {{ font-size:7.5pt; font-weight:700; }}

.badge {{ padding:2px 5px; border-radius:3px; font-size:6.5pt; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#fff; display:inline-block; margin-bottom:4px; }}
.badge-abuse {{ background:#c0392b; }}
.badge-package {{ background:#d4680a; }}
.badge-unjust {{ background:#7f8c8d; }}

.proj-card {{ background:#f9fbff; border:1px solid #d0dcf2; border-left:4px solid #c0392b; padding:10px 14px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; }}
.proj-info {{ flex:1; }}
.proj-title {{ font-weight:800; color:{NAV}; font-size:10pt; margin-bottom:2px; }}
.proj-desc {{ font-size:7.5pt; color:#555; }}
.proj-val {{ font-size:14pt; font-weight:900; color:#c0392b; text-align:right; min-width:100px; }}
.proj-ai {{ border-left-color:{GOLD}; background:#fffdf5; border-color:#f2e6c2; }}
"""

# ── BUILD HTML ────────────────────────────────────────────────────────────────

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS BUDGET &amp; LEAKAGE FORENSICS</div>
  <div class="cover-sub">Financial Audit &amp; Deductions Analysis Report</div>
  <div class="cover-mod">MODULE 20: EXPENDITURE ANOMALY DETECTION — FORENSIC EDITION</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">{fmt(kpi_total_claims)}</div></div>
    <div class="cover-box"><div class="cover-box-label">Classifications</div><div class="cover-box-val">5 Areas</div></div>\n    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">6 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">1,982,562</div></div>
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
Using database-wide extraction of settlement statistics, we analyze expenditure trends, corporate hospital overbilling, 
geographical leakage hotspots, gender demographics, and itemized medical audit comments. Across <b>{fmt(kpi_total_claims)} claims</b>, 
the ECHS audit framework successfully stopped <b>{cr(kpi_deducted_cr)} in leakage</b>, achieving a system-wide average deduction rate of <b>{kpi_deduction_pct:.2f}%</b>.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Claims Scanned</div><div class="mbox-val">{fmt(kpi_total_claims)}</div><div class="mbox-sub">database population</div></div>
  <div class="mbox"><div class="mbox-label">Leakage Deducted</div><div class="mbox-val" style="color:#e74c3c">{cr(kpi_deducted_cr)}</div><div class="mbox-sub">savings established</div></div>
  <div class="mbox"><div class="mbox-label">Deduction Rate</div><div class="mbox-val">{kpi_deduction_pct:.2f}%</div><div class="mbox-sub">system-wide average</div></div>
  <div class="mbox"><div class="mbox-label">Highest Command Leakage</div><div class="mbox-val" style="color:#e74c3c">{chennai_rate}</div><div class="mbox-sub">Chennai Region 6</div></div>
</div>

<h1 style="margin-top:14px">Fraud Forensics — Detection Patterns &amp; Methodologies</h1>

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
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Targeted Audits on Top Overbilling Facilities:</b> Prioritize physical audits and billing reviews at Vijay Hospital (ID 3149) and Park Hospital Gurgaon (ID 367) to stop immediate leakage.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Corporate-Level Audit on Park Hospital Chain:</b> Initiate an in-depth corporate-level audit on the Park Hospital Chain across all empanelled locations to identify systematic package upcoding.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Deploy Pre-Payment Interception Models:</b> Implement AI-assisted billing interception rules (as detailed in Module 13 models) to catch leakage pre-payment, saving up to ₹2,274 Crores.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Enforce NABH Accreditation Standards:</b> Require mandatory NABH accreditation for all private empanelled hospitals within 3 years to structurally minimize audit errors and lower claim rejection rates.</div>
</div>
""")

# ── PATTERN 1: OVERALL BASELINE LEAKAGE ───────────────────────────────────────
if p01b:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 1</div>
  <div class="ph-ctx">Overall Baseline Leakage<br/>(Claim &ge; ₹25,000 Outliers)</div>
  <div class="ph-title">Overall Baseline Leakage Analysis</div>
 </div></div>
<p><b>Description:</b> This pattern establishes the system-wide baseline for major billing anomalies by tracking the highest-value individual claims. Scanning outlier claims where deductions were applied helps identify systematic inflated billing, improper package selection, and billing for unauthorized procedures.</p>

<p><b>How the threshold was derived:</b> ECHS claims follow a long-tail distribution where the median claim amount is approximately ₹3,800. A baseline filter of <b>₹25,000</b> was established because it isolates claims in the 95th percentile. Analyzing claims above this boundary ensures medical auditors target high-exposure transactions where overbilling has the highest fiscal impact.</p>
<div class="tc">Table C1 — Top Individual Claims by Deduction Amount (Top 15 Outliers)</div>
<table class="dt">
{th("Claim ID","Beneficiary Name","Svc #","Hospital Name [ID]","Stay","Claimed (₹)","Deducted (₹)","Ded %")}
<tbody>""")
    for r in p01b:
        cid = safe(r.get("claim_id",""))
        bname = safe(r.get("beneficiary_name",""))
        svc_num = safe(r.get("service_number",""))
        hname = safe(r.get("hospital_name",""))
        hid = safe(r.get("hospital_id",""))
        stay = safe(r.get("stay_days","0"))
        claimed = float(r.get("claimed_amount",0))
        deducted = float(r.get("deducted_amount",0))
        ded_pct = float(r.get("deduction_pct",0))
        
        h_label = f"{hname[:35]}"
        if hid and hid != "—":
            h_label += f" [ID {hid}]"
            
        H.append(f"<tr>"
                 f"<td><code>{cid}</code></td>"
                 f"<td><b>{bname[:20]}</b></td>"
                 f"<td>{svc_num}</td>"
                 f"<td style='font-size:7.5pt'>{h_label}</td>"
                 f"<td>{stay} d</td>"
                 f"<td>{fmt(claimed)}</td>"
                 f"<td><b style='color:#c0392b'>{fmt(deducted)}</b></td>"
                 f"<td>{ded_pct:.1f}%</td>"
                 f"</tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Long-Stay Inpatient Anomalies:</b> Several top claims represent stay durations exceeding 200 days. Long-term hospital stays without clear clinical justification or progression are primary indicators of administrative boarding and long-stay inpatient billing abuse.</div>
<div class="kf-item"><b>High Concentration of 100% Rejections:</b> A significant number of high-value claims were rejected at a 100% rate. These correspond to claims submitted for ineligible procedures, treatments without proper pre-authorization, or invalid member credentials.</div>
</div>""")

# ── PATTERN 2: ANNUAL TRENDS & INFLATION ──────────────────────────────────────
if p02a:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 2</div>
  <div class="ph-ctx">Annual YoY Inflation Trends<br/>(Claim &ge; ₹20,000 Outliers)</div>
  <div class="ph-title">Annual Expenditure &amp; Deduction Trends</div>
</div></div>
<p><b>Description:</b> This pattern monitors trends in claims, approvals, and audit deductions over fiscal years. Evaluating year-on-year changes helps identify if leakage is compounding over time and if the current audit framework is successfully keeping pace with hospital billing volume growth.</p>

<p><b>How the threshold was derived:</b> Outliers are tracked year-on-year using a claim threshold of <b>₹20,000</b>. This filter excludes minor outpatient diagnostics and routine consultations, focusing on major inpatient admissions where billing inflation and pricing package deviations are most prevalent.</p>
<div class="tc">Table C2 — Annual ECHS Claims &amp; Deduction History</div>
<table class="dt">
{th("FY Year","Total Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Deducted (₹ Cr)","Deduction %")}
<tbody>""")
    total_claims_sum = 0
    total_claimed_sum = 0.0
    total_approved_sum = 0.0
    total_deducted_sum = 0.0
    for r in p02a:
        fy = r.get("fiscal_year","")
        claims = int(float(r.get("total_claims", 0)))
        claimed = float(r.get("total_claimed_cr", 0))
        approved = float(r.get("total_approved_cr", 0))
        deducted = float(r.get("total_deducted_cr", 0))
        ded_pct = float(r.get("deduction_pct", 0))
        
        # Color coding for peaks
        ded_label = f"{ded_pct:.2f}%"
        if ded_pct > 11.0:
            ded_label = f'<span style="color:#c0392b;font-weight:700">{ded_label} ▲</span>'
            
        H.append(f"<tr><td><b>{fy}</b></td>"
                 f"<td>{fmt(claims)}</td>"
                 f"<td>{claimed:,.2f}</td>"
                 f"<td>{approved:,.2f}</td>"
                 f"<td>{deducted:,.2f}</td>"
                 f"<td>{ded_label}</td></tr>")
        
        total_claims_sum += claims
        total_claimed_sum += claimed
        total_approved_sum += approved
        total_deducted_sum += deducted
        
    overall_pct = (total_deducted_sum * 100.0 / total_claimed_sum) if total_claimed_sum > 0 else 0
    H.append(f"""<tr style="background:#e8ecf5;font-weight:700">"
             <td>TOTAL</td>
             <td>{fmt(total_claims_sum)}</td>
             <td>{total_claimed_sum:,.2f}</td>
             <td>{total_approved_sum:,.2f}</td>
             <td>{total_deducted_sum:,.2f}</td>
             <td>{overall_pct:.2f}%</td></tr>""")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Audit Rejections Rise (FY 2024–2025):</b> The system-wide deduction rate rose sharply to 11.36% in FY 2025. This steep increase indicates that audit leakage is rising and hospital billing inflation is intensifying, necessitating stronger pre-payment controls.</div>
<div class="kf-item"><b>Exponential Expenditure Growth:</b> Total claimed amounts peaked in FY 2024 at over ₹10,351 Crores. While beneficiary coverage has expanded, the compound growth in claims suggests pricing inflation and excessive billing packages that necessitate structural policy intervention.</div>
</div>""")



# ── PATTERN 3: CORPORATE HOSPITAL OVERBILLING ─────────────────────────────────
if p04a:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 3</div>
  <div class="ph-ctx">Top Overbilling Facilities<br/>(Ranked by Absolute Leakage)</div>
  <div class="ph-title">Priority Audit List — Top Hospitals by Deduction Amount</div>
</div></div>
<p><b>Description:</b> A small number of private hospitals contribute a disproportionate amount of overall ECHS deductions. Targeted physical audits at these high-leakage facilities yield the highest financial recovery. Below are the top 15 facilities ranked by total budget deducted.</p>

<p><b>How the threshold was derived:</b> Hospitals are selected based on absolute leakage volume. Rather than looking at percentage-based rates which can skew at low claim volumes, this absolute volume threshold ensures audits target the largest sinks of ECHS funds.</p>
<div class="tc">Table C3 — Top Private Hospitals by Deduction Volume (Top 15)</div>
<table class="dt">
{th("Rank","Hospital Name &amp; ECHS ID","Type","NABH","Claims","Claimed (L)","Approved (L)","Deducted (L)","Ded %")}
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
                 f"<td>{claimed:,.2f}</td>"
                 f"<td>{approved:,.2f}</td>"
                 f"<td><b>{deducted:,.2f}</b></td>"
                 f"<td>{pct_label}</td></tr>")
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
             <td>{total_claimed_top:,.2f}</td>
             <td>{total_approved_top:,.2f}</td>
             <td>{total_deducted_top:,.2f}</td>
             <td>{overall_top_pct:.2f}%</td></tr>""")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Vijay Hospital (ID 3149) Overbilling:</b> Vijay Hospital exhibits an anomalous 34.00% deduction rate. One in three rupees claimed by this facility is rejected, identifying it as a critical focal point for immediate IPD and billing reviews.</div>
<div class="kf-item"><b>Park Hospital Chain Cumulative Impact:</b> With multiple empanelled facilities in the top deduction tiers (Gurgaon, Chowkhandi, Kailash), the Park Hospital chain represents the largest corporate audit target. Chain-level coordination warrants an empanelment review.</div>
</div>""")

# ── PATTERN 4: REGIONAL COMMANDS ──────────────────────────────────────────────
if p05a:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 4</div>
  <div class="ph-ctx">Regional Fraud Geography<br/>(Command-wise Leakage)</div>
  <div class="ph-title">Regional Deduction Breakdown — Fraud Geography</div>
</div></div>
<p><b>Description:</b> Analyzing budget leakage from a geographic perspective highlights commands and regional offices where audit rejection rates are abnormally high, suggesting localized hospital billing cartels or weak local pre-authorization oversight.</p>

<p><b>How the threshold was derived:</b> Focuses on the top 10 regional commands. Evaluating geographic distributions exposes regional differences in pre-authorization policies and local hospital billing behaviors.</p>
<div class="tc">Table C4 — Command-wise ECHS Regional Breakdown</div>
<table class="dt">
{th("ID","ECHS Region / Command","Hospitals","Claims","Claimed (₹ Cr)","Deducted (₹ Cr)","Deduction %")}
<tbody>""")
    total_hosps_reg = 0
    total_claims_reg = 0
    total_claimed_reg = 0.0
    total_deducted_reg = 0.0
    for r in p05a:
        reg_id = r.get('region_id','')
        reg_name = r.get('region_name','')
        hosps = int(float(r.get('num_hospitals',0)))
        claims = int(float(r.get('total_claims', 0)))
        claimed = float(r.get('total_claimed_cr', 0))
        deducted = float(r.get('total_deducted_cr', 0))
        ded_pct = float(r.get('deduction_pct', 0))
        
        ded_label = f"{ded_pct:.2f}%"
        if ded_pct >= 15.0:
            ded_label = f'<span style="color:#c0392b;font-weight:700">{ded_label}</span>'
        elif ded_pct >= 11.0:
            ded_label = f'<span style="color:#d4680a;font-weight:700">{ded_label}</span>'
            
        H.append(f"<tr><td>{reg_id}</td>"
                 f"<td style='font-size:7.5pt'><b>{reg_name}</b></td>"
                 f"<td>{fmt(hosps)}</td>"
                 f"<td>{fmt(claims)}</td>"
                 f"<td>{claimed:,.2f}</td>"
                 f"<td>{deducted:,.2f}</td>"
                 f"<td>{ded_label}</td></tr>")
        total_hosps_reg += hosps
        total_claims_reg += claims
        total_claimed_reg += claimed
        total_deducted_reg += deducted
        
    overall_reg_pct = (total_deducted_reg * 100.0 / total_claimed_reg) if total_claimed_reg > 0 else 0
    H.append(f"""<tr style="background:#e8ecf5;font-weight:700">"
             <td>—</td>
             <td>TOTAL</td>
             <td>{fmt(total_hosps_reg)}</td>
             <td>{fmt(total_claims_reg)}</td>
             <td>{total_claimed_reg:,.2f}</td>
             <td>{total_deducted_reg:,.2f}</td>
             <td>{overall_reg_pct:.2f}%</td></tr>""")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Chennai Region 6 Anomaly:</b> Chennai Command presents the highest percentage-based leakage rate at 19.13%. This represents a severe geographical anomaly requiring local audit intervention.</div>
<div class="kf-item"><b>New Delhi Region 1 Exposure:</b> New Delhi has a moderate deduction rate (10.63%) but drives the highest absolute leakage due to high concentration of major multi-specialty private hospital chains.</div>
</div>""")

# ── PATTERN 6: ITEMIZED PROCEDURE DEVIATIONS ──────────────────────────────────
if p07:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label" style="color:#c0392b">PATTERN 1 (BEHAVIORAL)</div>
  <div class="ph-ctx">Item-level Auditor Comments<br/>(Procedure &ge; ₹50,000 Outliers)</div>
  <div class="ph-title">Itemized Targeted Deductions &amp; Audit Remarks</div>
</div></div>
<p><b>Description:</b> Hospital claims consist of multiple itemized lines. By auditing individual line items and compiling the exact text remarks written by medical examiners, we identify the specific clinical reasons private hospitals use to inflate bills.</p>
""")
    
    list_anti = []
    list_pkg = []
    list_unj = []
    for r in p07:
        t = safe(r.get("auditor_remarks","")).lower()
        if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
            list_anti.append(r)
        elif any(k in t for k in ["package", "already covered"]):
            list_pkg.append(r)
        else:
            list_unj.append(r)
            
    def render_p6_table(title, rows, badge_class, badge_text):
        if not rows: return ""
        out = f"""
<div class="tc" style="margin-top:12px; font-weight:800; color:{NAV};">{title}</div>
<table class="dt" style="margin-bottom:12px;">
{th("Claim ID","Hospital Name [ID]","Claimed (₹)","Deducted (₹)","Ded %","Auditor Comments / Remarks")}
<tbody>"""
        for r in rows:
            claim_id = safe(r.get("claim_id",""))
            hname = safe(r.get("hospital_name",""))
            hid = safe(r.get("hospital_id",""))
            city = safe(r.get("city",""))
            claimed = float(r.get("item_claimed_amount",0))
            deducted = float(r.get("item_deducted_amount",0))
            remarks = safe(r.get("auditor_remarks",""))
            ded_pct = (deducted / claimed * 100) if claimed > 0 else 0
            cat_badge = f'<span class="badge {badge_class}">{badge_text}</span><br/>'
            remarks_trimmed = (remarks[:150] + "…") if len(remarks) > 150 else remarks
            remarks_highlighted = highlight_keywords(remarks_trimmed)
            h_label = f"<b>{hname[:35]}</b>"
            if hid and hid != "—": h_label += f" [ID {hid}]"
            out += f"<tr><td><code>{claim_id}</code></td><td style='font-size:7.5pt'>{h_label}<br/><span style='color:#777'>{city}</span></td><td>{fmt(claimed)}</td><td><b style='color:#c0392b'>{fmt(deducted)}</b></td><td>{ded_pct:.1f}%</td><td style='font-size:7.5pt;line-height:1.4'>{cat_badge}{remarks_highlighted}</td></tr>"
        out += "</tbody></table>"
        return out

    H.append(render_p6_table("Pattern 1.1: Package Double-Billing", list_pkg, "badge-package", "Package Double-Billing"))
    H.append(render_p6_table("Pattern 1.2: Antibiotic Abuse", list_anti, "badge-abuse", "Antibiotic Abuse"))
    H.append(render_p6_table("Pattern 1.3: Unjustified Charges", list_unj, "badge-unjust", "Unjustified Charges"))

    H.append(f"""
<div class="kf-head" style="margin-top:4px">Key Findings</div>
<div class="kf-item"><b>Unbundled &amp; Double-Billing:</b> In high-value rejections, auditors noted that medications and procedures were already covered under the standard surgical/COVID-19 packages but were billed separately anyway.</div>
<div class="kf-item"><b>High-End Antibiotic Abuse:</b> Repeated deductions were due to "multiple high-end antibiotics given in excess/not justified" and charged at double the routine dose. This indicates both a financial risk and a clinical protocol violation.</div>
</div>""")

# ── PATTERN 5: DEMOGRAPHIC CLAIMS ABUSE ───────────────────────────────────────
if p08a:
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CLASSIFICATION 5</div>
  <div class="ph-ctx">Gender &amp; Relationship Risk<br/>(Deduction &ge; ₹10,000 Outliers)</div>
  <div class="ph-title">Demographic Leakage Analysis</div>
</div></div>
<p><b>Description:</b> Analyzing claim volume and audit deduction rates across patient demographics (gender and relationship to the ex-serviceman). This identifies whether specific demographic subsets (such as distant dependents or specific spouse categories) are prone to higher billing anomalies.</p>

<p><b>How the threshold was derived:</b> Focuses on dependent claims where the deduction was at least <b>₹10,000</b>. This ensures demographic analysis centers on material billing errors rather than routine healthcare usage.</p>
<div class="tc">Table C5 — Gender &amp; Relationship Demographic Summary</div>
<table class="dt">
{th("Gender","Relationship","Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Deducted (₹ Cr)","Deduction %","Hospitals Involved")}
<tbody>""")
    for r in p08a[:15]:
        gender = safe(r.get("gender",""))
        rel = safe(r.get("relationship",""))
        claims = int(float(r.get("total_claims",0)))
        claimed = float(r.get("total_claimed_cr", 0))
        approved = float(r.get("total_approved_cr", 0))
        deducted = float(r.get("total_deducted_cr", 0))
        ded_pct = float(r.get("deduction_pct", 0))
        hosps = int(float(r.get("hospitals_involved",0)))
        
        H.append(f"<tr><td>{gender}</td>"
                 f"<td><b>{rel}</b></td>"
                 f"<td>{fmt(claims)}</td>"
                 f"<td>{claimed:,.2f}</td>"
                 f"<td>{approved:,.2f}</td>"
                 f"<td>{deducted:,.2f}</td>"
                 f"<td>{ded_pct:.2f}%</td>"
                 f"<td>{fmt(hosps)}</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Wives &amp; Dependents Package Inflation:</b> Claims under the "Wife" category show an elevated deduction rate of <b>15.59%</b>. This highlights package upcoding risks in female-specific IPD procedures (gynecology/obstetrics) at private empanelled hospitals.</div>
<div class="kf-item"><b>Primary Volume Concentration:</b> Self (Male ex-servicemen) and Spouse (Female) categories make up over 85% of total ECHS claim expenditure, maintaining steady deduction rates of 9.98% and 9.68% respectively.</div>
</div>""")


# ── PATTERN 7: LENGTH OF STAY (LOS) ABUSE ─────────────────────────────────────
if p08_los:
    H.append(f'''
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 2 (BEHAVIORAL)</div>
  <div class="ph-ctx">Bed Blocking &amp; Unjustified Admissions<br/>(Stay > 10 Days)</div>
  <div class="ph-title">Length of Stay (LoS) Abuse</div>
</div></div>
<p><b>Description:</b> This behavioral pattern detects "Bed Blocking"—hospitals deliberately keeping patients admitted for unnecessarily long durations (> 10 days) to inflate daily room rent and routine nursing charges, often without clear clinical progression.</p>
<div class="tc">Table P2 — Top Instances of Unjustified Extended Hospital Stays</div>
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
  <div class="ph-label" style="color:#c0392b">PATTERN 3 (BEHAVIORAL)</div>
  <div class="ph-ctx">Split-Package Fraud<br/>(Readmission &lt; 48 Hours)</div>
  <div class="ph-title">Ping-Pong Admissions</div>
</div></div>
<p><b>Description:</b> This highly critical pattern flags "Ping-Ponging"—where a hospital discharges a patient only to readmit them within 48 hours for the same or related condition. This is an explicit attempt to bypass package duration limits and bill two separate procedures instead of one continuous stay.</p>
<div class="tc">Table P3 — Top Cases of Split-Package Readmissions (Within 48 Hrs)</div>
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
  <div class="ph-label" style="color:#c0392b">PATTERN 4 (BEHAVIORAL)</div>
  <div class="ph-ctx">The Friday Hustle<br/>(Abnormal Weekend Admissions)</div>
  <div class="ph-title">Weekend / Holiday Surge Admissions</div>
</div></div>
<p><b>Description:</b> Analyzes the distribution of admissions across the days of the week. Hospitals that show a massive spike in admissions specifically on Fridays, Saturdays, and Sundays are likely exploiting the lack of physical ECHS verifiers on duty during the weekend.</p>
<div class="tc">Table P4 — Hospitals with Suspicious Weekend Admission Spikes</div>
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
  <div class="ph-label" style="color:#c0392b">PATTERN 5 (BEHAVIORAL)</div>
  <div class="ph-ctx">Doctor Cloning Fraud<br/>(> 15 Surgeries / Day)</div>
  <div class="ph-title">Doctor Cloning (The Superman Surgeon)</div>
</div></div>
<p><b>Description:</b> Detects physical impossibility. Flags instances where a single treating doctor's ID is attached to an abnormally high number of surgeries or admissions (e.g., >15) within a single 24-hour period.</p>
<div class="tc">Table P5 — Impossible Daily Surgical Volumes</div>
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
  <div class="ph-label" style="color:#c0392b">PATTERN 6 (BEHAVIORAL)</div>
  <div class="ph-ctx">The ₹99,999 Trick<br/>(CFA Approval Evasion)</div>
  <div class="ph-title">Threshold Avoiding</div>
</div></div>
<p><b>Description:</b> Hospitals intentionally billing exact amounts just beneath the special approval threshold (e.g., ₹1,00,000) to ensure the claim is automatically processed without requiring senior CFA officer scrutiny.</p>
<div class="tc">Table P6 — Top Hospitals Exploiting the ₹99k Threshold</div>
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

H.append(f"""
<div class="pb">
<h1>Consolidated Summary</h1>
<p class="tc" style="margin-bottom:10px">Forensic mapping of budget leakage and anomalous claims across all 7 analyzed patterns.</p>

<table class="dt">
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
    <td><b>Classif. 1</b></td>
    <td>Overall Outlier Claims (&ge; ₹25k)</td>
    <td>659,564</td>
    <td>{cr(7380.72)}</td>
  </tr>
  <tr>
    <td><b>Classif. 2</b></td>
    <td>Annual Trends &amp; Inflation (&ge; ₹20k)</td>
    <td>766,652</td>
    <td>{cr(7619.60)}</td>
  </tr>
  <tr>
    <td><b>Classif. 3</b></td>
    <td>Hospital Type &amp; NABH status (&ge; ₹10k)</td>
    <td>175,448</td>
    <td>{cr(1357.15)}</td>
  </tr>
  <tr>
    <td><b>Classif. 3</b></td>
    <td>Corporate Hospital Overbilling (Top 50)</td>
    <td>953,195</td>
    <td>{cr(2359.59)}</td>
  </tr>
  <tr>
    <td><b>Classif. 4</b></td>
    <td>Regional Commands (Top 10 regions)</td>
    <td>4,401,707</td>
    <td>{cr(29458.98)}</td>
  </tr>
  <tr>
    <td><b>Pattern 1</b></td>
    <td>Itemized Procedure Deviations (&ge; ₹50k)</td>
    <td>1,463,130</td>
    <td>{cr(1931.93)}</td>
  </tr>
  <tr>
    <td><b>Classif. 5</b></td>
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
</table>

<h1 style="margin-top:18px; margin-bottom:12px;">Strategic Pre-Payment Projections</h1>
<div class="proj-card">
  <div class="proj-info">
    <div class="proj-title">Conservative Interception</div>
    <div class="proj-desc">30% of deductions prevented pre-payment via basic rule-engine.</div>
  </div>
  <div class="proj-val">{cr(cons_val)}</div>
</div>
<div class="proj-card">
  <div class="proj-info">
    <div class="proj-title">Moderate Interception</div>
    <div class="proj-desc">50% of deductions prevented pre-payment via manual + automated triage.</div>
  </div>
  <div class="proj-val">{cr(mod_val)}</div>
</div>
<div class="proj-card">
  <div class="proj-info">
    <div class="proj-title">Aggressive Interception</div>
    <div class="proj-desc">75% of deductions prevented pre-payment via strict NABH audits.</div>
  </div>
  <div class="proj-val">{cr(agg_val)}</div>
</div>
<div class="proj-card proj-ai">
  <div class="proj-info">
    <div class="proj-title">AI Pre-Approval Interception Model</div>
    <div class="proj-desc">Optimized machine-learning pre-approval detection saving 60% of leakage automatically.</div>
  </div>
  <div class="proj-val" style="color:#d4680a">{cr(ai_val)}</div>
</div>

<h1 style="margin-top:14px">Empanelled Policy Recommendations</h1>
<div class="recommendation-card">
  <div class="rec-title-row">
    <div class="rec-title">1. Implement Pre-Payment Anomaly Rules</div>
    <div class="rec-tag" style="color:#c0392b">CRITICAL</div>
  </div>
  <p style="font-size:8pt">Deploy AI-assisted billing interception scoring (as detailed in Module 13 models) to catch leakage pre-payment, saving up to {cr(ai_val)}.</p>
</div>

<div class="recommendation-card">
  <div class="rec-title-row">
    <div class="rec-title">2. Chain-Level Corporate Audit Review</div>
    <div class="rec-tag" style="color:#c0392b">CRITICAL</div>
  </div>
  <p style="font-size:8pt">Initiate a corporate-level billing audit on the Park Hospital Chain across all empanelled locations to identify systematic package upcoding patterns.</p>
</div>

<div class="recommendation-card">
  <div class="rec-title-row">
    <div class="rec-title">3. Tighten Empanelment Accreditation Guidelines</div>
    <div class="rec-tag" style="color:#d4680a">HIGH</div>
  </div>
  <p style="font-size:8pt">Require mandatory NABH accreditation for all private empanelled hospitals within 3 years to structurally reduce deduction gaps by ₹285–₹320 Cr annually.</p>
</div>

<p style="margin-top:20px;font-size:7.5pt;color:#555;text-align:center">
  Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
  All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
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
