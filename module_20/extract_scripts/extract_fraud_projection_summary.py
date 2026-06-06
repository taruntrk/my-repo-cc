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
output_file = os.path.join(output_dir, 'fraud_projection_summary.csv')

query = """
SELECT 
    ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
    ROUND(SUM(SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.30, 2) AS conservative_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.50, 2) AS moderate_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.75, 2) AS aggressive_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.60, 2) AS ai_interception_cr
FROM settlement_stat
WHERE SS_FY_YEAR BETWEEN 2021 AND 2025;
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
        
    print("SUCCESS: Exported fraud projection summary.")
    print(f"Path: {output_file}")
    print(f"Row count: {len(rows)}")
    
except subprocess.CalledProcessError as e:
    print("ERROR: MySQL execution failed.")
    print(f"Stderr: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"ERROR: {str(e)}")
    exit(1)
