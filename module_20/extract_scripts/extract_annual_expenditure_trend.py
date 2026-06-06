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
output_file = os.path.join(output_dir, 'annual_expenditure_trend.csv')

query = """
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
        
    print("SUCCESS: Exported annual expenditure trend.")
    print(f"Path: {output_file}")
    print(f"Row count: {len(rows)}")
    
except subprocess.CalledProcessError as e:
    print("ERROR: MySQL execution failed.")
    print(f"Stderr: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"ERROR: {str(e)}")
    exit(1)
