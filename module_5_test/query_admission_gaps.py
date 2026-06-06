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

QUERY = """
WITH ci_filtered AS (
    SELECT
        ci.CI_INTIMATION_ID,
        ci.CI_BENF_ID,
        ci.CI_DEP_ID,
        ci.CI_ADMISSION_DATE,
        ci.CI_CARD_ID,
        ci.CI_HOSPITAL_ID,
        ci.CI_NONEMPANELLED_HOSPITAL
    FROM claim_intimation ci
    WHERE ci.CI_ADMISSION_DATE >= '2021-01-01'
      AND ci.CI_ADMISSION_DATE <  '2026-04-01'
      AND ci.CI_ADMISSION_DATE IS NOT NULL
      AND ci.CI_BENF_ID IS NOT NULL
      AND ci.CI_BENF_ID <> 0
),

diag_one AS (
    SELECT
        dd.DD_INTIMATION_ID,
        LEFT(
            COALESCE(
                NULLIF(TRIM(dd.DD_DIAG_APP_ICD_CODE), ''),
                NULLIF(TRIM(dd.DD_DIAG_SUP_ICD_CODE), ''),
                NULLIF(TRIM(dd.DD_DIAG_PAR_ICD_CODE), ''),
                NULLIF(TRIM(dd.DD_DIAG_ICD_CODE), ''),
                'UNKNOWN_ICD'
            ),
            250
        ) AS icd_code
    FROM diag_details dd
    INNER JOIN ci_filtered ci ON ci.CI_INTIMATION_ID = dd.DD_INTIMATION_ID
    WHERE dd.DD_DIAG_SEQ_NO = 1
),

sd_amount AS (
    SELECT
        sd.SD_INTIMATION_ID AS intimation_id,
        SUM(COALESCE(sd.SD_UTI_APP_AMT, 0)) AS sd_approved_amount
    FROM settlement_details sd
    INNER JOIN ci_filtered ci
        ON ci.CI_INTIMATION_ID = sd.SD_INTIMATION_ID
    GROUP BY sd.SD_INTIMATION_ID
),

cs_amount AS (
    SELECT
        cs.CS_INTIMATION_ID AS intimation_id,
        SUM(COALESCE(cs.CS_UTI_APP_AMT, 0)) AS cs_approved_amount
    FROM claim_submission cs
    INNER JOIN ci_filtered ci
        ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    GROUP BY cs.CS_INTIMATION_ID
),

ms_amount AS (
    SELECT
        ms.MS_CLAIM_ID AS intimation_id,
        SUM(COALESCE(ms.MS_APPROVED_AMT, 0)) AS ms_approved_amount
    FROM manual_settlement ms
    INNER JOIN ci_filtered ci
        ON ci.CI_INTIMATION_ID = ms.MS_CLAIM_ID
    GROUP BY ms.MS_CLAIM_ID
),

claim_base AS (
    SELECT
        ci.CI_INTIMATION_ID AS intimation_id,

        CONCAT(
            CAST(ci.CI_BENF_ID AS UNSIGNED),
            '-',
            CAST(COALESCE(ci.CI_DEP_ID, 0) AS UNSIGNED)
        ) AS patient_id,

        DATE(ci.CI_ADMISSION_DATE) AS admission_date,

        COALESCE(
            NULLIF(TRIM(ci.CI_HOSPITAL_ID), ''),
            CONCAT('NONEMP-', NULLIF(TRIM(ci.CI_NONEMPANELLED_HOSPITAL), '')),
            'UNKNOWN_HOSPITAL'
        ) AS hospital_key,

        COALESCE(d.icd_code, 'UNKNOWN_ICD') AS icd_code,

        COALESCE(
            sd.sd_approved_amount,
            cs.cs_approved_amount,
            ms.ms_approved_amount,
            0
        ) AS approved_amount

    FROM ci_filtered ci

    LEFT JOIN diag_one d
        ON d.DD_INTIMATION_ID = ci.CI_INTIMATION_ID

    LEFT JOIN sd_amount sd
        ON sd.intimation_id = ci.CI_INTIMATION_ID

    LEFT JOIN cs_amount cs
        ON cs.intimation_id = ci.CI_INTIMATION_ID

    LEFT JOIN ms_amount ms
        ON ms.intimation_id = ci.CI_INTIMATION_ID
),

ordered_admissions AS (
    SELECT
        cb.*,

        LAG(cb.admission_date) OVER (
            PARTITION BY cb.patient_id, cb.icd_code
            ORDER BY cb.admission_date, cb.intimation_id
        ) AS previous_admission_date

    FROM claim_base cb
),

admission_gaps AS (
    SELECT
        oa.*,
        DATEDIFF(oa.admission_date, oa.previous_admission_date) AS gap_days
    FROM ordered_admissions oa
)

SELECT
    icd_code AS `ICD code`,

    COUNT(DISTINCT CASE
        WHEN gap_days = 0
        THEN patient_id
    END) AS same_day_patient_admitted,

    COUNT(DISTINCT CASE
        WHEN gap_days = 1
        THEN patient_id
    END) AS one_day_gap_patient_admitted,

    COUNT(DISTINCT CASE
        WHEN gap_days BETWEEN 2 AND 7
        THEN patient_id
    END) AS two_to_seven_days_patient_admitted,

    COUNT(DISTINCT CASE
        WHEN gap_days BETWEEN 8 AND 15
        THEN patient_id
    END) AS seven_to_fifteen_days_patient_admitted,

    COUNT(DISTINCT CASE
        WHEN gap_days BETWEEN 16 AND 30
        THEN patient_id
    END) AS fifteen_to_thirty_days_patient_admitted,

    COUNT(DISTINCT hospital_key) AS total_hospital,

    ROUND(SUM(approved_amount), 2) AS total_amount_approved_by_hospitals_for_this_particular_ICD

FROM admission_gaps

GROUP BY icd_code

HAVING
       same_day_patient_admitted > 0
    OR one_day_gap_patient_admitted > 0
    OR two_to_seven_days_patient_admitted > 0
    OR seven_to_fifteen_days_patient_admitted > 0
    OR fifteen_to_thirty_days_patient_admitted > 0

ORDER BY
    total_amount_approved_by_hospitals_for_this_particular_ICD DESC,
    same_day_patient_admitted DESC,
    one_day_gap_patient_admitted DESC,
    two_to_seven_days_patient_admitted DESC,
    seven_to_fifteen_days_patient_admitted DESC,
    fifteen_to_thirty_days_patient_admitted DESC;
"""

def run_query(client, sql):
    escaped = sql.replace("'", "'\\''")
    cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e '{escaped}'"
    _, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    err_lines = [l for l in err.split('\\n') if l.strip() and 'Warning' not in l]
    if err_lines:
        print(f"  SQL error: {'; '.join(err_lines)}")
        return []
    reader = csv.reader(io.StringIO(out), delimiter='\t')
    rows = [r for r in reader if r]
    return rows

def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        transport = client.get_transport()
        if transport: transport.set_keepalive(30)
        print("Running query...")
        t0 = datetime.datetime.now()
        rows = run_query(client, QUERY)
        elapsed = datetime.datetime.now() - t0
        
        if len(rows) > 1:
            fname = os.path.join(data_dir, f'admission_gaps_icd_{ts}.csv')
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
