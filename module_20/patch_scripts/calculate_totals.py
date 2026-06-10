import glob
import csv
import os

def load_latest(pattern):
    files = glob.glob(os.path.join('new_data', pattern))
    if not files: return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def process_p3(file_path):
    tot_pkg_c, tot_pkg_d, count_pkg = 0.0, 0.0, 0
    tot_anti_c, tot_anti_d, count_anti = 0.0, 0.0, 0
    tot_unj_c, tot_unj_d, count_unj = 0.0, 0.0, 0
    
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            t = r.get("auditor_remarks", "").lower()
            try:
                c = float(r.get("item_claimed_amount", 0))
                d = float(r.get("item_deducted_amount", 0))
            except:
                continue
                
            if any(k in t for k in ["antibiotic", "tigecyhos", "dose", "excess", "amfight", "colihos"]):
                count_anti += 1
                tot_anti_c += c
                tot_anti_d += d
            elif any(k in t for k in ["package", "already covered"]):
                count_pkg += 1
                tot_pkg_c += c
                tot_pkg_d += d
            else:
                count_unj += 1
                tot_unj_c += c
                tot_unj_d += d
    
    return {
        "pkg_count": count_pkg, "pkg_c": tot_pkg_c, "pkg_d": tot_pkg_d,
        "anti_count": count_anti, "anti_c": tot_anti_c, "anti_d": tot_anti_d,
        "unj_count": count_unj, "unj_c": tot_unj_c, "unj_d": tot_unj_d,
        "total_count": count_pkg + count_anti + count_unj,
        "total_c": (tot_pkg_c + tot_anti_c + tot_unj_c) / 100000.0,
        "total_d": (tot_pkg_d + tot_anti_d + tot_unj_d) / 100000.0
    }

def process_csv(file_path, count_col, claimed_col, deducted_col):
    count = 0
    claimed = 0.0
    deducted = 0.0
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if count_col:
                try: count += int(float(r.get(count_col, 0)))
                except: count += 1
            else:
                count += 1
                
            try: claimed += float(r.get(claimed_col, 0))
            except: pass
            
            if deducted_col:
                try: deducted += float(r.get(deducted_col, 0))
                except: pass
                
    return count, claimed, deducted

def process_corporate(file_path):
    count, claimed, deducted = 0, 0.0, 0.0
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                count += int(float(r.get("total_claims", 0)))
                claimed += float(r.get("total_claimed_lakh", 0))
                deducted += float(r.get("total_deducted_lakh", 0))
            except: pass
    return count, claimed, deducted

print("--- RESULTS ---")

f_p1 = load_latest("new_04b_hospital_all_claims*.csv")
if f_p1:
    c_p1, cl_p1, d_p1 = process_corporate(f_p1)
    print(f"P1 (Corporate): {c_p1} claims | {cl_p1:.2f} L | {d_p1:.2f} L")

f_p3 = load_latest("new_07_targeted_itemized_deductions*.csv")
if f_p3:
    p3_res = process_p3(f_p3)
    print(f"P3 (Itemized): {p3_res['total_count']} cases | {p3_res['total_c']:.2f} L | {p3_res['total_d']:.2f} L")
    print(f"  Pkg: {p3_res['pkg_count']} | Anti: {p3_res['anti_count']} | Unj: {p3_res['unj_count']}")
    
f_p4 = load_latest("new_08_los_bed_blocking_abuse*.csv")
if f_p4:
    c_p4, cl_p4, d_p4 = process_csv(f_p4, None, "claimed_amount", "deducted_amount")
    print(f"P4 (LoS): {c_p4} cases | {cl_p4/100000.0:.2f} L | {d_p4/100000.0:.2f} L")

f_p5 = load_latest("new_09_ping_pong_admissions*.csv")
if f_p5:
    c_p5, cl_p5, d_p5 = process_csv(f_p5, None, "total_claimed_lakh", "total_deducted_lakh")
    print(f"P5 (PingPong): {c_p5} cases | {cl_p5:.2f} L | {d_p5:.2f} L")
    
f_p6 = load_latest("new_10_weekend_surge_abuse*.csv")
if f_p6:
    c_p6, cl_p6, d_p6 = process_csv(f_p6, "claims_this_weekend", "total_claimed_lakhs", "total_deducted_lakhs")
    print(f"P6 (Weekend): {c_p6} claims | {cl_p6:.2f} L | {d_p6:.2f} L")

f_p7 = load_latest("new_11_superman_surgeon*.csv")
if f_p7:
    c_p7, cl_p7, d_p7 = process_csv(f_p7, "surgeries_in_one_day", "total_claimed_lakhs", None)
    print(f"P7 (Superman): {c_p7} surgeries | {cl_p7:.2f} L | 0 L")

f_p8 = load_latest("new_12_threshold_avoiding*.csv")
if f_p8:
    c_p8, cl_p8, d_p8 = process_csv(f_p8, "trick_bills_count", "total_claimed_lakhs", "total_deducted_lakhs")
    print(f"P8 (Threshold): {c_p8} bills | {cl_p8:.2f} L | {d_p8:.2f} L")

