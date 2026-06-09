#!/usr/bin/env python3
"""
ECHS Module 20: Phase 3 Advanced Fraud Patterns - Data Extraction
==================================================================
Extracts specific ultra-advanced fraud patterns (Weekend Surge, 
Superman Surgeon, Threshold Avoiding) from the ECHS database.
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
    "10_weekend_surge_abuse": """
        SELECT 
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '') AS city,
            COUNT(*) as weekend_admissions,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT)/100000, 2) as total_claimed_lakhs,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT)/100000, 2) as total_deducted_lakhs
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
          AND DAYOFWEEK(ci.CI_ADMISSION_DATE) IN (1, 6, 7)
        GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY
        HAVING weekend_admissions > 50
        ORDER BY total_deducted_lakhs DESC
        LIMIT 200;
    """,
    
    "11_superman_surgeon": """
        SELECT 
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '') AS city,
            cs.CS_TREAT_DOCT as doctor_name,
            DATE(cs.CS_SUB_DATE) as claim_date,
            COUNT(*) as surgeries_in_one_day,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT)/100000, 2) as total_claimed_lakhs
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
          AND cs.CS_TREAT_DOCT IS NOT NULL AND cs.CS_TREAT_DOCT != ''
        GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY, cs.CS_TREAT_DOCT, DATE(cs.CS_SUB_DATE)
        HAVING surgeries_in_one_day >= 15
        ORDER BY surgeries_in_one_day DESC
        LIMIT 200;
    """,
    
    "12_threshold_avoiding": """
        SELECT 
            COALESCE(om.OM_OFFICE_NAME, 'Unknown') AS hospital_name,
            COALESCE(om.OM_OFFICE_CITY, '') AS city,
            COUNT(*) as trick_bills_count,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT)/100000, 2) as total_claimed_lakhs,
            ROUND(SUM(cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT)/100000, 2) as total_deducted_lakhs
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
          AND cs.CS_NET_CLAIM_AMT BETWEEN 99000 AND 99999
        GROUP BY ci.CI_CR_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY
        HAVING trick_bills_count > 10
        ORDER BY trick_bills_count DESC
        LIMIT 200;
    """
}

def execute_extraction():
    print(f"\n{'='*80}")
    print(f"ECHS Module 20 Phase 3 Fraud Extraction")
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
