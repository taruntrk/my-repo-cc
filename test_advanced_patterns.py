import subprocess
import datetime

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
        return f"SQL Error: {e.output.decode('utf-8')}"

print("Scanning ECHS Database for Advanced Fraud Patterns...")

# 1. Threshold Avoiding (The 99,999 Trick)
q_threshold = """
SELECT 
    CS_NET_CLAIM_AMT as claim_amount, 
    COUNT(*) as number_of_bills,
    ROUND(SUM(CS_NET_CLAIM_AMT - CS_UTI_APP_AMT)/100000, 2) as deducted_lakhs
FROM claim_submission
WHERE CS_SUB_DATE >= '2023-01-01' 
  AND CS_NET_CLAIM_AMT BETWEEN 99000 AND 99999
GROUP BY CS_NET_CLAIM_AMT
ORDER BY number_of_bills DESC
LIMIT 10;
"""
print("\n--- Pattern A: Threshold Avoiding (Bills exactly under ₹1 Lakh) ---")
print(run_query(q_threshold))

# 2. Weekend Surge Admissions
q_weekend = """
SELECT 
    DAYNAME(CS_ADMISSION_DATE) as admission_day,
    COUNT(*) as total_admissions,
    ROUND(SUM(CS_NET_CLAIM_AMT - CS_UTI_APP_AMT)/100000, 2) as deducted_lakhs
FROM claim_submission
WHERE CS_SUB_DATE >= '2023-01-01'
GROUP BY admission_day
ORDER BY total_admissions DESC;
"""
print("\n--- Pattern B: Day of Week Admission Distribution (Weekend Surge) ---")
print(run_query(q_weekend))

# 3. Superman Surgeon (Doctors doing massive numbers of claims in one day)
q_doctor = """
SELECT 
    CS_TREAT_DOCT as doctor_name,
    CS_SUB_DATE as claim_date,
    COUNT(*) as claims_in_one_day,
    ROUND(SUM(CS_NET_CLAIM_AMT)/100000, 2) as total_claimed_lakhs
FROM claim_submission
WHERE CS_SUB_DATE >= '2023-01-01' 
  AND CS_TREAT_DOCT IS NOT NULL 
  AND CS_TREAT_DOCT != ''
GROUP BY CS_TREAT_DOCT, CS_SUB_DATE
HAVING claims_in_one_day > 20
ORDER BY claims_in_one_day DESC
LIMIT 10;
"""
print("\n--- Pattern C: Superman Surgeon (>20 claims submitted on the exact same day) ---")
print(run_query(q_doctor))
