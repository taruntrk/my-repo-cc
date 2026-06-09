import subprocess
import pandas as pd
import io

DB_HOST = '127.0.0.1'
DB_PORT = '3307'
DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

def run_query(query):
    try:
        result = subprocess.check_output(
            ['mysql', '-h', DB_HOST, '-P', DB_PORT, '-u', DB_USER, f'-p{DB_PASS}', DB_NAME, '-e', query],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        return result
    except subprocess.CalledProcessError as e:
        print("SQL Error:", e.output.decode('utf-8'))
        return ""

q1 = """
SELECT 
    DATEDIFF(CS_DOD, CS_ADMISSION_DATE) as stay_days,
    COUNT(*) as count_claims,
    ROUND(SUM(CS_NET_CLAIM_AMT - CS_UTI_APP_AMT)/100000, 2) as deducted_lakhs
FROM claim_submission 
WHERE CS_SUB_DATE > '2023-01-01' 
  AND CS_NET_CLAIM_AMT > CS_UTI_APP_AMT
GROUP BY stay_days 
ORDER BY deducted_lakhs DESC 
LIMIT 10;
"""
print("\n--- Pattern A: Length of Stay (LoS) Impact ---")
print(run_query(q1))

q2 = """
SELECT 
    CS_ROOM_TYPE,
    COUNT(*) as count_claims,
    ROUND(SUM(CS_NET_CLAIM_AMT - CS_UTI_APP_AMT)/100000, 2) as deducted_lakhs
FROM claim_submission
WHERE CS_SUB_DATE > '2023-01-01'
GROUP BY CS_ROOM_TYPE
ORDER BY deducted_lakhs DESC
LIMIT 10;
"""
print("\n--- Pattern B: Room Type / ICU Fraud ---")
print(run_query(q2))
