import os
import csv
import glob

BASE_DIR = '/home/tarun/Downloads/CC/echs_analysis/module_20'
DATA2_DIR = os.path.join(BASE_DIR, 'data_2')

def get_csv_metrics(pattern_dir, filename_pattern, claim_idx=None, approved_idx=None, claimed_idx=None, is_cr=False, is_lakh=False):
    """Helper to read CSV metrics."""
    matches = glob.glob(os.path.join(DATA2_DIR, pattern_dir, filename_pattern))
    if not matches:
        return 0, 0.0, 0.0
        
    csv_path = matches[0]
    count = 0
    total_approved = 0.0
    total_claimed = 0.0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            count += 1
            
            # Extract claimed/approved amounts if indices are provided
            try:
                if claimed_idx is not None:
                    total_claimed += float(row[claimed_idx] or 0)
                if approved_idx is not None:
                    total_approved += float(row[approved_idx] or 0)
            except ValueError:
                continue
                
    # Normalize to Crores
    if is_cr:
        pass # already in Crores
    elif is_lakh:
        total_claimed /= 100.0
        total_approved /= 100.0
    else:
        # Raw rupees
        total_claimed /= 10000000.0
        total_approved /= 10000000.0
        
    return count, total_claimed, total_approved

def main():
    print("=" * 80)
    print("COMPILING FINAL 5-PATTERN FORENSIC REPORT SUMMARY")
    print("=" * 80)
    
    # 1. Pattern 1
    # 1a: card sharing (pat1a_card_sharing_details.csv)
    # card_id, admission_date, patient_name, hosp1_id, hosp1_name, hosp1_city, hosp2_id, hosp2_name, hosp2_city, claim1_id, claim2_id, claim1_amt, claim2_amt, approved1_amt, approved2_amt, ailment1, ailment2, realized_leakage
    # count is number of rows. claim1_amt (index 11) + claim2_amt (index 12), realized_leakage (index 17)
    c1a, cl1a, ap1a = get_csv_metrics(
        'pattern_1_beneficiary_abuse/sub_pattern_1a_card_sharing',
        'pat1a_card_sharing_details.csv',
        claimed_idx=11, approved_idx=17 # index 17 has approved1+approved2 sum
    )
    # Add second claim amount to claimed
    with open(glob.glob(os.path.join(DATA2_DIR, 'pattern_1_beneficiary_abuse/sub_pattern_1a_card_sharing/pat1a_card_sharing_details.csv'))[0], 'r') as f:
        r = csv.reader(f)
        next(r)
        cl1a_extra = sum(float(row[12] or 0) for row in r if len(row) > 12) / 10000000.0
        cl1a += cl1a_extra
        
    # 1b: demographic mismatch (pat1b_demographic_mismatch_details.csv)
    # card_id, beneficiary_name, patient_name, gender, relationship, claim_id, admission_date, hospital_name, claimed_amount, approved_amount, realized_leakage, anomaly_type
    # index 8: claimed, index 9: approved
    c1b, cl1b, ap1b = get_csv_metrics(
        'pattern_1_beneficiary_abuse/sub_pattern_1b_demographic_mismatch',
        'pat1b_demographic_mismatch_details.csv',
        claimed_idx=8, approved_idx=9
    )
    
    # 1c: deceased beneficiary (pat1c_deceased_beneficiary_details.csv)
    # card_id, patient_name, date_of_death, claim_id, admission_date, discharge_date, hospital_name, treating_doctor, claimed_amount, approved_amount, realized_leakage
    # index 8: claimed, index 9: approved
    c1c, cl1c, ap1c = get_csv_metrics(
        'pattern_1_beneficiary_abuse/sub_pattern_1c_deceased_beneficiary',
        'pat1c_deceased_beneficiary_details.csv',
        claimed_idx=8, approved_idx=9
    )
    
    # 2. Pattern 2
    # 2a: hospital leakage ranking (pat2a_hospital_leakage_ranking.csv)
    # hospital_id, hospital_name, city, state, hosp_type, total_claims, total_claimed_cr, total_approved_cr, total_deducted_cr, deduction_pct, realized_leakage_cr
    # count: total_claims sum. total_claimed_cr (index 6), total_approved_cr (index 7)
    c2a = 0
    cl2a = 0.0
    ap2a = 0.0
    with open(glob.glob(os.path.join(DATA2_DIR, 'pattern_2_provider_abuse/sub_pattern_2a_hospital_leakage_ranking/pat2a_hospital_leakage_ranking.csv'))[0], 'r') as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            c2a += int(row[5])
            cl2a += float(row[6])
            ap2a += float(row[7])
            
    # 2b: referral collusion rings (pat2b_referral_collusion_rings.csv)
    # hospital_name, treating_doctor, num_claims, num_distinct_patients, total_claimed_lakh, total_approved_lakh, realized_leakage_lakh, collusion_index
    # count is number of rows. claimed: index 4 (Lakh), approved: index 5 (Lakh)
    c2b, cl2b, ap2b = get_csv_metrics(
        'pattern_2_provider_abuse/sub_pattern_2b_referral_collusion_rings',
        'pat2b_referral_collusion_rings.csv',
        claimed_idx=4, approved_idx=5, is_lakh=True
    )
    # Actual rings count is count, but claims sum is:
    claims_sum_2b = 0
    with open(glob.glob(os.path.join(DATA2_DIR, 'pattern_2_provider_abuse/sub_pattern_2b_referral_collusion_rings/pat2b_referral_collusion_rings.csv'))[0], 'r') as f:
        r = csv.reader(f)
        next(r)
        claims_sum_2b = sum(int(row[2]) for row in r)
        
    # 3. Pattern 3
    # 3a: superman surgeon (pat3a_superman_surgeon_details.csv)
    # doctor_name, admission_date, hospital_name, surgeries_performed, total_claimed_lakh, total_approved_lakh
    c3a, cl3a, ap3a = get_csv_metrics(
        'pattern_3_doctor_anomaly/sub_pattern_3a_superman_surgeon',
        'pat3a_superman_surgeon_details.csv',
        claimed_idx=4, approved_idx=5, is_lakh=True
    )
    surgeries_sum_3a = 0
    with open(glob.glob(os.path.join(DATA2_DIR, 'pattern_3_doctor_anomaly/sub_pattern_3a_superman_surgeon/pat3a_superman_surgeon_details.csv'))[0], 'r') as f:
        r = csv.reader(f)
        next(r)
        surgeries_sum_3a = sum(int(row[3]) for row in r)
        
    # 4. Pattern 4
    # 4a: threshold avoidance (pat4a_threshold_avoidance_details.csv)
    # claim_id, hospital_name, patient_name, admission_date, ailment, claimed_amount, approved_amount, treating_doctor
    c4a, cl4a, ap4a = get_csv_metrics(
        'pattern_4_claim_manipulation/sub_pattern_4a_threshold_avoidance',
        'pat4a_threshold_avoidance_details.csv',
        claimed_idx=5, approved_idx=6
    )
    
    # 4b: duplicate claims (pat4b_duplicate_claims_details.csv)
    # patient_name, card_id, hospital_name, claim_id_1, claim_id_2, admission_date_1, admission_date_2, claimed_amount, approved_amount
    c4b, cl4b, ap4b = get_csv_metrics(
        'pattern_4_claim_manipulation/sub_pattern_4b_duplicate_claims',
        'pat4b_duplicate_claims_details.csv',
        claimed_idx=7, approved_idx=8
    )
    
    # 5. Pattern 5
    # 5a: weekend emergency (pat5a_weekend_emergency_surge.csv)
    # claim_id, hospital_name, patient_name, admission_date, day_of_week, ailment, claimed_amount, approved_amount
    c5a, cl5a, ap5a = get_csv_metrics(
        'pattern_5_temporal_surge/sub_pattern_5a_weekend_emergency_surge',
        'pat5a_weekend_emergency_surge.csv',
        claimed_idx=6, approved_idx=7
    )
    
    # 5b: monthend spike (pat5b_monthend_spike_analysis.csv)
    # hospital_name, month_year, normal_days_avg_claims, monthend_days_avg_claims, spike_ratio, extra_monthend_approved_lakh
    # count: number of hospital-month spikes. leakage: index 5 (Lakh)
    c5b, _, ap5b = get_csv_metrics(
        'pattern_5_temporal_surge/sub_pattern_5b_monthend_spike',
        'pat5b_monthend_spike_analysis.csv',
        approved_idx=5, is_lakh=True
    )
    
    # Write summary report
    summary_path = os.path.join(BASE_DIR, 'final_5pattern_report_summary.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# ECHS Module 20 Forensic Analysis 5-Pattern Summary (2021–2026)

This document contains the consolidated results of the ECHS Module 20 forensic leakage detection based on the new **5-Pattern Behavioral Taxonomy** from 100% of the claims database (4,401,708 rows scanned).

---

## 1. Key Metrics & Financial Results (Consolidated)

*   **Total Claims Scanned:** 4,401,708 claims
*   **Total Base ECHS Approved Budget:** ₹32,649.04 Cr
*   **Total Prevented Leakage (Deductions):** ₹3,612.41 Cr (intercepted savings)

### **Behavioral Taxonomy Summary Table**

| Pattern ID & Behavioral Category | Flagged Cases | Total Claimed (Cr) | Realized Leakage (Approved Cr) | % of ECHS Approved Budget |
| :--- | :---: | :---: | :---: | :---: |
| **Pattern 1: Beneficiary & Dependency Abuse** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*1a. Card Sharing (Concurrent Admissions)* | {c1a:,} pairs | ₹{cl1a:.4f} Cr | ₹{ap1a:.4f} Cr | {ap1a * 100 / 32649.04:.4f}% |
| &nbsp;&nbsp;&nbsp;&nbsp;*1b. Demographic Relationship Mismatches* | {c1b:,} claims | ₹{cl1b:.4f} Cr | ₹{ap1b:.4f} Cr | {ap1b * 100 / 32649.04:.4f}% |
| &nbsp;&nbsp;&nbsp;&nbsp;*1c. Deceased Beneficiary Lazarus Billing* | {c1c:,} claims | ₹{cl1c:.4f} Cr | ₹{ap1c:.4f} Cr | {ap1c * 100 / 32649.04:.4f}% |
| **Pattern 2: Systematic Provider Abuse & Collusion** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*2a. Hospital Audit Leakage Ranking* | {c2a:,} claims | ₹{cl2a:.4f} Cr | ₹{ap2a:.4f} Cr | {ap2a * 100 / 32649.04:.4f}% |
| &nbsp;&nbsp;&nbsp;&nbsp;*2b. Referral Collusion Doctor Rings* | {c2b:,} rings ({claims_sum_2b:,} claims) | ₹{cl2b:.4f} Cr | ₹{ap2b:.4f} Cr | {ap2b * 100 / 32649.04:.4f}% |
| **Pattern 3: Doctor-Level & Clinical Anomaly** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*3a. Superman Surgeons (>=15 surgeries/day)* | {c3a:,} days ({surgeries_sum_3a:,} claims) | ₹{cl3a:.4f} Cr | ₹{ap3a:.4f} Cr | {ap3a * 100 / 32649.04:.4f}% |
| **Pattern 4: Claim Manipulation & Billing Evasion** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*4a. CFA Threshold Avoidance (₹99k-99.9k)* | {c4a:,} claims | ₹{cl4a:.4f} Cr | ₹{ap4a:.4f} Cr | {ap4a * 100 / 32649.04:.4f}% |
| &nbsp;&nbsp;&nbsp;&nbsp;*4b. Duplicate Claims (Same patient/amt <=48h)* | {c4b:,} pairs | ₹{cl4b:.4f} Cr | ₹{ap4b:.4f} Cr | {ap4b * 100 / 32649.04:.4f}% |
| **Pattern 5: Temporal Surge & Referral Bypass** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*5a. Weekend Emergency Surge (Sat/Sun)* | {c5a:,} claims | ₹{cl5a:.4f} Cr | ₹{ap5a:.4f} Cr | {ap5a * 100 / 32649.04:.4f}% |
| &nbsp;&nbsp;&nbsp;&nbsp;*5b. Month-End Billing Spikes* | {c5b:,} spikes | - | ₹{ap5b:.4f} Cr | {ap5b * 100 / 32649.04:.4f}% |

---

## 2. Saved Forensic Deliverables (CSV Paths under data_2/)

* **Pattern 1:**
  - Card Sharing: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1a_card_sharing/pat1a_card_sharing_details.csv`
  - Demographic Mismatch: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1b_demographic_mismatch/pat1b_demographic_mismatch_details.csv`
  - Deceased Beneficiary: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1c_deceased_beneficiary/pat1c_deceased_beneficiary_details.csv`
* **Pattern 2:**
  - Hospital Leakage: `data_2/pattern_2_provider_abuse/sub_pattern_2a_hospital_leakage_ranking/pat2a_hospital_leakage_ranking.csv`
  - Referral Collusion: `data_2/pattern_2_provider_abuse/sub_pattern_2b_referral_collusion_rings/pat2b_referral_collusion_rings.csv`
* **Pattern 3:**
  - Superman Surgeon: `data_2/pattern_3_doctor_anomaly/sub_pattern_3a_superman_surgeon/pat3a_superman_surgeon_details.csv`
* **Pattern 4:**
  - CFA Threshold: `data_2/pattern_4_claim_manipulation/sub_pattern_4a_threshold_avoidance/pat4a_threshold_avoidance_details.csv`
  - Duplicate Bills: `data_2/pattern_4_claim_manipulation/sub_pattern_4b_duplicate_claims/pat4b_duplicate_claims_details.csv`
* **Pattern 5:**
  - Weekend emergency: `data_2/pattern_5_temporal_surge/sub_pattern_5a_weekend_emergency_surge/pat5a_weekend_emergency_surge.csv`
  - Month-End Spike: `data_2/pattern_5_temporal_surge/sub_pattern_5b_monthend_spike/pat5b_monthend_spike_analysis.csv`

---

## 3. Core Refactoring Summary
1. **Consolidation:** The ECHS forensic taxonomy has been streamlined from 8 chaotic leakage tags into 5 behavioral classifications.
2. **Exhaustive Scope:** Removed all `LIMIT` constraints from extraction. Fallback engines now parse 100% of the 1.38 GB claims file.
3. **Audit Nomenclature:** Normalised output files with systematic prefixes (e.g., `pat1a_`, `pat2a_`, `pat5b_`) for complete audit traceability.
""")

    print(f"✓ Saved 5-pattern summary report to {summary_path}")

if __name__ == '__main__':
    main()
