import os
import csv
import datetime
import paramiko
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(os.path.dirname(base_dir), '.env')
data_dir = os.path.join(base_dir, 'new_data')

load_dotenv(env_path)

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

def execute_targeted_extraction():
    print("="*60)
    print("STARTING TWO-STEP TARGETED FORENSIC EXTRACTION")
    print("Pattern 07: High Deduction Line-Item Level Audit")
    print("="*60)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(data_dir, f"new_07_targeted_itemized_deductions_{timestamp}.csv")
    
    try:
        print(f"[{datetime.datetime.now()}] Connecting to SSH ({SSH_HOST})...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        # STEP 1: Find the target IDs (High Deduction Claims)
        print(f"[{datetime.datetime.now()}] STEP 1: Identifying target claim IDs with >50,000 INR deductions...")
        query_a = """
            SELECT cs.CS_INTIMATION_ID 
            FROM claim_submission cs 
            JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
            WHERE ci.CI_ADMISSION_DATE >= '2021-04-01' 
              AND (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) >= 50000;
        """
        
        mysql_cmd_a = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query_a}\" -s -N"
        _, stdout_a, _ = client.exec_command(mysql_cmd_a, timeout=1200)
        
        target_ids = []
        for line in stdout_a:
            line = line.strip()
            if line and line.isdigit():
                target_ids.append(line)
        print(f"[{datetime.datetime.now()}] FOUND {len(target_ids):,} Target High-Fraud Claims!")
        
        if not target_ids:
            print("No targets found. Exiting.")
            return

        # STEP 2: Fetch detailed line-items ONLY for those targeted IDs
        print(f"[{datetime.datetime.now()}] STEP 2: Fetching deep line-item forensic data from 19-Crore row table...")
        
        batch_size = 500
        total_items_saved = 0
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write Header
            writer.writerow([
                'claim_id', 'hospital_id', 'hospital_name', 'city',
                'category_name', 'procedure_name', 'item_claimed_amount', 
                'item_approved_amount', 'item_deducted_amount', 'auditor_remarks'
            ])
            
            for i in range(0, len(target_ids), batch_size):
                batch_ids = target_ids[i:i+batch_size]
                formatted_ids = ",".join([f"'{tid}'" for tid in batch_ids])
                
                query_b = f"""
                    SELECT 
                        hed.HED_INTIMATION_ID,
                        ci.CI_CR_OFFICE_ID,
                        COALESCE(om.OM_OFFICE_NAME, 'Unknown'),
                        COALESCE(crm.CRM_CITY_NAME, 'Unknown'),
                        REPLACE(REPLACE(hed.HED_CAT_DESC, '\\t', ' '), '\\n', ' '),
                        REPLACE(REPLACE(hed.HED_PROC_DESC, '\\t', ' '), '\\n', ' '),
                        hed.HED_CLAIM_AMOUNT,
                        hed.HED_APP_AMOUNT,
                        hed.HED_APP_DEDUCT,
                        REPLACE(REPLACE(hed.HED_APP_REMARKS, '\\t', ' '), '\\n', ' ')
                    FROM hosp_exp_det hed
                    JOIN claim_intimation ci ON hed.HED_INTIMATION_ID = ci.CI_INTIMATION_ID
                    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
                    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
                    WHERE hed.HED_INTIMATION_ID IN ({formatted_ids})
                      AND hed.HED_APP_DEDUCT > 0
                    ORDER BY hed.HED_APP_DEDUCT DESC;
                """
                
                escaped_query_b = query_b.replace('"', '\\"').replace('`', '\\`')
                mysql_cmd_b = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{escaped_query_b}\" -s -N"
                
                _, stdout_b, stderr_b = client.exec_command(mysql_cmd_b, timeout=600)
                
                for line in stdout_b:
                    line = line.strip('\n')
                    if line:
                        row = line.split('\t')
                        writer.writerow(row)
                        total_items_saved += 1
                
                err = stderr_b.read().decode('utf-8')
                if err and 'Warning' not in err:
                    print(f"DB Error in batch: {err}")
                        
                print(f"[{datetime.datetime.now()}] Processed {min(i+batch_size, len(target_ids))}/{len(target_ids)} target claims... (Items extracted: {total_items_saved:,})")

        mb_size = os.path.getsize(filepath) / (1024 * 1024)
        print(f"[{datetime.datetime.now()}] COMPLETED! Saved {total_items_saved:,} forensic line-items to {filepath} ({mb_size:.2f} MB)")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    execute_targeted_extraction()
