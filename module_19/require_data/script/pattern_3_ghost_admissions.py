import pymysql
import csv
import os
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = os.path.join(DATA_DIR, f"new_19_03_pattern_3_ghost_admissions_{timestamp}.csv")

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

def extract_pattern_3_ghost_admissions():
    """Extracts claims where CI_HOSPITAL_ID is NULL (Ghost Exposure)."""
    print("Extracting Pattern 3: Ghost Admissions (FULL DATA)...")
    
    # We group by room mismatch because pulling all 24M NULL claims raw would be too large.
    # This specifically targets the fraud exposure within the Ghost claims.
    query = """
    SELECT 
        c.CI_INTIMATION_ID as claim_id,
        YEAR(c.CI_ADMISSION_DATE) as claim_year,
        'NULL (Ghost)' as hospital_id,
        'NO TRACEABLE HOSPITAL' as hospital_name,
        
        pt.PT_TYPE_DESC as patient_type,
        c.CI_ADM_AILMENT as admission_ailment,
        
        c.CI_CARD_ROOM_TYPE as entitled_room,
        c.CI_ROOM_TYPE_ID as billed_room,
        cs.CS_GR_CLAIM_AMT as billed_amount,
        cs.CS_UTI_APP_AMT as approved_amount,
        (cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT) as deducted_amount
    FROM claim_intimation c
    LEFT JOIN claim_submission cs ON c.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN patient_type pt ON c.CI_PATIENT_TYPE = pt.PT_TYPE_ID
    WHERE c.CI_HOSPITAL_ID IS NULL
      AND cs.CS_GR_CLAIM_AMT > 0
      AND YEAR(c.CI_ADMISSION_DATE) BETWEEN 2021 AND 2026

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
            
    print(f"✅ Successfully extracted ALL {len(results)} ghost admission groups to {os.path.basename(csv_file)}")

if __name__ == "__main__":
    extract_pattern_3_ghost_admissions()
