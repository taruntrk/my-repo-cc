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
PATTERN_DIR = os.path.join(DATA2_DIR, 'pattern_3_doctor_anomaly')

# Sub-pattern folders
SUB_3A_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_3a_superman_surgeon')

# Ensure directories exist
os.makedirs(SUB_3A_DIR, exist_ok=True)

# Queries for Pattern 3
queries = {
    "sub_pattern_3a_superman_surgeon": """
        SELECT
            cs.CS_TREAT_DOCT AS doctor_name,
            DATE(cs.CS_ADMISSION_DATE) AS admission_date,
            om.OM_OFFICE_NAME AS hospital_name,
            COUNT(cs.CS_INTIMATION_ID) AS surgeries_performed,
            ROUND(SUM(COALESCE(cs.CS_NET_CLAIM_AMT, 0)) / 100000, 2) AS total_claimed_lakh,
            ROUND(SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 100000, 2) AS total_approved_lakh
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE cs.CS_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
          AND cs.CS_TREAT_DOCT IS NOT NULL AND cs.CS_TREAT_DOCT NOT IN ('0', 'NA', 'UNKNOWN', '')
        GROUP BY cs.CS_TREAT_DOCT, DATE(cs.CS_ADMISSION_DATE), om.OM_OFFICE_NAME
        HAVING surgeries_performed >= 15
        ORDER BY surgeries_performed DESC;
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
    
    # --- SUB-PATTERN 3A: SUPERMAN SURGEON ---
    print("\nProcessing Sub-Pattern 3A: Superman Surgeon...")
    claims_files = glob.glob(os.path.join(BASE_DIR, 'new_data/new_05b_regional_all_claims_*.csv'))
    if not claims_files:
        print("❌ Error: Could not find new_05b_regional_all_claims_*.csv in new_data/")
        sys.exit(1)
        
    main_csv = claims_files[0]
    print(f"Using local claims file: {main_csv}")
    
    # Group by (treating_doctor, admission_date, hospital_name) -> list of [claimed, approved]
    surgeon_days = collections.defaultdict(list)
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 28:
                continue
            doc = row[23].strip()
            adm_date = row[19][:10]  # YYYY-MM-DD
            hosp_name = row[4].strip()
            claimed = float(row[25] or 0)
            approved = float(row[26] or 0)
            
            # Filter invalid names
            if doc and doc not in ['0', 'NA', 'UNKNOWN', ''] and len(doc) > 3:
                surgeon_days[(doc, adm_date, hosp_name)].append((claimed, approved))
                
    superman_cases = []
    for (doc, adm_date, hosp_name), claims in surgeon_days.items():
        surgeries_performed = len(claims)
        if surgeries_performed >= 15:
            total_claimed_l = round(sum(c[0] for c in claims) / 100000.0, 2)
            total_approved_l = round(sum(c[1] for c in claims) / 100000.0, 2)
            
            superman_cases.append([
                doc, adm_date, hosp_name, surgeries_performed,
                total_claimed_l, total_approved_l
            ])
            
    # Sort by surgeries_performed descending
    superman_cases.sort(key=lambda x: x[3], reverse=True)
    
    csv_3a = os.path.join(SUB_3A_DIR, 'pat3a_superman_surgeon_details.csv')
    with open(csv_3a, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'doctor_name', 'admission_date', 'hospital_name', 'surgeries_performed',
            'total_claimed_lakh', 'total_approved_lakh'
        ])
        writer.writerows(superman_cases)
    print(f"✓ Saved {len(superman_cases)} rows to {csv_3a}")

def main():
    print("=" * 80)
    print("ECHS MODULE 20 - PATTERN 3 DATA EXTRACTION SYSTEM")
    print("=" * 80)
    
    try:
        # Try database connection first
        results = run_db_extraction()
        
        # Save database results to CSVs
        for name, data in results.items():
            lines = data.strip().splitlines()
            path = os.path.join(SUB_3A_DIR, 'pat3a_superman_surgeon_details.csv')
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
    print("PATTERN 3 EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == '__main__':
    main()
