import paramiko
import csv
import datetime
import os

# Database credentials
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_aman'
SSH_PASS = 'aman@2026'

DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

# ═══════════════════════════════════════════════════════════════════════
# Pattern 04: Mobile Number Rings
# ═══════════════════════════════════════════════════════════════════════
# A "Mobile Number Ring" is when a single mobile phone number is linked
# to 5 or more distinct ECHS cards belonging to different service numbers.
# In a legitimate scenario, one mobile number might be shared within a
# family (2-3 cards max). When 5+ unrelated cards share one mobile, it
# indicates a coordinated fraud ring — a single agent is filing claims
# for multiple identities.
#
# "Service Number" = the ex-serviceman's unique military identifier.
# "Card" = the ECHS health card issued to a beneficiary (dependent/veteran).
# "Total Exposure" = sum of all claimed amounts across all cards on that mobile.
#
# We split results into two CSVs:
#   - Legitimate mobile numbers (10+ digits, starts with valid prefix)
#   - Dummy/invalid mobile numbers (all zeros, repeating digits, etc.)
# ═══════════════════════════════════════════════════════════════════════

query = """
    SELECT 
        ci.CI_MOBILE as mobile_number,
        COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
        COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
        COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
        COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
        COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_exposure,
        GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_numbers,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
        GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
        GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?')) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations
    FROM claim_intimation ci
    LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
    LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
    WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        AND ci.CI_MOBILE IS NOT NULL
        AND ci.CI_MOBILE != ''
        AND LENGTH(ci.CI_MOBILE) >= 10
    GROUP BY ci.CI_MOBILE
    HAVING COUNT(DISTINCT ci.CI_CARD_ID) >= 5
    ORDER BY total_exposure DESC;
"""

def is_dummy_number(num):
    """Check if a mobile number looks dummy/invalid."""
    num = str(num).strip()
    # All same digits (0000000000, 1111111111, etc.)
    if len(set(num)) <= 2:
        return True
    # All zeros
    if num.replace('0', '') == '':
        return True
    # Sequential (1234567890)
    if num in ('1234567890', '0123456789', '9876543210'):
        return True
    # Starts with 0000 or 1111 etc.
    if len(num) >= 10 and num[:4] == num[0] * 4:
        return True
    # Known dummy patterns
    dummy_patterns = ['9999999999', '8888888888', '7777777777', '1111111111', '0000000000']
    if num in dummy_patterns:
        return True
    return False


def run_query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
        
        mysql_cmd = f"mysql -u {DB_USER} -p'{DB_PASS}' {DB_NAME} -e \"{query.replace('\"', '\\\"')}\" | tr '\t' ','"
        
        print("Executing pattern 04 query (Mobile Number Rings)...")
        start_time = datetime.datetime.now()
        stdin, stdout, stderr = client.exec_command(mysql_cmd)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "mysql: [Warning]" not in error:
            print(f"Error executing query: {error}")
            return
            
        lines = [line for line in output.split('\n') if line.strip()]
        
        if len(lines) > 1:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            header = lines[0]
            
            # Split into real and dummy
            real_lines = [header]
            dummy_lines = [header]
            
            for line in lines[1:]:
                mobile = line.split(',')[0].strip()
                if is_dummy_number(mobile):
                    dummy_lines.append(line)
                else:
                    real_lines.append(line)
            
            # Save real mobile rings
            filename_real = os.path.join(data_dir, f'04_Mobile_Number_Rings_{timestamp}.csv')
            with open(filename_real, 'w', encoding='utf-8') as f:
                for line in real_lines:
                    f.write(line + '\n')
            
            # Save dummy numbers separately
            filename_dummy = os.path.join(data_dir, f'04_Mobile_Dummy_Numbers_{timestamp}.csv')
            with open(filename_dummy, 'w', encoding='utf-8') as f:
                for line in dummy_lines:
                    f.write(line + '\n')
                    
            end_time = datetime.datetime.now()
            print(f"Query completed in {end_time - start_time}")
            print(f"Total records: {len(lines) - 1}")
            print(f"  Real mobile rings: {len(real_lines) - 1} -> {filename_real}")
            print(f"  Dummy/invalid numbers: {len(dummy_lines) - 1} -> {filename_dummy}")
        else:
            print("No data found for this query.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_query()
