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

def execute_pattern_05():
    print("="*60)
    print("STARTING REGIONAL LEAKAGE BREAKDOWN EXTRACTION (PATTERN 05)")
    print("Targeted: Top 10 Highest Deduction Regions (No Row Limits)")
    print("="*60)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filepath = os.path.join(data_dir, f"new_05a_regional_deduction_breakdown_{timestamp}.csv")
    claims_filepath = os.path.join(data_dir, f"new_05b_regional_all_claims_{timestamp}.csv")
    
    try:
        print(f"[{datetime.datetime.now()}] Connecting to SSH ({SSH_HOST})...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        # ----------------- PART A: SUMMARY OF ALL REGIONS -----------------
        print(f"[{datetime.datetime.now()}] Running 05a: Extracting overall regional breakdown...")
        query_a = """
            SELECT
                ss.SS_REGION_ID                                                            AS region_id,
                COALESCE(crm.CRM_CITY_NAME, CONCAT('Region ', ss.SS_REGION_ID))           AS region_name,
                COALESCE(sm.SM_STATE_NAME, '')                                             AS state_name,
                COUNT(DISTINCT ss.SS_OFFICE_ID)                                            AS num_hospitals,
                SUM(ss.SS_CLAIM_CNT)                                                       AS total_claims,
                ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                               AS total_claimed_cr,
                ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                               AS total_approved_cr,
                ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                               AS total_deducted_cr,
                ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)              AS deduction_pct
            FROM settlement_stat ss
            LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
            LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
            LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
            WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
            GROUP BY ss.SS_REGION_ID, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
            ORDER BY total_deducted_cr DESC;
        """
        
        query_a_escaped = query_a.replace('`', '\\`').replace('"', '\\"')
        mysql_cmd_a = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_a_escaped}\" -s -N"
        _, stdout_a, _ = client.exec_command(mysql_cmd_a, timeout=600)
        
        with open(summary_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'region_id', 'region_name', 'state_name', 'num_hospitals', 'total_claims',
                'total_claimed_cr', 'total_approved_cr', 'total_deducted_cr', 'deduction_pct'
            ])
            for line in stdout_a:
                line = line.strip('\n')
                if line:
                    writer.writerow(line.split('\t'))
        print(f"[{datetime.datetime.now()}] Saved Summary to {summary_filepath}")
        
        # ----------------- PART B: TARGETED DEEP REGIONAL CLAIMS -----------------
        print(f"[{datetime.datetime.now()}] Running 05b: Identifying Top 10 highest-deduction regions...")
        query_top10 = """
            SELECT SS_REGION_ID FROM settlement_stat
            WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
            GROUP BY SS_REGION_ID
            ORDER BY SUM(SS_DED_AMT) DESC
            LIMIT 10;
        """
        
        mysql_cmd_top10 = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_top10}\" -s -N"
        _, stdout_top10, _ = client.exec_command(mysql_cmd_top10, timeout=300)
        
        region_ids = [line.strip() for line in stdout_top10 if line.strip()]
        
        if not region_ids:
            print("No top regions found. Exiting Part B.")
            return
            
        formatted_region_ids = ", ".join([f"'{rid}'" for rid in region_ids])
        
        # Fetch the office mappings for these regions to prevent Cartesian product duplication in JOIN
        print(f"[{datetime.datetime.now()}] Fetching office mapping for Top {len(region_ids)} regions...")
        query_offices = f"""
            SELECT DISTINCT SS_OFFICE_ID, SS_REGION_ID FROM settlement_stat
            WHERE SS_REGION_ID IN ({formatted_region_ids});
        """
        mysql_cmd_offices = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_offices}\" -s -N"
        _, stdout_offices, _ = client.exec_command(mysql_cmd_offices, timeout=300)
        
        office_to_region = {}
        for line in stdout_offices:
            line = line.strip()
            if line:
                parts = line.split('\t')
                if len(parts) == 2:
                    office_to_region[parts[0]] = parts[1]
                    
        if not office_to_region:
            print("No offices found for these regions. Exiting Part B.")
            return
            
        formatted_office_ids = ", ".join([f"'{oid}'" for oid in office_to_region.keys()])
        print(f"[{datetime.datetime.now()}] Fetching claims for {len(office_to_region)} hospitals in the Top {len(region_ids)} regions...")
        
        query_b = f"""
            SELECT
                ci.CI_CR_OFFICE_ID                                                          AS hospital_id,
                COALESCE(om.OM_OFFICE_NAME, 'Unknown')                                     AS hospital_name,
                COALESCE(crm.CRM_CITY_NAME, '')                                            AS city,
                COALESCE(sm.SM_STATE_NAME, '')                                             AS state,
                COALESCE(om.OM_HOSP_TYPE, '')                                              AS hosp_type,
                COALESCE(om.OM_NABH, 'N')                                                  AS nabh_status,
                ci.CI_INTIMATION_ID                                                         AS claim_id,
                ci.CI_SERVICE_NO                                                            AS service_number,
                ci.CI_CARD_ID                                                               AS card_number,
                ci.CI_BENEFICIARY_NAME                                                      AS beneficiary_name,
                COALESCE(rm2.rm_rank_def, ci.CI_SERVICE_RANK)                              AS `rank`,
                ci.CI_SERVICE_TYPE                                                          AS service_type,
                ci.CI_PATIENT_NAME                                                          AS patient_name,
                ci.CI_AGE                                                                   AS age,
                ci.CI_SEX                                                                   AS gender,
                COALESCE(rm.RM_RELATION_NAME, ci.CI_RELATION_ID)                           AS relationship,
                ci.CI_ADMISSION_DATE                                                        AS admission_date,
                COALESCE(cs.CS_DOD, 'Still Admitted')                                      AS discharge_date,
                DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE)            AS stay_days,
                ci.CI_ADM_AILMENT                                                           AS ailment,
                cs.CS_TREAT_DOCT                                                            AS treating_doctor,
                cs.CS_BILL_NO                                                               AS bill_number,
                COALESCE(cs.CS_NET_CLAIM_AMT, 0)                                           AS claimed_amount,
                COALESCE(cs.CS_UTI_APP_AMT, 0)                                             AS approved_amount,
                COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)        AS deducted_amount,
                ROUND(
                    (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0))
                    * 100.0 / NULLIF(cs.CS_NET_CLAIM_AMT, 0), 2
                )                                                                           AS deduction_pct,
                ci.CI_INT_STAGE                                                             AS claim_stage,
                ci.CI_INT_STATUS                                                            AS claim_status
            FROM claim_intimation ci
            JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
            LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
            LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
            LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
            LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
            LEFT JOIN rank_master rm2 ON ci.CI_SERVICE_RANK = rm2.rm_rank_id
            WHERE ci.CI_CR_OFFICE_ID IN ({formatted_office_ids})
                AND ci.CI_ADMISSION_DATE >= '2021-04-01'
                AND COALESCE(cs.CS_NET_CLAIM_AMT, 0) > 0
                AND (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) > 0
            ORDER BY city, deducted_amount DESC;
        """
        
        escaped_query_b = query_b.replace('"', '\\"').replace('`', '\\`')
        mysql_cmd_b = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{escaped_query_b}\" -s -N"
        
        _, stdout_b, stderr_b = client.exec_command(mysql_cmd_b, timeout=3600)
        
        total_claims_saved = 0
        with open(claims_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'region_id', 'region_name', 'state_name', 'hospital_id', 'hospital_name', 'hosp_type',
                'nabh_status', 'claim_id', 'service_number', 'card_number', 'beneficiary_name', 'rank',
                'service_type', 'patient_name', 'age', 'gender', 'relationship', 'admission_date',
                'discharge_date', 'stay_days', 'ailment', 'treating_doctor', 'bill_number',
                'claimed_amount', 'approved_amount', 'deducted_amount', 'deduction_pct',
                'claim_stage', 'claim_status'
            ])
            
            for line in stdout_b:
                line = line.strip('\n')
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 28:
                        hosp_id = parts[0]
                        city_name = parts[2]
                        state_name = parts[3]
                        
                        reg_id = office_to_region.get(hosp_id, '')
                        reg_name = city_name if city_name else f"Region {reg_id}"
                        
                        row = [reg_id, reg_name, state_name] + parts
                        writer.writerow(row)
                        
                        total_claims_saved += 1
                        if total_claims_saved % 20000 == 0:
                            print(f"[{datetime.datetime.now()}] Progress: Extracted {total_claims_saved:,} claims...")
                        
        err = stderr_b.read().decode('utf-8')
        if err and 'Warning' not in err:
            print(f"DB Error in claims: {err}")
            
        mb_size = os.path.getsize(claims_filepath) / (1024 * 1024)
        print(f"[{datetime.datetime.now()}] COMPLETED! Saved {total_claims_saved:,} claims to {claims_filepath} ({mb_size:.2f} MB)")
        
    except Exception as e:
        print(f"CRITICAL ERROR in Pattern 05: {e}")
        traceback.print_exc()
    finally:
        client.close()

if __name__ == '__main__':
    execute_pattern_05()
