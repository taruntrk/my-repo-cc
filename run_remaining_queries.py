import paramiko
import csv
import datetime

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
    "08_High_Frequency_Claims": """
        SELECT 
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            sm_svc.sm_desc as service_type,
            rm.rm_rank_def as rank_col,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
            COUNT(DISTINCT ci.CI_HOSPITAL_ID) as unique_hospitals,
            COUNT(DISTINCT YEAR(ci.CI_ADMISSION_DATE)) as years_with_claims,
            COUNT(DISTINCT ci.CI_PATIENT_NAME) as unique_patients,
            MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
            MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
            DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            ROUND(AVG(cs.CS_NET_CLAIM_AMT), 2) as avg_claim_amount,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_HOSPITAL_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_HOSPITAL_ID SEPARATOR ' | ') as hospitals_used,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations_used,
            GROUP_CONCAT(DISTINCT ci.CI_PATIENT_NAME ORDER BY ci.CI_PATIENT_NAME SEPARATOR ' | ') as patients_treated,
            ci.CI_MOBILE as contact_mobile,
            ci.CI_ADDRESS1 as address
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_HOSPITAL_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN service_master sm_svc ON ci.CI_SERVICE_TYPE = sm_svc.sm_code
        LEFT JOIN rank_master rm ON ci.CI_SERVICE_RANK = rm.rm_rank_id AND ci.CI_SERVICE_TYPE = rm.rm_service_code
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME, sm_svc.sm_desc, rm.rm_rank_def, ci.CI_MOBILE, ci.CI_ADDRESS1
        HAVING COUNT(DISTINCT ci.CI_INTIMATION_ID) >= 10
        ORDER BY total_claims DESC, total_claimed_amount DESC
        LIMIT 500;
    """,
    
    "09_Impossible_Dependent_Claims": """
        SELECT 
            ci.CI_INTIMATION_ID as claim_id,
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            ci.CI_PATIENT_NAME as patient_name,
            ci.CI_SEX as patient_gender,
            ci.CI_RELATION_ID as relationship_code,
            rm.RM_RELATION_NAME as relationship,
            ci.CI_AGE as patient_age,
            ci.CI_ADMISSION_DATE as admission_date,
            cs.CS_DOD as discharge_date,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) as claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) as approved_amount,
            ci.CI_HOSPITAL_ID as hospital_id,
            om.OM_OFFICE_NAME as hospital_name,
            CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as hospital_location,
            ci.CI_ADM_AILMENT as ailment,
            cs.CS_TREAT_DOCT as treating_doctor,
            ci.CI_MOBILE as contact_mobile,
            ci.CI_INT_STAGE as claim_stage,
            ci.CI_INT_STATUS as claim_status,
            CASE 
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25 THEN 'Dependent over age limit (>25)'
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) < 0 THEN 'Invalid negative age'
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 50 THEN 'Age too high for dependent'
                WHEN ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) < 18 THEN 'Wife age too young'
                WHEN ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > 100 THEN 'Wife age too old'
                ELSE 'Age relationship inconsistency'
            END as issue_type
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_HOSPITAL_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_RELATION_ID IS NOT NULL
            AND ci.CI_RELATION_ID != 'SEL'
            AND ci.CI_AGE IS NOT NULL
            AND (
                (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25)
                OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) < 18)
                OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > 100)
            )
        ORDER BY claimed_amount DESC
        LIMIT 500;
    """,
    
    "10_Doctor_Teleportation": """
        SELECT 
            cs.CS_TREAT_DOCT as doctor_name,
            DATE(ci.CI_ADMISSION_DATE) as treatment_date,
            COUNT(DISTINCT ci.CI_HOSPITAL_ID) as number_of_hospitals,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as number_of_patients,
            COUNT(DISTINCT crm.CRM_CITY_ID) as number_of_cities,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_HOSPITAL_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown'), ' [', crm.CRM_CITY_NAME, ']') ORDER BY ci.CI_HOSPITAL_ID SEPARATOR ' | ') as hospitals_and_locations,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as cities_visited,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_INTIMATION_ID, ':', ci.CI_PATIENT_NAME) ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as patients_treated,
            GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as service_numbers,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            MIN(ci.CI_ADMISSION_DATE) as first_treatment_time,
            MAX(ci.CI_ADMISSION_DATE) as last_treatment_time
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_HOSPITAL_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_TREAT_DOCT IS NOT NULL
            AND cs.CS_TREAT_DOCT != ''
            AND cs.CS_TREAT_DOCT != 'NA'
        GROUP BY cs.CS_TREAT_DOCT, DATE(ci.CI_ADMISSION_DATE)
        HAVING COUNT(DISTINCT ci.CI_HOSPITAL_ID) >= 2
            AND COUNT(DISTINCT crm.CRM_CITY_ID) >= 2
        ORDER BY number_of_hospitals DESC, total_claimed_amount DESC
        LIMIT 500;
    """
}

def run_mysql_query(client, query):
    """Execute a MySQL query via SSH and return the result."""
    mysql_cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e "{query}"'
    stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=900)
    
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    
    err_lines = [l for l in err.splitlines() if 'Using a password' not in l and l.strip()]
    if err_lines:
        print(f"  [WARNING] {' '.join(err_lines)}")
    
    return out

print(f"Starting remaining queries at {datetime.datetime.now()}\n")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {SSH_HOST}...")
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    print("✓ Connected\n")
    
    for name, query in queries.items():
        print(f"Executing: {name}")
        print(f"Time: {datetime.datetime.now()}")
        print("-" * 80)
        
        try:
            start_time = datetime.datetime.now()
            result = run_mysql_query(client, query.replace('"', '\\"').replace('\n', ' '))
            end_time = datetime.datetime.now()
            
            if result and result.strip():
                filename = f"{name}.csv"
                lines = result.splitlines()
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for line in lines:
                        writer.writerow(line.split('\t'))
                
                print(f"✓ Query completed in {end_time - start_time}")
                print(f"✓ Records found: {len(lines) - 1}")
                print(f"✓ Saved to: {filename}\n")
            else:
                print(f"⚠ No data returned\n")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}\n")
    
    print(f"Completed at {datetime.datetime.now()}")
    
except Exception as e:
    print(f"✗ Fatal Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
    print("Connection closed")
