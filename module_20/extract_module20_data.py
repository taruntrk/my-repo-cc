#!/usr/bin/env python3
"""
ECHS Module 20: Budget Impact & Leakage Analysis - Data Extraction
==================================================================
Unified master extraction script that runs all 6 Module 20 queries 
against the ECHS production database via the local port 3307 tunnel.
Uses the secure `subprocess` + `mysql` CLI pattern to avoid dependency issues.

Output Directory: data-tarun/module_20/
Date: June 5, 2026
"""

import os
import csv
import subprocess
import datetime

# Database Configuration (over active SSH tunnel on port 3307)
DB_HOST = '127.0.0.1'
DB_PORT = '3307'
DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

# Target output directory
OUTPUT_DIR = '/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Queries matching point20_budget_leakage_queries.sql
queries = {
    "overall_leakage_summary": """
        SELECT 
            SUM(SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(SS_APPR_AMT) / 10000000.0, 2) AS total_approved_cr,
            ROUND(SUM(SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(SS_DED_AMT) * 100.0 / SUM(SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat
        WHERE SS_FY_YEAR BETWEEN 2021 AND 2025;
    """,
    
    "annual_expenditure_trend": """
        WITH annual_stats AS (
            SELECT 
                SS_FY_YEAR AS fiscal_year,
                SUM(SS_CLAIM_CNT) AS total_claims,
                SUM(SS_CLAIM_AMT) AS total_claimed,
                SUM(SS_APPR_AMT) AS total_approved,
                SUM(SS_DED_AMT) AS total_deducted
            FROM settlement_stat
            WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
            GROUP BY SS_FY_YEAR
        )
        SELECT 
            fiscal_year,
            total_claims,
            ROUND(total_claimed / 10000000.0, 2) AS total_claimed_cr,
            ROUND(total_approved / 10000000.0, 2) AS total_approved_cr,
            ROUND(total_deducted / 10000000.0, 2) AS total_deducted_cr,
            ROUND(total_deducted * 100.0 / total_claimed, 2) AS deduction_pct,
            ROUND(
                (total_claimed - LAG(total_claimed) OVER (ORDER BY fiscal_year)) * 100.0 
                / LAG(total_claimed) OVER (ORDER BY fiscal_year), 
                2
            ) AS yoy_growth_pct
        FROM annual_stats
        ORDER BY fiscal_year;
    """,
    
    "hospital_type_nabh_leakage": """
        SELECT 
            COALESCE(om.OM_HOSP_TYPE, 'Unknown') AS hosp_type_code,
            COALESCE(om.OM_NABH, 'N') AS nabh_status,
            COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT) / 10000000.0, 2) AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY om.OM_HOSP_TYPE, om.OM_NABH
        ORDER BY deduction_pct DESC;
    """,
    
    "hospital_leakage_summary": """
        SELECT 
            CONCAT(COALESCE(om.OM_OFFICE_NAME, 'Unknown'), ' [', ss.SS_OFFICE_ID, ']') AS hospital_name_with_id,
            COALESCE(om.OM_HOSP_TYPE, '') AS hosp_type_code,
            COALESCE(om.OM_NABH, 'N') AS nabh_status,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 100000.0, 2) AS total_claimed_lakh,
            ROUND(SUM(ss.SS_APPR_AMT) / 100000.0, 2) AS total_approved_lakh,
            ROUND(SUM(ss.SS_DED_AMT) / 100000.0, 2) AS total_deducted_lakh,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_NABH
        ORDER BY total_deducted_lakh DESC;
    """,
    
    "regional_deduction_breakdown": """
        SELECT 
            ss.SS_REGION_ID AS region_id,
            COALESCE(crm.CRM_CITY_NAME, CONCAT('Region ', ss.SS_REGION_ID)) AS region_name,
            COALESCE(sm.SM_STATE_NAME, '') AS state_name,
            COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(ss.SS_APPR_AMT) / 10000000.0, 2) AS total_approved_cr,
            ROUND(SUM(ss.SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_REGION_ID, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
        ORDER BY total_deducted_cr DESC;
    """,
    
    "fraud_projection_summary": """
        SELECT 
            ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.30, 2) AS conservative_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.50, 2) AS moderate_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.75, 2) AS aggressive_fraud_cr,
            ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.60, 2) AS ai_interception_cr
        FROM settlement_stat
        WHERE SS_FY_YEAR BETWEEN 2021 AND 2025;
    """,

    # NEW: Claim-level detail for top 25 high-deduction hospitals
    # Mixes: claim_intimation + claim_submission + office_master + cghs_region_master + state_master
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
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_NET_CLAIM_AMT > 0
            AND (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) > 0
            AND ci.CI_CR_OFFICE_ID IN (
                SELECT ss.SS_OFFICE_ID
                FROM settlement_stat ss
                WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
                GROUP BY ss.SS_OFFICE_ID
                ORDER BY SUM(ss.SS_DED_AMT) DESC
                LIMIT 25
            )
        ORDER BY deducted_amount DESC
        LIMIT 500;
    """,

    # NEW: Gender + Relation breakdown — who drives deductions
    # Mixes: settlement_stat internal columns + relation_master
    "gender_relation_leakage": """
        SELECT 
            ss.SS_GENDER AS gender,
            COALESCE(rm.RM_RELATION_DESC, ss.SS_RELATION_ID) AS relationship,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
            ROUND(SUM(ss.SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_DESC
        ORDER BY total_deducted_cr DESC;
    """
}

def execute_extraction():
    print(f"\n{'='*80}")
    print(f"ECHS Module 20 Unified Data Extraction Pipeline")
    print(f"Target Period: FY 2021 - FY 2025")
    print(f"Start Time: {datetime.datetime.now()}")
    print(f"{'='*80}\n")
    
    success_count = 0
    
    for idx, (name, query) in enumerate(queries.items(), 1):
        print(f"[{idx}/{len(queries)}] Extracting dataset: {name}...")
        csv_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        
        # Format mysql CLI call
        cmd = [
            'mysql',
            '-h', DB_HOST,
            '-P', DB_PORT,
            '-u', DB_USER,
            f'-p{DB_PASS}',
            DB_NAME,
            '-B',
            '-e', query.strip()
        ]
        
        try:
            start_time = datetime.datetime.now()
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            end_time = datetime.datetime.now()
            
            out = res.stdout
            if out and out.strip():
                lines = out.strip().split('\n')
                
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for line in lines:
                        writer.writerow(line.split('\t'))
                
                print(f"  ✓ Saved {len(lines) - 1} records to {os.path.basename(csv_path)}")
                print(f"  ✓ Execution time: {end_time - start_time}")
                success_count += 1
            else:
                print(f"  ⚠ Query ran successfully but returned no records.")
                
        except subprocess.CalledProcessError as e:
            print(f"  ✗ MySQL CLI error: {e.stderr.strip()}")
        except Exception as e:
            print(f"  ✗ Unexpected error: {str(e)}")
            
        print("-" * 80)
        
    print(f"\n{'='*80}")
    print(f"EXTRACTION PIPELINE COMPLETED")
    print(f"Successful extractions: {success_count}/{len(queries)}")
    print(f"All outputs located at: {OUTPUT_DIR}")
    print(f"End Time: {datetime.datetime.now()}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    execute_extraction()
