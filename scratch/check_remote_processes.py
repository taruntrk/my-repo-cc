import paramiko, os
from dotenv import load_dotenv

# Load env variables
dotenv_path = '/home/tarun/Downloads/CC/echs_analysis/.env'
load_dotenv(dotenv_path)

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
    
    cmd = "ps -u echs_aman -f"
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    
    print("--- Remote Processes for echs_aman ---")
    print(out.strip())
            
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
