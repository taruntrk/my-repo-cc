import paramiko


import os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

def run_query(query):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
        mysql_cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -e "{query}" | tr "\\t" "|" '
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=300)
        return stdout.read().decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return ""
    finally:
        client.close()

def main():
    print("--- 1. Unique Audit Stages ---")
    out = run_query("SELECT AS_AUD_STAGE, COUNT(*) as count FROM audit_status GROUP BY AS_AUD_STAGE ORDER BY count DESC;")
    print(out)
    
    print("\n--- 2. Unique Audit Statuses ---")
    out = run_query("SELECT AS_AUD_STATUS, COUNT(*) as count FROM audit_status GROUP BY AS_AUD_STATUS ORDER BY count DESC;")
    print(out)
    
    print("\n--- 3. Time difference between stages (Average days) ---")
    query_time = """
    SELECT 
        AVG(DATEDIFF(AS_HOS_IN_DATE, AS_SAO_IN_DATE)) as SAO_to_HOS,
        AVG(DATEDIFF(AS_BPA_IN_DATE, AS_SAO_IN_DATE)) as SAO_to_BPA,
        AVG(DATEDIFF(AS_RC_IN_DATE, AS_HOS_IN_DATE)) as HOS_to_RC,
        AVG(DATEDIFF(AS_CFA_IN_DATE, AS_BPA_IN_DATE)) as BPA_to_CFA
    FROM audit_status
    LIMIT 10000;
    """
    out = run_query(query_time)
    print(out)
    
    print("\n--- 4. Query Count distribution ---")
    out = run_query("SELECT AS_QUERIES_NOS, COUNT(*) as count FROM audit_status GROUP BY AS_QUERIES_NOS ORDER BY count DESC LIMIT 5;")
    print(out)

if __name__ == "__main__":
    main()
