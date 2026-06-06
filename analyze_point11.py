import paramiko
import csv
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
    "Point11_Repeated_Claims": """
        SELECT 
            CI.CI_BENF_ID AS patient_id, 
            CI.CI_HOSPITAL_ID AS hospital_id, 
            CS.CS_ADMISSION_DATE AS admission_date, 
            CS.CS_DOD AS discharge_date, 
            CS.CS_GR_CLAIM_AMT AS claim_amount,
            COUNT(CS.CS_INTIMATION_ID) AS duplicate_count,
            GROUP_CONCAT(CS.CS_INTIMATION_ID) AS claim_ids
        FROM claim_submission CS
        JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
        WHERE CS.CS_ADMISSION_DATE IS NOT NULL 
          AND CS.CS_DOD IS NOT NULL 
          AND CS.CS_GR_CLAIM_AMT > 0
        GROUP BY CI.CI_BENF_ID, CI.CI_HOSPITAL_ID, CS.CS_ADMISSION_DATE, CS.CS_DOD, CS.CS_GR_CLAIM_AMT
        HAVING duplicate_count > 1
        ORDER BY duplicate_count DESC
        LIMIT 100;
    """,
    
    "Point11_ID_Duplication": """
        SELECT 
            PTR_UID_NUMBER AS duplicate_uid, 
            COUNT(DISTINCT PTR_BEN_ID) AS distinct_profiles,
            GROUP_CONCAT(DISTINCT PTR_PATIENT_NAME SEPARATOR ' | ') AS patient_names,
            GROUP_CONCAT(DISTINCT PTR_BEN_ID SEPARATOR ' | ') AS patient_ids
        FROM patient_register
        WHERE PTR_UID_NUMBER IS NOT NULL 
          AND LENGTH(PTR_UID_NUMBER) >= 10
          AND PTR_UID_NUMBER NOT IN ('000000000000', '999999999999', '123456789012', '111111111111')
        GROUP BY PTR_UID_NUMBER
        HAVING distinct_profiles > 1
        ORDER BY distinct_profiles DESC
        LIMIT 100;
    """,
    
    "Point11_Predictive_Identity_Misuse": """
        SELECT 
            A.CI_BENF_ID AS patient_id, 
            A.CI_HOSPITAL_ID AS hosp_A, 
            B.CI_HOSPITAL_ID AS hosp_B, 
            A.CI_ADMISSION_DATE AS admission_A, 
            B.CI_ADMISSION_DATE AS admission_B,
            A.CI_INTIMATION_ID as claim_A,
            B.CI_INTIMATION_ID as claim_B
        FROM claim_intimation A
        JOIN claim_intimation B 
            ON A.CI_BENF_ID = B.CI_BENF_ID 
            AND A.CI_INTIMATION_ID < B.CI_INTIMATION_ID
            AND A.CI_HOSPITAL_ID != B.CI_HOSPITAL_ID
        JOIN claim_submission CSA ON A.CI_INTIMATION_ID = CSA.CS_INTIMATION_ID
        JOIN claim_submission CSB ON B.CI_INTIMATION_ID = CSB.CS_INTIMATION_ID
        WHERE 
            A.CI_ADMISSION_DATE <= CSB.CS_DOD 
            AND CSA.CS_DOD >= B.CI_ADMISSION_DATE
        LIMIT 100;
    """
}

def run_analysis():
    print(f"[{datetime.datetime.now()}] Extracting Point 11 Data via SSH ({SSH_HOST})...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        print("Connected successfully. Fetching requested data...\n")
        
        for name, query in queries.items():
            print(f"--- Running {name} ---")
            mysql_cmd = f"mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e \"{query.replace('\"', '\\\"')}\""
            
            stdin, stdout, stderr = client.exec_command(mysql_cmd)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            
            if out:
                filename = f"{name}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for line in out.splitlines():
                        writer.writerow(line.split('\t'))
                print(f"Data successfully saved to {filename}")
                
                # Print a small preview
                lines = out.splitlines()
                for line in lines[:5]:
                    print(line.replace('\t', ' | '))
                if len(lines) > 5:
                    print("... (more results saved to file)\n")
            else:
                print("No data found or query is still running.\n")
                if err and "Using a password" not in err:
                    print(f"Error: {err}")
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_analysis()
