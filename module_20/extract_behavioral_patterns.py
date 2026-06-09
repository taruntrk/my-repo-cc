#!/usr/bin/env python3
"""
ECHS Module 20: Behavioral Fraud Patterns - Data Extraction
==================================================================
Extracts specific advanced behavioral/methodology patterns from the 
ECHS database via the local port 3307 tunnel.
Saves CSVs to module_20/new_data/ for report integration.
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

# Target output directory (new_data as requested)
BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, 'new_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

queries = {
    "08_los_bed_blocking_abuse": """
        SELECT 
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '') AS city,
            ci.CI_BENEFICIARY_NAME AS patient_name,
            cs.CS_ADM_AILMENT AS ailment,
            ci.CI_ADMISSION_DATE AS admission_date,
            cs.CS_DOD AS discharge_date,
            DATEDIFF(cs.CS_DOD, ci.CI_ADMISSION_DATE) AS stay_days,
            cs.CS_NET_CLAIM_AMT AS claimed_amount,
            (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) AS deducted_amount
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND DATEDIFF(cs.CS_DOD, ci.CI_ADMISSION_DATE) > 10
            AND (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) > 0
        ORDER BY deducted_amount DESC
        LIMIT 500;
    """,
    
    "09_ping_pong_admissions": """
        WITH PatientClaims AS (
            SELECT 
                ci.CI_CR_OFFICE_ID AS hospital_id,
                COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
                ci.CI_BENEFICIARY_NAME AS patient_name,
                ci.CI_SERVICE_NO AS service_no,
                ci.CI_ADMISSION_DATE AS admin_date,
                cs.CS_DOD AS discharge_date,
                cs.CS_NET_CLAIM_AMT AS claim_amt,
                LEAD(ci.CI_ADMISSION_DATE) OVER (PARTITION BY ci.CI_SERVICE_NO, ci.CI_BENEFICIARY_NAME ORDER BY ci.CI_ADMISSION_DATE) AS next_admin_date
            FROM claim_intimation ci
            JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
            LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
            WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
        )
        SELECT 
            hospital_name,
            patient_name,
            admin_date AS admission_1,
            discharge_date AS discharge_1,
            next_admin_date AS admission_2,
            DATEDIFF(next_admin_date, discharge_date) AS gap_days,
            claim_amt
        FROM PatientClaims
        WHERE DATEDIFF(next_admin_date, discharge_date) BETWEEN 0 AND 2
        ORDER BY gap_days ASC, claim_amt DESC
        LIMIT 500;
    """,
    
    "10_icu_conversion_abuse": """
        SELECT 
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '') AS city,
            COUNT(*) AS total_claims,
            COUNT(CASE WHEN cs.CS_ROOM_TYPE = 'ICU' THEN 1 END) AS icu_cases,
            ROUND(COUNT(CASE WHEN cs.CS_ROOM_TYPE = 'ICU' THEN 1 END) * 100.0 / COUNT(*), 2) AS icu_pct,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT)/100000, 2) AS total_deducted_lakhs
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE cs.CS_SUB_DATE >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY
        HAVING total_claims > 50 AND icu_pct > 15
        ORDER BY icu_pct DESC, total_deducted_lakhs DESC
        LIMIT 200;
    """
}

def execute_extraction():
    print(f"\n{'='*80}")
    print(f"ECHS Module 20 Behavioral Fraud Extraction")
    print(f"Start Time: {datetime.datetime.now()}")
    print(f"{'='*80}\n")
    
    success_count = 0
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for filename_prefix, query in queries.items():
        csv_filename = f"new_{filename_prefix}_{ts}.csv"
        csv_path = os.path.join(OUTPUT_DIR, csv_filename)
        
        print(f"Executing: {filename_prefix}")
        query_to_run = query.strip()
        
        cmd = [
            'mysql',
            '-h', DB_HOST,
            '-P', DB_PORT,
            '-u', DB_USER,
            f'-p{DB_PASS}',
            DB_NAME,
            '-B',
            '-e', query_to_run
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
                
                print(f"  ✓ Saved {len(lines) - 1} records to {csv_filename}")
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
    print(f"EXTRACTION COMPLETED")
    print(f"Successful extractions: {success_count}/{len(queries)}")
    print(f"Outputs located at: {OUTPUT_DIR}")
    print(f"End Time: {datetime.datetime.now()}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    execute_extraction()
