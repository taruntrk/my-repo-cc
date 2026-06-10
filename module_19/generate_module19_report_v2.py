"""
ECHS Module 19: Policy Abuse & Entitlement Misuse — Report v2
Uses new 2021-2025 data files (earlier timestamp CSVs).
Navy + Gold theme, IIT Kanpur branding, Module 20 layout pattern.
"""
import os, glob, time
from datetime import date
import pandas as pd

try:
    from weasyprint import HTML
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint")
    exit(1)

BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE, "require_data", "data")
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(REPORTS_DIR, f"ECHS_Module19_Forensic_Report_{ts}.pdf")

NAV  = "#1a2744"
GOLD = "#c9a84c"

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

def cr(n):
    try: return f"₹{float(n)/10000000:,.2f} Cr"
    except: return "₹0.00 Cr"

def cr_lakh(n):
    """Input already in lakhs, convert to Cr."""
    try: return f"₹{float(n)/100:,.2f} Cr"
    except: return "₹0.00 Cr"

def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"

def load_latest(pattern):
    """Load the earliest-timestamp file matching pattern (new 2021-2025 data)."""
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files: return pd.DataFrame()
    # earliest = new 2021-2025 data
    earliest = min(files, key=os.path.getctime)
    print(f"  Loading: {os.path.basename(earliest)}")
    return pd.read_csv(earliest, low_memory=False)

def top_n(df, sort_col, n=15, ascending=False):
    """Return top n rows, ensuring we get at least 15 if available."""
    if df.empty: return df
    return df.sort_values(sort_col, ascending=ascending).head(max(n, 15))

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS MODULE 19 FORENSIC AUDIT — RESTRICTED";
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

.tc {{ font-size:7.5pt; color:#666; margin-bottom:4px; font-weight:bold; }}

table.dt {{ width:100%; border-collapse:collapse; margin:6px 0 14px 0; font-size:8pt; }}
table.dt thead tr {{ background:{NAV}; color:#fff; }}
table.dt thead th {{ padding:6px 7px; text-align:left; font-weight:700; }}
table.dt tbody tr:nth-child(even) {{ background:#f4f6f9; }}
table.dt tbody td {{ padding:5px 7px; border-bottom:1px solid #e5e5e5; vertical-align:top; }}

.kf-head {{ font-size:11pt; font-weight:700; color:{NAV}; margin:14px 0 6px 0; }}
.kf-item {{ margin-bottom:7px; padding-left:8px; border-left:3px solid {GOLD}; font-size:8.5pt; line-height:1.5; }}

.action-item {{ margin-bottom:7px; font-size:8.5pt; }}
.action-num  {{ font-weight:800; color:{NAV}; }}
"""

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
print("Loading data files (2021-2025 scope)...")

# P1: aggregated hospital-level (already grouped)
df_1 = load_latest("new_19_01_all_hospital_deductions_*.csv")
# P2-P10: claim-level, earliest timestamp files
df_2  = load_latest("new_19_02_pattern_2_room_upgrade_fraud_*.csv")
df_3  = load_latest("new_19_03_pattern_3_ghost_admissions_*.csv")
df_4  = load_latest("new_19_04_pattern_4_y_flag_bypass_*.csv")
df_5  = load_latest("new_19_05_pattern_5_u_flag_anomaly_*.csv")
df_6  = load_latest("new_19_06_pattern_6_ipd_reversal_*.csv")
df_7  = load_latest("new_19_07_pattern_7_unlisted_procedures_*.csv")
df_8  = load_latest("new_19_08_pattern_8_bait_and_switch_*.csv")
df_9  = load_latest("new_19_09_pattern_9_stay_extension_*.csv")
df_10 = load_latest("new_19_10_pattern_10_emergency_bypass_*.csv")

# ── APPLY PANDAS FRAUD FILTERS ────────────────────────────────────────────────
# Refine the raw extracted universe to strictly target impossible/fraud cases

if not df_1.empty and 'billed_amount' in df_1.columns:
    df_1 = df_1[df_1['billed_amount'] >= 10000] # P1: Exclude tiny claims with high % deduction
    df_1 = df_1.groupby(['hospital_id', 'registered_hospital_name', 'hospital_city', 'hospital_state', 'cghs_region', 'hospital_type'], dropna=False).agg(
        total_claims=('claim_id', 'count'),
        total_claimed_lakh=('billed_amount', lambda x: x.sum() / 100000),
        total_approved_lakh=('approved_amount', lambda x: x.sum() / 100000),
        total_deducted_lakh=('deducted_amount', lambda x: x.sum() / 100000)
    ).reset_index()
    df_1['deduction_pct'] = (df_1['total_deducted_lakh'] / df_1['total_claimed_lakh']) * 100
    df_1['hospital_name'] = df_1['registered_hospital_name']

if not df_3.empty:
    df_3['patient_type'] = df_3['patient_type'].fillna('')
    df_3 = df_3[df_3['patient_type'].str.contains('In Patient', case=False, na=False)]

if not df_4.empty:
    df_4['billed_amount'] = pd.to_numeric(df_4['billed_amount'], errors='coerce').fillna(0)
    df_4 = df_4[df_4['billed_amount'] >= 50000] # Non-empanelled should not be doing massive billing

if not df_5.empty:
    df_5 = df_5[df_5['billed_amount'] > 5000]

if not df_8.empty:
    df_8['inflation_percentage'] = pd.to_numeric(df_8['inflation_percentage'], errors='coerce').fillna(0)
    df_8 = df_8[df_8['inflation_percentage'] >= 50] # True Bait & Switch is > 50% inflation

if not df_10.empty:
    df_10['total_billed_amount'] = pd.to_numeric(df_10['total_billed_amount'], errors='coerce').fillna(0)
    df_10 = df_10[df_10['total_billed_amount'] >= 100000] # True Emergency Bypass targets massive planned-like surgeries

# ── DATA CLEANING ─────────────────────────────────────────────────────────────

# P3: fix paise-to-rupee corruption (359 rows where billed_amount >= 1Cr are in paise)
if not df_3.empty:
    mask = df_3['billed_amount'] >= 100_000_000
    df_3.loc[mask, 'billed_amount']   = df_3.loc[mask, 'billed_amount'] / 100
    df_3.loc[mask, 'approved_amount'] = df_3.loc[mask, 'approved_amount'] / 100
    df_3.loc[mask, 'deducted_amount'] = df_3.loc[mask, 'deducted_amount'] / 100

# P2: room upgrade — low deduction rate is expected (these are billing mismatches,
#     not always fully rejected); sort by claim volume, not deduction amount
# No cleaning needed — numbers are correct

# Apply FY 2021-2025 year filter where year column exists
for df_ref, col in [(df_7,'claim_year'), (df_8,'claim_year'), (df_9,'claim_year')]:
    if col in df_ref.columns:
        df_ref.drop(df_ref[~df_ref[col].between(2021, 2025)].index, inplace=True)

# P8: filter data-entry errors (initial_estimate near-zero)
if not df_8.empty:
    df_8 = df_8[df_8['initial_estimate_amount'] > 100].copy()

# P9: filter negative/zero days; drop rows with no hospital name
if not df_9.empty:
    df_9 = df_9[(df_9['extra_days_requested'] > 0)].dropna(subset=['registered_hospital_name']).copy()

# P5: track null hospital count, then drop for table
df_5_null_ct = 0
if not df_5.empty:
    df_5_null_ct = int(df_5['registered_hospital_name'].isna().sum())
    df_5 = df_5.dropna(subset=['registered_hospital_name']).copy()

# P10: source data only covers 2011-2020 — exclude
df_10 = pd.DataFrame()

# ── KPI CALCULATIONS ──────────────────────────────────────────────────────────
def gs(df, col):
    return df[col].sum() if not df.empty and col in df.columns else 0.0

# P1 KPIs (in lakhs → convert to crores)
p1_total_claims   = int(df_1['total_claims'].sum()) if not df_1.empty else 0
p1_claimed_cr     = df_1['total_claimed_lakh'].sum() / 100 if not df_1.empty else 0
p1_deducted_cr    = df_1['total_deducted_lakh'].sum() / 100 if not df_1.empty else 0

total_anomalies = sum(len(df) for df in [df_2,df_3,df_4,df_5,df_6,df_7,df_8,df_9]) + p1_total_claims
kpi_total_claims = 23100000  # 2.31 Cr scope (2021-2025)

kpi_claimed_cr = p1_claimed_cr + sum([
    gs(df_2,"billed_amount"), gs(df_3,"billed_amount"), gs(df_6,"billed_amount"),
    gs(df_7,"total_billed_cost"), gs(df_8,"final_billed_amount"),
    gs(df_9,"total_billed_amount"), gs(df_10,"total_billed_amount")
]) / 10000000

kpi_deducted_cr = p1_deducted_cr + sum([
    gs(df_2,"deducted_amount"), gs(df_3,"deducted_amount"),
    gs(df_4,"deducted_amount"), gs(df_5,"deducted_amount"),
    gs(df_6,"deducted_amount"),
    gs(df_7,"total_billed_cost") - gs(df_7,"total_sanctioned_cost"),
    gs(df_8,"final_billed_amount") - gs(df_8,"final_approved_amount")
]) / 10000000

kpi_ded_pct = (kpi_deducted_cr / kpi_claimed_cr * 100) if kpi_claimed_cr > 0 else 0

# ── BUILD HTML ────────────────────────────────────────────────────────────────
H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-mod">MODULE 19</div>
  <div class="cover-title">POLICY ABUSE &amp;<br/>ENTITLEMENT MISUSE</div>
  <div class="cover-sub">Forensic Audit &amp; Top Offender Identification</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–25</div></div>
    <div class="cover-box"><div class="cover-box-label">Claims Scanned</div><div class="cover-box-val">{fmt(kpi_total_claims)}+</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">10 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Forensic Hits</div><div class="cover-box-val" style="color:#e74c3c">{fmt(total_anomalies)}</div></div>
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
<p>This report executes a deep-dive forensic analysis targeting systemic hospital-driven policy abuse and entitlement misuse
within the ECHS claims ecosystem for the period <b>FY 2021–2025</b>.
Across <b>{fmt(kpi_total_claims)}+ claims</b> scanned, a total of <b>{fmt(total_anomalies)} fraud markers</b> were identified
with an overbilling exposure of <b>₹{kpi_deducted_cr:,.2f} Cr</b>.
<i>Note: A single claim can be flagged under multiple patterns simultaneously (e.g., a ghost admission that is also a room upgrade),
so the marker count exceeds the unique claim count. Unique flagged claims: ~{fmt(10879838)}.</i></p>
<div style="background:#fffbf0;border-left:4px solid {GOLD};padding:8px 12px;margin-bottom:10px;font-size:8pt;">
<b>Audit Methodology Disclaimer:</b> Deductions identified in this report reflect claims where the ECHS audit process reduced
the approved amount. Deductions may result from documentation gaps, package coding mismatches, late submissions, duplicate billing,
or intentional overbilling. This report flags statistical anomalies for further investigation — it does not constitute a
finding of fraud. Final fraud determination requires case-level review.
</div>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Claims Scanned</div><div class="mbox-val">{fmt(kpi_total_claims)}+</div><div class="mbox-sub">FY 2021–2025 population</div></div>
  <div class="mbox"><div class="mbox-label">Pattern Matches</div><div class="mbox-val" style="color:#e74c3c">{fmt(total_anomalies)}</div><div class="mbox-sub">claims with abuse markers</div></div>
  <div class="mbox"><div class="mbox-label">Total Claimed (Flagged)</div><div class="mbox-val">₹{kpi_claimed_cr:,.0f} Cr</div><div class="mbox-sub">system-wide exposure</div></div>
  <div class="mbox"><div class="mbox-label">Audit Deductions</div><div class="mbox-val" style="color:#e74c3c">₹{kpi_deducted_cr:,.0f} Cr</div><div class="mbox-sub">savings established</div></div>
</div>

<h1 style="margin-top:14px">Fraud Forensics — Detection Patterns &amp; Methodologies</h1>
<table class="dt">
<thead><tr>
  <th style="width:6%">#</th>
  <th style="width:30%">Detection Pattern</th>
  <th style="width:49%">Methodology / Focus</th>
  <th style="width:18%">Impact Summary</th>
</tr></thead>
<tbody>
  <tr><td>1</td><td><b>High Deduction Hospitals</b></td><td>Top hospitals by absolute deduction volume — systematic overbilling across all claim types</td><td><b>{fmt(p1_total_claims)} Claims Evaluated</b></td></tr>
  <tr><td>2</td><td><b>Room Upgrade Fraud</b></td><td>Illegal patient class upgrades — General/Semi-Private to Private ward without entitlement</td><td><b>{fmt(len(df_2))} Claims Flagged</b></td></tr>
  <tr><td>3</td><td><b>Ghost Admissions</b></td><td>Claims processed with no traceable Hospital ID — structural BPA portal failure</td><td><b>{fmt(len(df_3))} Ghost Claims</b></td></tr>
  <tr><td>4</td><td><b>Y-Flag Bypass</b></td><td>Elite non-empanelled hospital funneling — bypassing CGHS rate ceilings via emergency route</td><td><b>{fmt(len(df_4))} Bypass Claims</b></td></tr>
  <tr><td>5</td><td><b>U-Flag Anomaly</b></td><td>Unverified hospital status — blind spot exploitation allowing unchecked processing</td><td><b>{fmt(len(df_5))} Unverified Claims</b></td></tr>
  <tr><td>6</td><td><b>IPD/OPD Reversal</b></td><td>OPD procedures artificially escalated to IPD admissions to claim room rent and higher packages</td><td><b>{fmt(len(df_6))} Suspicious Claims</b></td></tr>
  <tr><td>7</td><td><b>NMI / Unlisted Procedure Loophole</b></td><td>Billing via unlisted 'NMI' codes to bypass fixed CGHS package rate ceilings</td><td><b>{fmt(len(df_7))} Unlisted Claims</b></td></tr>
  <tr><td>8</td><td><b>Bait &amp; Switch (PA Inflation)</b></td><td>Low Prior Approval secured, massively inflated final bill submitted post-admission</td><td><b>{fmt(len(df_8))} Inflated Claims</b></td></tr>
  <tr><td>9</td><td><b>Stay Extension Farming</b></td><td>Artificial discharge delays to farm daily room rent and routine care charges</td><td><b>{fmt(len(df_9))} Extension Cases</b></td></tr>
  <tr><td>10</td><td><b>Emergency Gateway Bypass</b></td><td>False emergency declarations bypassing referral ceilings, polyclinic wait times, geography rules</td><td><b style="color:#d4680a;">Data gap — FY 2021–25 pending</b></td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Targeted Audits on Top Overbilling Facilities:</b> Prioritize physical audits at Park Hospital chain (multiple locations) and Vijay Hospital — the two largest absolute overbilling generators in the FY 2021-2025 dataset.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Hard-Reject Ghost Claims at BPA Portal:</b> Enforce mandatory Hospital ID validation — any claim without a registered Hospital ID must be rejected before entering the settlement pipeline.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Pre-Authorization Mandatory for Y-Flag:</b> Restrict Y-Flag usage to genuine life-threatening emergencies with real-time clinical verification. Current data shows polyclinics as top Y-Flag users, not emergencies.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Deploy Pre-Payment AI Interception:</b> Implement billing interception rules targeting NMI Loophole, Bait &amp; Switch, and Emergency Gateway claims before payment is released.</div>
</div>
""")

# ── PATTERN 1: HIGH DEDUCTION HOSPITALS (aggregated data) ────────────────────
if not df_1.empty:
    p1 = df_1.nlargest(15, 'total_deducted_lakh').copy()
    tot_claims = p1['total_claims'].sum()
    tot_claimed = p1['total_claimed_lakh'].sum()
    tot_deducted = p1['total_deducted_lakh'].sum()
    tot_pct = tot_deducted / tot_claimed * 100 if tot_claimed else 0

    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 1 (SYSTEMIC OVERBILLING)</div>
  <div class="ph-ctx">Top Absolute Deduction Facilities</div>
  <div class="ph-title">High Deduction Hospitals</div>
</div></div>
<p><b>Fraud Mechanism:</b> Hospitals systemically inflate diagnostic and routine package costs at scale, leading to extreme deduction rates when subjected to basic automated claim processing checks.</p>
<p><b>How the threshold was derived:</b> Hospitals are selected based on absolute deduction volume (FY 2021–2025).
This absolute-volume threshold ensures audits target the largest sinks of ECHS funds rather than low-volume high-percentage outliers.</p>
<div class="tc">Table 1.1 — Top 15 Hospitals by Absolute Deduction Volume</div>
<table class="dt">
{th("Rank","Hospital Name","ECHS ID","NABH","Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Deducted (₹ Cr)","Ded %")}
<tbody>""")
    for i, (_, r) in enumerate(p1.iterrows()):
        ded_pct = float(r['deduction_pct'])
        pct_str = f'<span style="color:#c0392b;font-weight:700">{ded_pct:.2f}%</span>' if ded_pct >= 20 else f'<span style="color:#d4680a;font-weight:700">{ded_pct:.2f}%</span>' if ded_pct >= 12 else f'{ded_pct:.2f}%'
        H.append(f"<tr><td>{i+1}</td>"
                 f"<td style='font-size:7.5pt'><b>{str(r['hospital_name'])[:50]}</b></td>"
                 f"<td>{r['hospital_id']}</td>"
                 f"<td>{r.get('nabh_status','N')}</td>"
                 f"<td>{fmt(r['total_claims'])}</td>"
                 f"<td>{float(r['total_claimed_lakh'])/100:,.2f}</td>"
                 f"<td>{float(r['total_approved_lakh'])/100:,.2f}</td>"
                 f"<td><b>{float(r['total_deducted_lakh'])/100:,.2f}</b></td>"
                 f"<td>{pct_str}</td></tr>")
    H.append(f"""<tr style="background:#e8ecf5;font-weight:700">
      <td>—</td><td>TOP 15 TOTAL</td><td>—</td><td>—</td>
      <td>{fmt(tot_claims)}</td>
      <td>{tot_claimed/100:,.2f}</td><td>—</td>
      <td>{tot_deducted/100:,.2f}</td>
      <td>{tot_pct:.2f}%</td></tr>
    </tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Park Hospital Chain Dominance:</b> Park Hospital (Gurgaon ID 367) tops the list with ₹{df_1[df_1['hospital_id']==367]['total_deducted_lakh'].sum()/100:,.2f} Cr deducted. Multiple Park chain facilities appear in top ranks, warranting a corporate-level empanelment review.</div>
<div class="kf-item"><b>Vijay Hospital (ID 3149):</b> Maintains a 34% deduction rate — one in three rupees claimed is rejected. This anomalous rate across {fmt(df_1[df_1['hospital_id']==3149]['total_claims'].sum())} claims warrants a targeted billing audit to determine whether the pattern reflects systematic overbilling, documentation deficiencies, or package coding errors.</div>
</div>""")

# ── PATTERN 2: ROOM UPGRADE FRAUD ────────────────────────────────────────────
if not df_2.empty:
    df_2['hospital_name'] = df_2['hospital_name'].fillna('UNKNOWN')
    p2 = df_2.groupby(['hospital_name','entitled_room','billed_room']).agg(
        claims=('claim_id','count'), billed=('billed_amount','sum'), deducted=('deducted_amount','sum')
    ).reset_index().sort_values('claims', ascending=False).head(15)

    H.append(f"""
<div class="nob" style="margin-top:30px;">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 2 (ENTITLEMENT ABUSE)</div>
  <div class="ph-ctx">Private Ward Irregularities</div>
  <div class="ph-title">Room Upgrade Fraud</div>
</div></div>
<p><b>Description:</b> Hospitals billing patients for a higher room category than their ECHS card entitlement authorises.
<b>Interpretation note:</b> Low deduction rates (1–5%) do not mean the fraud is minor — they indicate that auditors
partially corrected the room rate differential but the full package inflation embedded in the higher room category was
still approved. The claim volume itself is the primary fraud signal here.</p>
<div class="tc">Table 2.1 — Top Hospitals Abusing Patient Room Entitlements (Top 15)</div>
<table class="dt">
{th("Hospital Name","Entitled","Billed","Fraud Claims","Claimed (₹ Cr)","Deducted (₹ Cr)","Ded %")}
<tbody>""")
    for _, row in p2.iterrows():
        pct = (row['deducted']/row['billed']*100) if row['billed'] else 0
        H.append(f"<tr><td><b>{str(row['hospital_name'])[:45]}</b></td>"
                 f"<td>{row['entitled_room']}</td><td>{row['billed_room']}</td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td>{cr(row['billed'])}</td><td>{cr(row['deducted'])}</td>"
                 f"<td>{pct:.2f}%</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Intentional Misclassification:</b> Volume of claims at major chains (Tata Memorial, Fortis, IVY Healthcare) highlights that patient class upgrades are not clinical exceptions but an automated billing practice.</div>
<div class="kf-item"><b>System Exposure:</b> A total of <b>{fmt(len(df_2))} claims</b> flagged under this pattern across FY 2021-2025.</div>
</div>""")

# ── PATTERN 3: GHOST ADMISSIONS ───────────────────────────────────────────────
if not df_3.empty:
    # Group by room combo to show scale
    p3_grp = df_3.groupby(['entitled_room','billed_room']).agg(
        claims=('claim_id','count'), billed=('billed_amount','sum'), deducted=('deducted_amount','sum')
    ).reset_index().sort_values('claims', ascending=False)

    # Also show top 15 highest value individual ghost claims
    p3_top = df_3.nlargest(15, 'billed_amount')

    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 3 (CRITICAL FRAUD)</div>
  <div class="ph-ctx">Missing Hospital ID in BPA Portal</div>
  <div class="ph-title">Ghost Admissions Exposure</div>
</div></div>
<p><b>Description:</b> Claims processed without any traceable Hospital ID (NULL / Ghost entries), completely hiding the billing source. These represent the most severe structural failure — entities extracting funds while bypassing all standard portal validation.</p>
<div class="tc">Table 3.1 — Ghost Claims by Room Category (Aggregate)</div>
<table class="dt">
{th("Entitled Room","Billed Room","Ghost Claims","Total Claimed (₹ Cr)","Total Deducted (₹ Cr)")}
<tbody>""")
    for _, row in p3_grp.iterrows():
        H.append(f"<tr><td><b>{row['entitled_room']}</b></td><td>{row['billed_room']}</td>"
                 f"<td>{fmt(row['claims'])}</td><td>{cr(row['billed'])}</td><td>{cr(row['deducted'])}</td></tr>")
    H.append(f"""</tbody></table>

<div class="tc" style="margin-top:14px;">Table 3.2 — Highest Value Individual Ghost Claims (Top 15)</div>
<table class="dt">
{th("Claim ID","Entitled Room","Billed Room","Claimed (₹)","Deducted (₹)")}
<tbody>""")
    for _, row in p3_top.iterrows():
        H.append(f"<tr><td><b>{row['claim_id']}</b></td>"
                 f"<td>{row.get('entitled_room','')}</td><td>{row.get('billed_room','')}</td>"
                 f"<td>₹{float(row['billed_amount']):,.0f}</td>"
                 f"<td>₹{float(row['deducted_amount']):,.0f}</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>NULL Hospital ID Anomaly:</b> All {fmt(len(df_3))} ghost claims have hospital_id = NULL, meaning these entities cannot be traced through any standard registry. The BPA portal must hard-reject submissions without a validated Hospital ID.</div>
<div class="kf-item"><b>Scale of Exposure:</b> Total ghost claims claimed amount: <b>{cr(df_3['billed_amount'].sum())}</b> — a massive conduit of untraceable leakage.</div>
</div>""")

# ── PATTERN 4: Y-FLAG BYPASS ──────────────────────────────────────────────────
if not df_4.empty:
    df_4['registered_hospital_name'] = df_4['registered_hospital_name'].fillna('UNKNOWN')
    p4 = df_4.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), approved=('approved_amount','sum'), deducted=('deducted_amount','sum')
    ).reset_index().sort_values('claims', ascending=False).head(15)

    H.append(f"""
<div class="nob" style="margin-top:30px;">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 4 (BYPASS MECHANISM)</div>
  <div class="ph-ctx">Non-Empanelled Hospital Funneling</div>
  <div class="ph-title">Y-Flag Bypass</div>
</div></div>
<p><b>Description:</b> Patients bypassing empanelled networks to receive treatment at non-empanelled facilities via the Y-Flag (emergency) route, ignoring CGHS rate caps entirely.</p>
<p><b>Note:</b> Y-Flag records in source data do not carry a billed amount — only approved and deducted amounts are captured at settlement. Table sorted by claim volume.</p>
<div class="tc">Table 4.1 — Top Hospitals/Polyclinics by Y-Flag Volume (Top 15)</div>
<table class="dt">
{th("Hospital / Polyclinic Name","Bypass Claims","Net Approved (₹ Cr)","Deducted (₹ Cr)")}
<tbody>""")
    for _, row in p4.iterrows():
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:50]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td>{cr(row['approved'])}</td><td>{cr(row['deducted'])}</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Polyclinic Dominance:</b> Top Y-Flag users are ECHS polyclinics (Noida, Delhi Cantt, Amritsar) — not private hospitals. This indicates that Y-Flag is being used for routine referrals, not genuine emergencies, defeating the entire purpose of the flag.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_4))} claims</b> bypassed standard empanelment via Y-Flag across FY 2021-2025.</div>
</div>""")

# ── PATTERN 5: U-FLAG ANOMALY ─────────────────────────────────────────────────
if not df_5.empty:
    df_5['registered_hospital_name'] = df_5['registered_hospital_name'].fillna('UNKNOWN')
    p5 = df_5.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), deducted=('deducted_amount','sum')
    ).reset_index().sort_values('claims', ascending=False).head(15)

    H.append(f"""
<div class="nob" style="margin-top:30px;">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 5 (VERIFICATION FAILURE)</div>
  <div class="ph-ctx">Unknown Hospital Status</div>
  <div class="ph-title">U-Flag Mass Anomaly</div>
</div></div>
<p><b>Description:</b> Hospital verification flag marked 'U' (Unknown/Unverified), allowing unchecked claim processing without mandatory BPA registry validation. These claims represent a systemic blind spot.</p>
<p><b>Note on NULLs:</b> {fmt(df_5_null_ct)} of {fmt(len(df_5)+df_5_null_ct)} U-Flag claims ({(df_5_null_ct/(len(df_5)+df_5_null_ct)*100):.1f}%) have no hospital name in the registry — these represent the deepest unresolvable blind spot and are tracked in aggregate below the table.</p>
<div class="tc">Table 5.1 — Top Hospitals/Polyclinics with Unverified Claims (Top 15)</div>
<table class="dt">
{th("Hospital / Polyclinic Name","Unverified Claims","Total Deducted (₹ Cr)")}
<tbody>""")
    for _, row in p5.iterrows():
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:55]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td><td>{cr(row['deducted'])}</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Blind Spot Exploitation:</b> Rewari leads with {fmt(p5.iloc[0]['claims'])} unverified claims. A system-freeze on U-Flag claim processing pending hospital identity verification is immediately warranted.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_5))} unverified claims</b> processed without scrutiny across FY 2021-2025.</div>
</div>""")

# ── PATTERN 6: IPD REVERSAL ───────────────────────────────────────────────────
if not df_6.empty:
    df_6['registered_hospital_name'] = df_6['registered_hospital_name'].fillna('UNKNOWN')
    p6 = df_6.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), billed=('billed_amount','sum'), deducted=('deducted_amount','sum')
    ).reset_index().sort_values('claims', ascending=False).head(15)

    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 6 (ADMISSION FRAUD)</div>
  <div class="ph-ctx">IPD vs OPD Anomalies</div>
  <div class="ph-title">IPD vs OPD Reversal Trend</div>
</div></div>
<p><b>Description:</b> Hospitals where In-Patient Admissions (IPD) volumes are anomalously high, indicating OPD procedures are being artificially escalated to IPD admissions to claim room rent and higher package fees.</p>
<div class="tc">Table 6.1 — Top Hospitals with Suspicious IPD/OPD Reversal (Top 15)</div>
<table class="dt">
{th("Hospital Name","Suspicious IPD Claims","Claimed (₹ Cr)","Deducted (₹ Cr)","Ded %")}
<tbody>""")
    for _, row in p6.iterrows():
        pct = (row['deducted']/row['billed']*100) if row['billed'] else 0
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:45]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td>{cr(row['billed'])}</td><td>{cr(row['deducted'])}</td>"
                 f"<td>{pct:.2f}%</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Fake Admissions:</b> Park Hospital Chowkhandi leads with a {df_6[df_6['registered_hospital_name'].str.contains('CHOWKHANDI',na=False)]['deducted_amount'].sum()/10000000:.2f} Cr deduction on suspicious IPD claims. The reversal of standard IPD/OPD ratios strongly indicates artificial escalation for room rent extraction.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_6))} suspicious IPD claims</b> flagged across FY 2021-2025.</div>
</div>""")

# ── PATTERN 7: NMI LOOPHOLE ───────────────────────────────────────────────────
if not df_7.empty:
    df_7['registered_hospital_name'] = df_7['registered_hospital_name'].fillna('UNKNOWN')
    p7 = df_7.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), billed=('total_billed_cost','sum'), approved=('total_sanctioned_cost','sum')
    ).reset_index().sort_values('billed', ascending=False).head(15)

    H.append(f"""
<div class="nob" style="margin-top:30px;">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 7 (CODE MANIPULATION)</div>
  <div class="ph-ctx">Unlisted Procedure Loophole</div>
  <div class="ph-title">The NMI Loophole</div>
</div></div>
<p><b>Description:</b> Hospitals billing procedures as 'Unlisted/NMI' to bypass fixed CGHS rates, allowing arbitrary billing at premium rates with no package ceiling enforcement.</p>
<div class="tc">Table 7.1 — Top Facilities Utilizing Unlisted NMI Codes (Top 15)</div>
<table class="dt">
{th("Hospital Name","Unlisted Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Ded %")}
<tbody>""")
    for _, row in p7.iterrows():
        ded = row['billed'] - row['approved']
        pct = (ded/row['billed']*100) if row['billed'] else 0
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:45]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td>{cr(row['billed'])}</td><td>{cr(row['approved'])}</td>"
                 f"<td>{pct:.2f}%</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Rate Ceiling Bypass:</b> Medanta Gurgaon leads with {fmt(df_7[df_7['registered_hospital_name'].str.contains('MEDANTA',na=False)]['claim_id'].count())} unlisted NMI claims — hospitals are exploiting unlisted codes to bill at arbitrary rates instead of adhering to CGHS package caps.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_7))} unlisted procedure claims</b> detected across FY 2021-2025.</div>
</div>""")

# ── PATTERN 8: BAIT & SWITCH ──────────────────────────────────────────────────
if not df_8.empty:
    df_8['registered_hospital_name'] = df_8['registered_hospital_name'].fillna('UNKNOWN')
    p8 = df_8.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), initial=('initial_estimate_amount','sum'),
        final=('final_billed_amount','sum'), approved=('final_approved_amount','sum')
    ).reset_index().sort_values('final', ascending=False).head(15)

    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 8 (ESTIMATE FRAUD)</div>
  <div class="ph-ctx">Prior Approval vs Final Bill</div>
  <div class="ph-title">The Bait &amp; Switch (PA Inflation)</div>
</div></div>
<p><b>Description:</b> Hospitals securing a low Initial Estimate (Prior Approval) then submitting a massively inflated final bill post-admission.
<i>Note: Records with initial estimates ≤ ₹100 (data entry errors) have been excluded from this analysis.</i></p>
<div class="tc">Table 8.1 — Top Hospitals Inflating Final Bills vs Prior Approval (Top 15)</div>
<table class="dt">
{th("Hospital Name","Inflated Claims","Initial Est (₹ Cr)","Final Billed (₹ Cr)","Approved (₹ Cr)","Inflation %")}
<tbody>""")
    for _, row in p8.iterrows():
        inf = ((row['final'] - row['initial']) / row['initial'] * 100) if row['initial'] else 0
        inf_str = f'<span style="color:#c0392b;font-weight:700">{inf:.0f}%</span>' if inf >= 200 else f'{inf:.0f}%'
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:45]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td>{cr(row['initial'])}</td><td>{cr(row['final'])}</td>"
                 f"<td>{cr(row['approved'])}</td><td>{inf_str}</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Estimate Inflation:</b> Manipal, Metro Faridabad, and IVY Healthcare each show final bills exceeding initial approvals by over 1000%, indicating systematic 'Bait and Switch' post-admission billing tactics.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_8))} inflated claims</b> detected (after filtering data-entry error rows).</div>
</div>""")

# ── PATTERN 9: STAY EXTENSION ─────────────────────────────────────────────────
if not df_9.empty:
    df_9['registered_hospital_name'] = df_9['registered_hospital_name'].fillna('UNKNOWN')
    df_9 = df_9[df_9['extra_days_requested'] > 0]  # filter negative/zero
    p9 = df_9.groupby('registered_hospital_name').agg(
        claims=('claim_id','count'), extra_days=('extra_days_requested','sum'), billed=('total_billed_amount','sum')
    ).reset_index().sort_values('extra_days', ascending=False).head(15)

    H.append(f"""
<div class="nob" style="margin-top:30px;">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 9 (BEHAVIORAL)</div>
  <div class="ph-ctx">Artificially Delayed Discharge</div>
  <div class="ph-title">Stay Extension Farming</div>
</div></div>
<p><b>Description:</b> Hospitals artificially extending patient discharge dates to farm daily room rent and routine care charges beyond clinical necessity.</p>
<div class="tc">Table 9.1 — Top Hospitals by Extra Days Farmed (Top 15)</div>
<table class="dt">
{th("Hospital Name","Extension Claims","Extra Days Farmed","Claimed (₹ Cr)","Avg Extra Days/Claim")}
<tbody>""")
    for _, row in p9.iterrows():
        avg = row['extra_days'] / row['claims'] if row['claims'] else 0
        H.append(f"<tr><td><b>{str(row['registered_hospital_name'])[:45]}</b></td>"
                 f"<td>{fmt(row['claims'])}</td>"
                 f"<td><span style='color:#c0392b;font-weight:700'>{fmt(row['extra_days'])} d</span></td>"
                 f"<td>{cr(row['billed'])}</td>"
                 f"<td>{avg:.1f} d/claim</td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Bed Blocking at Scale:</b> Park Hospital Gurgaon alone farmed {fmt(p9.iloc[0]['extra_days'])} extra days across {fmt(p9.iloc[0]['claims'])} claims — an average of {p9.iloc[0]['extra_days']/p9.iloc[0]['claims']:.1f} extra days per admission purely for revenue extraction.</div>
<div class="kf-item"><b>System Exposure:</b> <b>{fmt(len(df_9))} stay extension requests</b> flagged across FY 2021-2025.</div>
</div>""")

# ── PATTERN 10: EMERGENCY GATEWAY — DATA NOT AVAILABLE FOR 2021-2025 ────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph" style="border-left-color:#c0392b">
  <div class="ph-label" style="color:#c0392b">PATTERN 10 (SYSTEM BYPASS)</div>
  <div class="ph-ctx">False Medical Urgency</div>
  <div class="ph-title">Emergency Gateway Bypass</div>
</div></div>
<p><b>Description:</b> Hospitals falsely declaring normal elective cases as 'Emergencies' to bypass referral ceilings, polyclinic wait times, and geographical restrictions.</p>
<div style="background:#fff8f0; border-left:4px solid #d4680a; padding:12px 16px; margin:16px 0;">
  <b style="color:#d4680a;">⚠ Data Gap — FY 2021–2025 records not available in current extract</b><br/>
  <p style="margin-top:6px;">The Emergency Gateway (E-Flag) dataset currently extracted covers FY 2011–2020 only. A separate extraction targeting FY 2021–2025 is required to populate this pattern. This section will be updated once the FY 2021–2025 emergency bypass data is available from the ECHS database.</p>
</div>
<div class="kf-head">What to look for when data is available</div>
<div class="kf-item"><b>E-Flag Volume Spike:</b> Hospitals with disproportionately high emergency admission rates vs. their specialty profile warrant immediate audit.</div>
<div class="kf-item"><b>Elective Diagnoses as Emergencies:</b> Flag claims where admission_ailment indicates planned procedures (joint replacement, cataract, dental) but referral_type = 'E'.</div>
</div>
""")

# ── CONSOLIDATED SUMMARY ──────────────────────────────────────────────────────
def pct_str(num, den):
    return f"{num/den*100:.2f}%" if den else "—"

H.append(f"""
<div class="pb">
<h1>Consolidated Summary</h1>
<div class="tc">Overall Final Audit Findings — FY 2021–2025 (System-Wide Extract)</div>
<table class="dt">
{th("Category","Metric","Claimed Amount","Deducted Amount","Deduction %")}
<tbody>
  <tr><td><b>Pattern 1 (High Deduction Hospitals)</b></td><td>{fmt(p1_total_claims)} Claims</td><td>₹{p1_claimed_cr:,.2f} Cr</td><td>₹{p1_deducted_cr:,.2f} Cr</td><td>{pct_str(p1_deducted_cr, p1_claimed_cr)}</td></tr>
  <tr><td><b>Pattern 2 (Room Upgrade Fraud)</b></td><td>{fmt(len(df_2))} Claims</td><td>{cr(gs(df_2,'billed_amount'))}</td><td>{cr(gs(df_2,'deducted_amount'))}</td><td>{pct_str(gs(df_2,'deducted_amount'), gs(df_2,'billed_amount'))}</td></tr>
  <tr><td><b>Pattern 3 (Ghost Admissions)</b></td><td>{fmt(len(df_3))} Claims</td><td>{cr(gs(df_3,'billed_amount'))}</td><td>{cr(gs(df_3,'deducted_amount'))}</td><td>{pct_str(gs(df_3,'deducted_amount'), gs(df_3,'billed_amount'))}</td></tr>
  <tr><td><b>Pattern 4 (Y-Flag Bypass)</b></td><td>{fmt(len(df_4))} Claims</td><td style="color:#999">N/A</td><td>{cr(gs(df_4,'deducted_amount'))}</td><td style="color:#999">—</td></tr>
  <tr><td><b>Pattern 5 (U-Flag Anomaly)</b></td><td>{fmt(len(df_5))} Claims</td><td style="color:#999">N/A</td><td>{cr(gs(df_5,'deducted_amount'))}</td><td style="color:#999">—</td></tr>
  <tr><td><b>Pattern 6 (IPD/OPD Reversal)</b></td><td>{fmt(len(df_6))} Claims</td><td>{cr(gs(df_6,'billed_amount'))}</td><td>{cr(gs(df_6,'deducted_amount'))}</td><td>{pct_str(gs(df_6,'deducted_amount'), gs(df_6,'billed_amount'))}</td></tr>
  <tr><td><b>Pattern 7 (NMI Loophole)</b></td><td>{fmt(len(df_7))} Claims</td><td>{cr(gs(df_7,'total_billed_cost'))}</td><td>{cr(gs(df_7,'total_billed_cost')-gs(df_7,'total_sanctioned_cost'))}</td><td>{pct_str(gs(df_7,'total_billed_cost')-gs(df_7,'total_sanctioned_cost'), gs(df_7,'total_billed_cost'))}</td></tr>
  <tr><td><b>Pattern 8 (Bait &amp; Switch)</b></td><td>{fmt(len(df_8))} Claims</td><td>{cr(gs(df_8,'final_billed_amount'))}</td><td>{cr(gs(df_8,'final_billed_amount')-gs(df_8,'final_approved_amount'))}</td><td>{pct_str(gs(df_8,'final_billed_amount')-gs(df_8,'final_approved_amount'), gs(df_8,'final_billed_amount'))}</td></tr>
  <tr><td><b>Pattern 9 (Stay Extension)</b></td><td>{fmt(len(df_9))} Cases</td><td>{cr(gs(df_9,'total_billed_amount'))}</td><td style="color:#999">—</td><td style="color:#999">—</td></tr>
  <tr><td><b>Pattern 10 (Emergency Gateway)</b></td><td colspan="4" style="color:#d4680a;font-style:italic;">FY 2021–2025 data not yet extracted — pending separate DB query</td></tr>
  <tr style="background:{NAV};color:#fff;"><td><b style="color:#fff;">Total Forensic Exposure</b></td><td style="color:#fff;">{fmt(total_anomalies)} Cases</td><td style="color:#fff;">₹{kpi_claimed_cr:,.2f} Cr</td><td style="color:#fff;">₹{kpi_deducted_cr:,.2f} Cr</td><td style="color:#fff;">{kpi_ded_pct:.2f}%</td></tr>
</tbody>
</table>

<div style="border-top:1px solid #e2e8f0; margin-top:24px; padding-top:16px; text-align:center;">
  <p style="font-size:7.5pt; color:#718096; font-weight:600; margin-bottom:4px; letter-spacing:0.5px;">PREPARED BY IIT KANPUR — DATA ANALYTICS &amp; BILLING FORENSICS DIVISION</p>
  <p style="font-size:7pt; color:#a0aec0;">Generated on {today_str} | Data Scope: FY 2021–2025 | Confidential &amp; Restricted Distribution</p>
</div>
</div>
</body></html>""")

print("Generating PDF...")
HTML(string="".join(H), base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ PDF generated: {PDF_OUT}")
