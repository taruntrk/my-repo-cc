import glob
import csv
import os

def load_latest(pattern):
    files = glob.glob(os.path.join('new_data', pattern))
    if not files: return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

# P5 Ping Pong
f_p5 = load_latest("new_09_ping_pong_admissions*.csv")
c_p5, cl_p5 = 0, 0.0
with open(f_p5, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        c_p5 += 1
        try: cl_p5 += float(r.get("claim_amt", 0))
        except: pass
print(f"P5: {c_p5} cases | {cl_p5/100000.0:.2f} L")

# P6 Weekend
f_p6 = load_latest("new_10_weekend_surge_abuse*.csv")
c_p6, cl_p6, d_p6 = 0, 0.0, 0.0
with open(f_p6, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        try: c_p6 += int(r.get("weekend_admissions", 0))
        except: pass
        try: cl_p6 += float(r.get("total_claimed_lakhs", 0))
        except: pass
        try: d_p6 += float(r.get("total_deducted_lakhs", 0))
        except: pass
print(f"P6: {c_p6} cases | {cl_p6:.2f} L | {d_p6:.2f} L")
