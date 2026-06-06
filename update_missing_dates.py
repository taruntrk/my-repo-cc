import json
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

def run_mysql(client, sql):
    cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -N'
    stdin_c, stdout, stderr = client.exec_command(cmd)
    stdin_c.write(sql.encode())
    stdin_c.channel.shutdown_write()
    out = stdout.read().decode(errors='replace').strip()
    return out

with open('/home/aman/Desktop/echs_analysis/echs_db_metadata.json', 'r') as f:
    data = json.load(f)

DATE_TYPES = {'date', 'datetime', 'timestamp'}

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)

updated = 0
for t in data:
    if not t.get('earliest_date'):
        cols = t.get('columns', [])
        d_cols = [c for c in cols if c['dtype'].lower() in DATE_TYPES]
        if d_cols:
            best = None
            for c in d_cols:
                n = c['name'].lower()
                if 'cr_date' in n or 'created' in n or 'int_date' in n: best = c['name']; break
            if not best:
                for c in d_cols:
                    if 'date' in c['name'].lower(): best = c['name']; break
            if not best: best = d_cols[0]['name']
            
            print(f"Fetching dates for {t['table']} using {best}...", end=' ', flush=True)
            sql = f"SELECT CAST(MIN(`{best}`) AS CHAR), CAST(MAX(`{best}`) AS CHAR) FROM `{t['table']}`;"
            try:
                res = run_mysql(client, sql)
                parts = res.split('\t')
                if len(parts) == 2:
                    t['earliest_date'] = parts[0].strip() if parts[0].strip() not in ('NULL','') else None
                    t['latest_date'] = parts[1].strip() if parts[1].strip() not in ('NULL','') else None
                    print(f"Got {t['earliest_date']} to {t['latest_date']}")
                    updated += 1
                else:
                    print(f"Failed parsing: {res}")
            except Exception as e:
                print(f"Error: {e}")

client.close()

if updated > 0:
    with open('/home/aman/Desktop/echs_analysis/echs_db_metadata.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {updated} tables in JSON.")
else:
    print("No updates needed.")
