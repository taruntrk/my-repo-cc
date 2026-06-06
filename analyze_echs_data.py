import paramiko
import csv
import io
import datetime

# Database credentials
import os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

queries = {
    "FA_02_Simultaneous_Admissions": """
        SELECT 
            A.CI_BENF_ID AS patient_id, A.CI_HOSPITAL_ID AS hosp_A, B.CI_HOSPITAL_ID AS hosp_B, 
            A.CI_ADMISSION_DATE AS admission_A, B.CI_ADMISSION_DATE AS admission_B
        FROM claim_intimation A
        JOIN claim_intimation B 
            ON A.CI_BENF_ID = B.CI_BENF_ID 
            AND A.CI_INTIMATION_ID != B.CI_INTIMATION_ID
            AND A.CI_HOSPITAL_ID != B.CI_HOSPITAL_ID
        JOIN claim_submission CSA ON A.CI_INTIMATION_ID = CSA.CS_INTIMATION_ID
        JOIN claim_submission CSB ON B.CI_INTIMATION_ID = CSB.CS_INTIMATION_ID
        WHERE 
            A.CI_ADMISSION_DATE <= CSB.CS_DOD 
            AND CSA.CS_DOD >= B.CI_ADMISSION_DATE
        LIMIT 100;
    """,
    "FA_03_Synthetic_Identities": """
        SELECT 
            PTR_UID_NUMBER AS uid_number, 
            COUNT(DISTINCT PTR_BEN_ID) AS profile_count,
            GROUP_CONCAT(DISTINCT PTR_PATIENT_NAME SEPARATOR ' | ') AS sample_names
        FROM patient_register
        WHERE PTR_UID_NUMBER IS NOT NULL 
          AND PTR_UID_NUMBER NOT IN ('', 'NA', '-1', '0', '999999999999')
        GROUP BY PTR_UID_NUMBER
        HAVING COUNT(DISTINCT PTR_BEN_ID) > 5
        ORDER BY profile_count DESC
        LIMIT 100;
    """,
    "FA_04_Revolving_Door": """
        SELECT 
            CI.CI_BENF_ID AS patient_id, CI.CI_HOSPITAL_ID AS hospital_id, COUNT(*) as readmission_count
        FROM claim_intimation CI
        JOIN claim_submission CS ON CI.CI_INTIMATION_ID = CS.CS_INTIMATION_ID
        WHERE CS.CS_DOD IS NOT NULL
        GROUP BY CI.CI_BENF_ID, CI.CI_HOSPITAL_ID
        HAVING readmission_count > 10
        ORDER BY readmission_count DESC
        LIMIT 100;
    """,
    "Phantom_Procedures_Module2": """
        SELECT 
            HED_CAT_ID, 
            COUNT(*) as claims_count,
            SUM(HED_CLAIM_AMOUNT) as total_claimed,
            SUM(HED_APP_AMOUNT) as total_approved,
            SUM(HED_CLAIM_AMOUNT - HED_APP_AMOUNT) as total_deducted
        FROM his_hosp_exp_det
        WHERE HED_CLAIM_AMOUNT > 0 
          AND HED_APP_AMOUNT = 0 
        GROUP BY HED_CAT_ID
        ORDER BY total_deducted DESC
        LIMIT 50;
    """
}

def run_analysis():
    print(f"[{datetime.datetime.now()}] Connecting to SSH at {SSH_HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        print("Connected successfully. Executing DB queries...\n")
        
        for name, query in queries.items():
            print(f"--- Running {name} ---")
            
            # Using mysql command line client in batch mode via SSH
            # We output as CSV by replacing tabs with commas, but to be safer we can just let mysql format it as tab-separated
            # and parse it properly.
            mysql_cmd = f"mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e \"{query.replace('\"', '\\\"')}\""
            
            stdin, stdout, stderr = client.exec_command(mysql_cmd)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            
            if err and "Using a password" not in err:
                print(f"Error executing {name}: {err}")
            
            if out:
                # Save to a CSV file locally
                filename = f"{name}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for line in out.splitlines():
                        writer.writerow(line.split('\t'))
                print(f"Results saved to {filename}")
                
                # Print a small preview
                lines = out.splitlines()
                for line in lines[:5]:
                    print(line.replace('\t', ' | '))
                if len(lines) > 5:
                    print("... (more results saved to file)\n")
            else:
                print("No results or query error.\n")
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_analysis()
