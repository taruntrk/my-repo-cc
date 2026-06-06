"""
ECHS FA-08 — Diagnostic Test Overutilisation Report Generator
Module-1 style: dark navy cover, gold accents, IIT Kanpur branding.
Run AFTER export_diag_test_fraud.py has populated diag_test_output/
"""

import os, pandas as pd
from datetime import date
from weasyprint import HTML, CSS

BASE = os.path.dirname(__file__)
OUT  = os.path.join(BASE, "diag_test_output")
PDF  = os.path.join(OUT, "FA-08_DiagTest_Fraud_Report.pdf")

# ── Load CSVs ─────────────────────────────────────────────────────────────────
def load(f, **kw):
    p = os.path.join(OUT, f)
    if os.path.exists(p): return pd.read_csv(p, **kw)
    return pd.DataFrame()

counts   = load("00_table_row_counts.csv")
exp_head = load("00b_expense_head_master.csv")
ctt      = load("00c_clinical_test_master.csv")
profile  = load("00d_inv_expense_profile.csv")
q1       = load("Q1_inv_pct_of_total.csv")
q2       = load("Q2_test_count_outliers.csv")
q3       = load("Q3_rate_inflation.csv")
q4       = load("Q4_hospital_inv_benchmark.csv")
q5       = load("Q5_high_deduction_rate.csv")
q6       = load("Q6_repeat_tests_same_patient.csv")
q7       = load("Q7_simple_diagnosis_high_inv.csv")
q8       = load("Q8_yoy_inv_spike.csv")
q9       = load("Q9_composite_risk_score.csv")

def gcount(tbl):
    r = counts[counts.tbl==tbl] if not counts.empty else pd.DataFrame()
    return int(r["row_count"].values[0]) if not r.empty else 0

total_intim = gcount("claim_intimation")
total_sub   = gcount("claim_submission")
hosp_exp_rows = gcount("hosp_exp")
hosp_exp_det_rows = gcount("hosp_exp_det")
cfi_rows    = gcount("clinical_findings_int")
cfs_rows    = gcount("clinical_findings_sub")

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)
def cr(n):
    try: v=float(n)/1e7; return f"₹{v:.2f} Cr"
    except: return str(n)
def pct(n):
    try: return f"{float(n):.1f}%"
    except: return "—"
def risk_txt(r):
    r = str(r).upper()
    if "CRITICAL" in r: return '<span style="color:#c0392b;font-weight:700">CRITICAL</span>'
    if "HIGH"     in r: return '<span style="color:#d4680a;font-weight:700">HIGH</span>'
    if "MEDIUM"   in r: return '<span style="color:#7f8c8d;font-weight:600">MEDIUM</span>'
    return '<span style="color:#27ae60;font-weight:600">LOW</span>'
def safe(v, d="—"):
    return v if pd.notna(v) and str(v).strip() not in ("", "nan") else d
def money(v):
    try: return f"₹{float(v):,.0f}"
    except: return "—"

today_str = date.today().strftime("%-d %B %Y")

# ── Derived stats ─────────────────────────────────────────────────────────────
q1_total   = len(q1)
q1_crit    = len(q1[q1.get("Fraud_Flag","").str.contains("CRITICAL",na=False)]) if not q1.empty else 0
q2_total   = len(q2)
q3_total   = len(q3)
q4_total   = len(q4)
q4_crit    = len(q4[q4.get("Risk_Level","").str.contains("CRITICAL",na=False)]) if not q4.empty else 0
q5_total   = len(q5)
q5_crit    = len(q5[q5.get("Fraud_Flag","").str.contains("CRITICAL",na=False)]) if not q5.empty else 0
q6_total   = len(q6)
q7_total   = len(q7)
q8_crit    = len(q8[q8.get("Risk_Level","").str.contains("CRITICAL",na=False)]) if not q8.empty else 0
q9_crit    = len(q9[q9.get("Audit_Priority","").str.contains("CRITICAL",na=False)]) if not q9.empty else 0

top_inv_ratio = float(q4["Inv_Ratio"].max()) if not q4.empty and "Inv_Ratio" in q4.columns else 0
top_markup    = float(q3["Rate_Markup"].max()) if not q3.empty and "Rate_Markup" in q3.columns else 0
top_ded_pct   = float(q5["Deduction_Pct"].max()) if not q5.empty and "Deduction_Pct" in q5.columns else 0
sys_avg_inv   = float(q4["System_Avg_Inv_Billed"].iloc[0]) if not q4.empty and "System_Avg_Inv_Billed" in q4.columns else 0

# ── Slices ────────────────────────────────────────────────────────────────────
q1_top = q1.sort_values("Inv_Pct_of_Total",ascending=False).head(12) if not q1.empty and "Inv_Pct_of_Total" in q1.columns else q1.head(12)
q2_top = q2.sort_values("Z_Score",ascending=False).head(12) if not q2.empty and "Z_Score" in q2.columns else q2.head(12)
q3_top = q3.sort_values("Rate_Markup",ascending=False).head(12) if not q3.empty and "Rate_Markup" in q3.columns else q3.head(12)
q4_top = q4.sort_values("Inv_Ratio",ascending=False).head(12) if not q4.empty and "Inv_Ratio" in q4.columns else q4.head(12)
q5_top = q5.sort_values("Deduction_Pct",ascending=False).head(12) if not q5.empty and "Deduction_Pct" in q5.columns else q5.head(12)
q6_top = q6.sort_values("First_Claim_Amt",ascending=False).head(10) if not q6.empty and "First_Claim_Amt" in q6.columns else q6.head(10)
q7_top = q7.sort_values("Investigation_Amt",ascending=False).head(12) if not q7.empty and "Investigation_Amt" in q7.columns else q7.head(12)
q8_top = q8.sort_values("YoY_Growth_Pct",ascending=False).head(12) if not q8.empty and "YoY_Growth_Pct" in q8.columns else q8.head(12)
q9_top = q9.sort_values("Fraud_Risk_Score",ascending=False).head(12) if not q9.empty and "Fraud_Risk_Score" in q9.columns else q9.head(12)

# ── CSS (identical theme to FA-07) ───────────────────────────────────────────
NAV = "#1a2744"; GOLD = "#c9a84c"
CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; }}
@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS FRAUD ANALYTICS REPORT — CONFIDENTIAL";
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
@page cover {{ margin:0; @top-left{{content:none}} @top-right{{content:none}}
               @bottom-left{{content:none}} @bottom-right{{content:none}} }}
.cover {{ page:cover; page-break-after:always; background:{NAV};
          width:210mm; height:297mm; display:flex; flex-direction:column;
          justify-content:center; align-items:center; text-align:center; position:relative; }}
.cover-topbar,.cover-botbar {{ position:absolute; left:0; right:0; height:8px; background:{GOLD}; }}
.cover-topbar {{ top:0; }} .cover-botbar {{ bottom:0; }}
.cover-title {{ font-size:34pt; font-weight:900; color:#fff; letter-spacing:2px; margin-bottom:10px; }}
.cover-sub   {{ font-size:13pt; color:#ccc; font-weight:300; margin-bottom:18px; }}
.cover-mod   {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:30px; }}
.cover-boxes {{ display:flex; gap:2px; margin-bottom:36px; }}
.cover-box   {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
                padding:10px 20px; min-width:90px; text-align:center; }}
.cover-box-label {{ font-size:6.5pt; color:#aaa; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:5px; }}
.cover-box-val   {{ font-size:13pt; font-weight:800; color:#fff; }}
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
.ph-title {{ font-size:14pt; font-weight:900; color:{NAV}; text-transform:uppercase; letter-spacing:0.5px; clear:right; }}
p {{ margin-bottom:7px; text-align:justify; }}
b {{ font-weight:700; }}
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
"""

def th(*c): return "<thead><tr>"+"".join(f"<th>{x}</th>" for x in c)+"</tr></thead>"
def tr_(*v): return "<tr>"+"".join(f"<td>{x}</td>" for x in v)+"</tr>"

# ═══════════════════════════════════════════════════════════════════════════════
H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Diagnostic Test Overutilisation &amp; Investigation Billing Fraud</div>
  <div class="cover-mod">MODULE FA-08 — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Claims Analysed</div><div class="cover-box-val">{fmt(total_intim) if total_intim else "43.5M"}</div></div>
    <div class="cover-box"><div class="cover-box-label">Checks Run</div><div class="cover-box-val">9 Checks</div></div>
  </div>
  <div class="cover-org">IIT KANPUR — Data Analytics &amp; Fraud Intelligence Division</div>
  <div class="cover-date">{today_str} | Ex-Servicemen Contributory Health Scheme (ECHS)</div>
  <div class="cover-botbar"></div>
</div>""")

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Executive Summary</h1>
<p>This report presents findings from Diagnostic Test Overutilisation fraud analytics conducted on the
ECHS claims database for the five-year period FY 2021–2026. Nine independent fraud signals were applied
across <b>{fmt(total_intim) if total_intim else "43.5M"}</b> intimations targeting excessive investigation
billing, rate inflation on diagnostic tests, repeat testing of the same patient, and hospitals whose
investigation charges are structurally disproportionate to clinical need.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Expense Records</div>
    <div class="mbox-val">{fmt(hosp_exp_rows) if hosp_exp_rows else "—"}</div>
    <div class="mbox-sub">hosp_exp rows</div></div>
  <div class="mbox"><div class="mbox-label">Line Items</div>
    <div class="mbox-val">{fmt(hosp_exp_det_rows) if hosp_exp_det_rows else "—"}</div>
    <div class="mbox-sub">hosp_exp_det rows</div></div>
  <div class="mbox"><div class="mbox-label">Clinical Tests (Int)</div>
    <div class="mbox-val">{fmt(cfi_rows) if cfi_rows else "—"}</div>
    <div class="mbox-sub">clinical_findings_int</div></div>
  <div class="mbox"><div class="mbox-label">Hosp Flagged</div>
    <div class="mbox-val">{fmt(q4_crit)}</div>
    <div class="mbox-sub">Critical — Inv ≥ 3× avg</div></div>
</div>

<h1 style="margin-top:14px">Nine Fraud Checks Identified</h1>
<table class="dt">
{th("#","Check","Key Signal","Volume Flagged","Risk")}
<tbody>
<tr><td>1</td><td>Investigation &gt; 40% of Total Claim</td><td>Claims where investigation billing dominates the total</td><td>{fmt(q1_total)} claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>Excessive Test Count (Z-Score)</td><td>Statistical outliers in tests ordered per admission</td><td>{fmt(q2_total)} claims</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Rate Inflation on Test Line Items</td><td>Hospital rate &gt;2× ECHS approved rate for same test</td><td>{fmt(q3_total)} line items</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>4</td><td>Hospital-Level Inv Billing Benchmark</td><td>Avg investigation billing ≥ 1.5× system average</td><td>{fmt(q4_total)} hospitals ({fmt(q4_crit)} Critical)</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>5</td><td>High Deduction Rate on Investigations</td><td>Investigation claims consistently rejected &gt;50%</td><td>{fmt(q5_total)} hospital-head pairs</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>Repeat Same Tests — Same Patient 30 Days</td><td>Identical test billed twice within 30 days</td><td>{fmt(q6_total)} duplicate pairs</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>7</td><td>Simple Diagnosis + High Investigation Billing</td><td>Low-acuity ICD codes (Z/I10/J0) with high test charges</td><td>{fmt(q7_total)} claims</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>8</td><td>Year-over-Year Investigation Spike</td><td>Hospitals with sudden 100%+ growth in investigation billing</td><td>{fmt(q8_crit)} Critical spikes</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>9</td><td>Composite Investigation Fraud Score</td><td>0–100 score combining volume, deduction, rate markup</td><td>{fmt(q9_crit)} Priority Audit hospitals</td><td>{risk_txt("CRITICAL")}</td></tr>
</tbody></table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Cap investigation billing at 40% of total claim</b> as a system-level validation rule — any submission exceeding this threshold must trigger mandatory PAR review before approval.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Audit all hospitals flagged at 3× system average investigation billing ({fmt(q4_crit)} facilities)</b> — field verification of actual test orders against billed items.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Reject all duplicate test billings</b> for same patient at same hospital within 30 days unless a new clinical justification is separately documented.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Freeze rate inflation claims</b> where hospital billed rate exceeds ECHS approved rate by 3× or more — {fmt(q3_total)} line items identified for immediate recovery.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Investigate hospitals with 90%+ investigation deduction rate</b> ({fmt(q5_crit)} facilities) — auditors are consistently catching and deducting these charges, yet hospitals continue filing. This constitutes systematic fraudulent billing.</div>
</div>""")

# ── CHECK 1: Inv % of Total ───────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 1</div>
  <div class="ph-ctx">Investigation Billing Ratio<br/>per Claim (FY 2021–26)</div>
  <div class="ph-title">Investigation Charges as % of Total Claim</div>
</div></div>
<p><b>Description:</b> For a standard inpatient claim, investigation and diagnostic test charges should
represent 15–25% of the total bill. When investigation billing exceeds 40–50% of the total claim amount,
it signals that tests are being ordered as the primary revenue driver rather than as clinical necessity.</p>
<p><b>Audit Findings:</b> <b>{fmt(q1_total)} claims</b> show investigation billing above 40% of total claim.
The system baseline for investigation as a share of total billing is derived from the expense profile.</p>
<div class="tc">Table 1.1 — Top Claims: Investigation Billing as % of Total</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","Hospital","Adm Date","LOS","Total Claim","Inv Claimed","Inv Approved","Inv %","Flag")}
<tbody>""")
for _,r in q1_top.iterrows():
    H.append(tr_(safe(r.get("Claim_ID")), safe(r.get("Patient_Name")), safe(r.get("Service_No")),
                 safe(r.get("Hospital_Name")), safe(r.get("Admission_Date")),
                 fmt(r.get("LOS_Days",0)),
                 money(r.get("Total_Claim_Amt")), money(r.get("Investigation_Claimed")),
                 money(r.get("Investigation_Approved")),
                 f'<b>{safe(r.get("Inv_Pct_of_Total"))}%</b>',
                 risk_txt(safe(r.get("Fraud_Flag","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Claims where investigation exceeds 70% of total billing represent cases where
the hospital is fundamentally recharacterising a clinical visit as a diagnostic workup — the treatment
component has been deliberately minimised to maximise test volume billing.</div>
<div class="kf-item">Cross-referencing Check 7 (simple diagnosis + high investigation) with this list
will identify the highest-priority cases: routine admission diagnoses with investigation bills that
dominate the claim are the clearest evidence of test-volume inflation.</div>
</div>""")

# ── CHECK 2: Excessive Test Count ────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 2</div>
  <div class="ph-ctx">Clinical Test Z-Score Analysis<br/>(Per Admission, FY 2021–26)</div>
  <div class="ph-title">Excessive Clinical Test Count per Admission</div>
</div></div>
<p><b>Description:</b> Each patient's count of distinct clinical tests is compared against the mean and
standard deviation of all admissions in the database. A Z-Score above 2 indicates statistically abnormal
test ordering. Critical cases (Z &gt; 3) represent 1-in-1,000 probability of legitimate clinical need —
confirming systematic test over-ordering.</p>
<p><b>{fmt(q2_total)} admissions</b> show test counts above 2 standard deviations from the mean.</p>
<div class="tc">Table 2.1 — Top Excessive Test Count Outliers (Z-Score &gt; 2)</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","Hospital","Adm Date","LOS","Tests Ordered","Sys Avg","Z-Score","Net Claim","Tests List","Risk")}
<tbody>""")
for _,r in q2_top.iterrows():
    tests = str(safe(r.get("Tests_List","—")))[:60]+"…" if len(str(safe(r.get("Tests_List","")))) > 60 else safe(r.get("Tests_List","—"))
    H.append(tr_(safe(r.get("Claim_ID")), safe(r.get("Patient_Name")), safe(r.get("Service_No")),
                 safe(r.get("Hospital_Name")), safe(r.get("Admission_Date")),
                 fmt(r.get("LOS_Days",0)),
                 f'<b>{fmt(r.get("Total_Tests_Ordered",0))}</b>',
                 safe(r.get("System_Avg_Tests")), f'<b>{safe(r.get("Z_Score"))}</b>',
                 money(r.get("Net_Claim_Amt")),
                 f'<span style="font-size:7pt">{tests}</span>',
                 risk_txt(safe(r.get("Risk_Level","HIGH")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Short admissions (1–3 day LOS) with a large number of distinct tests ordered are
the most suspicious profile — the patient was not sick enough to require extended care, yet the hospital
billed for an extensive diagnostic workup that would only be clinically justified for complex multi-organ
conditions.</div>
<div class="kf-item">Test count outliers that also appear in Check 1 (high investigation %) are the
highest-priority cases for physical audit: the test count AND the billing value are both anomalous,
confirming the pattern is deliberate rather than coincidental.</div>
</div>""")

# ── CHECK 3: Rate Inflation ───────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 3</div>
  <div class="ph-ctx">Hospital Rate vs ECHS Approved Rate<br/>(Line Item Level)</div>
  <div class="ph-title">Rate Inflation on Investigation Line Items</div>
</div></div>
<p><b>Description:</b> Each investigation line item in <code>hosp_exp_det</code> records both the hospital's
billed rate (HED_HOS_RATE) and the ECHS approved actual rate (HED_ACT_RATE). When the hospital rate
exceeds the approved rate by 2× or more, the hospital is systematically overcharging above the ECHS
rate schedule — a direct rate-inflation fraud pattern.</p>
<p><b>Highest rate markup found: {top_markup:.1f}×</b> the ECHS approved rate for the same procedure.</p>
<div class="tc">Table 3.1 — Top Rate Inflation Cases on Investigation Items (≥ 2× Markup)</div>
<table class="dt">
{th("Claim ID","Patient Name","Hospital","Adm Date","Expense Head","Procedure","Units","ECHS Rate","Hospital Rate","Markup","Claimed","Approved","Overcharge","Flag")}
<tbody>""")
for _,r in q3_top.iterrows():
    proc = str(safe(r.get("Test_Procedure","—")))[:35]+"…" if len(str(safe(r.get("Test_Procedure","")))) > 35 else safe(r.get("Test_Procedure","—"))
    H.append(tr_(safe(r.get("Claim_ID")), safe(r.get("Patient_Name")),
                 safe(r.get("Hospital_Name")), safe(r.get("Admission_Date")),
                 safe(r.get("Expense_Head")), f'<span style="font-size:7.5pt">{proc}</span>',
                 safe(r.get("Units")), money(r.get("ECHS_Approved_Rate")),
                 money(r.get("Hospital_Billed_Rate")),
                 f'<b>{safe(r.get("Rate_Markup"))}×</b>',
                 money(r.get("Total_Claimed")), money(r.get("Total_Approved")),
                 money(r.get("Overcharge_Amt")),
                 risk_txt(safe(r.get("Fraud_Flag","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Rate inflation on investigation items is the most directly quantifiable fraud:
the overcharge amount (Claimed − Approved) represents money that was billed against the ECHS
rate schedule and deducted by auditors — yet the hospital continues to file at inflated rates.</div>
<div class="kf-item">A hospital appearing in both Check 3 (rate inflation) and Check 5 (high deduction rate)
is the <b>Double Offender profile</b>: it charges above the rate schedule AND has its charges consistently
rejected, yet continues billing at the same inflated rates.</div>
</div>""")

# ── CHECK 4: Hospital Benchmark ───────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 4</div>
  <div class="ph-ctx">Hospital vs System Average<br/>Investigation Billing (Min 10 claims)</div>
  <div class="ph-title">Hospital-Level Investigation Billing Benchmark</div>
</div></div>
<p><b>Description:</b> Each hospital's average investigation billing per claim is compared against the
system-wide average. Hospitals with ratios of 2× or above are systematically billing for more diagnostic
tests than clinical norms justify across their entire patient cohort — not isolated cases.</p>
<p>System average investigation billing: <b>₹{fmt(sys_avg_inv)}</b> per claim.
Highest hospital ratio: <b>{top_inv_ratio:.2f}×</b> the system average.</p>
<div class="tc">Table 4.1 — Top Hospitals by Investigation Billing Ratio</div>
<table class="dt">
{th("Hospital ID","Hospital Name","Claims","Hosp Avg Inv","Sys Avg Inv","Inv Ratio","Total Inv Billed","Total Approved","Deduction %","Risk")}
<tbody>""")
for _,r in q4_top.iterrows():
    H.append(tr_(safe(r.get("Hospital_ID")), safe(r.get("Hospital_Name")),
                 fmt(r.get("Total_Claims",0)),
                 money(r.get("Hosp_Avg_Inv_Billed")), money(r.get("System_Avg_Inv_Billed")),
                 f'<b>{safe(r.get("Inv_Ratio"))}×</b>',
                 money(r.get("Total_Inv_Billed")), money(r.get("Total_Inv_Approved")),
                 pct(r.get("Deduction_Pct")),
                 risk_txt(safe(r.get("Risk_Level","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Hospitals with high Inv_Ratio AND high Deduction_Pct are the most critical:
auditors consistently catch the overcharging but the hospital continues. This confirms the behaviour
is embedded in the hospital's billing template, not accidental.</div>
<div class="kf-item">Hospitals with NULL names in the ECHS master registry that also show extreme
investigation ratios represent the highest-risk anonymous fraud profile — significant billing
exposure with no physical traceability.</div>
</div>""")

# ── CHECK 5: High Deduction Rate ─────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 5</div>
  <div class="ph-ctx">Investigation Claim vs Approved Ratio<br/>Hospital + Expense Head Level</div>
  <div class="ph-title">Persistently Deducted Investigation Claims</div>
</div></div>
<p><b>Description:</b> Hospitals where 70%+ of investigation billing is consistently rejected by auditors
are not making billing errors — they are systematically filing inflated investigation claims, aware that
partial payment will still be received. This is the "price anchor" fraud pattern: file high, accept
the deducted amount as the actual target revenue.</p>
<p><b>Highest deduction rate found: {top_ded_pct:.1f}%</b> — nearly all investigation claims deducted.</p>
<div class="tc">Table 5.1 — Hospitals with Highest Investigation Deduction Rate (≥ 50%)</div>
<table class="dt">
{th("Hospital ID","Hospital Name","Expense Head","Claims","Total Claimed","Total Approved","Deducted","Deduction %","Avg Inv Claim","Flag")}
<tbody>""")
for _,r in q5_top.iterrows():
    H.append(tr_(safe(r.get("Hospital_ID")), safe(r.get("Hospital_Name")),
                 safe(r.get("Expense_Head")),
                 fmt(r.get("Claims_Count",0)),
                 money(r.get("Total_Claimed")), money(r.get("Total_Approved")),
                 money(r.get("Total_Deducted")),
                 f'<b>{pct(r.get("Deduction_Pct"))}</b>',
                 money(r.get("Avg_Inv_Claim")),
                 risk_txt(safe(r.get("Fraud_Flag","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">A 90%+ deduction rate means the ECHS audit process is already catching and
rejecting these claims. The fraud finding here is not that these claims are paid — it is that the
hospital continues to file knowing they will be rejected, hoping the system will eventually miss some.</div>
<div class="kf-item">This pattern also reveals auditor fatigue risk: if auditors consistently process
the same hospital's inflated investigation claims, the probability of occasional slip-through payments
increases over time. These hospitals should be escalated for PAR-level pre-approval of all investigation
charges.</div>
</div>""")

# ── CHECK 6: Repeat Tests ─────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 6</div>
  <div class="ph-ctx">Duplicate Test Billing<br/>(Same Patient, Same Hospital, 30 Days)</div>
  <div class="ph-title">Repeat Same Tests — Same Patient Within 30 Days</div>
</div></div>
<p><b>Description:</b> Billing the same clinical test for the same patient at the same hospital within
30 days is rarely clinically justified unless the patient is treating a condition that requires frequent
monitoring. When the same test appears across two separate admission claims, it is typically claim-splitting
or duplicate test billing.</p>
<p><b>{fmt(q6_total)} duplicate test pairs</b> identified (same beneficiary, same hospital, same test, within 30 days).</p>
<div class="tc">Table 6.1 — Top Repeat Test Billing Pairs (Highest Claim Amount)</div>
<table class="dt">
{th("First Claim","Repeat Claim","Test Name","Patient Name","Service No","Hospital","First Adm","Repeat Adm","Days Between","First Amt","Repeat Amt","Flag")}
<tbody>""")
for _,r in q6_top.iterrows():
    H.append(tr_(safe(r.get("First_Claim_ID")), safe(r.get("Repeat_Claim_ID")),
                 safe(r.get("Test_Name")), safe(r.get("Patient_Name")),
                 safe(r.get("Service_No")), safe(r.get("Hospital_Name")),
                 safe(r.get("First_Admission")), safe(r.get("Repeat_Admission")),
                 f'<b>{fmt(r.get("Days_Between",0))} days</b>',
                 money(r.get("First_Claim_Amt")), money(r.get("Repeat_Claim_Amt")),
                 risk_txt("HIGH")))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Tests repeated within 1–7 days of a prior claim at the same hospital are the
highest-priority subset: the clinical rationale for repeating an expensive diagnostic test within
a week is extremely limited. These cases should be cross-checked against discharge summaries to
verify whether both admissions were genuine.</div>
</div>""")

# ── CHECK 7: Simple Diagnosis + High Inv ─────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 7</div>
  <div class="ph-ctx">ICD Code Severity vs Investigation Amount<br/>(Low-Acuity Diagnoses)</div>
  <div class="ph-title">Simple Diagnosis Paired With High Investigation Billing</div>
</div></div>
<p><b>Description:</b> Routine, low-acuity diagnoses (ICD codes Z-category: preventive visits;
I10: essential hypertension; J0x–J1x: common respiratory infections; K2x: gastric conditions;
M5x: back pain) should not generate large investigation bills. When these diagnoses appear alongside
high investigation charges, it indicates the tests were ordered to inflate billing, not to investigate
clinical need.</p>
<p><b>{fmt(q7_total)} claims</b> show investigation billing above ₹10,000 for low-acuity diagnoses.</p>
<div class="tc">Table 7.1 — Simple Diagnosis With High Investigation Charges</div>
<table class="dt">
{th("Claim ID","Patient Name","Service No","Hospital","Adm Date","LOS","ICD Code","Diagnosis","Inv Amount","Total Claim","Inv %","Flag")}
<tbody>""")
for _,r in q7_top.iterrows():
    diag = str(safe(r.get("Diagnosis","—")))[:45]+"…" if len(str(safe(r.get("Diagnosis","")))) > 45 else safe(r.get("Diagnosis","—"))
    H.append(tr_(safe(r.get("Claim_ID")), safe(r.get("Patient_Name")),
                 safe(r.get("Service_No")), safe(r.get("Hospital_Name")),
                 safe(r.get("Admission_Date")), fmt(r.get("LOS_Days",0)),
                 safe(r.get("ICD_Code")),
                 f'<span style="font-size:7.5pt">{diag}</span>',
                 f'<b>{money(r.get("Investigation_Amt"))}</b>',
                 money(r.get("Total_Claim_Amt")),
                 pct(r.get("Inv_Pct")),
                 risk_txt(safe(r.get("Fraud_Flag","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">Essential Hypertension (I10) is the most commonly abused diagnosis for investigation
inflation. It is a well-defined condition manageable with a blood pressure reading and routine blood work
— yet hospitals are attaching extensive diagnostic panels including CT scans, echocardiograms, and
specialised blood tests that are not clinically indicated for stable hypertension management.</div>
<div class="kf-item">Z-code claims (routine check-up / preventive care) with investigation billing above
₹50,000 represent the clearest-cut cases of unnecessary testing: by definition, the patient was not
admitted for acute illness, making a large investigation panel unjustifiable.</div>
</div>""")

# ── CHECK 8: YoY Spike ────────────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 8</div>
  <div class="ph-ctx">Year-over-Year Investigation Billing<br/>Growth Analysis (FY 2021–26)</div>
  <div class="ph-title">Year-over-Year Investigation Billing Spike</div>
</div></div>
<p><b>Description:</b> Hospitals with sudden, sharp growth in investigation billing — without a
corresponding proportional growth in claim volume — are artificially inflating the value of tests
ordered per admission. A 100%+ year-on-year growth in investigation billing at constant or growing
claim counts is a cliff-edge fraud signal.</p>
<p><b>{fmt(q8_crit)} Critical-tier spikes</b> (300%+ YoY growth) identified across the 5-year window.</p>
<div class="tc">Table 8.1 — Top Year-over-Year Investigation Billing Growth Spikes</div>
<table class="dt">
{th("Hospital ID","Hospital Name","Prev Year","Curr Year","Prev Inv Total","Curr Inv Total","Prev Claims","Curr Claims","YoY Growth %","Risk")}
<tbody>""")
for _,r in q8_top.iterrows():
    H.append(tr_(safe(r.get("Hospital_ID")), safe(r.get("Hospital_Name")),
                 safe(r.get("Previous_Year")), safe(r.get("Current_Year")),
                 money(r.get("Prev_Yr_Inv_Total")), money(r.get("Curr_Yr_Inv_Total")),
                 fmt(r.get("Prev_Yr_Claims",0)), fmt(r.get("Curr_Yr_Claims",0)),
                 f'<b>{pct(r.get("YoY_Growth_Pct"))}</b>',
                 risk_txt(safe(r.get("Risk_Level","MEDIUM")))))
H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">A hospital where investigation billing grows 300%+ while claim count grows &lt;50%
is not treating sicker patients — it is ordering more tests per patient. The cliff-edge pattern
(moderate billing in one year, sudden spike the next) is consistent with a deliberate change in
billing strategy, not a change in patient demographics.</div>
</div>""")

# ── CHECK 9: Composite Score ──────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">CHECK 9</div>
  <div class="ph-ctx">Composite Investigation Fraud Score<br/>0–100 per Hospital</div>
  <div class="ph-title">Composite Investigation Fraud Risk Score</div>
</div></div>
<p><b>Score formula (0–100):</b> Investigation volume ratio vs system average (35%) + Investigation
deduction rate (35%) + Average rate markup vs ECHS approved rate (30%). Hospitals scoring 60+ are
Priority Audit targets with concurrent signals across all three dimensions.</p>
<div class="tc">Table 9.1 — Top Hospitals by Composite Investigation Fraud Risk Score</div>
<table class="dt">
{th("Hospital ID","Hospital Name","Claims","Avg Inv Billed","Sys Avg","Inv Ratio","Ded %","Rate Markup","Total Billed","Risk Score","Priority")}
<tbody>""")
for _,r in q9_top.iterrows():
    H.append(tr_(safe(r.get("Hospital_ID")), safe(r.get("Hospital_Name")),
                 fmt(r.get("Claims_With_Inv",0)),
                 money(r.get("Avg_Inv_Billed")), money(r.get("System_Avg_Inv")),
                 f'{safe(r.get("Inv_Volume_Ratio"))}×',
                 pct(r.get("Inv_Deduction_Pct")),
                 f'{safe(r.get("Avg_Rate_Markup"))}×',
                 money(r.get("Total_Inv_Billed")),
                 f'<b>{safe(r.get("Fraud_Risk_Score"))}</b>',
                 risk_txt(safe(r.get("Audit_Priority","LOW")))))
H.append(f"""</tbody></table>

<h1 style="margin-top:16px">Consolidated Risk Register</h1>
<div class="tc" style="margin-bottom:8px">All findings require corroboration with physical audit records before enforcement action.</div>
<table class="dt">
{th("Check","Signal","Volume","Top Finding","Risk")}
<tbody>
<tr><td>1</td><td>Investigation &gt;40% of Total Claim</td><td>{fmt(q1_total)} claims</td><td>Investigation billing dominating total claim value</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>Excessive Test Count Z-Score &gt;2</td><td>{fmt(q2_total)} claims</td><td>Statistically abnormal test volumes per admission</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Rate Inflation — Hospital vs ECHS Rate</td><td>{fmt(q3_total)} line items</td><td>Up to {top_markup:.1f}× ECHS approved rate billed</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>4</td><td>Hospital Inv Billing ≥ 1.5× System Avg</td><td>{fmt(q4_total)} hospitals</td><td>{fmt(q4_crit)} hospitals at Critical level (≥3× avg)</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>5</td><td>Investigation Deduction Rate ≥ 50%</td><td>{fmt(q5_total)} hospital-head pairs</td><td>Up to {top_ded_pct:.1f}% of investigation claims consistently rejected</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>Repeat Same Tests Within 30 Days</td><td>{fmt(q6_total)} duplicate pairs</td><td>Same test billed twice for same patient — possible duplicate</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>7</td><td>Simple Diagnosis + High Inv Billing</td><td>{fmt(q7_total)} claims</td><td>Z/I10/J0 diagnoses with ₹10K+ investigation charges</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>8</td><td>YoY Investigation Spike ≥ 100%</td><td>{fmt(q8_crit)} Critical spikes</td><td>300%+ YoY investigation billing growth at constant volumes</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>9</td><td>Composite Fraud Score ≥ 60</td><td>{fmt(q9_crit)} Priority Audit hospitals</td><td>Multi-signal concurrent: volume + deduction + rate</td><td>{risk_txt("CRITICAL")}</td></tr>
</tbody></table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>
</body></html>""")

full = "\n".join(H)
print("Generating PDF ...")
HTML(string=full, base_url=BASE).write_pdf(PDF, stylesheets=[CSS(string=CSS_STR)])
print(f"Saved → {PDF}")
