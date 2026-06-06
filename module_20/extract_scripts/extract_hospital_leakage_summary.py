import os
import csv
import subprocess

# Read DB connection parameters from environment variables
host = os.environ.get('DB_HOST', '127.0.0.1')
port = os.environ.get('DB_PORT', '3307')
user = os.environ.get('DB_USER', 'aman')
password = os.environ.get('DB_PASS')  # Never hardcoded
db_name = os.environ.get('DB_NAME', 'ECHS')

if not password:
    raise ValueError("DB_PASS environment variable is required but not set.")

output_dir = '/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'hospital_leakage_summary.csv')

query = """
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
LEFT JOIN office_master om 
    ON CAST(ss.SS_OFFICE_ID AS UNSIGNED) = CAST(om.OM_OFFICE_ID AS UNSIGNED)
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_NABH
ORDER BY total_deducted_lakh DESC;
"""

cmd = [
    'mysql',
    '-h', host,
    '-P', port,
    '-u', user,
    f'-p{password}',
    db_name,
    '-B',
    '-e', query
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    lines = result.stdout.strip().split('\n')
    if not lines or len(lines) < 2:
        print("No data or headers returned.")
        exit(0)
        
    reader = csv.reader(lines, delimiter='\t')
    headers = next(reader)
    rows = list(reader)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
        
    print("SUCCESS: Exported hospital leakage summary.")
    print(f"Path: {output_file}")
    print(f"Row count: {len(rows)}")
    
except subprocess.CalledProcessError as e:
    print("ERROR: MySQL execution failed.")
    print(f"Stderr: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"ERROR: {str(e)}")
    exit(1)
