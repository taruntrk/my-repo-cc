"""
Module 20 — Pattern 04: Hospital-wise Leakage Detail
04a: All hospitals ranked by total deduction (settlement_stat summary)
04b: ALL individual claims from top 50 highest-deduction hospitals (2021-2026)
"""
import paramiko, csv, io, datetime, os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

QUERY_A = """
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

TOP50_QUERY = """
    SELECT SS_OFFICE_ID FROM settlement_stat
    WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
    GROUP BY SS_OFFICE_ID
    ORDER BY SUM(SS_DED_AMT) DESC
    LIMIT 50;
"""

QUERY_B_TEMPLATE = """
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
    JOIN  claim_submission cs   ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om       ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    LEFT JOIN relation_master rm     ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
    LEFT JOIN rank_master rm2        ON ci.CI_SERVICE_RANK = rm2.rm_rank_id
    WHERE YEAR(ci.CI_ADMISSION_DATE) BETWEEN 2021 AND 2026
        AND ci.CI_CR_OFFICE_ID IN ({ids})
        AND COALESCE(cs.CS_NET_CLAIM_AMT, 0) > 0
        AND (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) > 0
    ORDER BY hospital_name, deducted_amount DESC
    LIMIT 5000;
"""

def run_query(sql, label):
    print(f"Executing {label}...")
    start = datetime.datetime.now()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
    try:
        escaped = sql.replace('"', '\\"').replace('`', '\\`')
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{escaped}\""
        _, stdout, stderr = client.exec_command(mysql_cmd, timeout=3600)
        output = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        err_lines = [l for l in err.split('\n') if l.strip() and 'Warning' not in l]
        if err_lines:
            print(f"  DB Error: {err_lines[0]}")
            return []
    finally:
        client.close()
    elapsed = datetime.datetime.now() - start
    output_lines = [line.replace('\r', '') for line in output.split('\n')]
    rows = [r for r in csv.reader(output_lines, delimiter='\t') if r]
    print(f"  {len(rows)-1} rows  ({elapsed})")
    return rows

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        # 04a
        rows_a = run_query(QUERY_A, '04a_hospital_leakage_summary')
        if len(rows_a) > 1:
            fname = os.path.join(data_dir, f'04a_hospital_leakage_summary_{ts}.csv')
            with open(fname, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerows(rows_a)
            print(f"  ✅ Saved → {os.path.basename(fname)}")

        # top 50 IDs
        top_rows = run_query(TOP50_QUERY, 'top50_lookup')
        ids = [r[0] for r in top_rows[1:] if r]
        if not ids:
            print("  ⚠ No hospital IDs"); return
        ids_str = ', '.join(str(h) for h in ids)
        print(f"  Top 50: {ids[:3]}... ({len(ids)} total)")

        # 04b
        rows_b = run_query(QUERY_B_TEMPLATE.format(ids=ids_str), '04b_hospital_all_claims')
        if len(rows_b) > 1:
            fname = os.path.join(data_dir, f'04b_hospital_all_claims_{ts}.csv')
            with open(fname, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerows(rows_b)
            print(f"  ✅ Saved → {os.path.basename(fname)}")
        else:
            print("  ⚠ No data for 04b")

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()

if __name__ == '__main__':
    main()
