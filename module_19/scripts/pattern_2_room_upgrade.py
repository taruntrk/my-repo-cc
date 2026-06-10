import pymysql
import csv
import os
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # go up to module_19
DATA_DIR = os.path.join(BASE_DIR, 'new_data')
os.makedirs(DATA_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = os.path.join(DATA_DIR, f"new_19_02_pattern_2_room_upgrade_fraud_{timestamp}.csv")

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

def extract_pattern_2_room_upgrade():
    """Extracts all claims where billed room category exceeds card entitlement."""
    print("Extracting Pattern 2: Room Upgrade Fraud (FULL DATA)...")
    
    # Extract ALL room mismatches without limits
    query = """
    SELECT 
        c.CI_HOSPITAL_ID as hospital_id,
        MAX(o.OM_OFFICE_NAME) as hospital_name,
        MAX(o.OM_OFFICE_CITY) as hospital_city,
        MAX(st.SM_STATE_NAME) as hospital_state,
        c.CI_CARD_ROOM_TYPE as entitled_room,
        c.CI_ROOM_TYPE_ID as billed_room,
        COUNT(*) as mismatch_count,
        SUM(c.CI_APPROX_COST) / 100000 as total_billed_lakh
    FROM claim_intimation c
    LEFT JOIN user_details ud ON c.CI_HOSPITAL_ID = ud.UD_USER_ID
    LEFT JOIN office_master o ON ud.UD_OFFICE_ID = o.OM_OFFICE_ID
    LEFT JOIN state_master st ON o.OM_OFFICE_STATE_ID = st.SM_STATE_ID
    WHERE c.CI_CARD_ROOM_TYPE != c.CI_ROOM_TYPE_ID
      AND c.CI_CARD_ROOM_TYPE IN ('GEN', 'SPR') 
      AND c.CI_ROOM_TYPE_ID IN ('PRI', 'SPR')
      AND c.CI_HOSPITAL_ID IS NOT NULL
      AND c.CI_APPROX_COST > 0
    GROUP BY c.CI_HOSPITAL_ID, c.CI_CARD_ROOM_TYPE, c.CI_ROOM_TYPE_ID
    ORDER BY mismatch_count DESC
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
            
    print(f"✅ Successfully extracted ALL {len(results)} hospital mismatch groups to {os.path.basename(csv_file)}")

if __name__ == "__main__":
    extract_pattern_2_room_upgrade()
