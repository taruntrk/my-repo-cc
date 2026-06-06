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
        cs.CS_BILL_NO as bill_number,
        cs.CS_BILL_DATE as bill_date,
        COUNT(*) as duplicate_count,
        SUM(cs.CS_NET_CLAIM_AMT) as total_exposure,
        GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_INTIMATION_ID SEPARATOR ' | ') as claim_ids,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
        GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_numbers,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals,
        GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?')) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
        GROUP_CONCAT(DISTINCT ci.CI_ADMISSION_DATE ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as admission_dates
    FROM claim_submission cs
    JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE cs.CS_SUB_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        AND cs.CS_BILL_NO IS NOT NULL
        AND cs.CS_BILL_NO != ''
        AND cs.CS_BILL_NO != 'NA'
        AND cs.CS_BILL_NO != 'N/A'
        AND cs.CS_BILL_NO != 'na'
        AND cs.CS_BILL_NO != 'None'
        AND cs.CS_BILL_NO NOT REGEXP '^[[:space:]]*$'
    GROUP BY cs.CS_BILL_NO, cs.CS_BILL_DATE
    HAVING COUNT(*) > 1
    ORDER BY total_exposure DESC;
"""

def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\" | tr '\t' ','"
        
        print("Executing pattern 03 query (Duplicate Bill Numbers)...")
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
            
            filename = os.path.join(data_dir, f'03_Duplicate_Bill_Numbers_{timestamp}.csv')
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
                    
            end_time = datetime.datetime.now()
            print(f"Query completed in {end_time - start_time}")
            print(f"Saved {len(lines) - 1} records to {filename}")
        else:
            print("No data found for this query.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
