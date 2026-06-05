import paramiko
import csv
import datetime
import os

# Database credentials
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_aman'
SSH_PASS = 'aman@2026'

DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

query = """
    SELECT 
        ci.CI_CARD_ID as card_number,
        COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
        COUNT(DISTINCT ci.CI_BENEFICIARY_NAME) as unique_names,
        COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
        COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
        COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
        COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
        GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as service_numbers,
        GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME ORDER BY ci.CI_BENEFICIARY_NAME SEPARATOR ' | ') as beneficiary_names,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
        GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?')) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
        GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as all_claim_ids,
        MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
        MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
        DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        AND ci.CI_CARD_ID IS NOT NULL
        AND ci.CI_CARD_ID != ''
    GROUP BY ci.CI_CARD_ID
    HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) >= 3
    ORDER BY total_claimed_amount DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        # Prepare MySQL command
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\" | tr '\t' ','"
        
        print("Executing pattern 01 query...")
        start_time = datetime.datetime.now()
        stdin, stdout, stderr = client.exec_command(mysql_cmd)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "mysql: [Warning]" not in error:
            print(f"Error executing query: {error}")
            return
            
        lines = [line for line in output.split('\n') if line.strip()]
        
        if len(lines) > 1:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            filename = os.path.join(data_dir, f'01_Duplicate_Card_IDs_{timestamp}.csv')
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
                    
            print(f"Saved {len(lines) - 1} records to {filename}")
        else:
            print("No data found for this query.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
