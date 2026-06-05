"""
Module 12 — Pattern 03: Services Outside Empaneled Scope
=========================================================
Hospitals bill for services they are NOT registered to provide in the
empanel_hospital_service registry. A hospital empanelled only for OPD
billing inpatient (IPD) is scope creep fraud.

Tables:
  - empanel_hospital_service: EHS_OFFICE_ID, EHS_ID, EHS_FACILITY_ID
  - empanel_facility        : EF_FACILITY_ID, EF_FACILITY
  - empanel_header          : EH_ID, EH_NAME
  - claim_intimation        : CI_CR_OFFICE_ID, CI_PATIENT_TYPE
  - claim_submission        : CS_GR_CLAIM_AMT, CS_UTI_APP_AMT
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

# ── Query 3A: What service categories are empaneled per hospital ──────────────
QUERY_3A = """
SELECT
    ehs.EHS_OFFICE_ID                     AS hospital_id,
    om.OM_OFFICE_NAME                     AS hospital_name,
    om.OM_HOSP_TYPE                       AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')        AS hosp_type_desc,
    CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
    GROUP_CONCAT(DISTINCT ef.EF_FACILITY ORDER BY ef.EF_FACILITY SEPARATOR ' | ') AS empaneled_services,
    COUNT(DISTINCT ehs.EHS_FACILITY_ID)   AS service_count
FROM empanel_hospital_service ehs
JOIN office_master om ON ehs.EHS_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN empanel_facility ef ON ehs.EHS_FACILITY_ID = ef.EF_FACILITY_ID
WHERE ehs.EHS_TO_DATE IS NULL OR ehs.EHS_TO_DATE >= CURDATE()
GROUP BY ehs.EHS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_NABH
ORDER BY service_count DESC
LIMIT 200;
"""

# ── Query 3B: Hospitals with IPD claims but NOT empaneled for IPD ─────────────
QUERY_3B = """
SELECT
    curr.hospital_id,
    curr.hospital_name,
    curr.hosp_type,
    curr.hosp_type_desc,
    curr.nabh_status,
    curr.city,
    curr.ipd_claims_filed,
    curr.total_claimed,
    curr.total_approved,
    curr.deduction_pct,
    emp.actual_empaneled_services
FROM (
    SELECT
        om.OM_OFFICE_ID                      AS hospital_id,
        om.OM_OFFICE_NAME                    AS hospital_name,
        om.OM_HOSP_TYPE                      AS hosp_type,
        COALESCE(om.OM_HOSP_TYPES,'—')       AS hosp_type_desc,
        CASE om.OM_NABH WHEN 'Y' THEN 'NABH' ELSE 'Non-NABH' END AS nabh_status,
        om.OM_OFFICE_CITY                    AS city,
        COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS ipd_claims_filed,
        COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0)  AS total_claimed,
        COALESCE(SUM(cs.CS_UTI_APP_AMT),0)   AS total_approved,
        ROUND(CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0 THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100 ELSE 0 END, 2) AS deduction_pct
    FROM claim_intimation ci
    JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    WHERE ci.CI_PATIENT_TYPE = 'I'
      AND ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_HOSP_TYPES, om.OM_NABH, om.OM_OFFICE_CITY
    HAVING ipd_claims_filed > 0
) curr
LEFT JOIN (
    SELECT
        ehs.EHS_OFFICE_ID AS hospital_id,
        GROUP_CONCAT(DISTINCT ef.EF_FACILITY ORDER BY ef.EF_FACILITY SEPARATOR ' | ') AS actual_empaneled_services
    FROM empanel_hospital_service ehs
    JOIN empanel_facility ef ON ehs.EHS_FACILITY_ID = ef.EF_FACILITY_ID
    WHERE (ehs.EHS_TO_DATE IS NULL OR ehs.EHS_TO_DATE >= CURDATE())
    GROUP BY ehs.EHS_OFFICE_ID
) emp ON curr.hospital_id = emp.hospital_id
WHERE (emp.actual_empaneled_services IS NULL
        OR (emp.actual_empaneled_services NOT LIKE '%IPD%'
        AND emp.actual_empaneled_services NOT LIKE '%Indoor%'
        AND emp.actual_empaneled_services NOT LIKE '%Inpatient%'))
ORDER BY curr.total_claimed DESC
LIMIT 100;
"""

# ── Query 3C: Hospitals billing specialties not in empaneled list ─────────────
QUERY_3C = """
SELECT
    om.OM_OFFICE_ID                      AS hospital_id,
    om.OM_OFFICE_NAME                    AS hospital_name,
    om.OM_HOSP_TYPE                      AS hosp_type,
    COALESCE(om.OM_HOSP_TYPES,'—')       AS hosp_type_desc,
    om.OM_OFFICE_CITY                    AS city,
    COUNT(DISTINCT ci.CI_INTIMATION_ID)  AS total_claims,
    COALESCE(SUM(cs.CS_GR_CLAIM_AMT),0)  AS total_claimed,
    COALESCE(SUM(cs.CS_UTI_APP_AMT),0)   AS total_approved,
    ROUND(
        CASE WHEN SUM(cs.CS_GR_CLAIM_AMT)>0
             THEN (SUM(cs.CS_GR_CLAIM_AMT)-SUM(cs.CS_UTI_APP_AMT))/SUM(cs.CS_GR_CLAIM_AMT)*100
             ELSE 0 END, 2
    )                                    AS deduction_pct
FROM claim_intimation ci
JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  AND NOT EXISTS (
      SELECT 1 FROM empanel_hospital_service ehs
      WHERE ehs.EHS_OFFICE_ID = om.OM_OFFICE_ID
        AND (ehs.EHS_TO_DATE IS NULL OR ehs.EHS_TO_DATE >= CURDATE())
  )
GROUP BY om.OM_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE,
         om.OM_HOSP_TYPES, om.OM_OFFICE_CITY
HAVING total_claims >= 10
ORDER BY total_claimed DESC
LIMIT 100;
"""

QUERIES = {
    '03a_empaneled_services_registry':    QUERY_3A,
    '03b_ipd_without_ipd_empanelment':    QUERY_3B,
    '03c_billing_without_any_empanelment':QUERY_3C,
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
    return [r for r in csv.reader(io.StringIO(out), delimiter='\t') if r]

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
                print(f"  ⚠ No data for {name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
