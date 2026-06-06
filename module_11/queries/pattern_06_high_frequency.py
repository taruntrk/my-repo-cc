import paramiko
import csv
import datetime
import os
import statistics

# Database credentials
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

# ═══════════════════════════════════════════════════════════════════════
# Pattern 06: High Frequency Claims — Over-Utilization Detection
# ═══════════════════════════════════════════════════════════════════════
# Strategy:
#   Step 1: Get claim counts per beneficiary over 5 years
#   Step 2: Compute median claim count as baseline
#   Step 3: Set threshold = median + 2*IQR (or 3*median, whichever works)
#   Step 4: Flag all beneficiaries above threshold as fraud
#   Step 5: Get detailed data for those flagged beneficiaries
#
# "Service Number" = ex-serviceman's unique military identifier
# "Total Exposure" = sum of all claimed amounts for that beneficiary
# ═══════════════════════════════════════════════════════════════════════

# Step 1: Get distribution of claim counts per beneficiary
distribution_query = """
    SELECT 
        COUNT(DISTINCT ci.CI_INTIMATION_ID) as claim_count
    FROM claim_intimation ci
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID;
"""

# Step 2: Full detail query (threshold injected dynamically)
detail_query_template = """
    SELECT 
        ci.CI_SERVICE_NO as service_number,
        ci.CI_CARD_ID as card_number,
        ci.CI_BENEFICIARY_NAME as beneficiary_name,
        COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
        COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
        COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_exposure,
        ROUND(AVG(cs.CS_NET_CLAIM_AMT), 2) as avg_claim_amount,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
        GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?')) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME
    HAVING COUNT(DISTINCT ci.CI_INTIMATION_ID) >= {threshold}
    ORDER BY total_exposure DESC;
"""


def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        # ── Step 1: Get claim count distribution ──
        print("Step 1: Getting claim count distribution across all beneficiaries...")
        mysql_cmd_dist = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{distribution_query}\" -N"
        
        start_time = datetime.datetime.now()
        stdin, stdout, stderr = client.exec_command(mysql_cmd_dist)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "mysql: [Warning]" not in error:
            print(f"Error in distribution query: {error}")
            return
        
        # Parse claim counts
        claim_counts = []
        for line in output.strip().split('\n'):
            line = line.strip()
            if line:
                try:
                    claim_counts.append(int(line))
                except ValueError:
                    pass
        
        if not claim_counts:
            print("No distribution data found!")
            return
        
        # ── Step 2: Compute statistics ──
        median_val = statistics.median(claim_counts)
        mean_val = statistics.mean(claim_counts)
        sorted_counts = sorted(claim_counts)
        q1 = sorted_counts[len(sorted_counts) // 4]
        q3 = sorted_counts[3 * len(sorted_counts) // 4]
        iqr = q3 - q1
        
        # Threshold: Q3 + 1.5 * IQR (standard outlier detection)
        threshold = int(q3 + 1.5 * iqr)
        # Ensure minimum threshold is sensible (at least 10)
        threshold = max(threshold, 10)
        
        print(f"  Total beneficiaries: {len(claim_counts):,}")
        print(f"  Median claims: {median_val}")
        print(f"  Mean claims: {mean_val:.2f}")
        print(f"  Q1: {q1}, Q3: {q3}, IQR: {iqr}")
        print(f"  Threshold (Q3 + 1.5*IQR): {threshold}")
        print(f"  Beneficiaries above threshold: {sum(1 for c in claim_counts if c >= threshold):,}")
        
        # ── Step 3: Get detailed data above threshold ──
        detail_query = detail_query_template.format(threshold=threshold)
        print(f"\nStep 2: Fetching detailed data for beneficiaries with {threshold}+ claims...")
        
        mysql_cmd_detail = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{detail_query.replace('\"', '\\\"')}\" | tr '\t' ','"
        
        stdin2, stdout2, stderr2 = client.exec_command(mysql_cmd_detail)
        
        output2 = stdout2.read().decode('utf-8')
        error2 = stderr2.read().decode('utf-8')
        
        if error2 and "mysql: [Warning]" not in error2:
            print(f"Error in detail query: {error2}")
            return
        
        lines = [line for line in output2.split('\n') if line.strip()]
        
        if len(lines) > 1:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            filename = os.path.join(data_dir, f'08_High_Frequency_Claims_{timestamp}.csv')
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
            
            # Also save the threshold info
            meta_filename = os.path.join(data_dir, f'08_High_Frequency_Threshold_{timestamp}.txt')
            with open(meta_filename, 'w') as f:
                f.write(f"Analysis Date: {datetime.datetime.now().isoformat()}\n")
                f.write(f"Total Beneficiaries Analyzed: {len(claim_counts):,}\n")
                f.write(f"Median Claims per Beneficiary: {median_val}\n")
                f.write(f"Mean Claims per Beneficiary: {mean_val:.2f}\n")
                f.write(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}\n")
                f.write(f"Threshold Used (Q3 + 1.5*IQR): {threshold}\n")
                f.write(f"Flagged Beneficiaries: {len(lines) - 1}\n")
                    
            end_time = datetime.datetime.now()
            print(f"\nQuery completed in {end_time - start_time}")
            print(f"Saved {len(lines) - 1} flagged beneficiaries to {filename}")
            print(f"Threshold metadata saved to {meta_filename}")
        else:
            print("No data found above threshold.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
