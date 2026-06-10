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
        cur.execute("SELECT CI_PATIENT_TYPE, COUNT(*) as c FROM claim_intimation WHERE YEAR(CI_ADMISSION_DATE) BETWEEN 2021 AND 2026 GROUP BY CI_PATIENT_TYPE")
        ptypes = cur.fetchall()
        print("CI_PATIENT_TYPE stats:", ptypes)
        
        cur.execute("SELECT ht.hos_type_description, COUNT(*) as c FROM office_master o LEFT JOIN hos_types ht ON o.OM_HOSP_TYPE = ht.hos_type_code GROUP BY ht.hos_type_description")
        htypes = cur.fetchall()
        print("hos_type_description stats (from office_master):", htypes[:10]) # just show a few
