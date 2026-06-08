"""
Module 20 — Pattern 08: Gender & Relationship Leakage Breakdown
08a: Deduction totals grouped by gender and relationship
08b: ALL individual claims with deduction (2021-2026) — shows who (self/spouse/son/daughter) drives leakage
"""
import paramiko, csv, io, datetime, os
csv.field_size_limit(10000000)
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
        ss.SS_GENDER                                                               AS gender,
        COALESCE(rm.RM_RELATION_NAME, ss.SS_RELATION_ID)                          AS relationship,
        SUM(ss.SS_CLAIM_CNT)                                                       AS total_claims,
        ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                               AS total_claimed_cr,
        ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                               AS total_approved_cr,
        ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                               AS total_deducted_cr,
        ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)              AS deduction_pct,
        COUNT(DISTINCT ss.SS_OFFICE_ID)                                            AS hospitals_involved
    FROM settlement_stat ss
    LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
    WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
    GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_NAME
    ORDER BY total_deducted_cr DESC;
"""

QUERY_B = """
    SELECT
        ci.CI_SEX                                                                   AS gender,
        COALESCE(rm.RM_RELATION_NAME, ci.CI_RELATION_ID)                           AS relationship,
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
    JOIN  claim_submission cs   ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om       ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    LEFT JOIN relation_master rm     ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
    LEFT JOIN rank_master rm2        ON ci.CI_SERVICE_RANK = rm2.rm_rank_id
    WHERE YEAR(ci.CI_ADMISSION_DATE) BETWEEN 2021 AND 2026
        AND COALESCE(cs.CS_NET_CLAIM_AMT, 0) > 0
        AND (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) > 0
    ORDER BY gender, relationship, deducted_amount DESC
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

        for label, query, fname in [
            ('08a_gender_relation_summary', QUERY_A, f'08a_gender_relation_summary_{ts}.csv'),
            ('08b_gender_relation_claims',  QUERY_B, f'08b_gender_relation_claims_{ts}.csv'),
        ]:
            rows = run_query(query, label)
            if len(rows) > 1:
                path = os.path.join(data_dir, fname)
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerows(rows)
                print(f"  ✅ Saved → {fname}")
            else:
                print(f"  ⚠ No data for {label}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback; traceback.print_exc()

if __name__ == '__main__':
    main()
