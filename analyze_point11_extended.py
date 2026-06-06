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
    # BROAD CATEGORY 1: REPEATED CLAIMS
    "Repeated_Exact_Duplicates": """
        SELECT CI.CI_BENF_ID AS patient_id, CI.CI_HOSPITAL_ID AS hospital_id, CS.CS_ADMISSION_DATE, 
               CS.CS_GR_CLAIM_AMT, COUNT(CS.CS_INTIMATION_ID) AS duplicate_count
        FROM claim_submission CS
        JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
        WHERE CS.CS_GR_CLAIM_AMT > 0
        GROUP BY CI.CI_BENF_ID, CI.CI_HOSPITAL_ID, CS.CS_ADMISSION_DATE, CS.CS_GR_CLAIM_AMT
        HAVING duplicate_count > 1
        ORDER BY duplicate_count DESC LIMIT 100;
    """,
    "Repeated_Claim_Splitting_Unbundling": """
        -- New Pattern: Hospital files multiple different claims (different amounts) for the same patient on the exact same day to bypass package limits.
        SELECT CI.CI_BENF_ID, CI.CI_HOSPITAL_ID, CS.CS_ADMISSION_DATE, 
               COUNT(DISTINCT CS.CS_INTIMATION_ID) AS claims_filed_same_day,
               SUM(CS.CS_GR_CLAIM_AMT) AS total_daily_billed
        FROM claim_submission CS
        JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
        GROUP BY CI.CI_BENF_ID, CI.CI_HOSPITAL_ID, CS.CS_ADMISSION_DATE
        HAVING claims_filed_same_day > 2
        ORDER BY claims_filed_same_day DESC LIMIT 100;
    """,

    # BROAD CATEGORY 2: ID DUPLICATION
    "ID_Duplication_Shared_UID": """
        SELECT PTR_UID_NUMBER AS duplicate_uid, COUNT(DISTINCT PTR_BEN_ID) AS profiles
        FROM patient_register
        WHERE LENGTH(PTR_UID_NUMBER) >= 10 AND PTR_UID_NUMBER NOT IN ('000000000000', '999999999999')
        GROUP BY PTR_UID_NUMBER HAVING profiles > 1 ORDER BY profiles DESC LIMIT 100;
    """,
    "ID_Duplication_Agent_Mobile_Rings": """
        -- New Pattern: A single mobile number registered to dozens of different patients. Indicates an agent/broker controls the identities.
        SELECT PTR_MOBILE AS agent_mobile_number, COUNT(DISTINCT PTR_BEN_ID) AS controlled_profiles,
               GROUP_CONCAT(DISTINCT PTR_PATIENT_NAME SEPARATOR ' | ') AS patient_names
        FROM patient_register
        WHERE PTR_MOBILE IS NOT NULL AND LENGTH(PTR_MOBILE) >= 10 
          AND PTR_MOBILE NOT IN ('0000000000', '9999999999', '1234567890')
        GROUP BY PTR_MOBILE
        HAVING controlled_profiles > 10
        ORDER BY controlled_profiles DESC LIMIT 100;
    """,

    # BROAD CATEGORY 3: PREDICTIVE IDENTITY MISUSE
    "Predictive_Simultaneous_Admissions": """
        SELECT A.CI_BENF_ID, A.CI_HOSPITAL_ID AS hosp_A, B.CI_HOSPITAL_ID AS hosp_B, A.CI_ADMISSION_DATE
        FROM claim_intimation A JOIN claim_intimation B ON A.CI_BENF_ID = B.CI_BENF_ID 
        JOIN claim_submission CSA ON A.CI_INTIMATION_ID = CSA.CS_INTIMATION_ID
        JOIN claim_submission CSB ON B.CI_INTIMATION_ID = CSB.CS_INTIMATION_ID
        WHERE A.CI_INTIMATION_ID < B.CI_INTIMATION_ID AND A.CI_HOSPITAL_ID != B.CI_HOSPITAL_ID
          AND A.CI_ADMISSION_DATE <= CSB.CS_DOD AND CSA.CS_DOD >= B.CI_ADMISSION_DATE LIMIT 100;
    """,
    "Predictive_Doctor_Teleportation": """
        -- New Pattern: The same doctor ID/Name admitting patients in 3+ completely different hospitals on the exact same day.
        SELECT CS_TREAT_DOCT AS doctor_name, DATE(CS_ADMISSION_DATE) as admission_day,
               COUNT(DISTINCT CS_SUB_OFFICE_ID) AS distinct_hospitals_same_day,
               COUNT(CS_INTIMATION_ID) AS total_patients_admitted
        FROM claim_submission
        WHERE CS_TREAT_DOCT IS NOT NULL AND LENGTH(CS_TREAT_DOCT) > 3
          AND CS_TREAT_DOCT NOT IN ('NA', 'DOCTOR', 'DUTY DOCTOR', 'CMO', 'RMO')
        GROUP BY CS_TREAT_DOCT, DATE(CS_ADMISSION_DATE)
        HAVING distinct_hospitals_same_day >= 3
        ORDER BY distinct_hospitals_same_day DESC LIMIT 100;
    """
}

def run_analysis():
    print(f"[{datetime.datetime.now()}] Extracting Extended Point 11 Data via SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        for name, query in queries.items():
            print(f"--- Running {name} ---")
            mysql_cmd = f"mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e \"{query.replace('\"', '\\\"')}\""
            stdin, stdout, stderr = client.exec_command(mysql_cmd)
            out = stdout.read().decode('utf-8')
            if out:
                filename = f"{name}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for line in out.splitlines():
                        writer.writerow(line.split('\t'))
                print(f"  -> Saved to {filename}")
            else:
                print("  -> No data found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_analysis()
