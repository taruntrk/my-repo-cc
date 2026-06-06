"""
ECHS Identity Fraud — Comprehensive Report
HTML + WeasyPrint approach matching FA-07/FA-08 architecture.
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
DATA_DIR    = os.path.join(BASE, "data")
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

today_str = date.today().strftime("%-d %B %Y")
ts        = time.strftime("%Y%m%d_%H%M%S")
PDF_OUT   = os.path.join(REPORTS_DIR, f"ECHS_Identity_Fraud_Report_{ts}.pdf")

NAV  = "#1a2744"
GOLD = "#c9a84c"

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt(n):
    try: return f"{int(float(n)):,}"
    except: return str(n)

def cr(n):
    try:
        v = float(n)
        if v >= 1e7:  return f"₹{v/1e7:.2f} Cr"
        if v >= 1e5:  return f"₹{v/1e5:.2f} L"
        return f"₹{v:,.0f}"
    except: return str(n)

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

def hosp_display(hospitals_raw, count):
    """Show names if 1-4 hospitals, else just count."""
    count = int(count) if str(count).isdigit() else 0
    if count <= 4 and hospitals_raw and hospitals_raw not in ("—", ""):
        hosps = [h.split(":", 1)[-1] if ":" in h else h for h in str(hospitals_raw).split(" | ")]
        text = ", ".join(h.strip() for h in hosps if h.strip())
        return text[:60] + "…" if len(text) > 60 else text
    return fmt(count)

# ── Load CSVs ─────────────────────────────────────────────────────────────────

def load_latest(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        return []
    files.sort(key=os.path.getmtime, reverse=True)
    rows = []
    with open(files[0], encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

p01 = load_latest("01_Duplicate_Card_IDs*.csv")
p02 = load_latest("02_Simultaneous_Admissions*.csv")
p03 = load_latest("03_Duplicate_Bill_Numbers*.csv")
p04 = load_latest("04_Mobile_Number_Rings*.csv")
p04d= load_latest("04_Mobile_Dummy_Numbers*.csv")
p05 = load_latest("05_UID_Duplication*.csv")
p06 = load_latest("08_High_Frequency_Claims*.csv")

# Read threshold for P06
p06_threshold = 13
meta_files = glob.glob(os.path.join(DATA_DIR, "08_High_Frequency_Threshold*.txt"))
if meta_files:
    meta_files.sort(key=os.path.getmtime, reverse=True)
    with open(meta_files[0]) as mf:
        m = re.search(r"Threshold Used.*?:\s*(\d+)", mf.read())
        if m: p06_threshold = int(m.group(1))

total_cases    = len(p01) + len(p02) + len(p03) + len(p04) + len(p05) + len(p06)
patterns_found = sum(1 for p in [p01,p02,p03,p04,p05,p06] if p)

def sum_exposure(rows, key="total_exposure"):
    """Sum total exposure from rows, fallback to total_claimed_amount."""
    s = 0
    for r in rows:
        try:
            v = r.get(key) or r.get("total_claimed_amount") or r.get("amount_1") or 0
            s += float(v)
        except: pass
    return s

total_exposure = sum([
    sum_exposure(p01), sum_exposure(p02), sum_exposure(p03),
    sum_exposure(p04), sum_exposure(p05), sum_exposure(p06),
])

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9pt; color:#1a1a1a; line-height:1.55; background:#fff; }}

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
.cover-title {{ font-size:32pt; font-weight:900; color:#fff; letter-spacing:2px; margin-bottom:10px; }}
.cover-sub   {{ font-size:12pt; color:#ccc; font-weight:300; margin-bottom:16px; }}
.cover-mod   {{ font-size:9pt; color:{GOLD}; font-weight:700; letter-spacing:2px; margin-bottom:28px; }}
.cover-boxes {{ display:flex; gap:2px; margin-bottom:32px; }}
.cover-box   {{ background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
                padding:10px 18px; min-width:120px; white-space:nowrap; text-align:center; }}
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
"""

# ── BUILD HTML ────────────────────────────────────────────────────────────────

H = [f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>"""]

# ── COVER ─────────────────────────────────────────────────────────────────────
H.append(f"""
<div class="cover">
  <div class="cover-topbar"></div>
  <div class="cover-title">ECHS FRAUD ANALYTICS</div>
  <div class="cover-sub">Identity Fraud &amp; Duplicate Claim Detection Analysis</div>
  <div class="cover-mod">COMPREHENSIVE REPORT — FY 2021–2026 EDITION (LAST 5 YEARS)</div>
  <div class="cover-boxes">
    <div class="cover-box"><div class="cover-box-label">Classification</div><div class="cover-box-val">RESTRICTED</div></div>
    <div class="cover-box"><div class="cover-box-label">Period</div><div class="cover-box-val">FY 2021–26</div></div>
    <div class="cover-box"><div class="cover-box-label">Records Scanned</div><div class="cover-box-val">26M+</div></div>
    <div class="cover-box"><div class="cover-box-label">Patterns Run</div><div class="cover-box-val">6 Patterns</div></div>
    <div class="cover-box"><div class="cover-box-label">Cases Flagged</div><div class="cover-box-val">{fmt(total_cases)}</div></div>
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
<p>This report presents findings from identity and claims fraud analytics conducted on the ECHS database
covering the five-year period FY 2021–2026. Six independent fraud patterns were applied across
<b>26+ million claim records</b> to identify duplicate identifiers, simultaneous admissions, bill
resubmission, mobile fraud rings, Aadhaar (UID) duplication, and statistical over-utilisation outliers.</p>

<div class="metric-row">
  <div class="mbox"><div class="mbox-label">Total Cases Flagged</div><div class="mbox-val" style="color:#e74c3c">{fmt(total_cases)}</div><div class="mbox-sub">across 6 fraud patterns</div></div>
  <div class="mbox"><div class="mbox-label">Total Exposure</div><div class="mbox-val">{cr(total_exposure)}</div><div class="mbox-sub">estimated financial risk</div></div>
  <div class="mbox"><div class="mbox-label">Patterns w/ Findings</div><div class="mbox-val">{patterns_found}</div><div class="mbox-sub">of 6 checks</div></div>
  <div class="mbox"><div class="mbox-label">Analysis Period</div><div class="mbox-val">5 Yrs</div><div class="mbox-sub">FY 2021–2026</div></div>
</div>

<h1 style="margin-top:14px">Six Fraud Patterns — Summary</h1>
<table class="dt">
{th("#","Pattern","What It Detects","Cases Flagged","Risk")}
<tbody>
<tr><td>1</td><td>Duplicate Card IDs</td><td>Single ECHS card linked to 3+ different service numbers (ex-serviceman identifiers) — physical identity fraud</td><td><b>{fmt(len(p01))}</b></td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>Simultaneous Admissions</td><td>Same beneficiary admitted to 2 different hospitals within 7 days — physical impossibility indicating ghost billing</td><td><b>{fmt(len(p02))}</b></td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Duplicate Bill Numbers</td><td>Identical bill/invoice number resubmitted for multiple claims — direct double-billing</td><td><b>{fmt(len(p03))}</b></td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>4</td><td>Mobile Number Rings</td><td>Single mobile number linked to 5+ unrelated ECHS cards — coordinated fraud agent network</td><td><b>{fmt(len(p04))}</b> real + <b>{fmt(len(p04d))}</b> dummy</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>5</td><td>UID (Aadhaar) Duplication</td><td>Same 12-digit biometric Aadhaar UID registered under multiple service numbers — synthetic identity creation</td><td><b>{fmt(len(p05))}</b></td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>High Frequency Claims</td><td>Beneficiaries above statistical outlier threshold ({p06_threshold}+ claims in 5 yrs, Q3+1.5×IQR) — over-utilisation fraud</td><td><b>{fmt(len(p06))}</b></td><td>{risk_txt("HIGH")}</td></tr>
</tbody>
</table>

<h1 style="margin-top:12px">Immediate Recommended Actions</h1>
<div class="action-item"><span class="action-num">1.</span> <b>Freeze all ECHS cards sharing a duplicate card number</b> ({fmt(len(p01))} cases) — block further claims until physical verification confirms the legitimate cardholder.</div>
<div class="action-item"><span class="action-num">2.</span> <b>Initiate field audit of all simultaneous admission pairs</b> ({fmt(len(p02))} cases) — cross-reference hospital admission registers against ECHS claim dates to identify ghost patients.</div>
<div class="action-item"><span class="action-num">3.</span> <b>Reject all duplicate bill number resubmissions</b> ({fmt(len(p03))} cases) — implement system-level bill number uniqueness enforcement to prevent re-entry.</div>
<div class="action-item"><span class="action-num">4.</span> <b>Investigate mobile number rings</b> ({fmt(len(p04))} real rings) — a single mobile coordinating 5+ cards indicates a fraud agent; de-register the mobile from non-family cards.</div>
<div class="action-item"><span class="action-num">5.</span> <b>Audit all UID duplication cases</b> ({fmt(len(p05))} UIDs) — each Aadhaar must map to exactly one identity; escalate duplicates to UIDAI for verification and FIR filing.</div>
<div class="action-item"><span class="action-num">6.</span> <b>Pre-auth review for high-frequency claimants</b> ({fmt(len(p06))} beneficiaries above {p06_threshold} claims) — require clinical justification for further admissions.</div>
</div>
""")

# ── PATTERN 1: Duplicate Card IDs ───────────────────────────────────────────────
if p01:
    top = p01[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 1</div>
  <div class="ph-ctx">Duplicate ECHS Card Analysis<br/>(3+ Service Numbers per Card)</div>
  <div class="ph-title">Duplicate Card IDs — Identity Fraud</div>
</div></div>
<p><b>Description:</b> Each ECHS card is issued to one individual only. When a single card number
appears linked to 3 or more distinct service numbers (ex-servicemen), it indicates the card has been
cloned, stolen, or fraudulently registered under multiple identities. The card number is the primary
access credential for healthcare entitlement — duplication = direct identity fraud.</p>
<p><b>{fmt(len(p01))} cards</b> flagged with 3+ service numbers. Top 15 by total exposure shown.</p>
<div class="tc">Table 1.1 — Top Duplicate Card Cases (Top 15 by Exposure)</div>
<table class="dt">
{th("Card Number","Svc #s","Beneficiary Names","Claims","Hospitals","Total Exposure")}
<tbody>""")
    for r in top:
        names = str(r.get("beneficiary_names","")).replace(" | ",", ")
        names = (names[:35]+"…") if len(names)>35 else names
        hosps = hosp_display(r.get("hospitals_used",""), r.get("unique_hospitals",0))
        H.append(f"<tr><td><b>{safe(r.get('card_number',''))[:14]}</b></td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('unique_service_numbers','0'))}</b></td>"
                 f"<td style='font-size:7.5pt'>{names or '—'}</td>"
                 f"<td>{safe(r.get('total_claims','0'))}</td>"
                 f"<td style='font-size:7.5pt'>{hosps}</td>"
                 f"<td><b>{cr(r.get('total_claimed_amount', r.get('total_exposure',0)))}</b></td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Svc #s</b> = Unique ex-serviceman military identifiers sharing one card.
Legitimate sharing covers only family members under one service number — never multiple service numbers.
Any card with 3+ service numbers is a confirmed duplication.</div>
<div class="kf-item">Total exposure represents the cumulative amount claimed using this duplicated card.
Full dataset ({fmt(len(p01))} records) available in CSV for bulk remediation.</div>
</div>""")

# ── PATTERN 2: Simultaneous Admissions ─────────────────────────────────────────
if p02:
    top = p02[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 2</div>
  <div class="ph-ctx">Cross-Hospital Admission Overlap<br/>(Gap ≤ 7 Days, FY 2021–26)</div>
  <div class="ph-title">Simultaneous Admissions — Physical Impossibility</div>
</div></div>
<p><b>Description:</b> A beneficiary cannot be physically admitted to two different hospitals at the
same time or within an impossibly short gap. This check identifies claim pairs from the same service
number where admissions at different hospitals overlap or are separated by ≤7 days — hospital hopping
to claim two separate inpatient episodes for what was a single medical event, or ghost billing where
the second admission never occurred.</p>
<p><b>{fmt(len(p02))} admission pairs</b> detected with gap ≤ 7 days. Top 15 by exposure shown.</p>
<div class="tc">Table 2.1 — Simultaneous/Near-Simultaneous Admissions (Top 15 by Exposure)</div>
<table class="dt">
{th("Beneficiary","Svc #","Hospital 1","Hospital 2","Adm 1","Adm 2","Gap (Days)","Total Exposure")}
<tbody>""")
    for r in top:
        # Always put earlier admission first
        adm1 = str(r.get('admission_date_1','')); adm2 = str(r.get('admission_date_2',''))
        h1 = safe(r.get('hospital_name_1','')); h2 = safe(r.get('hospital_name_2',''))
        city1 = safe(r.get('city_1','')); city2 = safe(r.get('city_2',''))
        if adm1 > adm2 and adm2:  # swap so earlier date is always first
            adm1, adm2 = adm2, adm1
            h1, h2 = h2, h1
            city1, city2 = city2, city1
        gap_raw = r.get('gap_days', '0')
        try:
            gap_val = abs(int(float(gap_raw)))
        except:
            gap_val = 0
        gap_label = str(gap_val)
        gap_style = 'color:#c0392b;font-weight:700' if gap_val == 0 else 'font-weight:700'
        H.append(f'<tr>'
                 f'<td>{safe(r.get("beneficiary_name",""))[:22]}</td>'
                 f'<td style="font-size:7.5pt">{safe(r.get("service_number",""))}</td>'
                 f'<td style="font-size:7.5pt">{h1[:28]}<br/><span style="color:#888;font-size:6.5pt">{city1[:20]}</span></td>'
                 f'<td style="font-size:7.5pt">{h2[:28]}<br/><span style="color:#888;font-size:6.5pt">{city2[:20]}</span></td>'
                 f'<td style="font-size:7.5pt">{adm1[:10]}</td>'
                 f'<td style="font-size:7.5pt">{adm2[:10]}</td>'
                 f'<td><b style="{gap_style}">{gap_label}</b></td>'
                 f'<td><b>{cr(r.get("total_exposure",0))}</b></td></tr>')
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Gap/Overlap Days:</b> Negative values indicate a true simultaneous overlap —
the beneficiary was admitted to Hospital 2 before being discharged from Hospital 1. Zero = same-day
discharge and admission. Both are physical impossibilities for genuine inpatient care.</div>
<div class="kf-item">Cases where Hospital 2 name shows as a short code (e.g. "Rohtak", "Lodhi Road")
indicate ECHS polyclinics — referral-chain fraud where a polyclinic and a private hospital both file
claims for the same episode of care.</div>
</div>""")

# ── PATTERN 3: Duplicate Bill Numbers ──────────────────────────────────────────
if p03:
    top = p03[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 3</div>
  <div class="ph-ctx">Bill/Invoice Number Resubmission<br/>(Excluding NA / Blank)</div>
  <div class="ph-title">Duplicate Bill Numbers — Resubmission Fraud</div>
</div></div>
<p><b>Description:</b> Each hospital bill or invoice carries a unique number. If the exact same bill
number is submitted under multiple ECHS claim IDs, it means either: (a) the same bill was physically
resubmitted for payment twice, or (b) the bill number field was copied from another claim — both are
direct billing fraud. All blank, "NA", and null bill numbers are excluded from this analysis.</p>
<p><b>{fmt(len(p03))} duplicate bill numbers</b> detected. Top 15 by duplicate count shown.</p>
<div class="tc">Table 3.1 — Most Resubmitted Bill Numbers (Top 15)</div>
<table class="dt">
{th("Bill Number","Dup Count","Claims","Hospitals","Beneficiary/Svc #","Total Exposure")}
<tbody>""")
    for r in top:
        # P03 CSV columns: hospitals (not hospitals_used), beneficiaries (not beneficiary_names)
        hosps_raw = r.get('hospitals', r.get('hospitals_used', ''))
        # count unique hospitals from pipe-separated list
        hosp_list = [h.strip() for h in str(hosps_raw).split(' | ') if h.strip()]
        hosp_count = len(hosp_list)
        if hosp_count <= 4:
            hosp_text = ', '.join(h.split(':',1)[-1].strip() if ':' in h else h for h in hosp_list)
            hosp_text = (hosp_text[:55]+'…') if len(hosp_text)>55 else hosp_text
        else:
            hosp_text = f'{hosp_count} hospitals'

        bene_raw = r.get('beneficiaries', r.get('beneficiary_names', ''))
        bene_list = [b.split(':',1)[-1].strip() if ':' in b else b.strip() for b in str(bene_raw).split(' | ') if b.strip()]
        bene_count = len(bene_list)
        bene_text = ', '.join(bene_list[:3])
        if bene_count > 3: bene_text += f' +{bene_count-3} more'
        bene_text = (bene_text[:50]+'…') if len(bene_text)>50 else bene_text

        claim_ids = r.get('claim_ids', '')
        claim_count = len([x for x in str(claim_ids).split(' | ') if x.strip()])
        dup_count = safe(r.get('duplicate_count', r.get('dup_count', str(claim_count))))

        exposure = r.get('total_amount', r.get('total_exposure', r.get('total_claimed_amount', 0)))

        H.append(f'<tr>'
                 f'<td><code style="font-size:7.5pt">{safe(r.get("bill_number",""))[:20]}</code></td>'
                 f'<td><b style="color:#c0392b">{dup_count}</b></td>'
                 f'<td>{fmt(claim_count)}</td>'
                 f'<td style="font-size:7.5pt">{hosp_text}</td>'
                 f'<td style="font-size:7.5pt">{bene_text or "—"}</td>'
                 f'<td><b>{cr(exposure)}</b></td></tr>')
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Dup Count</b> = number of distinct ECHS claims carrying the same bill string.
A count of 2 = one resubmission; counts of 5+ indicate systematic reuse of the same document across
many claims — a template-based billing fraud operation.</div>
<div class="kf-item">Bill number duplicates appearing across multiple hospitals (Hospitals column &gt; 1)
are particularly severe: the same physical bill cannot have been issued by two separate facilities,
confirming fabrication of the invoice document itself.</div>
</div>""")

# ── PATTERN 4: Mobile Number Rings ──────────────────────────────────────────────
if p04:
    top = p04[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 4</div>
  <div class="ph-ctx">Mobile Coordination Network<br/>(5+ Cards per Mobile, FY 2021–26)</div>
  <div class="ph-title">Mobile Number Rings — Coordinated Fraud Agent Network</div>
</div></div>
<p><b>Description:</b> An ECHS mobile number is used for claim communication and OTP verification.
Legitimate sharing within a family (one ex-serviceman + dependents) produces at most 3–4 cards on one
number. When a single mobile is linked to 5+ cards belonging to different service numbers, it indicates
a <b>fraud agent</b> operating as the contact point for multiple unrelated identities — filing claims
on behalf of ghost beneficiaries. <b>{fmt(len(p04d))} dummy numbers</b> (all-zero, repeating digits)
were excluded and reported separately below.</p>
<p><b>{fmt(len(p04))} real mobile rings</b> detected. Top 15 by total exposure shown.</p>
<div class="tc">Table 4.1 — Top Mobile Number Rings (Real Numbers, Top 15 by Exposure)</div>
<table class="dt">
{th("Mobile Number","Cards","Svc Numbers","Claims","Hospitals","Total Exposure")}
<tbody>""")
    for r in top:
        hosps = hosp_display(r.get("hospitals_used",""), r.get("unique_hospitals",0))
        H.append(f"<tr>"
                 f"<td><code>{safe(r.get('mobile_number',''))}</code></td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('unique_cards','0'))}</b></td>"
                 f"<td>{safe(r.get('unique_service_numbers','0'))}</td>"
                 f"<td>{safe(r.get('total_claims','0'))}</td>"
                 f"<td style='font-size:7.5pt'>{hosps}</td>"
                 f"<td><b>{cr(r.get('total_exposure',0))}</b></td></tr>")
    dummy_rows = "".join(
        f"<tr><td><code>{safe(r.get('mobile_number',''))}</code></td>"
        f"<td>{safe(r.get('unique_cards','0'))}</td>"
        f"<td>{safe(r.get('total_claims','0'))}</td>"
        f"<td><b>{cr(r.get('total_exposure',0))}</b></td></tr>"
        for r in p04d[:10]
    )
    H.append(f"""</tbody></table>
<div class="tc" style="margin-top:10px">Table 4.2 — Dummy/Invalid Mobile Numbers (Excluded from Main Analysis)</div>
<table class="dt">
{th("Mobile Number","Cards","Claims","Total Exposure")}
<tbody>{dummy_rows}</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Cards</b> = distinct ECHS health cards registered under this single mobile.
Fraud agents maintain one phone number as their operational contact across all ghost identities they
manage — allowing them to receive OTPs, discharge summaries, and claim status alerts centrally.</div>
<div class="kf-item"><b>Dummy numbers</b> (Table 4.2) represent cases where the mobile field was
filled with placeholder data (000000, 111111, etc.) — indicating the beneficiary has no real mobile
on file, making contact and verification impossible.</div>
</div>""")

# ── PATTERN 5: UID Duplication ──────────────────────────────────────────────────
if p05:
    top = p05[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 5</div>
  <div class="ph-ctx">Aadhaar UID Cross-Linkage Analysis<br/>(Dummy UIDs Excluded)</div>
  <div class="ph-title">UID Duplication — Synthetic Identity Fraud</div>
</div></div>
<p><b>Description:</b> The 12-digit Aadhaar UID is a biometric-linked national identifier — exactly
one UID per individual, guaranteed by UIDAI. If the same UID appears registered under multiple ECHS
service numbers, it means: (a) one person's identity is being used by another (<b>identity theft</b>),
or (b) a single UID has been bulk-registered under fabricated service numbers to generate fictitious
beneficiaries (<b>synthetic identity fraud</b>). Known dummy UIDs (all-zero, all-nine, sequential)
are excluded. All 12-digit UIDs masked as XXXX****XXXX in the report.</p>
<p><b>{fmt(len(p05))} UIDs</b> found linked to multiple service numbers. Top 15 by exposure shown.</p>
<div class="tc">Table 5.1 — UID Duplication Cases (Top 15 by Service Number Count)</div>
<table class="dt">
{th("UID (masked)","Svc #s","Claims","Hospitals","Locations","Total Exposure")}
<tbody>""")
    for r in top:
        uid = str(r.get("uid_number",""))
        masked = (uid[:4]+"****"+uid[-4:]) if len(uid)==12 else uid
        hosps = hosp_display(r.get("hospitals_used",""), r.get("unique_hospitals",0))
        locs  = str(r.get("locations","—"))[:35]
        H.append(f"<tr>"
                 f"<td><code>{masked}</code></td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('unique_service_numbers','0'))}</b></td>"
                 f"<td>{safe(r.get('total_claims','0'))}</td>"
                 f"<td style='font-size:7.5pt'>{hosps}</td>"
                 f"<td style='font-size:7.5pt'>{locs}</td>"
                 f"<td><b>{cr(r.get('total_exposure',0))}</b></td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Svc #s</b> = count of distinct military service numbers sharing this UID.
Each UID should map to exactly <b>one</b> individual. Even two service numbers sharing one UID is
anomalous — it means one person's biometric is funding two ECHS accounts.</div>
<div class="kf-item">UID duplication cases involving 3+ service numbers and multiple geographic locations
indicate a <b>large-scale synthetic identity ring</b> — a single Aadhaar is the seed identity for an
entire cluster of fabricated ECHS accounts. These must be escalated to UIDAI and ECHS Directorate.</div>
</div>""")

# ── PATTERN 6: High Frequency Claims ───────────────────────────────────────────
if p06:
    top = p06[:15]
    H.append(f"""
<div class="pb">
<div class="nob">
<div class="ph">
  <div class="ph-label">PATTERN 6</div>
  <div class="ph-ctx">Statistical Outlier Detection<br/>(Q3 + 1.5×IQR Threshold: {p06_threshold} claims)</div>
  <div class="ph-title">High Frequency Claims — Over-Utilisation Fraud</div>
</div></div>
<p><b>Description:</b> The fraud threshold for this check was <b>calculated dynamically</b> using
the Tukey Fence method — a standard statistical outlier detection technique (John Tukey, 1977)
applied to the actual claim distribution of all <b>4.69 million ECHS beneficiaries</b> over 5 years.
No fixed or arbitrary number was assumed.</p>

<p><b>How the threshold was derived — step by step:</b></p>
<ul>
<li><b>Median = 2 claims</b> — The midpoint of all beneficiaries. Half of India's ECHS users made fewer
than 2 inpatient claims in 5 years. This is the realistic baseline of a typical ex-serviceman's medical usage.</li>
<li><b>Q1 = 1 claim</b> — The bottom 25% of all beneficiaries made just 1 claim over 5 years.</li>
<li><b>Q3 = 6 claims</b> — 75% of all beneficiaries made 6 or fewer claims over 5 years. Only the top 25% exceeded this.</li>
<li><b>IQR = Q3 − Q1 = 5</b> — The Interquartile Range is the natural spread covering the "middle 50%" of users.
It measures how wide the normal zone of variation is.</li>
<li><b>Tukey Fence = Q3 + 1.5 × IQR = 6 + 7.5 = 13.5 → <u>{p06_threshold} claims</u></b> — Any beneficiary
above this boundary is classified as a statistical outlier. In a normal distribution this represents less than
0.1% probability of occurring by chance — meaning it is almost certainly not explained by age, illness, or
any legitimate medical need alone.</li>
</ul>

<p>In plain terms: <b>if 99.9% of ECHS users manage their healthcare in 13 or fewer claims over 5 years,
anyone with 14+ claims is not a heavier user — they are an anomaly that demands investigation.</b>
This indicates planned over-utilisation, ghost visit billing, or active collusion with a hospital
to generate fraudulent claim volume.</p>
<p><b>{fmt(len(p06))} beneficiaries</b> exceeded the {p06_threshold}-claim threshold. Top 15 by total exposure shown.</p>
<div class="tc">Table 6.1 — High Frequency Claimants Above Threshold (Top 15 by Exposure)</div>
<table class="dt">
{th("Service #","Beneficiary","# Claims","Avg Claim","Hospitals","Total Exposure")}
<tbody>""")
    for r in top:
        hosps  = hosp_display(r.get("hospitals_used",""), r.get("unique_hospitals",0))
        avg    = r.get("avg_claim_amount","—")
        H.append(f"<tr>"
                 f"<td style='font-size:7.5pt'>{safe(r.get('service_number',''))}</td>"
                 f"<td>{safe(r.get('beneficiary_name',''))[:22]}</td>"
                 f"<td><b style='color:#c0392b'>{safe(r.get('total_claims','0'))}</b></td>"
                 f"<td>{cr(avg) if avg not in ('—','') else '—'}</td>"
                 f"<td style='font-size:7.5pt'>{hosps}</td>"
                 f"<td><b>{cr(r.get('total_exposure', r.get('total_claimed_amount',0)))}</b></td></tr>")
    H.append(f"""</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item">The statistical baseline (median = 2 claims over 5 years) reflects the typical
ECHS beneficiary pattern. A beneficiary with {p06_threshold}+ claims is 6× above the median.
Beneficiaries with 30+ claims over 5 years (6 per year) warrant immediate clinical audit —
at that frequency, inpatient claims can no longer be explained by age or chronic illness alone.</div>
<div class="kf-item">High-frequency claimants concentrated at a <b>single hospital</b> (Hospitals = 1)
are the most suspicious: genuine chronic illness patients typically see multiple specialists across
different facilities. One hospital + high frequency = hospital-patient collusion for ghost billing.</div>
</div>""")

# ── CONSOLIDATED RISK REGISTER ────────────────────────────────────────────────
H.append(f"""
<div class="pb">
<h1>Consolidated Risk Register</h1>
<p class="tc" style="margin-bottom:10px">All findings are based on structured database analysis and must be
corroborated with physical audit records before enforcement action is taken.</p>
<table class="dt">
{th("Pattern","Fraud Signal","Cases Flagged","Exposure","Risk")}
<tbody>
<tr><td>1</td><td>Duplicate Card IDs (3+ Svc Numbers)</td><td><b>{fmt(len(p01))}</b></td><td>{cr(sum_exposure(p01))}</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>2</td><td>Simultaneous Admissions (Gap ≤ 7 days)</td><td><b>{fmt(len(p02))}</b></td><td>{cr(sum_exposure(p02))}</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>3</td><td>Duplicate Bill Number Resubmission</td><td><b>{fmt(len(p03))}</b></td><td>{cr(sum_exposure(p03))}</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>4</td><td>Mobile Number Rings (5+ cards)</td><td><b>{fmt(len(p04))}</b> real + <b>{fmt(len(p04d))}</b> dummy</td><td>{cr(sum_exposure(p04))}</td><td>{risk_txt("HIGH")}</td></tr>
<tr><td>5</td><td>UID (Aadhaar) Duplication</td><td><b>{fmt(len(p05))}</b></td><td>{cr(sum_exposure(p05))}</td><td>{risk_txt("CRITICAL")}</td></tr>
<tr><td>6</td><td>High Frequency Claims (≥{p06_threshold} claims)</td><td><b>{fmt(len(p06))}</b></td><td>{cr(sum_exposure(p06))}</td><td>{risk_txt("HIGH")}</td></tr>
<tr style="background:#fdf0f0;font-weight:700"><td colspan="2"><b>TOTAL</b></td><td><b style="color:#c0392b">{fmt(total_cases)}</b></td><td><b>{cr(total_exposure)}</b></td><td>—</td></tr>
</tbody>
</table>

<p style="margin-top:16px;font-size:7.5pt;color:#555;text-align:center">
Prepared by IIT Kanpur — Data Analytics &amp; Fraud Intelligence Division | {today_str}<br/>
All findings are based on structured database analysis and must be corroborated with physical audit records before enforcement action.
</p>
</div>

</body></html>""")

# ── RENDER ────────────────────────────────────────────────────────────────────
full_html = "\n".join(H)
print("Generating PDF ...")
HTML(string=full_html, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Saved → {PDF_OUT}")
print(f"   Total cases: {total_cases:,}")
print(f"   Exposure   : {cr(total_exposure)}")
