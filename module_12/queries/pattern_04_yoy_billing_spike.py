"""
Module 12 — Pattern 04: Year-over-Year Billing Spike by Hospital Type
======================================================================
Tables: claim_intimation, claim_submission, office_master
"""
import paramiko, csv, io, datetime, os

SSH_HOST = 'samar.iitk.ac.in'; SSH_PORT = 22
SSH_USER = 'echs_aman'; SSH_PASS = 'aman@2026'
DB_USER = 'aman'; DB_PASS = 'aman@2026'; DB_NAME = 'ECHS'

QUERY_4A = """
SELECT
    curr.hospital_id, curr.hospital_name, curr.hosp_type, curr.hosp_type_desc,
    curr.nabh_status, curr.city,
    prev.yr AS prev_year, curr.yr AS curr_year,
    prev.total_claims AS prev_claims, curr.total_claims AS curr_claims,
    ROUND(prev.total_claimed/1e5,2) AS prev_claimed_lakh,
    ROUND(curr.total_claimed/1e5,2) AS curr_claimed_lakh,
    ROUND((curr.total_claimed-prev.total_claimed)/NULLIF(prev.total_claimed,0)*100,1) AS yoy_amount_growth_pct,
    ROUND((curr.total_claims-prev.total_claims)/NULLIF(prev.total_claims,0)*100,1)  AS yoy_claim_growth_pct,
    ROUND(curr.deduction_pct,2) AS curr_deduction_pct
FROM (
    SELECT om.OM_OFFICE_ID AS hospital_id, om.OM_OFFICE_NAME AS hospital_name,
           om.OM_HOSP_TYPE AS hosp_type, COALESCE(om.OM_HOSP_TYPES,'—') AS hosp_type_desc,
           CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
           om.OM_OFFICE_CITY AS city, YEAR(ci.CI_CR_DATE) AS yr,
           COUNT(DISTINCT ci.CI_INTIMATION_ID) AS total_claims,
           COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0) AS total_claimed,
           ROUND(CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
                 THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
                 ELSE 0 END, 2) AS deduction_pct
    FROM claim_intimation ci
    JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    GROUP BY om.OM_OFFICE_ID,om.OM_OFFICE_NAME,om.OM_HOSP_TYPE,om.OM_HOSP_TYPES,
             om.OM_NABH,om.OM_OFFICE_CITY,YEAR(ci.CI_CR_DATE)
) curr
JOIN (
    SELECT om.OM_OFFICE_ID AS hospital_id, YEAR(ci.CI_CR_DATE) AS yr,
           COUNT(DISTINCT ci.CI_INTIMATION_ID) AS total_claims,
           COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0) AS total_claimed
    FROM claim_intimation ci
    JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 6 YEAR)
    GROUP BY om.OM_OFFICE_ID,YEAR(ci.CI_CR_DATE)
) prev ON curr.hospital_id=prev.hospital_id AND curr.yr=prev.yr+1
WHERE prev.total_claims >= 50
  AND (curr.total_claimed-prev.total_claimed)/NULLIF(prev.total_claimed,0) >= 1.0
ORDER BY yoy_amount_growth_pct DESC LIMIT 100;
"""

QUERY_4B = """
SELECT
    YEAR(ci.CI_CR_DATE) AS yr,
    om.OM_HOSP_TYPE AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'Unknown') AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    COUNT(DISTINCT om.OM_OFFICE_ID) AS active_hospitals,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) AS total_claims,
    ROUND(SUM(cs.CS_GR_CLAIM_AMT)/1e7,2) AS claimed_cr,
    ROUND(SUM(cs.CS_UTI_APP_AMT)/1e7,2) AS approved_cr,
    ROUND(CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
          THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
          ELSE 0 END, 2) AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID=om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID=cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY YEAR(ci.CI_CR_DATE),om.OM_HOSP_TYPE,om.OM_HOSP_TYPES,om.OM_NABH
ORDER BY yr, hosp_type, nabh_status;
"""

QUERIES = {'04a_hospital_yoy_billing_spike': QUERY_4A, '04b_type_level_yoy_trend': QUERY_4B}

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
