#!/usr/bin/env python3
"""
ECHS Module 20 - Fresh Data Extraction
Runs 3 queries and saves CSVs:
  1. regional_deduction_breakdown.csv  (re-run with fixed join)
  2. high_deduction_hospital_claims.csv (new - claim-level detail)
  3. gender_relation_leakage.csv        (new - who drives deductions)

SSH tunnel must be active on port 3307 before running.
Usage: python3 extract_module20_fresh.py
"""

import os, csv, subprocess

DB_HOST = '127.0.0.1'
DB_PORT = '3307'
DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'
OUT_DIR = '/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20'

os.makedirs(OUT_DIR, exist_ok=True)

queries = {

    # Fixed: uses office_master → cghs_region_master → state_master (Module 11 pattern)
    # Previously broken: ecs_region table had missing region names
    "regional_deduction_breakdown": """
        SELECT
            ss.SS_REGION_ID AS region_id,
            COALESCE(crm.CRM_CITY_NAME, CONCAT('Region ', ss.SS_REGION_ID)) AS region_name,
            COALESCE(sm.SM_STATE_NAME, '') AS state_name,
            COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2) AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_REGION_ID, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
        ORDER BY total_deducted_cr DESC;
    """,

    # New: individual claim detail for top 25 highest-deduction hospitals
    "high_deduction_hospital_claims": """
        SELECT
            ci.CI_CR_OFFICE_ID AS hospital_id,
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, crm.CRM_CITY_NAME, '') AS city,
            COALESCE(sm.SM_STATE_NAME, '') AS state,
            COALESCE(om.OM_HOSP_TYPE, '') AS hosp_type,
            COALESCE(om.OM_NABH, 'N') AS nabh_status,
            ci.CI_INTIMATION_ID AS claim_id,
            ci.CI_SERVICE_NO AS service_number,
            ci.CI_BENEFICIARY_NAME AS beneficiary_name,
            ci.CI_PATIENT_NAME AS patient_name,
            ci.CI_AGE AS age,
            ci.CI_SEX AS gender,
            ci.CI_ADMISSION_DATE AS admission_date,
            cs.CS_DOD AS discharge_date,
            DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) AS stay_days,
            ci.CI_ADM_AILMENT AS ailment,
            cs.CS_TREAT_DOCT AS treating_doctor,
            cs.CS_BILL_NO AS bill_number,
            cs.CS_NET_CLAIM_AMT AS claimed_amount,
            cs.CS_UTI_APP_AMT AS approved_amount,
            (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) AS deducted_amount,
            ROUND((cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) * 100.0 / NULLIF(cs.CS_NET_CLAIM_AMT, 0), 2) AS deduction_pct,
            ci.CI_INT_STAGE AS claim_stage,
            ci.CI_INT_STATUS AS claim_status
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om       ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_NET_CLAIM_AMT > 0
            AND (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) > 0
            AND ci.CI_CR_OFFICE_ID IN (
                SELECT ss.SS_OFFICE_ID FROM settlement_stat ss
                WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
                GROUP BY ss.SS_OFFICE_ID
                ORDER BY SUM(ss.SS_DED_AMT) DESC
                LIMIT 25
            )
        ORDER BY deducted_amount DESC
        LIMIT 500;
    """,

    # New: who drives deductions — self, wife, son, daughter etc.
    "gender_relation_leakage": """
        SELECT
            ss.SS_GENDER AS gender,
            COALESCE(rm.RM_RELATION_DESC, ss.SS_RELATION_ID) AS relationship,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2) AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_DESC
        ORDER BY total_deducted_cr DESC;
    """
}

def run_query(name, query):
    csv_path = os.path.join(OUT_DIR, f"{name}.csv")
    cmd = ['mysql', '-h', DB_HOST, '-P', DB_PORT, '-u', DB_USER,
           f'-p{DB_PASS}', DB_NAME, '-B', '-e', query.strip()]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = res.stdout.strip().split('\n')
        if len(lines) < 2:
            print(f"  ⚠ No data returned for {name}")
            return
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in lines:
                writer.writerow(line.split('\t'))
        print(f"  ✓ {name}.csv — {len(lines)-1} rows")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {name} FAILED: {e.stderr.strip()[:200]}")

if __name__ == '__main__':
    print("="*60)
    print("ECHS Module 20 — Fresh Extraction (3 queries)")
    print("="*60)
    for i, (name, query) in enumerate(queries.items(), 1):
        print(f"\n[{i}/{len(queries)}] Running: {name} ...")
        run_query(name, query)
    print("\n✅ Done. CSVs saved to:", OUT_DIR)
