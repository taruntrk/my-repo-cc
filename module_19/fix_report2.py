with open("generate_module19_report_v2.py", "r") as f:
    code = f.read()

replacement = """
df_1 = load_csv("new_19_01_all_hospital_deductions_")
if not df_1.empty and 'billed_amount' in df_1.columns:
    df_1['billed_amount'] = df_1['billed_amount'].astype(float)
    df_1['deducted_amount'] = df_1['deducted_amount'].astype(float)
    df_1 = df_1.groupby(['hospital_id', 'registered_hospital_name', 'hospital_city', 'hospital_state', 'cghs_region', 'hospital_type'], dropna=False).agg(
        total_claims=('claim_id', 'count'),
        total_claimed_lakh=('billed_amount', lambda x: x.sum() / 100000),
        total_deducted_lakh=('deducted_amount', lambda x: x.sum() / 100000)
    ).reset_index()
"""

code = code.replace('df_1 = load_csv("new_19_01_all_hospital_deductions_")', replacement)

with open("generate_module19_report_v2.py", "w") as f:
    f.write(code)
print("Updated generate_module19_report_v2.py to handle raw df_1 data")
