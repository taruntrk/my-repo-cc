import os
import csv
import sys
import glob
import collections
from datetime import datetime

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
PATTERN_DIR = os.path.join(DATA2_DIR, 'pattern_4_claim_manipulation')

# Sub-pattern folders
SUB_4A_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_4a_threshold_avoidance')
SUB_4B_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_4b_duplicate_claims')

# Ensure directories exist
os.makedirs(SUB_4A_DIR, exist_ok=True)
os.makedirs(SUB_4B_DIR, exist_ok=True)

# Queries for Pattern 4
queries = {
    "sub_pattern_4a_threshold_avoidance": """
        SELECT
            ci.CI_INTIMATION_ID AS claim_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ci.CI_PATIENT_NAME AS patient_name,
            DATE(ci.CI_ADMISSION_DATE) AS admission_date,
            ci.CI_ADM_AILMENT AS ailment,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) AS claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) AS approved_amount,
            cs.CS_TREAT_DOCT AS treating_doctor
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE cs.CS_NET_CLAIM_AMT BETWEEN 99000 AND 99999
          AND cs.CS_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
        ORDER BY cs.CS_ADMISSION_DATE DESC;
    """,

    "sub_pattern_4b_duplicate_claims": """
        SELECT
            ci1.CI_PATIENT_NAME AS patient_name,
            ci1.CI_CARD_ID AS card_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ci1.CI_INTIMATION_ID AS claim_id_1,
            ci2.CI_INTIMATION_ID AS claim_id_2,
            DATE(ci1.CI_ADMISSION_DATE) AS admission_date_1,
            DATE(ci2.CI_ADMISSION_DATE) AS admission_date_2,
            COALESCE(cs1.CS_NET_CLAIM_AMT, 0) AS claimed_amount,
            COALESCE(cs1.CS_UTI_APP_AMT, 0) AS approved_amount
        FROM claim_submission cs1
        JOIN claim_intimation ci1 ON cs1.CS_INTIMATION_ID = ci1.CI_INTIMATION_ID
        JOIN claim_submission cs2 ON cs1.CS_BENF_ID = cs2.CS_BENF_ID 
            AND cs1.CS_NET_CLAIM_AMT = cs2.CS_NET_CLAIM_AMT
            AND cs1.CS_INTIMATION_ID < cs2.CS_INTIMATION_ID
        JOIN claim_intimation ci2 ON cs2.CS_INTIMATION_ID = ci2.CI_INTIMATION_ID
            AND ci1.CI_CR_OFFICE_ID = ci2.CI_CR_OFFICE_ID
        LEFT JOIN office_master om ON ci1.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE cs1.CS_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
          AND ABS(DATEDIFF(cs1.CS_ADMISSION_DATE, cs2.CS_ADMISSION_DATE)) <= 2
        ORDER BY cs1.CS_ADMISSION_DATE DESC;
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
    
    claims_files = glob.glob(os.path.join(BASE_DIR, 'new_data/new_05b_regional_all_claims_*.csv'))
    if not claims_files:
        print("❌ Error: Could not find new_05b_regional_all_claims_*.csv in new_data/")
        sys.exit(1)
        
    main_csv = claims_files[0]
    print(f"Using local claims file: {main_csv}")
    
    # --- SUB-PATTERN 4A: THRESHOLD AVOIDANCE ---
    print("\nProcessing Sub-Pattern 4A: Threshold Avoidance...")
    threshold_cases = []
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 28:
                continue
            claimed = float(row[25] or 0)
            if 99000 <= claimed <= 99999:
                approved = float(row[26] or 0)
                threshold_cases.append([
                    row[9], row[4], row[15], row[19][:10],
                    row[22], claimed, approved, row[23]
                ])
                
    # Sort by date descending
    threshold_cases.sort(key=lambda x: x[3], reverse=True)
    
    csv_4a = os.path.join(SUB_4A_DIR, 'pat4a_threshold_avoidance_details.csv')
    with open(csv_4a, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'claim_id', 'hospital_name', 'patient_name', 'admission_date',
            'ailment', 'claimed_amount', 'approved_amount', 'treating_doctor'
        ])
        writer.writerows(threshold_cases)
    print(f"✓ Saved {len(threshold_cases)} rows to {csv_4a}")
    
    # --- SUB-PATTERN 4B: DUPLICATE CLAIMS ---
    print("\nProcessing Sub-Pattern 4B: Duplicate Claims...")
    
    # Group by (card_number, hospital_id, claimed_amount) -> list of rows
    claims_groups = collections.defaultdict(list)
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 28:
                continue
            card = row[11].strip()
            hosp_id = row[3].strip()
            claimed = float(row[25] or 0)
            if card and hosp_id and claimed > 0:
                claims_groups[(card, hosp_id, claimed)].append(row)
                
    duplicate_cases = []
    for (card, hosp_id, claimed), rows in claims_groups.items():
        if len(rows) > 1:
            # Check date differences between all pairs
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    r1, r2 = rows[i], rows[j]
                    try:
                        date1 = datetime.strptime(r1[19][:10], '%Y-%m-%d')
                        date2 = datetime.strptime(r2[19][:10], '%Y-%m-%d')
                        days_diff = abs((date1 - date2).days)
                        if days_diff <= 2:
                            duplicate_cases.append([
                                r1[15], card, r1[4],
                                r1[9], r2[9],
                                r1[19][:10], r2[19][:10],
                                claimed, float(r1[26] or 0)
                            ])
                    except Exception:
                        continue
                        
    # Sort duplicates by date_1 descending
    duplicate_cases.sort(key=lambda x: x[5], reverse=True)
    
    csv_4b = os.path.join(SUB_4B_DIR, 'pat4b_duplicate_claims_details.csv')
    with open(csv_4b, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'patient_name', 'card_id', 'hospital_name',
            'claim_id_1', 'claim_id_2',
            'admission_date_1', 'admission_date_2',
            'claimed_amount', 'approved_amount'
        ])
        writer.writerows(duplicate_cases)
    print(f"✓ Saved {len(duplicate_cases)} rows to {csv_4b}")

def main():
    print("=" * 80)
    print("ECHS MODULE 20 - PATTERN 4 DATA EXTRACTION SYSTEM")
    print("=" * 80)
    
    try:
        # Try database connection first
        results = run_db_extraction()
        
        # Save database results to CSVs
        for name, data in results.items():
            lines = data.strip().splitlines()
            if name == "sub_pattern_4a_threshold_avoidance":
                path = os.path.join(SUB_4A_DIR, 'pat4a_threshold_avoidance_details.csv')
            else:
                path = os.path.join(SUB_4B_DIR, 'pat4b_duplicate_claims_details.csv')
                
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
    print("PATTERN 4 EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == '__main__':
    main()
