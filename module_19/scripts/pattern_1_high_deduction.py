import pymysql
import csv
import os
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'new_data')
os.makedirs(DATA_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = os.path.join(DATA_DIR, f"new_19_01_all_hospital_deductions_{timestamp}.csv")

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

def extract_all_hospital_deductions():
    """Extracts deduction stats for ALL hospitals without any limits."""
    print("Extracting Pattern 1: High Deduction Hospitals (FULL DATA)...")
    
    # We extract every single hospital's total claims, approved, and deducted amounts.
    # No LIMIT, no HAVING deduction_pct > 25. We extract everything.
    query = """
    SELECT 
        s.SS_OFFICE_ID as hospital_id,
        o.OM_OFFICE_NAME as hospital_name,
        o.OM_OFFICE_CITY as hospital_city,
        st.SM_STATE_NAME as hospital_state,
        o.OM_HOSP_TYPE as hosp_type_code,
        IFNULL(o.OM_NABH, 'N') as nabh_status,
        SUM(s.SS_CLAIM_CNT) as total_claims,
        SUM(s.SS_CLAIM_AMT) / 100000 as total_claimed_lakh,
        SUM(s.SS_APPR_AMT) / 100000 as total_approved_lakh,
        SUM(s.SS_DED_AMT) / 100000 as total_deducted_lakh,
        (SUM(s.SS_DED_AMT) / NULLIF(SUM(s.SS_CLAIM_AMT), 0)) * 100 as deduction_pct
    FROM settlement_stat s
    LEFT JOIN office_master o ON s.SS_OFFICE_ID = o.OM_OFFICE_ID
    LEFT JOIN state_master st ON o.OM_OFFICE_STATE_ID = st.SM_STATE_ID
    GROUP BY s.SS_OFFICE_ID
    ORDER BY deduction_pct DESC
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            
    if results:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"✅ Successfully extracted ALL {len(results)} hospital records to {os.path.basename(csv_file)}")

if __name__ == "__main__":
    extract_all_hospital_deductions()
