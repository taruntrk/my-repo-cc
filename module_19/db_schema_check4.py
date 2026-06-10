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
        # What is actually in CI_PATIENT_TYPE?
        cur.execute("SELECT CI_PATIENT_TYPE, COUNT(*) FROM claim_intimation GROUP BY CI_PATIENT_TYPE")
        print("CI_PATIENT_TYPE counts:", cur.fetchall())
        
        # What is in CS_ROOM_TYPE?
        cur.execute("SELECT CS_ROOM_TYPE, COUNT(*) FROM claim_submission GROUP BY CS_ROOM_TYPE")
        print("CS_ROOM_TYPE counts:", cur.fetchall())
        
        # What is in CI_SERVICE_TYPE?
        cur.execute("SELECT CI_SERVICE_TYPE, COUNT(*) FROM claim_intimation GROUP BY CI_SERVICE_TYPE")
        print("CI_SERVICE_TYPE counts:", cur.fetchall())
        
        # Are there other patient type columns in patient_register?
        cur.execute("SELECT PTR_SERVICE_TYPE, PTR_CARD_ROOM_TYPE FROM patient_register LIMIT 5")
        print("patient_register sample:", cur.fetchall())
