import re

file_path = "/home/tarun/Downloads/CC/echs_analysis/module_19/generate_module19_report_v2.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # 1. Stay Extension Aggressive Wording
    (r"purely for revenue extraction\.", "requires clinical review to determine whether the extended stays were medically justified."),
    
    # 2. Rename Aggressive Pattern Names
    (r"Room Upgrade Fraud", "Room Upgrade Anomalies"),
    (r"PATTERN 3 \(CRITICAL FRAUD\)", "PATTERN 3 (GHOST ADMISSION EXPOSURE)"),
    (r"PATTERN 6 \(ADMISSION FRAUD\)", "PATTERN 6 (IPD/OPD ESCALATION PATTERN)"),
    (r"PATTERN 8 \(ESTIMATE FRAUD\)", "PATTERN 8 (PRIOR APPROVAL INFLATION PATTERN)"),
    (r"Fraud Claims", "Anomalous Claims"),
    
    # 3. Remove Vijay Hospital Orphan Paragraph
    (r'<div class="kf-item"><b>Vijay Hospital \(ID 3149\):</b> Maintains a 34% deduction rate — one in three rupees claimed is rejected\. This anomalous rate across \{fmt\(df_1\[df_1\[\'hospital_id\'\]==3149\]\[\'total_claims\'\]\.sum\(\)\)\} claims warrants a targeted billing audit to determine whether the pattern reflects systematic overbilling, documentation deficiencies, or package coding errors\.</div>', ""),
    
    # 4. Ghost Admission Wording
    (r"These represent the most severe structural failure — entities extracting funds while bypassing all standard portal validation\.", 
     "These represent claims processed without standard portal validation controls.")
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully.")
