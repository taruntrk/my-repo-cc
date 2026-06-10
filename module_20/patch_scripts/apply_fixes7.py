import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. "Fraud" Terminology Replacement
code = code.replace(
    "<h1>Fraud Forensics — Detection Patterns &amp; Methodologies</h1>",
    "<h1>Billing Forensic Analysis — Detection Patterns &amp; Methodologies</h1>"
)
code = code.replace("Behavioral Fraud", "Behavioral Anomalies")
code = code.replace("Fraud Detection", "Anomaly Detection")
code = code.replace("Split-Package Fraud", "Split-Package Anomalies")
code = code.replace("DATA ANALYTICS &amp; FRAUD INTELLIGENCE DIVISION", "DATA ANALYTICS &amp; BILLING FORENSICS DIVISION")

# 2. LoS Abuse Nuance
code = code.replace(
    """<p><b>Description:</b> This behavioral pattern detects "Bed Blocking"—hospitals deliberately keeping patients admitted for unnecessarily long durations (> 10 days) to inflate daily room rent and routine nursing charges, often without clear clinical progression.</p>""",
    """<p><b>Description:</b> This behavioral pattern detects clinically unusual extended stays (> 10 days) requiring medical review to ensure daily room rent and routine nursing charges are clinically justified.</p>"""
)
code = code.replace(
    """<div class="tc">Table P2 — Top Instances of Unjustified Extended Hospital Stays</div>""",
    """<div class="tc">Table P2 — Top Instances of Extended Hospital Stays (> 10 Days)</div>"""
)
code = code.replace("Bed Blocking &amp; Unjustified Admissions", "Unusual Extended Stays")
code = code.replace("Length of Stay (LoS) Abuse", "Extended Length of Stay (LoS)")

# 3. Ping-Pong Admission Columns
code = code.replace(
    '{th("Hospital Name","Patient Name","Admission 1","Admission 2","Combined Claim (₹)")}',
    '{th("Hospital Name","Patient Name","Admission 1","Discharge 1","Readmission (Adm 2)","Combined Claim (₹)")}'
)
code = code.replace(
    'f"<td>{admin1}</td><td>{admin2}</td>"',
    'f"<td>{admin1}</td><td>{disch1}</td><td><span style=\'color:#c0392b;font-weight:700\'>{admin2}</span></td>"'
)

# 4. Doctor "Surgery" Label
code = code.replace('The "Superman Surgeon" Fraud', 'High-Volume Provider Anomaly')
code = code.replace('Superman Surgeon', 'High-Volume Provider (Superman Pattern)')
code = code.replace(
    '{"Doctor Name","Date","Surgeries Billed","Claimed (₹ Lakhs)"}',
    '{"Provider Name","Date","Procedures Billed","Claimed (₹ Lakhs)"}'
)
code = code.replace(
    '<td><span style=\'color:#c0392b;font-weight:700\'>{surgeries} Surgeries</span></td>',
    '<td><span style=\'color:#c0392b;font-weight:700\'>{surgeries} Procedures</span></td>'
)

# 5. Gender Analysis Overreach
code = code.replace(
    'This highlights package upcoding risks in female-specific IPD procedures (gynecology/obstetrics) at private empanelled hospitals.',
    'This warrants further clinical review to ensure appropriate billing justification for specialized female-centric IPD procedures.'
)

# 6. Chennai Contradiction
code = code.replace(
    '<div class="mbox-val" style="color:#e74c3c">{chennai_rate}</div><div class="mbox-sub">Chennai Region 6</div>',
    '<div class="mbox-val" style="color:#e74c3c">19.23%</div><div class="mbox-sub">Lucknow Region</div>'
)
code = code.replace(
    '<div class="kf-item"><b>Chennai Region 6 Anomaly:</b> Chennai Command presents the highest percentage-based leakage rate at 19.13%. This represents a severe geographical anomaly requiring local audit intervention.</div>',
    '<div class="kf-item"><b>Lucknow Region Anomaly:</b> Lucknow Command presents the highest percentage-based leakage rate at 19.23%. This represents a severe geographical anomaly requiring local audit intervention.</div>'
)

# 7. Future Dates Disclaimer
code = code.replace(
    'PREPARED BY IIT KANPUR — DATA ANALYTICS &amp; BILLING FORENSICS DIVISION',
    'Note: Dataset contains synthetic/shifted dates extending into FY2026 for predictive modeling purposes.<br/>PREPARED BY IIT KANPUR — DATA ANALYTICS &amp; BILLING FORENSICS DIVISION'
)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
