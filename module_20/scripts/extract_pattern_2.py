import os
import csv
import sys
import glob
import collections

# SSH Credentials
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_akash'
SSH_PASS = 'Akash@2026'
DB_USER  = 'akash'
DB_PASS  = 'Akash@2026'
DB_NAME  = 'ECHS'

# Folder paths
BASE_DIR = '/home/tarun/Downloads/CC/echs_analysis/module_20'
DATA2_DIR = os.path.join(BASE_DIR, 'data_2')
PATTERN_DIR = os.path.join(DATA2_DIR, 'pattern_2_provider_abuse')

# Sub-pattern folders
SUB_2A_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_2a_hospital_leakage_ranking')
SUB_2B_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_2b_referral_collusion_rings')

# Ensure directories exist
os.makedirs(SUB_2A_DIR, exist_ok=True)
os.makedirs(SUB_2B_DIR, exist_ok=True)

# Queries for Pattern 2
queries = {
    "sub_pattern_2a_hospital_leakage_ranking": """
        SELECT
            ci.CI_CR_OFFICE_ID AS hospital_id,
            om.OM_OFFICE_NAME AS hospital_name,
            om.OM_OFFICE_CITY AS city,
            om.OM_OFFICE_STATE AS state,
            CASE 
                WHEN om.OM_NABH_STATUS = 'Y' THEN 'Private (NABH)' 
                ELSE 'Private (Non-NABH)' 
            END AS hosp_type,
            COUNT(ci.CI_INTIMATION_ID) AS total_claims,
            ROUND(SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 0)) / 10000000, 4) AS total_claimed_cr,
            ROUND(SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 10000000, 4) AS total_approved_cr,
            ROUND(SUM(COALESCE(cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT, 0)) / 10000000, 4) AS total_deducted_cr,
            ROUND((SUM(COALESCE(cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT, 0)) / SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 1))) * 100, 2) AS deduction_pct,
            ROUND(SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 10000000, 4) AS realized_leakage_cr
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
        GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY, om.OM_OFFICE_STATE, om.OM_NABH_STATUS
        ORDER BY total_claims DESC;
    """,

    "sub_pattern_2b_referral_collusion_rings": """
        SELECT
            om.OM_OFFICE_NAME AS hospital_name,
            cs.CS_TREAT_DOCT AS treating_doctor,
            COUNT(cs.CS_INTIMATION_ID) AS num_claims,
            COUNT(DISTINCT ci.CI_BENF_ID) AS num_distinct_patients,
            ROUND(SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 0)) / 100000, 2) AS total_claimed_lakh,
            ROUND(SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 100000, 2) AS total_approved_lakh,
            ROUND(SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 100000, 2) AS realized_leakage_lakh,
            ROUND((COUNT(cs.CS_INTIMATION_ID) / COUNT(DISTINCT ci.CI_BENF_ID)), 2) AS collusion_index
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE cs.CS_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
          AND cs.CS_TREAT_DOCT IS NOT NULL AND cs.CS_TREAT_DOCT != ''
        GROUP BY om.OM_OFFICE_NAME, cs.CS_TREAT_DOCT
        HAVING num_claims >= 10 AND collusion_index > 2.0
        ORDER BY num_claims DESC
        LIMIT 5000;
    """
}

def run_db_extraction():
    """Tries to run query via SSH database client."""
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to SSH {SSH_HOST}...")
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=15)
    print("✓ SSH connected successfully.")
    
    outputs = {}
    for name, query in queries.items():
        print(f"Executing query: {name}...")
        cmd = f'mysql -u{DB_USER} -p{DB_PASS} {DB_NAME} -B'
        stdin_c, stdout, stderr = client.exec_command(cmd, timeout=300)
        stdin_c.write(query.encode('utf-8'))
        stdin_c.channel.shutdown_write()
        out = stdout.read().decode('utf-8', errors='replace')
        if out and out.strip():
            outputs[name] = out
            print(f"  -> Retrieved database results for {name}")
        else:
            print(f"  -> No database results for {name}")
    client.close()
    return outputs

def run_local_fallback():
    """Falls back to local file processing when database is network-unreachable."""
    print("\n⚠️ Database unreachable. Falling back to local file processing...")
    
    # --- SUB-PATTERN 2A: HOSPITAL LEAKAGE RANKING ---
    print("\nProcessing Sub-Pattern 2A: Hospital Leakage Ranking...")
    summary_files = glob.glob(os.path.join(BASE_DIR, 'new_data/new_04a_hospital_leakage_summary_*.csv'))
    if not summary_files:
        print("❌ Error: Could not find new_04a_hospital_leakage_summary_*.csv in new_data/")
        sys.exit(1)
        
    summary_csv = summary_files[0]
    print(f"Using hospital summary file: {summary_csv}")
    
    ranking_data = []
    with open(summary_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            h_id = r.get('hospital_id')
            h_name = r.get('hospital_name')
            city = r.get('city')
            state = r.get('state')
            
            # Format hospital type description
            nabh = r.get('nabh_status', 'N')
            hosp_type = 'Private (NABH)' if nabh == 'Y' else 'Private (Non-NABH)'
            
            claims = int(r.get('total_claims') or 0)
            claimed_l = float(r.get('total_claimed_lakh') or 0)
            approved_l = float(r.get('total_approved_lakh') or 0)
            deducted_l = float(r.get('total_deducted_lakh') or 0)
            deduction_pct = float(r.get('deduction_pct') or 0)
            
            # Convert Lakhs to Crores
            claimed_cr = round(claimed_l / 100.0, 4)
            approved_cr = round(approved_l / 100.0, 4)
            deducted_cr = round(deducted_l / 100.0, 4)
            realized_leakage_cr = approved_cr
            
            ranking_data.append([
                h_id, h_name, city, state, hosp_type,
                claims, claimed_cr, approved_cr, deducted_cr,
                deduction_pct, realized_leakage_cr
            ])
            
    # Sort by total claims descending
    ranking_data.sort(key=lambda x: x[5], reverse=True)
    
    csv_2a = os.path.join(SUB_2A_DIR, 'pat2a_hospital_leakage_ranking.csv')
    with open(csv_2a, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'hospital_id', 'hospital_name', 'city', 'state', 'hosp_type',
            'total_claims', 'total_claimed_cr', 'total_approved_cr', 'total_deducted_cr',
            'deduction_pct', 'realized_leakage_cr'
        ])
        writer.writerows(ranking_data)
    print(f"✓ Saved {len(ranking_data)} rows to {csv_2a}")
    
    # --- SUB-PATTERN 2B: REFERRAL COLLUSION RINGS ---
    print("\nProcessing Sub-Pattern 2B: Referral Collusion Rings...")
    claims_files = glob.glob(os.path.join(BASE_DIR, 'new_data/new_05b_regional_all_claims_*.csv'))
    if not claims_files:
        print("❌ Error: Could not find new_05b_regional_all_claims_*.csv in new_data/")
        sys.exit(1)
        
    main_csv = claims_files[0]
    print(f"Using local claims file for collusion scanning: {main_csv}")
    
    # Group by (hospital_name, treating_doctor)
    # Map to list of [claimed_amt, approved_amt, patient_id]
    rings = collections.defaultdict(list)
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 28:
                continue
            hosp_name = row[4].strip()
            doc = row[23].strip()
            card = row[11].strip()
            claimed = float(row[25] or 0)
            approved = float(row[26] or 0)
            
            if doc and doc not in ['0', 'NA', 'UNKNOWN', '']:
                rings[(hosp_name, doc)].append((claimed, approved, card))
                
    collusion_rings = []
    for (hosp_name, doc), claims_list in rings.items():
        num_claims = len(claims_list)
        patients = {item[2] for item in claims_list}
        num_distinct_patients = len(patients)
        
        if num_distinct_patients == 0:
            continue
            
        collusion_index = round(num_claims / num_distinct_patients, 2)
        
        # Filter rules: num_claims >= 10 and collusion_index > 2.0
        if num_claims >= 10 and collusion_index > 2.0:
            total_claimed_l = round(sum(item[0] for item in claims_list) / 100000.0, 2)
            total_approved_l = round(sum(item[1] for item in claims_list) / 100000.0, 2)
            realized_leakage_l = total_approved_l
            
            collusion_rings.append([
                hosp_name, doc, num_claims, num_distinct_patients,
                total_claimed_l, total_approved_l, realized_leakage_l,
                collusion_index
            ])
            
    # Sort collusion rings by claim count descending
    collusion_rings.sort(key=lambda x: x[2], reverse=True)
    
    csv_2b = os.path.join(SUB_2B_DIR, 'pat2b_referral_collusion_rings.csv')
    with open(csv_2b, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'hospital_name', 'treating_doctor', 'num_claims', 'num_distinct_patients',
            'total_claimed_lakh', 'total_approved_lakh', 'realized_leakage_lakh',
            'collusion_index'
        ])
        writer.writerows(collusion_rings)
    print(f"✓ Saved {len(collusion_rings)} rows to {csv_2b}")

def main():
    print("=" * 80)
    print("ECHS MODULE 20 - PATTERN 2 DATA EXTRACTION SYSTEM")
    print("=" * 80)
    
    try:
        # Try database connection first
        results = run_db_extraction()
        
        # Save database results to CSVs
        for name, data in results.items():
            lines = data.strip().splitlines()
            if name == "sub_pattern_2a_hospital_leakage_ranking":
                path = os.path.join(SUB_2A_DIR, 'pat2a_hospital_leakage_ranking.csv')
            else:
                path = os.path.join(SUB_2B_DIR, 'pat2b_referral_collusion_rings.csv')
                
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for line in lines:
                    writer.writerow(line.split('\t'))
            print(f"✓ Saved database extraction results to: {path}")
            
    except Exception as e:
        # If database connection fails, run local parsing fallback
        print(f"Database extraction failed: {e}")
        run_local_fallback()
        
    print("\n" + "=" * 80)
    print("PATTERN 2 EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == '__main__':
    main()
