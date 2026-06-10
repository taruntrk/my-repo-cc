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
        cur.execute("SELECT * FROM hos_types LIMIT 10")
        print("hos_types:", cur.fetchall())
        
        cur.execute("SELECT CI_PATIENT_TYPE, COUNT(*) FROM claim_intimation WHERE CI_PATIENT_TYPE IS NOT NULL LIMIT 10")
        print("CI_PATIENT_TYPE not null:", cur.fetchall())
        
        cur.execute("SELECT COUNT(*) FROM claim_intimation WHERE CI_PATIENT_TYPE IS NULL")
        print("CI_PATIENT_TYPE is null:", cur.fetchall())
