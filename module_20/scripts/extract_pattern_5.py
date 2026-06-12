import os
import csv
import sys
import glob
import collections
from datetime import datetime

# SSH Credentials
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_akash'
SSH_PASS = 'Akash@2026'
DB_USER  = 'akash'
DB_PASS  = 'Akash@2026'
DB_NAME  = 'ECHS'

# Folder paths
BASE_DIR = '/home/tarun/Downloads/CC/echs_analysis/module_20'
DATA2_DIR = os.path.join(BASE_DIR, 'data_2')
PATTERN_DIR = os.path.join(DATA2_DIR, 'pattern_5_temporal_surge')

# Sub-pattern folders
SUB_5A_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_5a_weekend_emergency_surge')
SUB_5B_DIR = os.path.join(PATTERN_DIR, 'sub_pattern_5b_monthend_spike')

# Ensure directories exist
os.makedirs(SUB_5A_DIR, exist_ok=True)
os.makedirs(SUB_5B_DIR, exist_ok=True)

# Queries for Pattern 5
queries = {
    "sub_pattern_5a_weekend_emergency_surge": """
        SELECT
            ci.CI_INTIMATION_ID AS claim_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ci.CI_PATIENT_NAME AS patient_name,
            DATE(ci.CI_ADMISSION_DATE) AS admission_date,
            DAYNAME(ci.CI_ADMISSION_DATE) AS day_of_week,
            ci.CI_ADM_AILMENT AS ailment,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) AS claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) AS approved_amount
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE DAYOFWEEK(ci.CI_ADMISSION_DATE) IN (1, 7)
          AND ci.CI_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
        ORDER BY ci.CI_ADMISSION_DATE DESC
        LIMIT 50000;
    """,

    "sub_pattern_5b_monthend_spike": """
        SELECT
            om.OM_OFFICE_NAME AS hospital_name,
            DATE_FORMAT(ci.CI_ADMISSION_DATE, '%Y-%m') AS month_year,
            ROUND(COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) <= 27 THEN ci.CI_INTIMATION_ID END) / 27, 2) AS normal_days_avg_claims,
            ROUND(COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) >= 28 THEN ci.CI_INTIMATION_ID END) / 3.25, 2) AS monthend_days_avg_claims,
            ROUND(
                (COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) >= 28 THEN ci.CI_INTIMATION_ID END) / 3.25) / 
                NULLIF(COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) <= 27 THEN ci.CI_INTIMATION_ID END) / 27, 0),
                2
            ) AS spike_ratio,
            ROUND(
                (
                    COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) >= 28 THEN ci.CI_INTIMATION_ID END) - 
                    (COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) <= 27 THEN ci.CI_INTIMATION_ID END) / 27) * 3.25
                ) * AVG(COALESCE(cs.CS_UTI_APP_AMT, 0)) / 100000,
                2
            ) AS extra_monthend_approved_lakh
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ci.CI_ADMISSION_DATE BETWEEN '2021-01-01' AND '2026-05-31'
        GROUP BY om.OM_OFFICE_NAME, DATE_FORMAT(ci.CI_ADMISSION_DATE, '%Y-%m')
        HAVING normal_days_avg_claims > 0 AND spike_ratio > 1.5 AND COUNT(CASE WHEN DAY(ci.CI_ADMISSION_DATE) >= 28 THEN ci.CI_INTIMATION_ID END) >= 5
        ORDER BY extra_monthend_approved_lakh DESC;
    """
}

def run_db_extraction():
    """Tries to run query via SSH database client."""
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to SSH {SSH_HOST}...")
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=15)
    print("✓ SSH connected successfully.")
    
    outputs = {}
    for name, query in queries.items():
        print(f"Executing query: {name}...")
        cmd = f'mysql -u{DB_USER} -p{DB_PASS} {DB_NAME} -B'
        stdin_c, stdout, stderr = client.exec_command(cmd, timeout=300)
        stdin_c.write(query.encode('utf-8'))
        stdin_c.channel.shutdown_write()
        out = stdout.read().decode('utf-8', errors='replace')
        if out and out.strip():
            outputs[name] = out
            print(f"  -> Retrieved database results for {name}")
        else:
            print(f"  -> No database results for {name}")
    client.close()
    return outputs

def run_local_fallback():
    """Falls back to local file processing when database is network-unreachable."""
    print("\n⚠️ Database unreachable. Falling back to local file processing...")
    
    claims_files = glob.glob(os.path.join(BASE_DIR, 'new_data/new_05b_regional_all_claims_*.csv'))
    if not claims_files:
        print("❌ Error: Could not find new_05b_regional_all_claims_*.csv in new_data/")
        sys.exit(1)
        
    main_csv = claims_files[0]
    print(f"Using local claims file: {main_csv}")
    
    # --- SUB-PATTERN 5A: WEEKEND EMERGENCY SURGE ---
    print("\nProcessing Sub-Pattern 5A: Weekend Emergency Surge...")
    weekend_cases = []
    
    # Track metrics for 5B aggregation
    # Map (hospital_name, month_year) -> {'normal': [], 'monthend': [], 'approved_amounts': []}
    monthly_stats = collections.defaultdict(lambda: {'normal_count': 0, 'monthend_count': 0, 'approved_sum': 0.0, 'claims_count': 0})
    
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    with open(main_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 28:
                continue
            
            hosp_name = row[4].strip()
            adm_date_str = row[19][:10]
            claimed = float(row[25] or 0)
            approved = float(row[26] or 0)
            
            try:
                dt = datetime.strptime(adm_date_str, '%Y-%m-%d')
                weekday = dt.weekday() # 0 = Monday, 5 = Sat, 6 = Sun
                day_name = day_names[weekday]
                month_year = dt.strftime('%Y-%m')
                day_of_month = dt.day
                
                # Check for Weekend Emergency Surge (Sat / Sun)
                if weekday in [5, 6]:
                    weekend_cases.append([
                        row[9], hosp_name, row[15], adm_date_str,
                        day_name, row[22], claimed, approved
                    ])
                    
                # Track for 5B Month-End Spike
                if day_of_month <= 27:
                    monthly_stats[(hosp_name, month_year)]['normal_count'] += 1
                else:
                    monthly_stats[(hosp_name, month_year)]['monthend_count'] += 1
                
                monthly_stats[(hosp_name, month_year)]['approved_sum'] += approved
                monthly_stats[(hosp_name, month_year)]['claims_count'] += 1
                
            except Exception:
                continue
                
    # Sort weekend cases by date descending
    weekend_cases.sort(key=lambda x: x[3], reverse=True)
    
    csv_5a = os.path.join(SUB_5A_DIR, 'pat5a_weekend_emergency_surge.csv')
    with open(csv_5a, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'claim_id', 'hospital_name', 'patient_name', 'admission_date',
            'day_of_week', 'ailment', 'claimed_amount', 'approved_amount'
        ])
        writer.writerows(weekend_cases)
    print(f"✓ Saved {len(weekend_cases)} rows to {csv_5a}")
    
    # --- SUB-PATTERN 5B: MONTH-END SPIKE ANALYSIS ---
    print("\nProcessing Sub-Pattern 5B: Month-End Spike Analysis...")
    monthend_spike_cases = []
    
    for (hosp_name, month_year), stats in monthly_stats.items():
        normal_count = stats['normal_count']
        monthend_count = stats['monthend_count']
        approved_sum = stats['approved_sum']
        claims_count = stats['claims_count']
        
        normal_avg = round(normal_count / 27.0, 2)
        monthend_avg = round(monthend_count / 3.25, 2) # average month end length is 3.25 days
        
        if normal_avg > 0:
            spike_ratio = round(monthend_avg / normal_avg, 2)
        else:
            spike_ratio = 0.0
            
        # Filter rules: normal_days_avg_claims > 0 and spike_ratio > 1.5 and monthend_count >= 5
        if normal_avg > 0 and spike_ratio > 1.5 and monthend_count >= 5:
            avg_approved = approved_sum / claims_count if claims_count > 0 else 0
            excess_claims = monthend_count - (normal_avg * 3.25)
            extra_approved_l = round((excess_claims * avg_approved) / 100000.0, 2)
            
            # If extra leakage is negative, cap at 0
            if extra_approved_l < 0:
                extra_approved_l = 0.0
                
            monthend_spike_cases.append([
                hosp_name, month_year, normal_avg, monthend_avg,
                spike_ratio, extra_approved_l
            ])
            
    # Sort spike cases by extra leakage descending
    monthend_spike_cases.sort(key=lambda x: x[5], reverse=True)
    
    csv_5b = os.path.join(SUB_5B_DIR, 'pat5b_monthend_spike_analysis.csv')
    with open(csv_5b, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'hospital_name', 'month_year', 'normal_days_avg_claims', 'monthend_days_avg_claims',
            'spike_ratio', 'extra_monthend_approved_lakh'
        ])
        writer.writerows(monthend_spike_cases)
    print(f"✓ Saved {len(monthend_spike_cases)} rows to {csv_5b}")

def main():
    print("=" * 80)
    print("ECHS MODULE 20 - PATTERN 5 DATA EXTRACTION SYSTEM")
    print("=" * 80)
    
    try:
        # Try database connection first
        results = run_db_extraction()
        
        # Save database results to CSVs
        for name, data in results.items():
            lines = data.strip().splitlines()
            if name == "sub_pattern_5a_weekend_emergency_surge":
                path = os.path.join(SUB_5A_DIR, 'pat5a_weekend_emergency_surge.csv')
            else:
                path = os.path.join(SUB_5B_DIR, 'pat5b_monthend_spike_analysis.csv')
                
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for line in lines:
                    writer.writerow(line.split('\t'))
            print(f"✓ Saved database extraction results to: {path}")
            
    except Exception as e:
        # If database connection fails, run local parsing fallback
        print(f"Database extraction failed: {e}")
        run_local_fallback()
        
    print("\n" + "=" * 80)
    print("PATTERN 5 EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == '__main__':
    main()
