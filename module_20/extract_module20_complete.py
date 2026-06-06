import paramiko
import csv
import datetime
import json
import os
import warnings
warnings.filterwarnings('ignore')

# ── Credentials ────────────────────────────────────────────────────────────────
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_akash'
SSH_PASS = 'Akash@2026'
DB_USER  = 'akash'
DB_PASS  = 'Akash@2026'
DB_NAME  = 'ECHS'

OUTPUT_DIR = '/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Queries ────────────────────────────────────────────────────────────────────
queries = {

    # ── Q01: Overall system-wide leakage summary ──────────────────────────────
    "01_overall_leakage_summary": """
        SELECT
            SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                    AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                    AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                    AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
        FROM settlement_stat ss
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025;
    """,

    # ── Q02: Year-on-year expenditure trend ───────────────────────────────────
    "02_annual_expenditure_trend": """
        SELECT
            SS_FY_YEAR                                                          AS fiscal_year,
            SUM(SS_CLAIM_CNT)                                                   AS total_claims,
            ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2)                           AS total_claimed_cr,
            ROUND(SUM(SS_APPR_AMT)  / 10000000.0, 2)                           AS total_approved_cr,
            ROUND(SUM(SS_DED_AMT)   / 10000000.0, 2)                           AS total_deducted_cr,
            ROUND(SUM(SS_DED_AMT) * 100.0 / SUM(SS_CLAIM_AMT), 2)             AS deduction_pct
        FROM settlement_stat
        WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY SS_FY_YEAR
        ORDER BY SS_FY_YEAR;
    """,

    # ── Q03: Leakage by hospital type and NABH status ─────────────────────────
    "03_hospital_type_nabh_leakage": """
        SELECT
            COALESCE(om.OM_HOSP_TYPE, 'Unknown')                            AS hosp_type_code,
            COALESCE(om.OM_NABH, 'N')                                       AS nabh_status,
            COUNT(DISTINCT ss.SS_OFFICE_ID)                                 AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                    AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                    AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                    AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY om.OM_HOSP_TYPE, om.OM_NABH
        ORDER BY deduction_pct DESC;
    """,

    # ── Q04: Hospital-wise leakage with full details ──────────────────────────
    "04_hospital_leakage_summary": """
        SELECT
            ss.SS_OFFICE_ID                                                 AS hospital_id,
            COALESCE(om.OM_OFFICE_NAME, 'Unknown')                         AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '')                                AS hospital_city_direct,
            COALESCE(crm.CRM_CITY_NAME, '')                                AS cghs_city,
            COALESCE(sm.SM_STATE_NAME, '')                                  AS state,
            COALESCE(om.OM_HOSP_TYPE, '')                                   AS hosp_type_code,
            COALESCE(om.OM_NABH, 'N')                                       AS nabh_status,
            COALESCE(om.OM_NABL, 'N')                                       AS nabl_status,
            COALESCE(om.OM_OFFICE_PIN, '')                                  AS pincode,
            SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 100000.0, 2)                      AS total_claimed_lakh,
            ROUND(SUM(ss.SS_APPR_AMT)  / 100000.0, 2)                      AS total_approved_lakh,
            ROUND(SUM(ss.SS_DED_AMT)   / 100000.0, 2)                      AS total_deducted_lakh,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY,
                 crm.CRM_CITY_NAME, sm.SM_STATE_NAME, om.OM_HOSP_TYPE,
                 om.OM_NABH, om.OM_NABL, om.OM_OFFICE_PIN
        ORDER BY total_deducted_lakh DESC;
    """,

    # ── Q05: Regional breakdown (fixed — cghs_region_master chain) ───────────
    "05_regional_deduction_breakdown": """
        SELECT
            ss.SS_REGION_ID                                                         AS region_id,
            COALESCE(crm.CRM_CITY_NAME, CONCAT('Region ', ss.SS_REGION_ID))        AS region_name,
            COALESCE(sm.SM_STATE_NAME, '')                                          AS state_name,
            COUNT(DISTINCT ss.SS_OFFICE_ID)                                         AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT)                                                    AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                            AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                            AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                            AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)           AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_REGION_ID, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
        ORDER BY total_deducted_cr DESC;
    """,

    # ── Q06: Fraud projection estimates ───────────────────────────────────────
    "06_fraud_projection_summary": """
        SELECT
            ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2)               AS total_claimed_cr,
            ROUND(SUM(SS_DED_AMT)   / 10000000.0, 2)               AS total_deducted_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.30, 2)        AS conservative_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.50, 2)        AS moderate_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.75, 2)        AS aggressive_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.60, 2)        AS ai_interception_cr
        FROM settlement_stat
        WHERE SS_FY_YEAR BETWEEN 2021 AND 2025;
    """,

    # ── Q07: Individual claim detail for top 25 highest-deduction hospitals ───
    # Mix: claim_intimation + claim_submission + office_master + cghs_region_master
    "07_high_deduction_hospital_claims": """
        SELECT
            ci.CI_CR_OFFICE_ID                                                  AS hospital_id,
            COALESCE(om.OM_OFFICE_NAME, 'Unknown')                             AS hospital_name,
            COALESCE(crm.CRM_CITY_NAME, '')                                    AS city,
            COALESCE(sm.SM_STATE_NAME, '')                                      AS state,
            COALESCE(om.OM_HOSP_TYPE, '')                                       AS hosp_type,
            COALESCE(om.OM_NABH, 'N')                                           AS nabh_status,
            ci.CI_INTIMATION_ID                                                 AS claim_id,
            ci.CI_SERVICE_NO                                                    AS service_number,
            ci.CI_CARD_ID                                                       AS card_number,
            ci.CI_BENEFICIARY_NAME                                              AS beneficiary_name,
            ci.CI_PATIENT_NAME                                                  AS patient_name,
            ci.CI_AGE                                                           AS age,
            ci.CI_SEX                                                           AS gender,
            ci.CI_RELATION_ID                                                   AS relation_code,
            rm.RM_RELATION_NAME                                                 AS relationship,
            ci.CI_ADMISSION_DATE                                                AS admission_date,
            COALESCE(cs.CS_DOD, 'Still Admitted')                              AS discharge_date,
            DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE)    AS stay_days,
            ci.CI_ADM_AILMENT                                                   AS ailment,
            cs.CS_TREAT_DOCT                                                    AS treating_doctor,
            cs.CS_BILL_NO                                                       AS bill_number,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0)                                   AS claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0)                                     AS approved_amount,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0) AS deducted_amount,
            ROUND(
                (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) * 100.0
                / NULLIF(cs.CS_NET_CLAIM_AMT, 0), 2
            )                                                                   AS deduction_pct,
            ci.CI_INT_STAGE                                                     AS claim_stage,
            ci.CI_INT_STATUS                                                    AS claim_status
        FROM claim_intimation ci
        JOIN  claim_submission cs  ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om       ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN relation_master rm     ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND COALESCE(cs.CS_NET_CLAIM_AMT, 0) > 0
            AND (COALESCE(cs.CS_NET_CLAIM_AMT, 0) - COALESCE(cs.CS_UTI_APP_AMT, 0)) > 0
            AND ci.CI_CR_OFFICE_ID IN (
                SELECT office_id FROM (
                    SELECT ss.SS_OFFICE_ID AS office_id
                    FROM settlement_stat ss
                    WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
                    GROUP BY ss.SS_OFFICE_ID
                    ORDER BY SUM(ss.SS_DED_AMT) DESC
                    LIMIT 25
                ) AS top25
            )
        ORDER BY deducted_amount DESC
        LIMIT 500;
    """,

    # ── Q08: Gender + relationship breakdown of deductions ────────────────────
    "08_gender_relation_leakage": """
        SELECT
            ss.SS_GENDER                                                            AS gender,
            COALESCE(rm.RM_RELATION_NAME, ss.SS_RELATION_ID)                       AS relationship,
            SUM(ss.SS_CLAIM_CNT)                                                    AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                            AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                            AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                            AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)           AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_NAME
        ORDER BY total_deducted_cr DESC;
    """
}


def run_query(client, query):
    """Run a MySQL query via stdin (Module 11 pattern) — avoids shell escaping issues."""
    cmd = f'mysql -u{DB_USER} -p{DB_PASS} {DB_NAME} -B'
    stdin_c, stdout, stderr = client.exec_command(cmd, timeout=600)
    stdin_c.write(query.encode('utf-8'))
    stdin_c.channel.shutdown_write()
    stdout.channel.settimeout(590)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    warn = [l for l in err.splitlines() if 'Using a password' not in l and l.strip()]
    if warn:
        print(f"  [WARNING] {' | '.join(warn)[:200]}")
    return out


def main():
    print(f"\n{'='*80}")
    print(f"ECHS Module 20: Budget Leakage Analysis — Data Extraction")
    print(f"Execution Start: {datetime.datetime.now()}")
    print(f"{'='*80}\n")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to SSH: {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER,
                       password=SSH_PASS, timeout=30)
        print("✓ Connected.\n")

        results_summary = {}
        all_data        = {}

        for idx, (name, query) in enumerate(queries.items(), 1):
            print(f"\n[{idx}/{len(queries)}] Executing: {name}")
            print(f"Time: {datetime.datetime.now()}")
            print("-" * 80)

            try:
                t0  = datetime.datetime.now()
                raw = run_query(client, query)
                t1  = datetime.datetime.now()

                if raw and raw.strip():
                    lines = raw.strip().splitlines()

                    # Save CSV
                    csv_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for line in lines:
                            writer.writerow(line.split('\t'))

                    # Parse for JSON
                    headers = lines[0].split('\t')
                    rows    = [dict(zip(headers, l.split('\t'))) for l in lines[1:]]
                    all_data[name] = {'filename': csv_path, 'rows': len(rows),
                                      'query_time': str(t1 - t0), 'data': rows}

                    print(f"✓ Completed in {t1 - t0}")
                    print(f"✓ Records: {len(rows)}")
                    print(f"✓ Saved: {csv_path}")

                    # Preview
                    print("\nPreview (first 3 records):")
                    for i, line in enumerate(lines[:4]):
                        label = "HEADERS" if i == 0 else f"Row {i}"
                        print(f"  {label}: {line.replace(chr(9), ' | ')[:160]}")
                    if len(lines) > 4:
                        print(f"  ... and {len(lines)-4} more records")

                    results_summary[name] = {'status': 'success',
                                             'records': len(rows),
                                             'file': csv_path,
                                             'query_time': str(t1 - t0)}
                else:
                    print("⚠ No data returned")
                    results_summary[name] = {'status': 'no_data', 'records': 0}

            except Exception as e:
                print(f"✗ Error: {e}")
                results_summary[name] = {'status': 'error', 'error': str(e)}

        # Save JSON report
        json_path = os.path.join(OUTPUT_DIR, 'Module20_Budget_Leakage_Complete_Data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'execution_time': datetime.datetime.now().isoformat(),
                'total_queries': len(queries),
                'summary': results_summary,
                'data': all_data
            }, f, indent=2, default=str)

        # Final summary
        print(f"\n{'='*80}")
        print("EXTRACTION COMPLETE")
        print(f"{'='*80}")
        print(f"  Total Queries : {len(queries)}")
        print(f"  Successful    : {sum(1 for r in results_summary.values() if r['status']=='success')}")
        print(f"  No Data       : {sum(1 for r in results_summary.values() if r['status']=='no_data')}")
        print(f"  Errors        : {sum(1 for r in results_summary.values() if r['status']=='error')}")
        print(f"\nRecords Extracted:")
        for name, info in results_summary.items():
            if info['status'] == 'success':
                print(f"  {name}: {info['records']} records")
        print(f"\n✓ CSVs saved to : {OUTPUT_DIR}")
        print(f"✓ JSON report   : {json_path}")
        print(f"\nEnd Time: {datetime.datetime.now()}")

    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        import traceback; traceback.print_exc()
    finally:
        client.close()
        print("\n✓ SSH connection closed.")


if __name__ == "__main__":
    main()
