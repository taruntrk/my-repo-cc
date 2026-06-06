"""
Module 12 — Pattern 01: Specialty Category Billing Fraud
=========================================================
Detect hospitals billing for service types OUTSIDE their registered category.
Key signal: Type-3 facilities (dental clinics, diagnostic labs) billing IPD admissions.

Tables used:
  - office_master        : OM_HOSP_TYPE, OM_HOSP_TYPES, OM_NABH, OM_OFFICE_NAME
  - claim_intimation     : CI_CR_OFFICE_ID, CI_PATIENT_TYPE (1=OPD, 2=IPD)
  - claim_submission     : CS_GR_CLAIM_AMT, CS_NET_CLAIM_AMT, CS_UTI_APP_AMT
  - cghs_region_master   : city/state
"""

import paramiko, csv, io, datetime, os

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

# ── Query 1A: IPD claims by non-IPD hospital types ────────────────────────────
# CI_PATIENT_TYPE = 2 means IPD; OM_HOSP_TYPE 3 = Dental/Diagnostic
QUERY_1A = """
SELECT
    om.OM_OFFICE_ID          AS hospital_id,
    om.OM_OFFICE_NAME        AS hospital_name,
    om.OM_HOSP_TYPE          AS hosp_type,
    om.OM_HOSP_TYPES         AS hosp_type_desc,
    CASE om.OM_NABH
        WHEN 'Y' THEN 'NABH Accredited'
        WHEN 'N' THEN 'Non-NABH'
        ELSE 'Unknown'
    END                      AS nabh_status,
    om.OM_OFFICE_CITY        AS city,
    COALESCE(sm.SM_STATE_NAME,'—') AS state,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)               AS ipd_claims,
    COUNT(DISTINCT ci.CI_CARD_ID)                     AS unique_patients,
    COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0)               AS total_claimed,
    COALESCE(SUM(cs.CS_UTI_APP_AMT),0)                AS total_approved,
    COALESCE(SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT),0) AS total_deducted,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT) > 0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                        AS deduction_pct,
    MIN(ci.CI_ADMISSION_DATE) AS first_ipd_date,
    MAX(ci.CI_ADMISSION_DATE) AS last_ipd_date
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_PATIENT_TYPE = 'I'
  AND om.OM_HOSP_TYPE IN ('3','03')
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_NABH, om.OM_OFFICE_CITY, sm.SM_STATE_NAME
HAVING ipd_claims > 0
ORDER BY ipd_claims DESC;
"""

# ── Query 1B: Detail rows — top IPD claims at misuse facilities ───────────────
QUERY_1B = """
SELECT
    ci.CI_INTIMATION_ID     AS claim_id,
    ci.CI_BENEFICIARY_NAME  AS beneficiary_name,
    ci.CI_SERVICE_NO        AS service_number,
    ci.CI_PATIENT_TYPE      AS patient_type,
    ci.CI_ADMISSION_DATE    AS admission_date,
    cs.CS_DOD               AS discharge_date,
    om.OM_OFFICE_ID         AS hospital_id,
    om.OM_OFFICE_NAME       AS hospital_name,
    om.OM_HOSP_TYPE         AS hosp_type,
    om.OM_HOSP_TYPES        AS hosp_type_desc,
    COALESCE(cs.CS_GR_CLAIM_AMT,0)   AS gross_claimed,
    COALESCE(cs.CS_UTI_APP_AMT,0)    AS approved,
    COALESCE(cs.CS_GR_CLAIM_AMT,0)-COALESCE(cs.CS_UTI_APP_AMT,0) AS deducted
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_PATIENT_TYPE = 'I'
  AND om.OM_HOSP_TYPE IN ('3','03')
ORDER BY gross_claimed DESC
LIMIT 500;
"""

# ── Query 1C: Full NABH vs Non-NABH deduction rate by hospital type ───────────
QUERY_1C = """
SELECT
    om.OM_HOSP_TYPE                      AS hosp_type,
    om.OM_HOSP_TYPES                     AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    COUNT(DISTINCT om.OM_OFFICE_ID)      AS hospital_count,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0) AS total_claimed,
    COALESCE(SUM(cs.CS_UTI_APP_AMT),0)  AS total_approved,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT) > 0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY om.OM_HOSP_TYPE, om.OM_HOSP_TYPES, om.OM_NABH
ORDER BY om.OM_HOSP_TYPE, nabh_status;
"""

# ── Query 1D: Top hospitals by deduction rate (all types, min 100 claims) ─────
QUERY_1D = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    om.OM_HOSP_TYPE                      AS hosp_type,
    om.OM_HOSP_TYPES                     AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0) AS total_claimed,
    COALESCE(SUM(cs.CS_UTI_APP_AMT),0)  AS total_approved,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT) > 0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_NABH, om.OM_OFFICE_CITY
HAVING total_claims >= 100
ORDER BY deduction_pct DESC
LIMIT 100;
"""

QUERIES = {
    '01a_specialty_misuse_hospitals': QUERY_1A,
    '01b_specialty_misuse_claims':    QUERY_1B,
    '01c_nabh_deduction_benchmark':   QUERY_1C,
    '01d_top_deduction_hospitals':    QUERY_1D,
}

def run_query(client, sql):
    escaped = sql.replace("'", "'\\''")
    cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e '{escaped}'"
    _, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    err_lines = [l for l in err.split('\n') if l.strip() and 'Warning' not in l]
    if err_lines:
        print(f"  SQL error: {'; '.join(err_lines)}")
        return []
    reader = csv.reader(io.StringIO(out), delimiter='\t')
    rows = [r for r in reader if r]
    return rows

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        for name, sql in QUERIES.items():
            print(f"Running {name}...")
            t0 = datetime.datetime.now()
            rows = run_query(client, sql)
            elapsed = datetime.datetime.now() - t0
            if len(rows) > 1:
                fname = os.path.join(data_dir, f'{name}_{ts}.csv')
                with open(fname, 'w', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerows(rows)
                print(f"  ✅ {len(rows)-1} rows → {os.path.basename(fname)}  ({elapsed})")
            else:
                print(f"  ⚠ No data returned")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
