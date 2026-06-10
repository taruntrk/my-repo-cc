import csv, glob
f_p3 = glob.glob("new_data/new_07_targeted_itemized_deductions*.csv")[0]
tot_pkg_c, tot_pkg_d, count_pkg = 0.0, 0.0, 0
tot_anti_c, tot_anti_d, count_anti = 0.0, 0.0, 0
tot_unj_c, tot_unj_d, count_unj = 0.0, 0.0, 0

with open(f_p3, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        t = r.get("auditor_remarks", "").lower()
        try:
            c = float(r.get("item_claimed_amount", 0))
            d = float(r.get("item_deducted_amount", 0))
        except: continue
        if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
            count_anti += 1; tot_anti_c += c; tot_anti_d += d
        elif any(k in t for k in ["package", "already covered"]):
            count_pkg += 1; tot_pkg_c += c; tot_pkg_d += d
        else:
            count_unj += 1; tot_unj_c += c; tot_unj_d += d

print(f"Pkg: {count_pkg} cases | C: {tot_pkg_c/10000000:.2f} Cr | D: {tot_pkg_d/10000000:.2f} Cr")
print(f"Anti: {count_anti} cases | C: {tot_anti_c/10000000:.2f} Cr | D: {tot_anti_d/10000000:.2f} Cr")
print(f"Unj: {count_unj} cases | C: {tot_unj_c/10000000:.2f} Cr | D: {tot_unj_d/10000000:.2f} Cr")
