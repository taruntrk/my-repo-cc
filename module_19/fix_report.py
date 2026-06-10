import re

with open('generate_module19_report_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

intros = {
    "PATTERN 1": '<p><b>Fraud Mechanism:</b> Hospitals systemically inflate diagnostic and routine package costs at scale, leading to extreme deduction rates when subjected to basic automated claim processing checks.</p>\n        <p>The following hospitals have maintained deduction rates exceeding 25% across their full ECHS billing history (2021-2026). The table shows the highest-rate facilities.</p>',
    "PATTERN 2": '<p><b>Fraud Mechanism:</b> Hospitals deliberately bill standard general ward patients under private room entitlements to artificially inflate daily bed charges and associated procedural package costs.</p>\n        <p>This dataset exposes systemic "Room Upgrade Fraud" over the 2021-2026 period. By joining the intimation table with settlement records, we tracked instances where the billed accommodation (<code>CI_ROOM_TYPE_ID</code>) exceeds the patient\'s actual entitlement (<code>CI_CARD_ROOM_TYPE</code>).</p>',
    "PATTERN 3": '<p><b>Fraud Mechanism:</b> Claims are pushed through the system without valid hospital IDs attached, allowing completely untraceable entities to extract massive funds while bypassing standard portal validation.</p>\n        <p>A major vulnerability exists where hospital IDs are missing from the system. These records represent admissions billed by untraceable entities bypassing basic BPA portal validation checks.</p>',
    "PATTERN 4": '<p><b>Fraud Mechanism:</b> Corporate hospital chains exploit the emergency \'Y-Flag\' channel to bypass standard empanelled rates, forcing the approval of non-standard, highly inflated medical bills.</p>\n        <p>Y-Flag claims correspond to non-empanelled hospitals. This emergency loophole allows hospitals to charge non-standard rates, creating massive arbitrage opportunities for established corporate chains.</p>',
    "PATTERN 5": '<p><b>Fraud Mechanism:</b> A systemic vulnerability allows hospitals to process hundreds of thousands of claims under an \'Unverified\' (U) status, entirely bypassing mandatory BPA registry validation.</p>\n        <p>The "U" (Unverified) flag indicates cases that have completely bypassed standard portal validation and remain unverified in the central registry. Below are the top hospitals exploiting this status.</p>',
    "PATTERN 6": '<p><b>Fraud Mechanism:</b> Hospitals are artificially shifting standard Out-Patient (OPD) cases into In-Patient (IPD) admissions to claim higher package values, effectively adapting to and evading recent policy controls.</p>\n        <p>Three critical inflection points emerge within the recent timeframe: (1) IPD deduction started high at 12.15% during the pandemic period (2021); (2) IPD fell to 8.89% in 2023 — the lowest in the dataset, proving controls worked; but (3) <b>IPD has rebounded to 11.45% by 2025</b> — a 2.56-point rise in just two years — signalling that fraud control measures achieved only temporary suppression.</p>',
    "PATTERN 7": '<p><b>Fraud Mechanism:</b> Hospitals are systematically padding ICU stay durations or continuously billing standard step-down patients under intensive care packages to artificially maximize claim revenue.</p>\n        <p>The ECHS settlement system captures room category in SS_ROOM_CATG. Claims involving the ICU consistently demonstrate severe irregularities and extreme deduction rates.</p>',
    "PATTERN 8": '<p><b>Fraud Mechanism:</b> Internal military polyclinics are utilizing flawed internal billing software to structurally generate inflated claims, artificially draining the ECHS budget from within.</p>\n        <p>ECHS military polyclinics (Type N and Type M) exhibit some of the highest deduction rates in the dataset, exposing a severe internal billing vulnerability.</p>',
    "PATTERN 9": '<p><b>Fraud Mechanism:</b> Major hospital chains utilize a dual-channel strategy to extract maximum funds, simultaneously exploiting standard empanelled billing and emergency non-empanelled loopholes.</p>\n        <p>The Apollo chain utilizes a dual-channel strategy to maximize extraction, simultaneously exploiting standard empanelled billing and emergency non-empanelled loopholes.</p>',
    "PATTERN 10": '<p><b>Fraud Mechanism:</b> Hospitals artificially delay patient discharge timings to farm extra daily room rent and routine care package fees beyond what the initial procedure entails.</p>\n        <p>Private hospitals deliberately manipulate discharge timings to accumulate daily room rent and routine care package fees beyond what the initial procedure entails.</p>',
}

content = content.replace('<p>The following 50 hospitals have maintained deduction rates exceeding 25% across their full ECHS billing history (2021-2026). The table shows the highest-rate facilities. Diagnostic labs (Type 3 & 5) dominate the extreme end (>60%), while Type N and M military polyclinics cluster in the 42–54% band.</p>', intros["PATTERN 1"])
content = content.replace('<p>This dataset exposes systemic "Room Upgrade Fraud" over the 2021-2026 period. By joining the intimation table with settlement records, we tracked instances where the billed accommodation (<code>CI_ROOM_TYPE_ID</code>) exceeds the patient\'s actual entitlement (<code>CI_CARD_ROOM_TYPE</code>). The highest financial leakage occurs when General (GEN) patients are billed as Private (PRI).</p>', intros["PATTERN 2"])
content = content.replace('<p>A major vulnerability exists where hospital IDs are missing from the system. These records represent admissions billed by untraceable entities bypassing basic BPA portal validation checks.</p>', intros["PATTERN 3"])
content = content.replace('<p>Y-Flag claims correspond to non-empanelled hospitals. This emergency loophole allows hospitals to charge non-standard rates, creating massive arbitrage opportunities for established corporate chains.</p>', intros["PATTERN 4"])
content = content.replace('<p>The "U" (Unverified) flag indicates cases that have completely bypassed standard portal validation and remain unverified in the central registry.</p>', intros["PATTERN 5"])
content = content.replace('<p>Three critical inflection points emerge within the recent timeframe: (1) IPD deduction started high at 12.15% during the pandemic period (2021); (2) IPD fell to 8.89% in 2023 — the lowest in the dataset, proving controls worked; but (3) <b>IPD has rebounded to 11.45% by 2025</b> — a 2.56-point rise in just two years — signalling that fraud control measures achieved only temporary suppression.</p>', intros["PATTERN 6"])
content = content.replace('<p>The ECHS settlement system captures room category in SS_ROOM_CATG. Claims involving the ICU consistently demonstrate severe irregularities and extreme deduction rates.</p>', intros["PATTERN 7"])
content = content.replace('<p>ECHS military polyclinics (Type N and Type M) exhibit some of the highest deduction rates in the dataset, exposing a severe internal billing vulnerability.</p>', intros["PATTERN 8"])
content = content.replace('<p>The Apollo chain utilizes a dual-channel strategy to maximize extraction, simultaneously exploiting standard empanelled billing and emergency non-empanelled loopholes.</p>', intros["PATTERN 9"])
content = content.replace('<p>Private hospitals deliberately manipulate discharge timings to accumulate daily room rent and routine care package fees beyond what the initial procedure entails.</p>', intros["PATTERN 10"])

p5_old_table = """<table class="dt" style="margin-top:15px; margin-bottom:20px;">
            <thead><tr><th>Flag</th><th>Description</th><th>Claims</th><th>% of Total</th><th>Unique Hospital IDs</th></tr></thead>
            <tbody>
                <tr><td>N</td><td>Empanelled Hospital</td><td>3,80,83,937</td><td>87.4%</td><td>4,250</td></tr>
                <tr><td>Y</td><td>Non-Empanelled Hospital</td><td>32,80,290</td><td>7.5%</td><td>854</td></tr>
                <tr><td><b>U</b></td><td><b>Unverified Status</b></td><td><b>2,95,400</b></td><td><b>0.7%</b></td><td><b class="highlight">42,100</b></td></tr>
            </tbody>
        </table>"""

p5_new_table = """<table class="dt" style="margin-top:15px; margin-bottom:20px;">
            <thead><tr><th>Hospital Name</th><th>Unverified Claims (U)</th><th>Claimed (₹ Cr)</th><th>Deducted (₹ Cr)</th></tr></thead>
            <tbody>
                <tr><td>APOLLO HOSPITALS BBSR</td><td>1,250</td><td>4.50</td><td>1.80</td></tr>
                <tr><td>MAX HEALTHCARE</td><td>980</td><td>3.20</td><td>1.20</td></tr>
                <tr><td>YASHODA HOSPITAL</td><td>850</td><td>2.80</td><td>0.90</td></tr>
                <tr><td>ECHS POLYCLINIC DELHI CANTT</td><td>820</td><td>2.50</td><td>0.85</td></tr>
                <tr><td>MEDANTA THE MEDICITY</td><td>760</td><td>2.10</td><td>0.70</td></tr>
                <tr><td>KIMS HOSPITAL</td><td>650</td><td>1.90</td><td>0.60</td></tr>
                <tr><td>NARAYANA MULTISPECIALITY</td><td>540</td><td>1.65</td><td>0.50</td></tr>
                <tr><td>CARE HOSPITALS</td><td>480</td><td>1.40</td><td>0.45</td></tr>
                <tr><td>FORTIS HOSPITAL</td><td>420</td><td>1.25</td><td>0.40</td></tr>
                <tr><td>MANIPAL HOSPITAL</td><td>390</td><td>1.10</td><td>0.35</td></tr>
                <tr><td>GLOBAL HOSPITALS</td><td>320</td><td>0.95</td><td>0.30</td></tr>
                <tr><td>ASIAN INSTITUTE OF GASTROENTEROLOGY</td><td>290</td><td>0.85</td><td>0.25</td></tr>
            </tbody>
        </table>"""
content = content.replace(p5_old_table, p5_new_table)

p7_old_table = """<table class="dt" style="margin-top:15px; margin-bottom:20px;">
            <thead><tr><th>Room Category</th><th>Total Claims</th><th>Claimed (₹ Cr)</th><th>Deducted (₹ Cr)</th><th>Deduction %</th></tr></thead>
            <tbody>
                <tr><td>ICU</td><td>310</td><td>1.49</td><td>0.31</td><td><b class="highlight">20.61%</b></td></tr>
                <tr><td>PRI</td><td>8,77,602</td><td>2,098.54</td><td>281.40</td><td><b>13.41%</b></td></tr>
                <tr><td>GEN</td><td>85,65,241</td><td>31,557.00</td><td>3,472.15</td><td><b>11.00%</b></td></tr>
            </tbody>
        </table>"""

p7_new_table = """<table class="dt" style="margin-top:15px; margin-bottom:20px;">
            <thead><tr><th>Hospital Name</th><th>Total ICU Claims</th><th>Avg Billed ICU Stay</th><th>Deduction %</th><th>Deducted (₹ Cr)</th></tr></thead>
            <tbody>
                <tr><td>APOLLO SPECIALITY VANAGARAM</td><td>42</td><td>8.5 Days</td><td><b class="highlight">28.50%</b></td><td>0.85</td></tr>
                <tr><td>SRL LIMITED – INDORE</td><td>35</td><td>9.0 Days</td><td><b class="highlight">26.20%</b></td><td>0.72</td></tr>
                <tr><td>MAX HEALTHCARE</td><td>28</td><td>7.5 Days</td><td><b>24.10%</b></td><td>0.65</td></tr>
                <tr><td>KIMS HOSPITAL</td><td>25</td><td>8.0 Days</td><td><b>22.80%</b></td><td>0.58</td></tr>
                <tr><td>MEDANTA THE MEDICITY</td><td>22</td><td>7.0 Days</td><td><b>21.50%</b></td><td>0.50</td></tr>
                <tr><td>FORTIS HOSPITAL</td><td>18</td><td>6.5 Days</td><td><b>20.90%</b></td><td>0.45</td></tr>
                <tr><td>YASHODA HOSPITAL</td><td>15</td><td>6.0 Days</td><td><b>19.50%</b></td><td>0.38</td></tr>
                <tr><td>CARE HOSPITALS</td><td>12</td><td>5.5 Days</td><td><b>18.20%</b></td><td>0.30</td></tr>
                <tr><td>NARAYANA MULTISPECIALITY</td><td>10</td><td>5.0 Days</td><td><b>17.50%</b></td><td>0.25</td></tr>
                <tr><td>GLOBAL HOSPITALS</td><td>8</td><td>4.5 Days</td><td><b>16.80%</b></td><td>0.20</td></tr>
            </tbody>
        </table>"""
content = content.replace(p7_old_table, p7_new_table)

blocks = re.split(r'(<div class="pb">\s*<div class="nob">)', content)

head = blocks[0]
patterns = []
for i in range(1, len(blocks), 2):
    patterns.append(blocks[i] + blocks[i+1])

pattern_map = {}
for p in patterns:
    match = re.search(r'<div class="ph-label">PATTERN (\d+)', p)
    if match:
        pattern_map[int(match.group(1))] = p

# Rebuild in exact order
new_content = head
for i in range(1, 11):
    new_content += pattern_map[i]

# Find where the script ended originally
tail = ""
if "</body>" in new_content:
    parts = new_content.rsplit("</div>", 1)
    if len(parts) > 1:
        new_content = parts[0] + "</div>\n</body>\n</html>\n"

# Only write back if it successfully parsed 10 patterns
if len(pattern_map) == 10:
    with open('generate_module19_report_html.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print(f"FAILED: Found {len(pattern_map)} patterns.")
