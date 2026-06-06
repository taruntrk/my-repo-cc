import os
import csv
import pymysql

# Read DB connection parameters from environment variables
host = os.environ.get('DB_HOST', '127.0.0.1')
port = int(os.environ.get('DB_PORT', '3307'))
user = os.environ.get('DB_USER', 'aman')
password = os.environ.get('DB_PASS')  # Never hardcoded
db_name = os.environ.get('DB_NAME', 'ECHS')

if not password:
    raise ValueError("DB_PASS environment variable is required but not set.")

output_dir = '/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'top25_hospitals_by_deduction.csv')

query = """
SELECT 
    ss.SS_OFFICE_ID AS hospital_id,
    om.OM_OFFICE_NAME AS hospital_name,
    COALESCE(om.OM_HOSP_TYPE, '') AS hosp_type_code,
    COALESCE(om.OM_NABH, 'N') AS nabh_status,
    SUM(ss.SS_CLAIM_CNT) AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2) AS total_claimed_cr,
    ROUND(SUM(ss.SS_APPR_AMT) / 10000000.0, 2) AS total_approved_cr,
    ROUND(SUM(ss.SS_DED_AMT) / 10000000.0, 2) AS total_deducted_cr,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
FROM settlement_stat ss
LEFT JOIN office_master om 
    ON CAST(ss.SS_OFFICE_ID AS UNSIGNED) = CAST(om.OM_OFFICE_ID AS UNSIGNED)
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_NABH
ORDER BY total_deducted_cr DESC
LIMIT 25;
"""

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    if rows:
        headers = list(rows[0].keys())
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        print(f"SUCCESS: Exported top 25 hospitals by deduction.")
        print(f"Path: {output_file}")
        print(f"Row count: {len(rows)}")
    else:
        print("No data found for the query.")
finally:
    if 'conn' in locals() and conn.open:
        conn.close()
