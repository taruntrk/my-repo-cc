import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Weekend Admission Pattern
code = code.replace(
    "Hospitals that show a massive spike in admissions specifically on Fridays, Saturdays, and Sundays are likely exploiting the lack of physical ECHS verifiers on duty during the weekend.",
    "Hospitals exhibiting weekend admission rates significantly above peer benchmarks represent a statistical anomaly that may require further audit review."
)

# 2. Ping-Pong Pattern
code = code.replace(
    "This is an explicit attempt to bypass package duration limits and bill two separate procedures instead of one continuous stay.",
    "This indicates potential package-splitting behavior requiring clinical validation to ensure both admissions were medically distinct and necessary."
)

# 3. LOS Findings
code = code.replace(
    "Cases with >15 days for routine ailments signify clear abuse of inpatient resources.",
    "Cases with prolonged stays warrant review against diagnosis severity and clinical necessity to rule out potential resource abuse."
)

# 4. Annual Trend Finding
code = code.replace(
    "directly correlating with increased private hospital utilization.",
    "warranting further review of utilization rates and inflation drivers."
)

# 5. Weekend Pattern - Key Finding softening
code = code.replace(
    '<div class="kf-item"><b>Targeted Evasion:</b> The massive cluster of admissions on non-working days indicates systematic evasion of physical verification protocols.</div>',
    '<div class="kf-item"><b>Statistical Deviation:</b> The cluster of admissions on non-working days deviates from standard elective admission distributions, indicating a potential anomaly in scheduling practices.</div>'
)

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
