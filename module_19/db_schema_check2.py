import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

with get_connection() as conn:
    with conn.cursor() as cur:
        # Check patient_type table
        cur.execute("SELECT * FROM patient_type LIMIT 5")
        print("patient_type:", cur.fetchall())
        
        # Check OM_HOSP_TYPES in office_master
        cur.execute("SELECT OM_HOSP_TYPE, OM_HOSP_TYPES FROM office_master WHERE OM_HOSP_TYPES IS NOT NULL AND OM_HOSP_TYPES != '' LIMIT 5")
        print("office_master OM_HOSP_TYPES:", cur.fetchall())
        
        # Are patient types filled in patient_register?
        cur.execute("DESCRIBE patient_register")
        pr_cols = [r['Field'] for r in cur.fetchall()]
        print("patient_register columns:", [c for c in pr_cols if 'type' in c.lower() or 'pat' in c.lower()])
