"""
Module 12 — Pattern 02: NABH Accreditation & Deduction Rate Divergence
========================================================================
Hospitals with NABH accreditation should have better quality control leading
to lower claim deduction rates. This pattern measures that gap and flags
hospitals exploiting NABH status while still showing high deductions.

Tables used:
  - office_master     : OM_NABH, OM_HOSP_TYPE, OM_NABL, OM_SUPER
  - claim_intimation  : CI_CR_OFFICE_ID, CI_CR_DATE
  - claim_submission  : CS_GR_CLAIM_AMT, CS_UTI_APP_AMT, CS_UTI_PAR_AMT
"""

import paramiko, csv, io, datetime, os

SSH_HOST = 'samar.iitk.ac.in'; SSH_PORT = 22
SSH_USER = 'echs_aman';        SSH_PASS = 'aman@2026'
DB_USER  = 'aman';             DB_PASS  = 'aman@2026'; DB_NAME = 'ECHS'

# ── Query 2A: NABH vs Non-NABH deduction summary by type ─────────────────────
QUERY_2A = """
SELECT
    om.OM_HOSP_TYPE                      AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'Unknown') AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    COUNT(DISTINCT om.OM_OFFICE_ID)      AS hospital_count,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7,2) AS claimed_cr,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e7,2)  AS approved_cr,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                    AS deduction_pct,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/NULLIF(COUNT(DISTINCT ci.CI_INTIMATION_ID),0),0) AS avg_claim_amt
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_HOSP_TYPE, om.OM_HOSP_TYPES, om.OM_NABH
HAVING total_claims >= 50
ORDER BY hosp_type, nabh_status;
"""

# ── Query 2B: NABH hospitals with anomalously HIGH deduction (cheating system) ─
QUERY_2B = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    om.OM_HOSP_TYPE                      AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')       AS hosp_type_desc,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e5,2) AS claimed_lakh,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e5,2)  AS approved_lakh,
    ROUND(
        (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100, 2
    )                                    AS deduction_pct,
    ROUND(AVG(cs.CS_GR_CLAIM_AMT),0)    AS avg_claim_amt
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND om.OM_NABH = 'Y'
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_OFFICE_CITY
HAVING total_claims >= 100 AND deduction_pct > 15
ORDER BY deduction_pct DESC
LIMIT 50;
"""

# ── Query 2C: Non-NABH hospitals with LOWEST deduction (unexpectedly clean) ──
QUERY_2C = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    om.OM_HOSP_TYPE                      AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')       AS hosp_type_desc,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e5,2) AS claimed_lakh,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e5,2)  AS approved_lakh,
    ROUND(
        (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100, 2
    )                                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND (om.OM_NABH IS NULL OR om.OM_NABH != 'Y')
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_OFFICE_CITY
HAVING total_claims >= 200 AND deduction_pct < 5
ORDER BY deduction_pct ASC
LIMIT 30;
"""

# ── Query 2D: Military hospitals (type M) detailed breakdown ──────────────────
QUERY_2D = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7,2) AS claimed_cr,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e7,2)  AS approved_cr,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                    AS deduction_pct,
    ROUND(AVG(cs.CS_GR_CLAIM_AMT),0)    AS avg_claim_amt
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE om.OM_HOSP_TYPE IN ('M','m')
  AND cs.CS_GR_CLAIM_AMT IS NOT NULL
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_NABH, om.OM_OFFICE_CITY
HAVING total_claims >= 10
ORDER BY deduction_pct DESC
LIMIT 50;
"""

QUERIES = {
    '02a_nabh_benchmark_by_type':        QUERY_2A,
    '02b_nabh_high_deduction_anomalies': QUERY_2B,
    '02c_non_nabh_low_deduction':        QUERY_2C,
    '02d_military_hospital_breakdown':   QUERY_2D,
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
    rows = [r for r in csv.reader(io.StringIO(out), delimiter='\t') if r]
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
                print(f"  ⚠ No data returned for {name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
