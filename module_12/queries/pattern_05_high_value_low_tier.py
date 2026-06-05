"""
Module 12 — Pattern 05: High-Value Claims at Low-Tier Facilities
=================================================================
Small/specialist-only hospitals (type 3, dental, diagnostic) billing
extremely high claim amounts per admission that exceed their clinical
capacity. A dental clinic billing ₹5L+ per IPD admission is impossible
without fabrication. Also flags claims where approved amount is
disproportionately low vs claimed (>80% deduction on high-value claim).

Tables: claim_intimation, claim_submission, office_master
"""
import paramiko, csv, io, datetime, os

SSH_HOST = 'samar.iitk.ac.in'; SSH_PORT = 22
SSH_USER = 'echs_aman'; SSH_PASS = 'aman@2026'
DB_USER = 'aman'; DB_PASS = 'aman@2026'; DB_NAME = 'ECHS'

QUERY_5A = """
SELECT
    ci.CI_INTIMATION_ID     AS claim_id,
    ci.CI_BENEFICIARY_NAME  AS beneficiary_name,
    ci.CI_SERVICE_NO        AS service_number,
    ci.CI_ADMISSION_DATE    AS admission_date,
    cs.CS_DOD               AS discharge_date,
    om.OM_OFFICE_ID         AS hospital_id,
    om.OM_OFFICE_NAME       AS hospital_name,
    om.OM_HOSP_TYPE         AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—') AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    om.OM_OFFICE_CITY       AS city,
    COALESCE(cs.CS_GR_CLAIM_AMT,0)  AS gross_claimed,
    COALESCE(cs.CS_UTI_APP_AMT,0)   AS approved,
    COALESCE(cs.CS_GR_CLAIM_AMT,0)-COALESCE(cs.CS_UTI_APP_AMT,0) AS deducted,
    ROUND(CASE WHEN cs.CS_GR_CLAIM_AMT>0
          THEN (cs.CS_GR_CLAIM_AMT-COALESCE(cs.CS_UTI_APP_AMT,0))/cs.CS_GR_CLAIM_AMT*100
          ELSE 0 END, 2) AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID=om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID=cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND om.OM_HOSP_TYPE IN ('3','03')
  AND cs.CS_GR_CLAIM_AMT >= 100000
ORDER BY gross_claimed DESC
LIMIT 200;
"""

QUERY_5B = """
SELECT
    om.OM_OFFICE_ID                         AS hospital_id,
    om.OM_OFFICE_NAME                       AS hospital_name,
    om.OM_HOSP_TYPE                         AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')          AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    om.OM_OFFICE_CITY                       AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)     AS high_val_claims,
    ROUND(MAX(cs.CS_GR_CLAIM_AMT)/1e5,2)   AS max_single_claim_lakh,
    ROUND(AVG(cs.CS_GR_CLAIM_AMT)/1e5,2)   AS avg_claim_lakh,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e5,2)   AS total_claimed_lakh,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e5,2)    AS total_approved_lakh,
    ROUND(CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
          THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
          ELSE 0 END, 2)                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID=om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID=cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND om.OM_HOSP_TYPE IN ('3','03')
  AND cs.CS_GR_CLAIM_AMT >= 50000
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_NABH, om.OM_OFFICE_CITY
HAVING high_val_claims >= 3
ORDER BY total_claimed_lakh DESC
LIMIT 50;
"""

QUERY_5C = """
SELECT
    om.OM_OFFICE_ID                         AS hospital_id,
    om.OM_OFFICE_NAME                       AS hospital_name,
    om.OM_HOSP_TYPE                         AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')          AS hosp_type_desc,
    om.OM_OFFICE_CITY                       AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)     AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7,2)   AS claimed_cr,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e7,2)    AS approved_cr,
    ROUND(CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
          THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
          ELSE 0 END, 2)                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID=om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID=cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_OFFICE_CITY
HAVING total_claims >= 100 AND deduction_pct >= 80
ORDER BY claimed_cr DESC
LIMIT 50;
"""

QUERIES = {
    '05a_high_value_low_tier_claims':    QUERY_5A,
    '05b_low_tier_hospitals_high_value': QUERY_5B,
    '05c_extreme_deduction_hospitals':   QUERY_5C,
}

def run_query(client, sql):
    escaped = sql.replace("'", "'\\''")
    _, stdout, stderr = client.exec_command(f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e '{escaped}'")
    out = stdout.read().decode('utf-8')
    err_lines = [l for l in stderr.read().decode().split('\n') if l.strip() and 'Warning' not in l]
    if err_lines: print(f"  SQL error: {'; '.join(err_lines)}"); return []
    return [r for r in csv.reader(io.StringIO(out), delimiter='\t') if r]

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {SSH_HOST}..."); client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        for name, sql in QUERIES.items():
            print(f"Running {name}..."); t0 = datetime.datetime.now()
            rows = run_query(client, sql); elapsed = datetime.datetime.now() - t0
            if len(rows) > 1:
                fname = os.path.join(data_dir, f'{name}_{ts}.csv')
                with open(fname, 'w', newline='', encoding='utf-8') as f: csv.writer(f).writerows(rows)
                print(f"  ✅ {len(rows)-1} rows → {os.path.basename(fname)}  ({elapsed})")
            else: print(f"  ⚠ No data for {name}")
    except Exception as e: print(f"Error: {e}")
    finally: client.close()

if __name__ == '__main__':
    main()
