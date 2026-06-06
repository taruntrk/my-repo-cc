import os
import glob
import re

files = glob.glob('**/*.py', recursive=True)

REPLACEMENT = """
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
"""

for file_path in files:
    if file_path == 'refactor_env.py' or 'venv' in file_path: continue
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
        
    if 'aman@2026' in content:
        # Pattern to match the entire block if they are close together
        block_pattern = r"SSH_HOST\s*=\s*['\"]samar\.iitk\.ac\.in['\"].*?DB_NAME\s*=\s*['\"]ECHS['\"]"
        
        if re.search(block_pattern, content, flags=re.DOTALL):
            content = re.sub(block_pattern, REPLACEMENT.strip(), content, flags=re.DOTALL)
        else:
            # Fallback line-by-line replace
            content = re.sub(r"SSH_HOST\s*=\s*['\"]samar\.iitk\.ac\.in['\"]", "SSH_HOST = os.getenv('SSH_HOST')", content)
            content = re.sub(r"SSH_PORT\s*=\s*22", "SSH_PORT = int(os.getenv('SSH_PORT', 22))", content)
            content = re.sub(r"SSH_USER\s*=\s*['\"]echs_aman['\"]", "SSH_USER = os.getenv('SSH_USER')", content)
            content = re.sub(r"SSH_PASS\s*=\s*['\"]aman@2026['\"]", "SSH_PASS = os.getenv('SSH_PASS')", content)
            content = re.sub(r"DB_USER\s*=\s*['\"]aman['\"]", "DB_USER = os.getenv('DB_USER')", content)
            content = re.sub(r"DB_PASS\s*=\s*['\"]aman@2026['\"]", "DB_PASS = os.getenv('DB_PASS')", content)
            content = re.sub(r"DB_NAME\s*=\s*['\"]ECHS['\"]", "DB_NAME = os.getenv('DB_NAME')", content)
            
            if 'from dotenv import load_dotenv' not in content:
                content = "import os\nfrom dotenv import load_dotenv\nload_dotenv()\n\n" + content
                
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
