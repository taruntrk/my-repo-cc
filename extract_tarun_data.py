import csv
import io
import os
import subprocess
import datetime

# Database credentials (connecting via local tunnel port 3307)
DB_HOST = '127.0.0.1'
DB_PORT = '3307'
DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

OUTPUT_DIR = '/home/tarun/Downloads/CC/echs_analysis/data-tarun'
os.makedirs(OUTPUT_DIR, exist_ok=True)

queries = {
    "Point01_Annual_Leakage_Trend": """
        SELECT 
            SS_FY_YEAR AS fiscal_year,
            SUM(SS_CLAIM_CNT) AS total_claims,
            SUM(SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(SS_APPR_AMT) AS total_approved_amount,
            SUM(SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(SS_DED_AMT) * 100.0 / SUM(SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat
        WHERE SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY SS_FY_YEAR
        ORDER BY SS_FY_YEAR;
    """,
    "Point02_HospType_NABH_Leakage": """
        SELECT 
            COALESCE(om.OM_HOSP_TYPE, 'Unknown') AS hosp_type,
            COALESCE(om.OM_NABH, 'N') AS nabh_status,
            COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY om.OM_HOSP_TYPE, om.OM_NABH
        ORDER BY deduction_pct DESC;
    """,
    "Point03_Command_Regional_Leakage": """
        SELECT 
            ss.SS_REGION_ID AS region_id,
            CASE ss.SS_REGION_ID
                WHEN '1' THEN 'NEW DELHI'
                WHEN '2' THEN 'MUMBAI'
                WHEN '3' THEN 'KOLKATA'
                WHEN '4' THEN 'BANGALORE'
                WHEN '5' THEN 'HYDERABAD'
                WHEN '6' THEN 'CHENNAI'
                WHEN '7' THEN 'DEHRADUN'
                WHEN '8' THEN 'JAIPUR'
                WHEN '9' THEN 'PUNE'
                WHEN '10' THEN 'CHANDIGARH'
                WHEN '11' THEN 'ALLAHABAD'
                WHEN '12' THEN 'PATNA'
                WHEN '13' THEN 'AHMEDABAD'
                ELSE CONCAT('Region ', ss.SS_REGION_ID)
            END AS region_name,
            COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_REGION_ID
        ORDER BY total_deducted_amount DESC;
    """,
    "Point04_PatientType_Leakage": """
        SELECT 
            ss.SS_PAT_TYPE_ID AS patient_type_id,
            pt.PT_TYPE_DESC AS patient_type_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN patient_type pt ON ss.SS_PAT_TYPE_ID = pt.PT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_PAT_TYPE_ID, pt.PT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """,
    "Point05_ReferralType_Leakage": """
        SELECT 
            ss.SS_REF_TYPE_ID AS referral_type_id,
            rt.RT_TYPE_DESC AS referral_type_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN referal_type rt ON ss.SS_REF_TYPE_ID = rt.RT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_REF_TYPE_ID, rt.RT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """,
    "Point06_RoomCategory_Leakage": """
        SELECT 
            ss.SS_ROOM_CATG AS room_category_id,
            rm.RT_TYPE_DESC AS room_category_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN room_type rm ON ss.SS_ROOM_CATG = rm.RT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_ROOM_CATG, rm.RT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """,
    "Point07_Hospital_Leakage_Summary": """
        SELECT 
            ss.SS_OFFICE_ID AS hospital_id,
            om.OM_OFFICE_NAME AS hospital_name,
            COALESCE(om.OM_HOSP_TYPE, '') AS hosp_type,
            COALESCE(om.OM_NABH, 'N') AS nabh_status,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_NABH
        ORDER BY total_deducted_amount DESC;
    """,
    "Point08_Hospital_Referral_Leakage": """
        SELECT 
            ss.SS_OFFICE_ID AS hospital_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ss.SS_REF_TYPE_ID AS referral_type_id,
            rt.RT_TYPE_DESC AS referral_type_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN referal_type rt ON ss.SS_REF_TYPE_ID = rt.RT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, ss.SS_REF_TYPE_ID, rt.RT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """,
    "Point09_Hospital_Room_Category_Leakage": """
        SELECT 
            ss.SS_OFFICE_ID AS hospital_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ss.SS_ROOM_CATG AS room_category_id,
            rm.RT_TYPE_DESC AS room_category_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN room_type rm ON ss.SS_ROOM_CATG = rm.RT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, ss.SS_ROOM_CATG, rm.RT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """,
    "Point10_Gender_Relation_Leakage": """
        SELECT 
            ss.SS_GENDER AS gender,
            ss.SS_RELATION_ID AS relation_id,
            rm.RM_RELATION_NAME AS relation_name,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_NAME
        ORDER BY total_deducted_amount DESC;
    """,
    "Point11_Hospital_PatientType_Leakage": """
        SELECT 
            ss.SS_OFFICE_ID AS hospital_id,
            om.OM_OFFICE_NAME AS hospital_name,
            ss.SS_PAT_TYPE_ID AS patient_type_id,
            pt.PT_TYPE_DESC AS patient_type_desc,
            SUM(ss.SS_CLAIM_CNT) AS total_claims,
            SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
            SUM(ss.SS_APPR_AMT) AS total_approved_amount,
            SUM(ss.SS_DED_AMT) AS total_deducted_amount,
            ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
        FROM settlement_stat ss
        LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN patient_type pt ON ss.SS_PAT_TYPE_ID = pt.PT_TYPE_ID
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2026
        GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, ss.SS_PAT_TYPE_ID, pt.PT_TYPE_DESC
        ORDER BY total_deducted_amount DESC;
    """
}

def run_extraction():
    print(f"[{datetime.datetime.now()}] Starting data extraction locally via port {DB_PORT}...")
    
    for name, query in queries.items():
        print(f"[{datetime.datetime.now()}] Executing {name}...")
        
        # Build local mysql call using subprocess
        cmd = [
            'mysql',
            '-h', DB_HOST,
            '-P', DB_PORT,
            '-u', DB_USER,
            f'-p{DB_PASS}',
            DB_NAME,
            '-B',
            '-e', query
        ]
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            out = res.stdout
            
            if out:
                csv_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
                lines = out.strip().split('\n')
                
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for line in lines:
                        writer.writerow(line.split('\t'))
                
                print(f"  Saved {len(lines) - 1} records to {csv_path}")
            else:
                print("  No output received.")
        except subprocess.CalledProcessError as e:
            print(f"  Error running query: {e.stderr}")
        except Exception as e:
            print(f"  Unexpected error: {e}")
            
    print(f"\n[{datetime.datetime.now()}] All tasks completed.")

if __name__ == "__main__":
    run_extraction()
