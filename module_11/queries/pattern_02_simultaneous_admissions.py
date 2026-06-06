import paramiko
import csv
import datetime
import os

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

query = """
    SELECT 
        a.CI_SERVICE_NO as service_number,
        a.CI_CARD_ID as card_number,
        a.CI_BENEFICIARY_NAME as beneficiary_name,
        a.CI_INTIMATION_ID as claim_id_1,
        a.CI_ADMISSION_DATE as admission_date_1,
        COALESCE(cs1.CS_DOD, 'Still Admitted') as discharge_date_1,
        a.CI_CR_OFFICE_ID as hospital_id_1,
        om1.OM_OFFICE_NAME as hospital_name_1,
        CONCAT(COALESCE(crm1.CRM_CITY_NAME,'?'), ', ', COALESCE(sm1.SM_STATE_NAME,'?')) as city_1,
        b.CI_INTIMATION_ID as claim_id_2,
        b.CI_ADMISSION_DATE as admission_date_2,
        COALESCE(cs2.CS_DOD, 'Still Admitted') as discharge_date_2,
        b.CI_CR_OFFICE_ID as hospital_id_2,
        om2.OM_OFFICE_NAME as hospital_name_2,
        CONCAT(COALESCE(crm2.CRM_CITY_NAME,'?'), ', ', COALESCE(sm2.SM_STATE_NAME,'?')) as city_2,
        DATEDIFF(
            GREATEST(a.CI_ADMISSION_DATE, b.CI_ADMISSION_DATE),
            LEAST(COALESCE(cs1.CS_DOD, DATE_ADD(a.CI_ADMISSION_DATE, INTERVAL 10 DAY)), COALESCE(cs2.CS_DOD, DATE_ADD(b.CI_ADMISSION_DATE, INTERVAL 10 DAY)))
        ) as gap_days,
        (COALESCE(cs1.CS_NET_CLAIM_AMT, 0) + COALESCE(cs2.CS_NET_CLAIM_AMT, 0)) as total_exposure
    FROM claim_intimation a
    JOIN claim_intimation b ON a.CI_SERVICE_NO = b.CI_SERVICE_NO
        AND a.CI_INTIMATION_ID < b.CI_INTIMATION_ID
        AND a.CI_CR_OFFICE_ID != b.CI_CR_OFFICE_ID
    LEFT JOIN claim_submission cs1 ON a.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
    LEFT JOIN claim_submission cs2 ON b.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
    LEFT JOIN office_master om1 ON a.CI_CR_OFFICE_ID = om1.OM_OFFICE_ID
    LEFT JOIN office_master om2 ON b.CI_CR_OFFICE_ID = om2.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm1 ON om1.OM_OFFICE_CGHS_CITY_ID = crm1.CRM_CITY_ID
    LEFT JOIN cghs_region_master crm2 ON om2.OM_OFFICE_CGHS_CITY_ID = crm2.CRM_CITY_ID
    LEFT JOIN state_master sm1 ON crm1.CRM_STATE_ID = sm1.SM_STATE_ID
    LEFT JOIN state_master sm2 ON crm2.CRM_STATE_ID = sm2.SM_STATE_ID
    WHERE a.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        AND b.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        AND DATEDIFF(
            GREATEST(a.CI_ADMISSION_DATE, b.CI_ADMISSION_DATE),
            LEAST(COALESCE(cs1.CS_DOD, DATE_ADD(a.CI_ADMISSION_DATE, INTERVAL 10 DAY)), COALESCE(cs2.CS_DOD, DATE_ADD(b.CI_ADMISSION_DATE, INTERVAL 10 DAY)))
        ) <= 7
    ORDER BY total_exposure DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\""
        
        print("Executing pattern 02 query...")
        start_time = datetime.datetime.now()
        stdin, stdout, stderr = client.exec_command(mysql_cmd)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error:
            # Filter out just the warning line
            error_lines = [line for line in error.split('\n') if line.strip() and "mysql: [Warning]" not in line]
            if error_lines:
                print(f"Error executing query: {chr(10).join(error_lines)}")
                return
            
        import io
        import csv
        reader = csv.reader(io.StringIO(output), delimiter='\t')
        rows = list(reader)
        
        if len(rows) > 1:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            filename = os.path.join(data_dir, f'02_Simultaneous_Admissions_{timestamp}.csv')
            
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
                    
            print(f"Saved {len(rows) - 1} records to {filename}")
        else:
            print("No data found for this query.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
