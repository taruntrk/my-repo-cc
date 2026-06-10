with open("generate_module19_report_v2.py", "r") as f:
    code = f.read()

replacements = {
    "Leakage Identified": "Audit Deductions",
    "Anomalies Detected": "Forensic Hits",
    "Anomalies Flagged": "Pattern Matches",
    "with a leakage exposure of": "with an overbilling exposure of",
    "Absolute Leakage Facilities": "Absolute Deduction Facilities",
    "CORPORATE LEAKAGE": "SYSTEMIC OVERBILLING",
    "Total Claimed (Anomalies)": "Total Claimed (Flagged)",
    "Total System Exposure": "Total Forensic Exposure",
    "leakage generators": "overbilling generators"
}

for old, new in replacements.items():
    code = code.replace(old, new)

with open("generate_module19_report_v2.py", "w") as f:
    f.write(code)
print("Updated report strings!")
