import csv, glob
f_top = glob.glob("new_data/new_04a_hospital_leakage_summary_*.csv")[0]
tot_claims = 0
with open(f_top, encoding='utf-8') as f:
    reader = list(csv.DictReader(f))
    for r in reader[:50]:
        tot_claims += int(float(r.get('total_claims', 0)))
print(f"Top 50 claims: {tot_claims}")
