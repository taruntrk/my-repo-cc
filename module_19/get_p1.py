import pandas as pd

df = pd.read_csv('require_data/data/new_19_01_all_hospital_deductions_20260610_153534.csv')
p1 = df.groupby('hospital_id').agg(
    hospital_name=('registered_hospital_name', 'first'),
    total_claims=('claim_id', 'count'),
    total_claimed_lakh=('billed_amount', lambda x: x.sum() / 100000),
    total_approved_lakh=('approved_amount', lambda x: x.sum() / 100000),
    total_deducted_lakh=('deducted_amount', lambda x: x.sum() / 100000)
).reset_index()

p1['deduction_pct'] = (p1['total_deducted_lakh'] / p1['total_claimed_lakh']) * 100
top15 = p1.sort_values('total_deducted_lakh', ascending=False).head(15)

for i, row in enumerate(top15.itertuples(), 1):
    print(f"{i}. {row.hospital_name} (ID {row.hospital_id}) | Claims: {row.total_claims} | Claimed: {row.total_claimed_lakh/100:.2f} Cr | Deducted: {row.total_deducted_lakh/100:.2f} Cr | Ded %: {row.deduction_pct:.2f}%")
