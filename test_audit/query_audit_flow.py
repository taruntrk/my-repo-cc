import paramiko
import pandas as pd
import json

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
        # Using -e flag to run query and export to TSV which is easy to parse
        mysql_cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -e "{query}" | tr "\\t" "|" '
        stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=300)
        out = stdout.read().decode('utf-8')
        return out
    except Exception as e:
        print(f"Error: {e}")
        return ""
    finally:
        client.close()

def main():
    # Let's get a sample of 1000 claims that have at least some audit dates
    query_audit_status = """
    SELECT 
        AS_HOS_IN_DATE,
        AS_BPA_IN_DATE,
        AS_RC_IN_DATE,
        AS_SAO_IN_DATE,
        AS_CORG_IN_DATE,
        AS_CFA_IN_DATE
    FROM audit_status 
    WHERE AS_HOS_IN_DATE IS NOT NULL OR AS_BPA_IN_DATE IS NOT NULL 
    LIMIT 5000;
    """
    print("Running query on audit_status...")
    out_as = run_query(query_audit_status)
    with open('test_audit/audit_status_sample.txt', 'w') as f:
        f.write(out_as)
        
    query_claim_int = """
    SELECT 
        CI_CR_DATE,
        CI_INT_DATE,
        CI_AUDIT_DATE_1,
        CI_AUDIT_DATE_2,
        CI_AUDIT_DATE_3,
        CI_REPLY_DATE
    FROM claim_intimation 
    WHERE CI_AUDIT_DATE_1 IS NOT NULL
    LIMIT 5000;
    """
    print("Running query on claim_intimation...")
    out_ci = run_query(query_claim_int)
    with open('test_audit/claim_intimation_sample.txt', 'w') as f:
        f.write(out_ci)

    print("Queries finished.")

if __name__ == "__main__":
    main()
