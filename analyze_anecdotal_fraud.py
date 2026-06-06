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
    "Anecdotal_1_Lazarus_Post_Death_Billing": """
        -- Finding claims admitted AFTER the patient was recorded as 'Dead' (Discharge Type 'D') in a previous claim.
        WITH DeathRecords AS (
            SELECT CI.CI_BENF_ID, MIN(CS.CS_DOD) as date_of_death, CI.CI_HOSPITAL_ID as hospital_declaring_death
            FROM claim_submission CS
            JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
            WHERE CS.CS_DISCHARGE_TYPE = 'D'
            GROUP BY CI.CI_BENF_ID, CI.CI_HOSPITAL_ID
        )
        SELECT D.CI_BENF_ID as deceased_patient_id, 
               D.date_of_death, 
               CS.CS_ADMISSION_DATE as zombie_admission_date, 
               CI.CI_HOSPITAL_ID as billing_hospital,
               CS.CS_GR_CLAIM_AMT as amount_claimed
        FROM claim_submission CS
        JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
        JOIN DeathRecords D ON CI.CI_BENF_ID = D.CI_BENF_ID
        WHERE CS.CS_ADMISSION_DATE > D.date_of_death
        ORDER BY CS.CS_ADMISSION_DATE DESC
        LIMIT 100;
    """,
    
    "Anecdotal_2_Family_Cloning_Impossible_Dependents": """
        -- Finding a single veteran Service No that has an impossible number of dependents (e.g., > 15 distinct people)
        -- Indicates the primary card is being used as a free-for-all pass for an extended network.
        SELECT PTR_SERVICE_NO as primary_veteran_id, 
               COUNT(DISTINCT PTR_BEN_ID) as number_of_dependents,
               GROUP_CONCAT(DISTINCT PTR_PATIENT_NAME SEPARATOR ' | ') as names_claimed
        FROM patient_register
        WHERE PTR_SERVICE_NO IS NOT NULL AND PTR_SERVICE_NO != ''
          AND PTR_SERVICE_NO NOT IN ('0', 'NA', 'UNKNOWN')
        GROUP BY PTR_SERVICE_NO
        HAVING number_of_dependents > 15
        ORDER BY number_of_dependents DESC
        LIMIT 100;
    """,
    
    "Anecdotal_3_The_Forever_Patient_Chronic_Stay": """
        -- Finding patients who practically live at the hospital (Cumulative LOS > 300 days)
        -- Indicates the hospital is using a captive patient to perpetually bill daily bed/ICU charges.
        SELECT CI.CI_BENF_ID as patient_id, 
               COUNT(CS.CS_INTIMATION_ID) as total_admissions,
               SUM(DATEDIFF(CS.CS_DOD, CS.CS_ADMISSION_DATE)) as total_days_in_hospital,
               MAX(CI.CI_HOSPITAL_ID) as primary_hospital_exploiting_card
        FROM claim_submission CS
        JOIN claim_intimation CI ON CS.CS_INTIMATION_ID = CI.CI_INTIMATION_ID
        WHERE CS.CS_ADMISSION_DATE IS NOT NULL AND CS.CS_DOD IS NOT NULL
        GROUP BY CI.CI_BENF_ID
        HAVING total_days_in_hospital > 300
        ORDER BY total_days_in_hospital DESC
        LIMIT 100;
    """
}

def run_analysis():
    print(f"[{datetime.datetime.now()}] Extracting Anecdotal Fraud Patterns via SSH...")
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
