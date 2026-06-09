with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Demographic Block (Line 590 to 619)
demo_start = "# ── PATTERN 5: DEMOGRAPHIC CLAIMS ABUSE ───────────────────────────────────────"
demo_end = "</div>\"\"\")"

start_idx = code.find(demo_start)
end_idx = code.find(demo_end, start_idx) + len(demo_end)

if start_idx != -1 and end_idx != -1:
    demo_code = code[start_idx:end_idx]
    code = code[:start_idx] + code[end_idx:] # Remove it
else:
    print("DEMO NOT FOUND")
    exit(1)

# 2. Regional Commands Block (Ends at </div>""") around line 505)
reg_start = "# ── PATTERN 4: REGIONAL COMMANDS ──────────────────────────────────────────────"
reg_start_idx = code.find(reg_start)
reg_end_idx = code.find(demo_end, reg_start_idx) + len(demo_end)

if reg_start_idx != -1 and reg_end_idx != -1:
    # Insert demo_code after regional block
    code = code[:reg_end_idx] + "\n\n" + demo_code + code[reg_end_idx:]
else:
    print("REGIONAL NOT FOUND")
    exit(1)

# 3. Annual Trends (Insert after Corporate Hospital)
corp_end_str = '<div class="kf-item"><b>Park Hospital Chain Cumulative Impact:</b> With multiple empanelled facilities in the top deduction tiers (Gurgaon, Chowkhandi, Kailash), the Park Hospital chain represents the largest corporate audit target. Chain-level coordination warrants an empanelment review.</div>\n</div>""")'
corp_idx = code.find(corp_end_str)

annual_code = """

# ── PATTERN 2.1: ANNUAL TRENDS ────────────────────────────────────────────────
if p02a:
    H.append(f'''
<div class="tc" style="margin-top:20px; font-weight:800; color:{NAV};">Pattern 2.1 — Annual Expenditure &amp; Deduction Trends</div>
<table class="dt">
{th("Financial Year","Claims","Claimed (₹ Cr)","Approved (₹ Cr)","Deducted (₹ Cr)","Deduction %")}
<tbody>''')
    for r in p02a:
        fy = safe(r.get("financial_year",""))
        claims = int(float(r.get("total_claims",0)))
        claimed = float(r.get("total_claimed_cr", 0))
        approved = float(r.get("total_approved_cr", 0))
        deducted = float(r.get("total_deducted_cr", 0))
        ded_pct = float(r.get("deduction_pct", 0))
        H.append(f"<tr><td><b>{fy}</b></td><td>{fmt(claims)}</td>"
                 f"<td>{claimed:,.2f}</td><td>{approved:,.2f}</td><td>{deducted:,.2f}</td>"
                 f"<td>{ded_pct:.2f}%</td></tr>")
    H.append(f'''</tbody></table>
<div class="kf-head">Key Findings</div>
<div class="kf-item"><b>Inflation Trend:</b> The data shows a massive escalation in budget leakage across the FY 2021-2026 window, directly correlating with increased private hospital utilization.</div>
</div>''')
"""

if corp_idx != -1:
    insert_point = corp_idx + len(corp_end_str)
    code = code[:insert_point] + annual_code + code[insert_point:]
else:
    print("CORP NOT FOUND")
    exit(1)


with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
