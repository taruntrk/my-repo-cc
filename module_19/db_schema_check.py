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
        # Show tables matching patient or hospital
        cur.execute("SHOW TABLES LIKE '%patient%'")
        print("Patient tables:", cur.fetchall())
        
        cur.execute("SHOW TABLES LIKE '%hos%'")
        print("Hospital tables:", cur.fetchall())
        
        # Check claim_submission columns
        cur.execute("DESCRIBE claim_submission")
        cs_cols = [r['Field'] for r in cur.fetchall()]
        print("claim_submission columns:", [c for c in cs_cols if 'pat' in c.lower() or 'hos' in c.lower() or 'type' in c.lower()])
        
        # Check office_master columns
        cur.execute("DESCRIBE office_master")
        om_cols = [r['Field'] for r in cur.fetchall()]
        print("office_master columns:", [c for c in om_cols if 'type' in c.lower()])
        
        # Check claim_intimation columns
        cur.execute("DESCRIBE claim_intimation")
        ci_cols = [r['Field'] for r in cur.fetchall()]
        print("claim_intimation columns:", [c for c in ci_cols if 'pat' in c.lower() or 'type' in c.lower() or 'cat' in c.lower()])

