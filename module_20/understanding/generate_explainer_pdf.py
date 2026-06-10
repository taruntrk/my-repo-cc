import os, time
from datetime import date
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_OUT = os.path.join(BASE, "ECHS_Data_Explainer.pdf")
today_str = date.today().strftime("%-d %B %Y")

NAV = "#1a2744"
GOLD = "#c9a84c"
RED = "#c0392b"
GREEN = "#27ae60"

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:9.5pt; color:#2d3748; line-height:1.6; background:#fff; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS FORENSICS — DATA EXPLAINER"; font-family:Arial; font-size:7.5pt; font-weight:800; color:{NAV}; border-bottom:1px solid #e2e8f0; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"Page " counter(page); font-family:Arial; font-size:7.5pt; color:#718096; border-bottom:1px solid #e2e8f0; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"Internal Briefing Document — Actual Dataset Findings"; font-family:Arial; font-size:7pt; color:#718096; border-top:1px solid #e2e8f0; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}"; font-family:Arial; font-size:7pt; color:#718096; border-top:1px solid #e2e8f0; padding-top:3px; }}
}}

.title-box {{ text-align:center; margin-bottom:20px; padding-bottom:10px; border-bottom:3px solid {GOLD}; }}
h1 {{ font-size:18pt; font-weight:900; color:{NAV}; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }}
.subtitle {{ font-size:10pt; color:#718096; font-weight:600; text-transform:uppercase; letter-spacing:2px; }}

.pattern-card {{ margin-bottom:24px; padding-bottom:16px; border-bottom:1px solid #e2e8f0; page-break-inside:avoid; }}
.p-header {{ display:flex; align-items:center; margin-bottom:8px; }}
.p-num {{ background:{NAV}; color:#fff; font-size:11pt; font-weight:900; padding:4px 10px; border-radius:4px; margin-right:10px; }}
.p-title {{ font-size:13pt; font-weight:800; color:{NAV}; }}

.section-label {{ font-size:8.5pt; font-weight:800; color:#4a5568; text-transform:uppercase; letter-spacing:1px; margin-top:8px; margin-bottom:2px; }}
.desc {{ margin-bottom:10px; text-align:justify; }}

.data-box {{ background:#fff5f5; border:1px solid #fed7d7; border-left:4px solid {RED}; padding:10px 14px; border-radius:0 4px 4px 0; margin-top:8px; }}
.data-box-title {{ color:{RED}; font-size:8.5pt; font-weight:800; text-transform:uppercase; letter-spacing:1px; display:flex; align-items:center; margin-bottom:4px; }}
.data-icon {{ font-size:12pt; margin-right:6px; }}
.data-content {{ color:#742a2a; font-size:9pt; font-weight:600; line-height:1.5; }}
.data-content b {{ font-weight:800; color:#9b2c2c; background:#fed7d7; padding:0 4px; border-radius:3px; }}
"""

H = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS_STR}</style></head><body>"]

H.append(f"""
<div class="title-box">
  <h1>ECHS FRAUD FORENSICS</h1>
  <div class="subtitle">Behavioral Detection Patterns &amp; Real Data Evidence</div>
</div>
<p style="margin-bottom:20px; text-align:center; font-style:italic; color:#4a5568;">This document bridges theoretical audit patterns with explicit statistical findings derived from the Module 20 forensic database extraction (19.8 Million cases / ₹3,612 Cr exposure).</p>
""")

patterns = [
    {
        "num": "PATTERN 1", "title": "Corporate Hospital Overbilling",
        "desc": "Instead of relying on percentage-based rejection rates (which artificially flag small clinics), this pattern targets massive corporate chains by <b>absolute leakage volume</b> to identify the largest sinks of ECHS funds.",
        "how": "Auditors rank facilities by the total Rupee value deducted across all claims, isolating corporate entities driving systemic leakage.",
        "data": "The <b>Vijay Hospital (ID 3149)</b> exhibited an anomalous 34.00% deduction rate. Concurrently, the <b>Park Hospital Chain</b> (Gurgaon, Chowkhandi, Kailash) emerged as the largest corporate target, requiring an immediate chain-level empanelment review."
    },
    {
        "num": "PATTERN 2", "title": "Macro Analytics: Annual, Regional & Demographics",
        "desc": "This mega-pattern evaluates systemic structural leakage. It identifies year-over-year inflation, geographic hotspots, and targeted patient demographics.",
        "how": "By aggregating millions of records along these three dimensions, the system flags entire segments of the ECHS program operating outside normal statistical bounds.",
        "data": "<b>Chennai Region 6</b> was flagged with a severe geographic anomaly (<b>19.13%</b> deduction rate vs 10% average). Demographically, the <b>'Wife'</b> category exhibited an elevated rejection rate of <b>15.59%</b>, exposing targeted upcoding in female-specific IPD procedures."
    },
    {
        "num": "PATTERN 3", "title": "Itemized Procedure Deviations",
        "desc": "Detects the unbundling of surgical packages and unjustified pharmacy inflation.",
        "how": "The system runs text-analytics on medical auditor remarks. It flags when a hospital attempts to bill separately for oxygen, ICU, or equipment already covered in the fixed package.",
        "data": "Auditors heavily cited <b>'Package Double-Billing'</b> and <b>'High-End Antibiotic Abuse'</b>. E.g., multiple high-end antibiotics were administered in massive, clinically unjustified doses solely to inflate the pharmacy bill."
    },
    {
        "num": "PATTERN 4", "title": "Length of Stay (LoS) Bed-Blocking",
        "desc": "Detects hospitals deliberately keeping patients admitted for unnecessarily long durations (>10 days) without clinical justification.",
        "how": "The script calculates the gap between Admission and Discharge dates for routine ailments, identifying pure room-rent and nursing charge inflation.",
        "data": "The system isolated multiple cases where routine ailments were stretched to <b>>15 days</b>, converting standard observation cases into highly lucrative, extended IPD stays."
    },
    {
        "num": "PATTERN 5", "title": "Ping-Pong Admissions (Split-Package Fraud)",
        "desc": "Identifies hospitals circumventing fixed package duration limits by discharging and immediately readmitting patients within 48 hours.",
        "how": "The patient is never physically discharged. The hospital merely closes their file and opens a new one (Ping-Ponging) to trigger a fresh package rate.",
        "data": "The extraction detected numerous readmissions with a literal <b>0 Days Gap</b>. This is definitive proof of paperwork manipulation to split a single continuous stay into two separate claims."
    },
    {
        "num": "PATTERN 6", "title": "Weekend Admission Surge (The Friday Hustle)",
        "desc": "Exploiting the physical absence of ECHS verifiers during the weekends.",
        "how": "Analyzes the day-of-the-week distribution for admissions. A massive spike strictly on Fridays, Saturdays, and Sundays indicates the hospital is pushing through unnecessary or fake admissions while authorities are off-duty.",
        "data": "A high concentration of 'Suspicious Weekend Admission Spikes' was flagged, pinpointing facilities orchestrating their highest IPD intake exactly when oversight is minimal."
    },
    {
        "num": "PATTERN 7", "title": "Doctor Cloning (The Superman Surgeon)",
        "desc": "Detects physical impossibility by flagging a single 'Treating Doctor' attached to an absurd number of surgeries in a single day.",
        "how": "If a surgeon bills for >15 complex procedures in 24 hours, the hospital is bulk-billing under one ID or hiding the true physicians.",
        "data": "Hospitals are bypassing the system using generic garbage text: <b>'CMO'</b> (79 surgeries in one day at Sarvodaya Hospital), <b>'ECHS'</b> (80 at Max Super Speciality). Even dentists like <b>Dr. Naveen Garg</b> logged an impossible <b>80 procedures</b> in a single day."
    },
    {
        "num": "PATTERN 8", "title": "Threshold Avoiding (The ₹99k Trick)",
        "desc": "Hospitals intentionally manipulating the final bill amount to avoid senior scrutiny.",
        "how": "If an automatic CFA approval threshold is set at ₹1,00,000, hospitals will intentionally bill exactly ₹99,000 or ₹99,999 so the claim slips through the automated system unnoticed.",
        "data": "The algorithm successfully flagged a high volume of 'Trick Bills' sitting uniformly tight against the automated approval ceiling, demonstrating a calculated evasion of senior officer review."
    }
]

for p in patterns:
    H.append(f"""
    <div class="pattern-card">
        <div class="p-header">
            <div class="p-num">{p['num']}</div>
            <div class="p-title">{p['title']}</div>
        </div>
        <div class="section-label">Core Concept</div>
        <div class="desc">{p['desc']}</div>
        <div class="section-label">Bypass Mechanism</div>
        <div class="desc">{p['how']}</div>
        <div class="data-box">
            <div class="data-box-title"><span class="data-icon">&#128680;</span> Real Data Evidence</div>
            <div class="data-content">{p['data']}</div>
        </div>
    </div>
    """)

H.append("</body></html>")

html_str = "\n".join(H)
HTML(string=html_str, base_url=BASE).write_pdf(PDF_OUT)
print(f"Generated {PDF_OUT}")
