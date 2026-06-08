import os
import csv
import datetime
import paramiko
import traceback
from dotenv import load_dotenv

# Setup Paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(os.path.dirname(base_dir), '.env')
data_dir = os.path.join(base_dir, 'new_data')

load_dotenv(env_path)

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

def execute_pattern_04():
    print("="*60)
    print("STARTING DEEP HOSPITAL LEAKAGE EXTRACTION (PATTERN 04)")
    print("Targeted: Top 50 Highest Deduction Hospitals (No Row Limits)")
    print("="*60)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filepath = os.path.join(data_dir, f"new_04a_hospital_leakage_summary_{timestamp}.csv")
    claims_filepath = os.path.join(data_dir, f"new_04b_hospital_all_claims_{timestamp}.csv")
    
    try:
        print(f"[{datetime.datetime.now()}] Connecting to SSH ({SSH_HOST})...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        # ----------------- PART A: SUMMARY OF ALL HOSPITALS -----------------
        print(f"[{datetime.datetime.now()}] Running 04a: Extracting overall hospital ranking...")
        query_a = """
            SELECT
                ss.SS_OFFICE_ID                                                    AS hospital_id,
                COALESCE(om.OM_OFFICE_NAME, 'Unknown')                            AS hospital_name,
                COALESCE(crm.CRM_CITY_NAME, '')                                   AS city,
                COALESCE(sm.SM_STATE_NAME, '')                                    AS state,
                COALESCE(om.OM_HOSP_TYPE,  '')                                    AS hosp_type_code,
                COALESCE(om.OM_HOSP_TYPES, '')                                    AS hosp_type_desc,
                COALESCE(om.OM_NABH, 'N')                                         AS nabh_status,
                COALESCE(om.OM_NABL, 'N')                                         AS nabl_status,
                COALESCE(om.OM_OFFICE_PIN, '')                                    AS pincode,
                SUM(ss.SS_CLAIM_CNT)                                              AS total_claims,
                ROUND(SUM(ss.SS_CLAIM_AMT) / 100000.0, 2)                        AS total_claimed_lakh,
                ROUND(SUM(ss.SS_APPR_AMT)  / 100000.0, 2)                        AS total_approved_lakh,
                ROUND(SUM(ss.SS_DED_AMT)   / 100000.0, 2)                        AS total_deducted_lakh,
                ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)     AS deduction_pct
            FROM settlement_stat ss
            LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
            LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
            LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
            WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
            GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, crm.CRM_CITY_NAME,
                     sm.SM_STATE_NAME, om.OM_HOSP_TYPE, om.OM_HOSP_TYPES,
                     om.OM_NABH, om.OM_NABL, om.OM_OFFICE_PIN
            ORDER BY total_deducted_lakh DESC;
        """
        
        query_a_escaped = query_a.replace('`', '\\`').replace('"', '\\"')
        mysql_cmd_a = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_a_escaped}\" -s -N"
        _, stdout_a, _ = client.exec_command(mysql_cmd_a, timeout=600)
        
        with open(summary_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'hospital_id', 'hospital_name', 'city', 'state', 'hosp_type_code', 'hosp_type_desc',
                'nabh_status', 'nabl_status', 'pincode', 'total_claims', 'total_claimed_lakh',
                'total_approved_lakh', 'total_deducted_lakh', 'deduction_pct'
            ])
            for line in stdout_a:
                line = line.strip('\n')
                if line:
                    writer.writerow(line.split('\t'))
        print(f"[{datetime.datetime.now()}] Saved Summary to {summary_filepath}")
        
        # ----------------- PART B: TARGETED DEEP CLAIMS -----------------
        print(f"[{datetime.datetime.now()}] Running 04b: Identifying Top 50 highest-deduction hospitals...")
        query_top50 = """
            SELECT SS_OFFICE_ID FROM settlement_stat
            WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
            GROUP BY SS_OFFICE_ID
            ORDER BY SUM(SS_DED_AMT) DESC
            LIMIT 50;
        """
        
        mysql_cmd_top50 = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_top50}\" -s -N"
        _, stdout_top50, _ = client.exec_command(mysql_cmd_top50, timeout=300)
        
        hospital_ids = [line.strip() for line in stdout_top50 if line.strip()]
        
        if not hospital_ids:
            print("No top hospitals found. Exiting Part B.")
            return
            
        formatted_hosp_ids = ", ".join([f"'{hid}'" for hid in hospital_ids])
        print(f"[{datetime.datetime.now()}] Fetching claims for Top {len(hospital_ids)} hospitals...")
        
        # Single query stream because claim_intimation and claim_submission joins on 50 hospitals is fast
        query_b = f"""
            SELECT
                ci.CI_CR_OFFICE_ID                                                 AS hospital_id,
                COALESCE(om.OM_OFFICE_NAME, 'Unknown')                            AS hospital_name,
                COALESCE(crm.CRM_CITY_NAME, '')                                   AS city,
                COALESCE(sm.SM_STATE_NAME, '')                                    AS state,
                COALESCE(om.OM_HOSP_TYPE, '')                                     AS hosp_type,
                COALESCE(om.OM_NABH, 'N')                                         AS nabh_status,
                ci.CI_INTIMATION_ID                                                AS claim_id,
                ci.CI_SERVICE_NO                                                   AS service_number,
                ci.CI_CARD_ID                                                      AS card_number,
                ci.CI_BENEFICIARY_NAME                                             AS beneficiary_name,
                COALESCE(rm2.rm_rank_def, '')                                      AS rank_name,
                ci.CI_SERVICE_TYPE                                                 AS service_type,
                ci.CI_PATIENT_NAME                                                 AS patient_name,
                ci.CI_AGE                                                          AS age,
                ci.CI_SEX                                                          AS gender,
                COALESCE(rm.RM_RELATION_NAME, ci.CI_RELATION_ID)                  AS relationship,
                ci.CI_ADMISSION_DATE                                               AS admission_date,
                COALESCE(cs.CS_DOD, 'Still Admitted')                             AS discharge_date,
                DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE)   AS stay_days,
                ci.CI_ADM_AILMENT                                                  AS ailment,
                cs.CS_TREAT_DOCT                                                   AS treating_doctor,
                cs.CS_BILL_NO                                                      AS bill_number,
                COALESCE(cs.CS_NET_CLAIM_AMT, 0)                                  AS claimed_amount,
                COALESCE(cs.CS_UTI_APP_AMT, 0)                                    AS approved_amount,
                COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0) AS deducted_amount,
                ROUND((COALESCE(cs.CS_NET_CLAIM_AMT,0)-COALESCE(cs.CS_UTI_APP_AMT,0))*100.0/NULLIF(cs.CS_NET_CLAIM_AMT,0),2) AS deduction_pct,
                ci.CI_INT_STAGE                                                    AS claim_stage,
                ci.CI_INT_STATUS                                                   AS claim_status
            FROM claim_intimation ci
            JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
            LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
            LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
            LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
            LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
            LEFT JOIN rank_master rm2 ON ci.CI_SERVICE_RANK = rm2.rm_rank_id
            WHERE ci.CI_ADMISSION_DATE >= '2021-04-01'
                AND ci.CI_CR_OFFICE_ID IN ({formatted_hosp_ids})
                AND COALESCE(cs.CS_NET_CLAIM_AMT, 0) > 0
                AND (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) > 0
            ORDER BY hospital_name, deducted_amount DESC;
        """
        
        escaped_query_b = query_b.replace('"', '\\"').replace('`', '\\`')
        mysql_cmd_b = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{escaped_query_b}\" -s -N"
        
        _, stdout_b, stderr_b = client.exec_command(mysql_cmd_b, timeout=3600)
        
        total_claims_saved = 0
        with open(claims_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'hospital_id', 'hospital_name', 'city', 'state', 'hosp_type', 'nabh_status',
                'claim_id', 'service_number', 'card_number', 'beneficiary_name', 'rank_name',
                'service_type', 'patient_name', 'age', 'gender', 'relationship', 'admission_date',
                'discharge_date', 'stay_days', 'ailment', 'treating_doctor', 'bill_number',
                'claimed_amount', 'approved_amount', 'deducted_amount', 'deduction_pct',
                'claim_stage', 'claim_status'
            ])
            
            for line in stdout_b:
                line = line.strip('\n')
                if line:
                    writer.writerow(line.split('\t'))
                    total_claims_saved += 1
                    if total_claims_saved % 20000 == 0:
                        print(f"[{datetime.datetime.now()}] Progress: Extracted {total_claims_saved:,} claims...")
                        
        err = stderr_b.read().decode('utf-8')
        if err and 'Warning' not in err:
            print(f"DB Error in claims: {err}")
            
        mb_size = os.path.getsize(claims_filepath) / (1024 * 1024)
        print(f"[{datetime.datetime.now()}] COMPLETED! Saved {total_claims_saved:,} claims to {claims_filepath} ({mb_size:.2f} MB)")
        
    except Exception as e:
        print(f"CRITICAL ERROR in Pattern 04: {e}")
        traceback.print_exc()
    finally:
        client.close()

if __name__ == '__main__':
    execute_pattern_04()
