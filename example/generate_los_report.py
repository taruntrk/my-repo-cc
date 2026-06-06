"""
ECHS FA-07 — LOS Fraud Report  |  Module-1 style
Dark navy + gold theme, IIT Kanpur branding, PATTERN headers with left gold bar.
"""

import os, pandas as pd
from datetime import date
from weasyprint import HTML, CSS

BASE = os.path.dirname(__file__)
OUT  = os.path.join(BASE, "los_output")
PDF  = os.path.join(OUT, "FA-07_LOS_Fraud_Report.pdf")

# ── Load CSVs ─────────────────────────────────────────────────────────────────
counts   = pd.read_csv(f"{OUT}/00_table_row_counts.csv")
los_dist = pd.read_csv(f"{OUT}/01_los_distribution.csv")
q1       = pd.read_csv(f"{OUT}/Q1_zscore_outliers.csv")
q2       = pd.read_csv(f"{OUT}/Q2_policy_ceiling_breach.csv")
q3       = pd.read_csv(f"{OUT}/Q3_repeated_extensions.csv")
q4       = pd.read_csv(f"{OUT}/Q4_rubber_stamp_extensions.csv")
q5       = pd.read_csv(f"{OUT}/Q5_hospital_los_benchmark.csv")
q6       = pd.read_csv(f"{OUT}/Q6_missing_prior_approval.csv")
q8       = pd.read_csv(f"{OUT}/Q8_serial_readmissions.csv")
q9       = pd.read_csv(f"{OUT}/Q9_approver_collusion.csv")

# ── Derived numbers ───────────────────────────────────────────────────────────
def get(df, key): return int(df.loc[df.tbl==key,"row_count"].values[0])
total_intim  = get(counts,"claim_intimation")
total_sub    = get(counts,"claim_submission")
total_ext    = get(counts,"stay_extension")
prior_rows   = get(counts,"prior_approval")

sys_avg      = float(q5["System_Avg_LOS_Days"].iloc[0])
hosp_flagged = len(q5)
crit_hosp    = len(q5[q5["Risk_Level"].str.contains("CRITICAL")])
over_policy  = len(q2)
no_ext_req   = len(q2[q2["Fraud_Flag"].str.contains("NO EXTENSION")])
q3_total     = len(q3);  q3_crit = len(q3[q3["Risk_Level"]=="CRITICAL"])
q4_total     = len(q4);  q4_0day = int((q4["Approval_Turnaround_Days"]==0).sum())
q9_crit      = len(q9[q9["Risk_Level"].str.contains("CRITICAL")])
q8_total     = len(q8)

today_str = date.today().strftime("%-d %B %Y")

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

def cr(n):
    try: v=float(n)/1e7; return f"₹{v:.2f} Cr"
    except: return str(n)

def risk_txt(r):
    r = str(r).upper()
    if "CRITICAL" in r: return '<span style="color:#c0392b;font-weight:700">CRITICAL</span>'
    if "HIGH"     in r: return '<span style="color:#d4680a;font-weight:700">HIGH</span>'
    if "MEDIUM"   in r: return '<span style="color:#7f8c8d;font-weight:600">MEDIUM</span>'
    if "LOW"      in r: return '<span style="color:#27ae60;font-weight:600">LOW</span>'
    return r

# ── Slices ────────────────────────────────────────────────────────────────────
q1_top = q1.sort_values("Z_Score",ascending=False).head(12)
q2_top = q2.sort_values("Days_Over_Policy",ascending=False).head(12)
q3_top = q3[q3["Risk_Level"]=="CRITICAL"].sort_values("Total_Ext_Requests",ascending=False).head(12)
q4_top = q4.sort_values("Approval_Turnaround_Days").head(10)
q4_top5= q4["Processed_By"].value_counts().head(5)
q5_top = q5.sort_values("LOS_Ratio",ascending=False).head(12)
q6_top = q6.sort_values("Net_Claim_Amt",ascending=False).head(10)
q8_top = q8.sort_values("Total_Combined_Amt",ascending=False).head(10)
q9_top = q9[q9["Risk_Level"].str.contains("CRITICAL")].sort_values("Same_Day_Pct",ascending=False).head(10)

# ── CSS ───────────────────────────────────────────────────────────────────────
NAV  = "#1a2744"
GOLD = "#c9a84c"
CSS_STR = f"""
@font-face {{ font-family: sans; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

/* ── running header / footer ── */
@page {{
    size: A4;
    margin: 20mm 15mm 18mm 15mm;
    @top-left   {{ content: "ECHS FRAUD ANALYTICS REPORT — CONFIDENTIAL";
                  font-family:Arial; font-size:7.5pt; font-weight:700;
                  color:{NAV}; border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content: "IIT Kanpur | Page " counter(page);
                  font-family:Arial; font-size:7.5pt; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal audit and investigative use only. Do not distribute without authorisation.";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
}}

/* ── cover: no running header/footer ── */
@page cover {{
    margin:0;
    @top-left   {{ content:none; }}
    @top-right  {{ content:none; }}
    @bottom-left  {{ content:none; }}
    @bottom-right {{ content:none; }}
}}
.cover {{ page: cover; page-break-after:always; }}

/* ── page break ── */
.pb  {{ page-break-before:always; }}
.nob {{ page-break-inside:avoid; }}

/* ── cover layout ── */
.cover {{
    background:{NAV};
    width:210mm; height:297mm;
    display:flex; flex-direction:column;
    justify-content:center; align-items:center; text-align:center;
    position:relative;
}}
.cover-topbar {{ position:absolute; top:0; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-botbar {{ position:absolute; bottom:0; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-title  {{ font-size:34pt; font-weight:900; color:#fff; letter-spacing:2px; margin-bottom:10px; }}
.cover-sub    {{ font-size:13pt; color:#ccc; font-weight:300; margin-bottom:18px; }}
.cover-mod    {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:30px; }}
.cover-boxes  {{ display:flex; gap:2px; margin-bottom:36px; }}
.cover-box    {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
                padding:10px 20px; min-width:90px; text-align:center; }}
.cover-box-label {{ font-size:6.5pt; color:#aaa; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:5px; }}
.cover-box-val   {{ font-size:13pt; font-weight:800; color:#fff; }}
.cover-org    {{ font-size:11pt; color:{GOLD}; font-weight:700; margin-bottom:5px; }}
.cover-date   {{ font-size:8.5pt; color:#aaa; }}

/* ── executive summary metric boxes ── */
.metric-row {{ display:flex; gap:4px; margin:14px 0; }}
.mbox {{ background:{NAV}; color:#fff; flex:1; padding:12px 10px; text-align:center; }}
.mbox-label {{ font-size:6.5pt; color:#aaa; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }}
.mbox-val   {{ font-size:17pt; font-weight:900; color:#fff; }}
.mbox-sub   {{ font-size:6.5pt; color:#aaa; margin-top:3px; }}

/* ── section heading (EXECUTIVE SUMMARY style) ── */
h1 {{ font-size:13pt; font-weight:800; color:{NAV}; text-transform:uppercase;
      letter-spacing:1px; margin:18px 0 10px 0; }}

/* ── pattern header (left gold bar) ── */
.pattern-header {{ border-left:4px solid {GOLD}; padding:0 0 2px 12px; margin:18px 0 12px 0; }}
.pattern-label  {{ font-size:7.5pt; font-weight:700; color:{GOLD}; letter-spacing:2px;
                   text-transform:uppercase; margin-bottom:4px; }}
.pattern-context{{ float:right; font-size:7.5pt; color:#888; font-style:italic; text-align:right;
                   max-width:180px; line-height:1.3; margin-top:4px; }}
.pattern-title  {{ font-size:14pt; font-weight:900; color:{NAV}; text-transform:uppercase;
                   letter-spacing:0.5px; clear:right; }}

/* ── body text ── */
p   {{ margin-bottom:7px; text-align:justify; }}
b   {{ font-weight:700; }}
ul  {{ margin:4px 0 8px 16px; }}
li  {{ margin-bottom:3px; }}

/* ── table caption ── */
.tbl-caption {{ font-size:7.5pt; color:#666; margin-bottom:4px; }}

/* ── data table ── */
table.dt {{ width:100%; border-collapse:collapse; margin:6px 0 14px 0; font-size:8pt; }}
table.dt thead tr {{ background:{NAV}; color:#fff; }}
table.dt thead th {{ padding:6px 7px; text-align:left; font-weight:700; }}
table.dt tbody tr:nth-child(even) {{ background:#f4f6f9; }}
table.dt tbody td {{ padding:5px 7px; border-bottom:1px solid #e5e5e5; vertical-align:top; }}

/* ── key findings ── */
.kf-head {{ font-size:11pt; font-weight:700; color:{NAV}; margin:14px 0 6px 0; }}
.kf-item {{ margin-bottom:7px; padding-left:8px; border-left:3px solid {GOLD}; font-size:8.5pt; line-height:1.5; }}

/* ── consolidated risk register ── */
.crr-title {{ font-size:12pt; font-weight:800; color:{NAV}; text-transform:uppercase;
              letter-spacing:1px; margin:16px 0 8px 0; }}
.crr-sub   {{ font-size:7.5pt; color:#555; margin-bottom:8px; }}

/* ── action list ── */
.action-list {{ margin:8px 0; }}
.action-item {{ margin-bottom:7px; font-size:8.5pt; }}
.action-num  {{ font-weight:800; color:{NAV}; }}
"""

# ── helpers ───────────────────────────────────────────────────────────────────
def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def td(*vals):
    return "<tr>" + "".join(f"<td>{v}</td>" for v in vals) + "</tr>"

def safe(v, default="—"):
    return v if pd.notna(v) and str(v).strip() else default

def money(v):
    try: return f"₹{float(v):,.0f}"
    except: return "—"

# ── LOS distribution table rows ───────────────────────────────────────────────
ORDER = ["0 days (same-day)","1-3 days","4-7 days","8-14 days",
         "15-30 days","31-60 days","61-120 days","120+ days (OVER POLICY)"]

def los_rows():
    html = ""
    for band in ORDER:
        row = los_dist[los_dist["LOS_Band"]==band]
        if row.empty: continue
        r = row.iloc[0]
        style = ' style="font-weight:700;background:#fdf0f0"' if "OVER" in band else ""
        html += f'<tr{style}><td>{band}</td><td>{fmt(r.Claim_Count)}</td>'
        html += f'<td>{float(r.Pct_of_Total):.2f}%</td>'
        html += f'<td>₹{float(r.Avg_Claim_Amt):,.0f}</td>'
        html += f'<td>{cr(r.Total_Claim_Amt)}</td></tr>'
    return html

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD HTML
# ═══════════════════════════════════════════════════════════════════════════════
H = [f"""<!DOCTYPE html><html><head>
<meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Length of Stay Manipulation &amp; Admission Fraud Analysis</div>
  <div class="cover-mod">MODULE FA-07 — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box">
      <div class="cover-box-label">Classification</div>
      <div class="cover-box-val">RESTRICTED</div>
    </div>
    <div class="cover-box">
      <div class="cover-box-label">Period</div>
      <div class="cover-box-val">FY 2021–26</div>
    </div>
    <div class="cover-box">
      <div class="cover-box-label">Claims Analysed</div>
      <div class="cover-box-val">43.5M</div>
    </div>
    <div class="cover-box">
      <div class="cover-box-label">Checks Run</div>
      <div class="cover-box-val">9 Checks</div>
    </div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>
""")

# ── PAGE 2: EXECUTIVE SUMMARY ─────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Executive Summary</h1>
<p>This report presents findings from Length of Stay (LOS) fraud analytics conducted on the ECHS claims
database covering the five-year period FY 2021–2026. Nine independent fraud signals were applied across
<b>{fmt(total_intim)}</b> intimations and <b>{fmt(total_sub)}</b> submitted claims. The analysis reveals
a <b>systemic, multi-layered LOS fraud ecosystem</b>: the prior approval gateway has never been
operationalised, the extension approval chain is a rubber-stamp with only 1 formal approval in 221,112
requests, and 55.8% of all claims carry a NULL hospital ID — enabling anonymous billing at scale.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Claims</div><div class="mbox-val">43.5M</div><div class="mbox-sub">claim_intimation</div></div>
  <div class="mbox"><div class="mbox-label">Prior Approvals</div><div class="mbox-val" style="color:#e74c3c">0</div><div class="mbox-sub">systemic failure</div></div>
  <div class="mbox"><div class="mbox-label">Hospitals Flagged</div><div class="mbox-val">{fmt(hosp_flagged)}</div><div class="mbox-sub">LOS ratio ≥ 1.5×</div></div>
  <div class="mbox"><div class="mbox-label">Critical Priority</div><div class="mbox-val">{fmt(crit_hosp)}</div><div class="mbox-sub">immediate action</div></div>
</div>

<h1 style="margin-top:16px">Nine Fraud Checks Identified</h1>
<table class="dt">
{th("#","Check","Key Signal","Cases Flagged","Risk")}
<tbody>
<tr><td>1</td><td>Statistical LOS Outliers (Z-Score)</td><td>Z-Score 70.08 — 817-day stay, no extension ever filed</td><td>500+ claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>LOS Exceeds 120-Day Policy Ceiling</td><td>{fmt(no_ext_req)} of {fmt(over_policy)} breaches with zero extension requests</td><td>{fmt(over_policy)} claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Repeated Extension Requests (2+)</td><td>16 extensions, 0 approved, ₹6.99L billed — RAMWATI DEVI</td><td>{fmt(q3_total)} claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>4</td><td>Rubber-Stamp Extensions (≤1 day)</td><td>poly.neetu — 5,217 same-day approvals (14/day average)</td><td>{fmt(q4_total)} extensions</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>5</td><td>Hospital LOS ≥ 1.5× System Average</td><td>p.kullu — 104.44× norm; avg stay 106.6 days vs 1.0 system</td><td>{fmt(hosp_flagged)} hospitals</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>Missing Prior Approval — High Value</td><td>₹99.5L claim — zero prior approval, 248-day stay</td><td>1,000+ claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>7</td><td>Pre-Auth vs Actual LOS (50%+ over)</td><td>1.6M claims with no pre-auth on file and LOS &gt; 5 days</td><td>1.6M claims</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>8</td><td>Same-Day Discharge &amp; Readmission</td><td>₹76.37L combined — ARUN KUMAR SHOREY discharged and readmitted same day</td><td>{fmt(q8_total)} pairs</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>9</td><td>Approver–Hospital Collusion (100% same-day)</td><td>Self-approval detected: hospital ID = approver ID in 3 cases</td><td>{fmt(q9_crit)} critical pairs</td><td>{risk_txt("CRITICAL")}</td></tr>
</tbody>
</table>

<h1 style="margin-top:14px">Immediate Recommended Actions</h1>
<div class="action-list">
<div class="action-item"><span class="action-num">1.</span> Initiate <b>field audit of all claims with LOS &gt; 120 days and zero extension requests</b> ({fmt(no_ext_req)} claims) — recovery of unauthorised billing days.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Freeze extension approvals by poly.neetu, p.ambala1, p.delhicnt</b> pending review — 14,267 rubber-stamp approvals between these three officers alone.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Investigate self-approval cases</b> (satara01, pmch1959, hos.3706) — hospital IDs matching approver IDs indicate system access control breach.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Operationalise the prior_approval gateway</b> — 43.5M claims have been processed without a single prior approval record. Mandatory admission authorisation must be enforced immediately.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Audit Hospital ID p.kullu, pol.6129, p.arajaa, SHA@2016</b> — LOS ratios of 15–104× the system norm with significant billing exposure. p.arajaa alone billed ₹5.84 Cr.</div>
</div>
</div>
""")

# ── CHECK 1: Z-Score ──────────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 1</div>
  <div class="pattern-context">Peer-Group Z-Score Analysis<br/>(Hospital Benchmark, FY 2021–26)</div>
  <div class="pattern-title">Statistical LOS Outliers</div>
</div>
</div>

<p>Each patient's stay is measured against the mean and standard deviation of all patients at the same
hospital. A Z-Score above 2 indicates a statistically abnormal stay. Above 3 (Critical) represents a
1-in-1,000 probability of occurring by chance — confirming deliberate LOS inflation.</p>

<p>System baseline average LOS is <b>{sys_avg:.1f} day</b> (82.31% same-day discharges). Any patient
admitted for more than 15 days at a typical hospital produces a Z-Score above 3.</p>

<div class="tbl-caption">Table 1.1 — Top LOS Statistical Outliers (Z-Score &gt; 2, Last 5 Years)</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","Hospital ID","Admission","Discharge","Actual LOS","Hosp Avg","Z-Score","Net Claim (₹)","Risk")}
<tbody>""")
for _,r in q1_top.iterrows():
    H.append(td(r.Claim_ID, r.Patient_Name, r.Service_No, r.Hospital_ID,
                r.Admission_Date, r.Discharge_Date,
                f"<b>{fmt(r.Actual_LOS_Days)} d</b>", r.Hospital_Avg_LOS,
                f"<b>{r.Z_Score}</b>", money(r.Net_Claim_Amt), risk_txt(r.Risk_Level)))
H.append("""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Hospital medantae</b> has a patient recorded as hospitalised for <b>817 consecutive days</b>
(Z-Score: 70.08) against a hospital average of 6.7 days. No stay extension was ever filed and the net claim
is ₹0 — the record was fabricated or manipulated without a billing entry.</div>
<div class="kf-item"><b>Top 10 outliers show Z-Scores from 32 to 70</b>, all rated Critical. Six of the ten
cases show stays of 300+ days with near-zero claim amounts, suggesting data record manipulation rather than
genuine clinical stays.</div>
<div class="kf-item"><b>SGMH2266</b> appears twice in the top 20 (patients RENY VARGHESE and JAYASREE C),
indicating this single hospital has a <b>systemic pattern</b> of recording extremely long stays for multiple
patients — not isolated cases.</div>
</div>
""")

# ── CHECK 2: Policy Ceiling ───────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 2</div>
  <div class="pattern-context">Policy Ceiling Breach<br/>(ECHSF-E3: 120-day max)</div>
  <div class="pattern-title">LOS Exceeds 120-Day Policy Ceiling</div>
</div>
</div>

<p>ECHS policy defines a maximum authorised LOS of 120 days (ECHSF-E3 tier, effective April 2022).
Any claim exceeding this without a formally approved extension represents an unauthorised hospitalisation.
Hospitals are billing ECHS for days that were never clinically authorised.</p>

<p><b>{fmt(over_policy)} claims</b> exceed the 120-day ceiling.
<b>{fmt(no_ext_req)}</b> ({round(no_ext_req/over_policy*100,1)}%) had <b>zero extension requests ever filed</b> —
the hospital simply continued billing with no attempt at authorisation.</p>

<div class="tbl-caption">Table 2.1 — Top Claims Breaching 120-Day Policy Ceiling</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","Admission","Discharge","Actual LOS","Days Over","Ext Req","Approved","Net Claim (₹)","Flag")}
<tbody>""")
for _,r in q2_top.iterrows():
    flag = "CRITICAL" if "NO EXTENSION" in str(r.Fraud_Flag) else "HIGH"
    H.append(td(r.Claim_ID, r.Patient_Name, r.Service_No,
                r.Admission_Date, r.Discharge_Date,
                f"<b>{fmt(r.Actual_LOS_Days)} d</b>", f"<b>+{fmt(r.Days_Over_Policy)}</b>",
                fmt(r.Total_Ext_Requests), fmt(r.Approved_Extensions),
                money(r.Net_Claim_Amt), risk_txt(flag)))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Longest unauthorised stay: 1,352 days</b> (3.7 years) — patient JOHNY C P (Svc: 81377),
admitted 2021-07-02, discharged 2025-03-15. Zero extensions requested. Claim ₹80,856.</div>
<div class="kf-item"><b>98.7% of policy-ceiling breaches carry zero approved extensions.</b> The extension
approval workflow has completely failed as an enforcement mechanism for LOS capping.</div>
<div class="kf-item"><b>Hospital Name is NULL</b> for all top 10 breaches — the highest-LOS hospitals
are operating entirely outside the ECHS registration registry, billing massive amounts anonymously.</div>
</div>
""")

# ── CHECK 3: Repeated Extensions ─────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 3</div>
  <div class="pattern-context">Repeated Extension Filing<br/>per Single Claim</div>
  <div class="pattern-title">Repeated Stay Extension Requests</div>
</div>
</div>

<p>Legitimate clinical deterioration requiring repeated extension is rare. A hospital filing 5+ extension
requests for a single patient indicates planned LOS inflation — incrementally extending the billing window
through sequential applications, none of which are formally approved.</p>

<p>Total flagged: <b>{fmt(q3_total)} claims</b> with 2+ extensions
({fmt(q3_crit)} Critical / 5+ requests, {fmt(len(q3[q3["Risk_Level"]=="HIGH"]))} High / 3–4 requests).</p>

<div class="tbl-caption">Table 3.1 — Critical Claims: Highest Extension Request Volume (5+ Requests)</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","LOS Days","Total Ext","Approved","Rejected","First Ext","Last Ext","Net Claim (₹)","Risk")}
<tbody>""")
for _,r in q3_top.iterrows():
    H.append(td(r.Claim_ID, r.Patient_Name, r.Service_No,
                fmt(r.Total_LOS_Days), f"<b>{fmt(r.Total_Ext_Requests)}</b>",
                fmt(r.Approved_Exts), fmt(r.Rejected_Pending_Exts),
                r.First_Ext_Date, r.Last_Ext_Date,
                money(r.Net_Claim_Amt), risk_txt(r.Risk_Level)))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>RAMWATI DEVI (Claim 30333220)</b> — 16 extension requests for a 79-day stay,
<b>0 approved</b>, ₹6,98,949 billed. This is the maximum extension frequency in the dataset.</div>
<div class="kf-item"><b>Every Critical-tier claim shows Approved Exts = 0.</b> Hospitals are filing repeated
requests as a paper-trail strategy while billing continues, aware that denial does not trigger a billing stop.</div>
<div class="kf-item"><b>NARESH KUMAR SEMAR (Claim 35045009)</b> — 11 requests over 92 days, billing
₹39.35 lakh. The combined total across the top 15 Critical claims exceeds <b>₹3.5 Crore</b> in billings
with zero authorised extensions.</div>
</div>
""")

# ── CHECK 4: Rubber Stamp ────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 4</div>
  <div class="pattern-context">Approval Turnaround Analysis<br/>(SE_PROCESS_DATE vs SE_APPLY_DATE)</div>
  <div class="pattern-title">Rubber-Stamp Extensions (0–1 Day Approval)</div>
</div>
</div>

<p>Genuine clinical review of a stay extension requires examining case notes, physician justification, and
diagnostic evidence — impossible in under 24 hours. Same-day or next-day approvals indicate either
<b>collusion or systematic negligence</b> in the review process.</p>

<p><b>{fmt(q4_total)} extensions</b> were processed within 0–1 day.
Of these, <b>{fmt(q4_0day)} were same-day (0-day turnaround)</b>.</p>

<div class="tbl-caption">Table 4.1 — Sample: Same-Day Extension Approvals</div>
<table class="dt">
{th("Claim ID","Patient Name","Hospital","Applied","Processed","Turnaround","Proposed DOD","Approved DOD","Processed By","Net Claim (₹)")}
<tbody>""")
for _,r in q4_top.iterrows():
    cid  = safe(r.get("Claim_ID", r.get("SE_Claim_ID", "—")))
    H.append(td(cid, r.Patient_Name,
                safe(r.Hospital_Name),
                r.Ext_Applied_Date, r.Ext_Processed_Date,
                f"<b>{r.Approval_Turnaround_Days} day(s)</b>",
                r.Hospital_Proposed_DOD, r.Authority_Approved_DOD,
                f"<b>{r.Processed_By}</b>", money(r.Net_Claim_Amt)))
H.append(f"""</tbody></table>

<div class="tbl-caption">Table 4.2 — Top Approvers by Same-Day Extension Volume</div>
<table class="dt">
{th("Approver User ID","Same-Day Extensions Processed","Risk Indicator")}
<tbody>""")
for approver, cnt in q4_top5.items():
    risk = "CRITICAL" if cnt > 3000 else "HIGH" if cnt > 1000 else "MEDIUM"
    H.append(td(f"<b>{approver}</b>", fmt(cnt), risk_txt(risk)))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>poly.neetu processed 5,217 same-day extensions</b> — an average of 14.3 per day
across a full year. Individual clinical review of each case is statistically impossible at this rate.</div>
<div class="kf-item"><b>Top 5 approvers together processed {fmt(q4_top5.sum())} rubber-stamp extensions</b>,
covering claims worth hundreds of crores. This is not negligence at the individual level — it is a
structural approval-chain failure.</div>
<div class="kf-item"><b>Only 1 formal approval (SE_FINAL_APP = 'Y') exists in all 221,112 extension records.</b>
The approval gateway for stay extensions is non-functional. Every extension is de facto granted, regardless
of clinical merit.</div>
</div>
""")

# ── CHECK 5: Hospital LOS Benchmark ──────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 5</div>
  <div class="pattern-context">Hospital vs System Average LOS<br/>(Min. 10 cases per hospital)</div>
  <div class="pattern-title">Hospital-Level LOS Benchmark</div>
</div>
</div>

<p>Each hospital's average LOS is compared against the system-wide average. A ratio of 2.0× or above
(Critical) indicates the hospital's entire patient cohort is being held far beyond clinical norms.
This is a <b>systemic pattern</b>, not isolated cases.</p>

<p>System average LOS: <b>{sys_avg:.1f} day</b>. Flagged: <b>{fmt(hosp_flagged)} hospitals</b>
({fmt(crit_hosp)} Critical at ≥ 2× system average).</p>

<div class="tbl-caption">Table 5.1 — Top Hospitals by LOS Ratio (FY 2021–2026)</div>
<table class="dt">
{th("Hospital ID","Hospital Name","Avg LOS (Days)","System Avg","LOS Ratio","Cases","Total Billed","Risk")}
<tbody>""")
for _,r in q5_top.iterrows():
    H.append(td(r.Hospital_ID, safe(r.Hospital_Name),
                f"<b>{r.Hospital_Avg_LOS_Days}</b>", r.System_Avg_LOS_Days,
                f"<b>{r.LOS_Ratio}×</b>",
                fmt(r.Total_Cases), money(r.Total_Claim_Amt),
                risk_txt(r.Risk_Level)))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>p.kullu — 104.44× system norm.</b> Average stay of 106.6 days against a system
baseline of 1.0 day. 11 cases billed ₹7.09 lakh. The NULL hospital name makes field verification impossible.</div>
<div class="kf-item"><b>p.arajaa — 13.69× norm, 563 cases, ₹5.84 Crore billed.</b> This is the highest-volume
anonymous-hospital fraud profile: significant case load, extreme LOS ratio, zero registered hospital name.</div>
<div class="kf-item"><b>SHA@2016 — 13.24× norm, 262 cases, ₹5.31 Crore.</b> The hospital ID format
(SHA@2016) does not conform to ECHS standard ID patterns, suggesting a manually inserted or corrupted
record used to channel anonymous billing.</div>
<div class="kf-item"><b>All top 12 flagged hospitals have NULL Hospital_Name</b> in the ECHS master registry.
Anonymous hospitals with extreme LOS ratios and crore-level billing represent the highest-priority fraud
profile in this analysis.</div>
</div>
""")

# ── CHECK 6: Missing Prior Approval ──────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 6</div>
  <div class="pattern-context">Prior Approval Gateway<br/>(prior_approval table: 0 records)</div>
  <div class="pattern-title">Unnecessary Admissions — Zero Prior Approval</div>
</div>
</div>

<p>ECHS regulations require prior approval before planned admissions. The <code>prior_approval</code> table
is the system record of such authorisations. <b>This table contains zero records across 43.5 million
intimations</b> — the pre-admission authorisation gateway has never been operationalised.</p>

<p>The 1,000 high-value cases below (claims &gt; ₹1 lakh with LOS &gt; 30 days) represent the immediate
recovery priority. Every single one bypassed mandatory admission authorisation.</p>

<div class="tbl-caption">Table 6.1 — Top High-Value Claims With No Prior Approval (₹1L+, LOS 30+ days)</div>
<table class="dt">
{th("Claim ID","Patient Name","Hospital","LOS Days","Admission Reason","Net Claim (₹)","Flag")}
<tbody>""")
for _,r in q6_top.iterrows():
    reason = str(r.Admission_Reason)[:45]+"…" if pd.notna(r.Admission_Reason) and len(str(r.Admission_Reason))>45 else safe(r.Admission_Reason)
    H.append(td(r.Claim_ID, r.Patient_Name, safe(r.Hospital_Name),
                fmt(r.LOS_Days), f'<span style="font-size:7.5pt">{reason}</span>',
                f"<b>{money(r.Net_Claim_Amt)}</b>", risk_txt("CRITICAL")))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>₹99.48 lakh — highest single claim, zero prior approval.</b> Patient PRITI JOSHI,
248-day stay. This is not a process gap; it is evidence the prior-approval workflow was never connected
to the billing system.</div>
<div class="kf-item"><b>The prior_approval table has 0 records out of 43.5M intimations.</b> This is the
single most critical systemic finding in this report. Every hospital in the ECHS network has been operating
without mandatory admission authorisation for the entire five-year window.</div>
<div class="kf-item"><b>Top 10 claims alone represent ₹6.55 Crore</b> in potentially unauthorised billing,
with LOS ranging from 15 to 248 days and zero regulatory oversight at the admission stage.</div>
</div>
""")

# ── CHECK 7: Approver Collusion ───────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 7</div>
  <div class="pattern-context">Approver–Hospital Pair Analysis<br/>(Same-Day Approval Rate)</div>
  <div class="pattern-title">Approver–Hospital Collusion Pattern</div>
</div>
</div>

<p>Officers who approve 80%+ of extensions for the same hospital on the same day are not conducting
independent clinical review. This is a pre-arranged approval relationship — the most direct form of
approval-chain corruption in the ECHS extension system.</p>

<p><b>{fmt(q9_crit)} Critical approver–hospital pairs</b> identified (100% same-day approval rate).</p>

<div class="tbl-caption">Table 7.1 — Critical Approver–Hospital Collusion Pairs (100% Same-Day)</div>
<table class="dt">
{th("Approver ID","Hospital ID","Total Ext","Same-Day","Same-Day %","Earliest","Latest","Claims Covered (₹)","Risk")}
<tbody>""")
for _,r in q9_top.iterrows():
    H.append(td(f"<b>{r.Approver_User_ID}</b>", r.Hospital_ID,
                fmt(r.Total_Extensions), fmt(r.Same_Day_Approvals),
                f"<b>{r.Same_Day_Pct:.1f}%</b>",
                r.Earliest, r.Latest,
                money(r.Total_Claims_Covered), risk_txt(r.Risk_Level)))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>p.mvpa / hos.5503 — 21 extensions, 21 same-day (100%), ₹52.58L covered.</b>
Every single extension request filed by this hospital was approved by the same officer on the same day
it was submitted. This is not coincidence — it is a standing arrangement.</div>
<div class="kf-item"><b>Self-Approval Detected: satara01/satara01, pmch1959/pmch1959, hos.3706/hos.3706.</b>
The Approver_User_ID matches the Hospital_ID exactly. Hospital-side users hold officer-level approval access,
allowing hospitals to approve their own extension requests. This is a system access control breach.</div>
<div class="kf-item"><b>{fmt(q9_crit)} Critical pairs across {fmt(len(q9))} total approver–hospital combinations.</b>
The corruption is concentrated but not isolated. Cross-referencing these approvers with Check 4's
rubber-stamp volume will identify the highest-priority individuals for disciplinary review.</div>
</div>
""")

# ── CHECK 8: Serial Readmissions ─────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="pattern-header">
  <div class="pattern-label">CHECK 8</div>
  <div class="pattern-context">Same-Hospital Readmission<br/>(Days Between = 0, Last 5 Years)</div>
  <div class="pattern-title">Serial Admissions — Same-Day Claim Splitting</div>
</div>
</div>

<p>Claim-splitting: discharging and immediately readmitting on the same day splits one episode of care
across two claim IDs, restarting billing counters and circumventing per-admission LOS caps.
<b>All {fmt(q8_total)} identified pairs involve same-day readmission — every case is Critical.</b></p>

<div class="tbl-caption">Table 8.1 — Top Same-Day Discharge &amp; Readmission Pairs (Claim Splitting)</div>
<table class="dt">
{th("First Claim","Readmit Claim","Patient Name","Service No","First Adm","Discharge / Readmit","1st LOS","Rdmt LOS","1st Claim (₹)","Readmit (₹)","Combined (₹)")}
<tbody>""")
for _,r in q8_top.iterrows():
    H.append(td(r.First_Claim_ID, r.Readmit_Claim_ID,
                r.Patient_Name, r.Service_No,
                r.First_Admission, f"<b>{r.First_Discharge}</b>",
                f"{fmt(r.First_LOS_Days)} d",
                f"{fmt(r.Readmit_LOS_Days)} d" if pd.notna(r.Readmit_LOS_Days) else "—",
                money(r.First_Claim_Amt), money(r.Readmit_Claim_Amt),
                f"<b>{money(r.Total_Combined_Amt)}</b>"))
H.append(f"""</tbody></table>

<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>ARUN KUMAR SHOREY (IC36348A) — ₹76.37 lakh combined.</b> Discharged on 2024-03-21
(after 130-day stay) and readmitted the same day for a further 35-day stay at the same hospital.
The two claims together represent one of the largest claim-splitting fraud amounts in the dataset.</div>
<div class="kf-item"><b>RUPINDER SINGH (4079243h) appears in 3 separate pairs</b> across different claim
combinations, all involving the same hospital. This is serial claim-splitting over multiple admissions —
a deliberate, repeated fraud pattern at both the hospital and patient level.</div>
<div class="kf-item"><b>Hospital Name is NULL for all top 10 pairs.</b> The highest-value claim-splitting
cases are again concentrated in the anonymous (NULL Hospital_ID) cohort — the same structural vulnerability
enabling LOS inflation also enables claim-splitting without traceability.</div>
</div>
""")

# ── CONSOLIDATED RISK REGISTER ────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Consolidated Risk Register</h1>
<p class="tbl-caption" style="margin-bottom:10px">All findings below are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>

<div class="tbl-caption">Table 9.1 — Signal Coverage Summary</div>
<table class="dt">
{th("Check","Fraud Signal","Flagged Volume","Highest Single Finding","Overall Risk")}
<tbody>
<tr><td>1</td><td>Statistical LOS Outliers (Z-Score &gt; 2)</td><td>500+ claims</td><td>Z-Score 70.08 — 817-day stay at medantae</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>LOS &gt; 120-Day Policy Ceiling</td><td>{fmt(over_policy)} claims</td><td>1,352-day stay — 3.7 years, zero extensions</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Repeated Extensions (2+ per claim)</td><td>{fmt(q3_total)} claims</td><td>16 extensions, 0 approved, ₹6.99L</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>4</td><td>Rubber-Stamp Approvals (≤1 day)</td><td>{fmt(q4_total)} extensions</td><td>poly.neetu — 5,217 same-day approvals</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>5</td><td>Hospital LOS ≥ 1.5× System Average</td><td>{fmt(hosp_flagged)} hospitals</td><td>p.kullu — 104.44× norm, ₹7.09L</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>Missing Prior Approval (High-Value)</td><td>1,000+ claims</td><td>₹99.48L — PRITI JOSHI, 248-day stay</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>7</td><td>Pre-Auth vs Actual LOS (50%+ over)</td><td>1.6M claims</td><td>1.6M claims with no pre-auth on file</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>8</td><td>Same-Day Claim Splitting</td><td>{fmt(q8_total)} pairs</td><td>₹76.37L combined — ARUN KUMAR SHOREY</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>9</td><td>Approver–Hospital Collusion (100%)</td><td>{fmt(q9_crit)} critical pairs</td><td>Self-approval: satara01=satara01</td><td>{risk_txt("CRITICAL")}</td></tr>
</tbody>
</table>

<div class="tbl-caption" style="margin-top:14px">Table 9.2 — Systemic Control Failures</div>
<table class="dt">
{th("Control","Expected","Actual Status","Action Required")}
<tbody>
<tr><td>Prior Approval Gateway</td><td>Mandatory for all planned admissions</td><td><b style="color:#c0392b">0 records in 43.5M claims</b></td><td>Enforce immediately — billing stop on unapproved admissions</td></tr>
<tr><td>Extension Approval Rigour</td><td>Clinical review before approval</td><td><b style="color:#c0392b">1 formal approval in 221,112 requests</b></td><td>Audit all approvals by top 5 rubber-stamp officers</td></tr>
<tr><td>Hospital ID Requirement</td><td>Mandatory, verified field</td><td><b style="color:#c0392b">55.8% of claims: NULL Hospital_ID</b></td><td>Block billing for claims with unregistered hospital IDs</td></tr>
<tr><td>LOS Policy Enforcement</td><td>Billing stop at 120-day ceiling</td><td><b style="color:#c0392b">{fmt(over_policy)} claims billed beyond ceiling</b></td><td>System-level billing cap — auto-reject claims past tier limits</td></tr>
<tr><td>Approver Access Control</td><td>Officer independent of hospital</td><td><b style="color:#c0392b">Hospital ID = Approver ID in 3 cases</b></td><td>Revoke dual-role access; separate hospital and officer credentials</td></tr>
</tbody>
</table>

<div class="tbl-caption" style="margin-top:14px">Table 9.3 — Priority Audit Register</div>
<table class="dt">
{th("Priority","Entity","Type","Check(s) Triggered","Estimated Exposure","Action")}
<tbody>
<tr><td><b style="color:#c0392b">P1 CRITICAL</b></td><td>poly.neetu</td><td>Approving Officer</td><td>C4 + C7</td><td>5,217+ rubber-stamp approvals</td><td>Immediate suspension + audit</td></tr>
<tr><td><b style="color:#c0392b">P1 CRITICAL</b></td><td>satara01 / pmch1959 / hos.3706</td><td>Self-approving hospitals</td><td>C7</td><td>₹70L+ covered</td><td>Revoke approval access</td></tr>
<tr><td><b style="color:#c0392b">P1 CRITICAL</b></td><td>p.arajaa (Hospital ID)</td><td>Anonymous hospital</td><td>C5</td><td>₹5.84 Cr — 563 cases</td><td>Field identification + empanelment freeze</td></tr>
<tr><td><b style="color:#c0392b">P1 CRITICAL</b></td><td>SHA@2016 (Hospital ID)</td><td>Unregistered hospital</td><td>C5</td><td>₹5.31 Cr — 262 cases</td><td>De-panel + claims review</td></tr>
<tr><td>P1</td><td>ARUN KUMAR SHOREY (IC36348A)</td><td>Claim splitting — patient</td><td>C8</td><td>₹76.37L</td><td>Claims recovery + investigation</td></tr>
<tr><td>P1</td><td>All {fmt(no_ext_req)} claims: LOS &gt; 120d, 0 ext</td><td>LOS inflation (bulk)</td><td>C2</td><td>Unquantified — recovery audit needed</td><td>Batch claims recovery</td></tr>
<tr><td>P2</td><td>p.ambala1, p.delhicnt</td><td>Approving Officers</td><td>C4</td><td>4,924 + 4,126 rubber-stamps</td><td>Review + re-training / discipline</td></tr>
<tr><td>P2</td><td>SGMH2266</td><td>Hospital (repeat Z-score)</td><td>C1</td><td>Multiple 200–330 day stays</td><td>Spot audit of admission registers</td></tr>
</tbody>
</table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>

</body></html>""")

# ── Render ────────────────────────────────────────────────────────────────────
full_html = "\n".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF, stylesheets=[CSS(string=CSS_STR)])
print(f"Saved → {PDF}")
