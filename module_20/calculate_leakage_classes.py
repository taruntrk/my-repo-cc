import os
import csv

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'new_data')
    
    # Files to look for (using latest files)
    import glob
    def get_latest_csv(pattern):
        matches = glob.glob(os.path.join(data_dir, pattern))
        if matches:
            matches.sort(key=os.path.getmtime, reverse=True)
            return matches[0]
        return None

    # Let's define leakage categories
    print("="*80)
    print("CLASSIFYING ECHS APPROVED LEAKAGE (REALIZED FRAUD/ABUSE) 2021-2026")
    print("="*80)

    # 1. Total Approved Volume for 2021-2026 (Base)
    # Total claimed: ~36,261.45 Cr, Total approved: ~32,649.04 Cr, Total prevented: ~3,612.41 Cr
    total_approved_cr = 32649.04
    total_claimed_cr = 36261.45

    # 2. Individual/Beneficiary-Level Leakage (Demographic & Relation Mismatches)
    gender_relation_file = get_latest_csv("new_08a_gender_relation_summary_*.csv")
    demographic_leakage_approved_cr = 0.0
    demographic_leakage_deducted_cr = 0.0
    demographic_claims = 0
    
    mismatch_categories = []
    
    if gender_relation_file:
        with open(gender_relation_file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                gender = r.get('gender', '')
                relation = r.get('relationship', '')
                claims = int(r.get('total_claims', 0))
                claimed_cr = float(r.get('total_claimed_cr', 0.0))
                approved_cr = float(r.get('total_approved_cr', 0.0))
                deducted_cr = float(r.get('total_deducted_cr', 0.0))
                
                # Check for clear demographic/gender-relationship mismatches
                # e.g., Male listed as Wife/Mother/Daughter or Female listed as Father/Son/Husband
                is_mismatch = False
                reason = ""
                
                if gender == 'M' and relation in ['Wife', 'Mother', 'Daughter', 'Sister', 'Daughters-Daughter']:
                    is_mismatch = True
                    reason = "Male registered as Female Relationship"
                elif gender == 'F' and relation in ['Husband', 'Father', 'Son', 'Brother', 'Daughters-Son']:
                    is_mismatch = True
                    reason = "Female registered as Male Relationship"
                
                if is_mismatch:
                    demographic_leakage_approved_cr += approved_cr
                    demographic_leakage_deducted_cr += deducted_cr
                    demographic_claims += claims
                    mismatch_categories.append({
                        'gender': gender,
                        'relation': relation,
                        'claims': claims,
                        'approved_cr': approved_cr,
                        'reason': reason
                    })
                    
    print("\n[CATEGORY A] INDIVIDUAL / BENEFICIARY-LEVEL LEAKAGE (Demographic & Relation Mismatch)")
    print(f"Total claims flagged: {demographic_claims:,}")
    print(f"Total realized leakage (Approved amount): ₹{demographic_leakage_approved_cr:.2f} Cr")
    print(f"Leakage % of Total ECHS Approved Budget: {demographic_leakage_approved_cr * 100.0 / total_approved_cr:.4f}%")
    print("\nDetailed Mismatch Breakdown:")
    for m in mismatch_categories:
        print(f"  - Gender: {m['gender']} | Relation: {m['relation']} | Claims: {m['claims']:,} | Approved: ₹{m['approved_cr']:.2f} Cr ({m['reason']})")

    # 3. Policy-Evasion / System-Vetting Leakage (Threshold Evasion & Ping-Pong Readmission)
    # Threshold Evasion: claims between 99k and 99.99k
    threshold_file = get_latest_csv("new_12_threshold_avoiding_*.csv")
    threshold_claims_count = 0
    threshold_claimed_lakhs = 0.0
    threshold_deducted_lakhs = 0.0
    if threshold_file:
        with open(threshold_file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                threshold_claims_count += int(r.get('trick_bills_count', 0))
                threshold_claimed_lakhs += float(r.get('total_claimed_lakhs', 0.0))
                threshold_deducted_lakhs += float(r.get('total_deducted_lakhs', 0.0))
                
    # Ping-Pong Readmission
    ping_pong_file = get_latest_csv("new_09_ping_pong_admissions_*.csv")
    ping_pong_claims_count = 0
    ping_pong_claim_amt_lakhs = 0.0
    if ping_pong_file:
        with open(ping_pong_file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                ping_pong_claims_count += 1
                ping_pong_claim_amt_lakhs += float(r.get('claim_amt', 0.0)) / 100000.0

    print("\n[CATEGORY B] POLICY-EVASION / SYSTEM-VETTING LEAKAGE")
    # CS_UTI_APP_AMT is net claim amt minus deducted amt
    threshold_approved_lakhs = threshold_claimed_lakhs - threshold_deducted_lakhs
    threshold_approved_cr = threshold_approved_lakhs / 100.0
    print(f"1. CFA Threshold Evasion (₹99k-99.9k bills):")
    print(f"   - Flagged claims: {threshold_claims_count:,}")
    print(f"   - Total realized leakage (Approved amount): ₹{threshold_approved_cr:.2f} Cr")
    print(f"   - Leakage % of Total ECHS Approved Budget: {threshold_approved_cr * 100.0 / total_approved_cr:.4f}%")
    
    ping_pong_approved_cr = ping_pong_claim_amt_lakhs / 100.0
    print(f"2. Ping-Pong Readmissions (Discharge & readmit < 48 hours):")
    print(f"   - Flagged claims: {ping_pong_claims_count:,}")
    print(f"   - Total realized leakage (Approved amount): ₹{ping_pong_approved_cr:.2f} Cr")
    print(f"   - Leakage % of Total ECHS Approved Budget: {ping_pong_approved_cr * 100.0 / total_approved_cr:.4f}%")

    # 4. Hospital-Level Systematic Leakage (Weekend Surges & Surgeon Cloning)
    weekend_file = get_latest_csv("new_10_weekend_surge_abuse_*.csv")
    weekend_claims_count = 0
    weekend_claimed_lakhs = 0.0
    weekend_deducted_lakhs = 0.0
    if weekend_file:
        with open(weekend_file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                weekend_claims_count += int(r.get('weekend_admissions', 0))
                weekend_claimed_lakhs += float(r.get('total_claimed_lakhs', 0.0))
                weekend_deducted_lakhs += float(r.get('total_deducted_lakhs', 0.0))

    surgeon_file = get_latest_csv("new_11_superman_surgeon_*.csv")
    surgeon_claims_count = 0
    surgeon_claimed_lakhs = 0.0
    if surgeon_file:
        with open(surgeon_file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                surgeon_claims_count += int(r.get('surgeries_in_one_day', 0))
                surgeon_claimed_lakhs += float(r.get('total_claimed_lakhs', 0.0))

    print("\n[CATEGORY C] HOSPITAL-LEVEL SYSTEMATIC LEAKAGE (Accreditation & Billing Surges)")
    weekend_approved_cr = (weekend_claimed_lakhs - weekend_deducted_lakhs) / 100.0
    print(f"1. Weekend Emergency Surge Admissions (Bypassing Vetting):")
    print(f"   - Flagged admissions: {weekend_claims_count:,}")
    print(f"   - Total realized leakage (Approved amount): ₹{weekend_approved_cr:.2f} Cr")
    print(f"   - Leakage % of Total ECHS Approved Budget: {weekend_approved_cr * 100.0 / total_approved_cr:.4f}%")
    
    surgeon_approved_cr = surgeon_claimed_lakhs / 100.0
    print(f"2. Superman Surgeon Cloning (>15 surgeries/day per doctor):")
    print(f"   - Flagged claims: {surgeon_claims_count:,}")
    print(f"   - Total realized leakage (Approved amount): ₹{surgeon_approved_cr:.2f} Cr")
    print(f"   - Leakage % of Total ECHS Approved Budget: {surgeon_approved_cr * 100.0 / total_approved_cr:.4f}%")

    print("\n" + "="*80)
    print("SUMMARY OF CLASSIFIED LEAKAGE BUDGET EXPOSURE")
    print("="*80)
    total_classified_leakage = demographic_leakage_approved_cr + threshold_approved_cr + ping_pong_approved_cr + weekend_approved_cr + surgeon_approved_cr
    print(f"Total Classified Realized Leakage: ₹{total_classified_leakage:.2f} Cr")
    print(f"Overall Fraud Leakage %: {total_classified_leakage * 100.0 / total_approved_cr:.2f}% of total approved budget")
    print("="*80)

if __name__ == '__main__':
    main()
