import pymysql
import csv
import os
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = os.path.join(DATA_DIR, f"new_19_10_pattern_10_emergency_bypass_{timestamp}.csv")

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

def extract_pattern_10_emergency_bypass():
    """Extracts RAW claims marked as Emergency (Gateway Bypass)."""
    print("Extracting Pattern 10: Emergency Gateway Bypass (RAW FULL DATA)...")
    
    query = """
    SELECT 
        c.CI_INTIMATION_ID as claim_id,
        YEAR(c.CI_ADMISSION_DATE) as claim_year,
        c.CI_HOSPITAL_ID as hospital_id,
        o.OM_OFFICE_NAME as registered_hospital_name,
        o.OM_OFFICE_CITY as hospital_city,
        st.SM_STATE_NAME as hospital_state,
        crm.CRM_CITY_NAME as cghs_region,
        ht.hos_type_description as hospital_type,
        
        c.CI_REF_TYPE_ID as referral_type,
        c.CI_NONEMP_FLG as is_non_empanelled,
        pt.PT_TYPE_DESC as patient_type,
        c.CI_ADM_AILMENT as admission_ailment,
        
        c.CI_ADMISSION_DATE as admission_date,
        cs.CS_DOD as discharge_date,
        
        cs.CS_GR_CLAIM_AMT as total_billed_amount,
        cs.CS_UTI_APP_AMT as total_approved_amount,
        (cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT) as deducted_amount
    FROM claim_intimation c
    LEFT JOIN claim_submission cs ON c.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN patient_type pt ON c.CI_PATIENT_TYPE = pt.PT_TYPE_ID
    LEFT JOIN user_details ud ON c.CI_HOSPITAL_ID = ud.UD_USER_ID
    LEFT JOIN office_master o ON ud.UD_OFFICE_ID = o.OM_OFFICE_ID
    LEFT JOIN state_master st ON o.OM_OFFICE_STATE_ID = st.SM_STATE_ID
    LEFT JOIN hos_types ht ON o.OM_HOSP_TYPE = ht.hos_type_id
    LEFT JOIN cghs_region_master crm ON o.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    WHERE c.CI_REF_TYPE_ID = 'E'
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
            
    print(f"✅ Successfully extracted ALL {len(results)} raw individual claims to {os.path.basename(csv_file)}")

if __name__ == "__main__":
    extract_pattern_10_emergency_bypass()
