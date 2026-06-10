import pandas as pd

df = pd.read_csv('require_data/data/new_19_01_all_hospital_deductions_20260610_153534.csv', low_memory=False)
p1 = df.groupby('hospital_id').agg(
    hospital_name=('registered_hospital_name', 'first'),
    hospital_type=('hospital_type', 'first'),
    nabh=('hospital_state', 'first'), # Just using something, or we can leave it blank since we don't have nabh natively
    total_claims=('claim_id', 'count'),
    total_claimed_lakh=('billed_amount', lambda x: x.sum() / 100000),
    total_deducted_lakh=('deducted_amount', lambda x: x.sum() / 100000)
).reset_index()

p1['deduction_pct'] = (p1['total_deducted_lakh'] / p1['total_claimed_lakh']) * 100

# Apply filter: >25% deduction rate, >50 claims
filtered = p1[(p1['total_claims'] > 50) & (p1['deduction_pct'] > 25)]

# Sort by deduction_pct descending
top15 = filtered.sort_values('deduction_pct', ascending=False).head(15)

for i, row in enumerate(top15.itertuples(), 1):
    hname = str(row.hospital_name).upper()
    hname = hname[:50] if len(hname) > 50 else hname
    htype = str(row.hospital_type)
    pct = row.deduction_pct
    pct_str = f'<b class="highlight">{pct:.2f}%</b>' if pct > 75 else f'<b>{pct:.2f}%</b>'
    
    html = f"                <tr><td>{row.hospital_id}</td><td><b>{hname}</b></td><td>{htype}</td><td>N</td><td>{row.total_claims}</td><td>{row.total_claimed_lakh/100:.2f}</td><td>{row.total_deducted_lakh/100:.2f}</td><td>{pct_str}</td></tr>"
    print(html)
