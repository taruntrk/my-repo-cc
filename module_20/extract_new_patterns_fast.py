import os
import pymysql
import csv
import datetime

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'new_data')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Connecting to database on 127.0.0.1:3307...")
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3307,
        user='aman',
        password='aman@2026',
        database='ECHS',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        with connection.cursor() as cursor:
            # 1. Card Sharing (Pattern 6)
            print("\nExtracting Pattern 6 (Individual Card-Sharing) - Fast...")
            query_card = """
                SELECT 
                    ci1.CI_CARD_ID AS card_id,
                    ci1.CI_BENEFICIARY_NAME AS beneficiary_name,
                    DATE(ci1.CI_ADMISSION_DATE) AS admission_date,
                    om1.OM_OFFICE_NAME AS hospital_1,
                    om2.OM_OFFICE_NAME AS hospital_2,
                    cs1.CS_UTI_APP_AMT AS approved_amt_1,
                    cs2.CS_UTI_APP_AMT AS approved_amt_2,
                    (cs1.CS_UTI_APP_AMT + cs2.CS_UTI_APP_AMT) AS total_approved
                FROM claim_intimation ci1
                JOIN claim_intimation ci2 ON ci1.CI_CARD_ID = ci2.CI_CARD_ID 
                  AND ci1.CI_INTIMATION_ID < ci2.CI_INTIMATION_ID
                  AND DATE(ci1.CI_ADMISSION_DATE) = DATE(ci2.CI_ADMISSION_DATE)
                  AND ci1.CI_CR_OFFICE_ID <> ci2.CI_CR_OFFICE_ID
                JOIN claim_submission cs1 ON ci1.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
                JOIN claim_submission cs2 ON ci2.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
                LEFT JOIN office_master om1 ON ci1.CI_CR_OFFICE_ID = om1.OM_OFFICE_ID
                LEFT JOIN office_master om2 ON ci2.CI_CR_OFFICE_ID = om2.OM_OFFICE_ID
                WHERE ci1.CI_ADMISSION_DATE BETWEEN '2025-06-01' AND '2025-09-30'
                  AND ci1.CI_CARD_ID IS NOT NULL AND ci1.CI_CARD_ID != '' AND ci1.CI_CARD_ID != '0' AND ci1.CI_CARD_ID NOT LIKE '0000%'
                  AND cs1.CS_UTI_APP_AMT >= 10000 
                  AND cs2.CS_UTI_APP_AMT >= 10000
                ORDER BY total_approved DESC
                LIMIT 50;
            """
            cursor.execute(query_card)
            res_card = cursor.fetchall()
            card_file = os.path.join(output_dir, f"new_13_card_sharing_{ts}.csv")
            with open(card_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['card_id', 'beneficiary_name', 'admission_date', 'hospital_1', 'hospital_2', 'approved_amt_1', 'approved_amt_2', 'total_approved'])
                for r in res_card:
                    writer.writerow([r['card_id'], r['beneficiary_name'], r['admission_date'], r['hospital_1'], r['hospital_2'], r['approved_amt_1'], r['approved_amt_2'], r['total_approved']])
            print(f"  ✓ Saved {len(res_card)} records to {os.path.basename(card_file)}")
            
            # 2. Family Sharing (Pattern 7)
            print("\nExtracting Pattern 7 (Family Simultaneous Admissions) - Fast...")
            query_family = """
                SELECT 
                    ci1.CI_SERVICE_NO AS service_no,
                    ci1.CI_BENEFICIARY_NAME AS member_1,
                    rm1.RM_RELATION_NAME AS relation_1,
                    ci2.CI_BENEFICIARY_NAME AS member_2,
                    rm2.RM_RELATION_NAME AS relation_2,
                    DATE(ci1.CI_ADMISSION_DATE) AS admission_date,
                    om1.OM_OFFICE_NAME AS hospital_1,
                    om2.OM_OFFICE_NAME AS hospital_2,
                    cs1.CS_UTI_APP_AMT AS approved_amt_1,
                    cs2.CS_UTI_APP_AMT AS approved_amt_2,
                    (cs1.CS_UTI_APP_AMT + cs2.CS_UTI_APP_AMT) AS total_approved
                FROM claim_intimation ci1
                JOIN claim_intimation ci2 ON ci1.CI_SERVICE_NO = ci2.CI_SERVICE_NO 
                  AND ci1.CI_CARD_ID <> ci2.CI_CARD_ID
                  AND ci1.CI_INTIMATION_ID < ci2.CI_INTIMATION_ID
                  AND DATE(ci1.CI_ADMISSION_DATE) = DATE(ci2.CI_ADMISSION_DATE)
                  AND ci1.CI_CR_OFFICE_ID <> ci2.CI_CR_OFFICE_ID
                JOIN claim_submission cs1 ON ci1.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
                JOIN claim_submission cs2 ON ci2.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
                LEFT JOIN relation_master rm1 ON ci1.CI_RELATION_ID = rm1.RM_RELATION_ID
                LEFT JOIN relation_master rm2 ON ci2.CI_RELATION_ID = rm2.RM_RELATION_ID
                LEFT JOIN office_master om1 ON ci1.CI_CR_OFFICE_ID = om1.OM_OFFICE_ID
                LEFT JOIN office_master om2 ON ci2.CI_CR_OFFICE_ID = om2.OM_OFFICE_ID
                WHERE ci1.CI_ADMISSION_DATE BETWEEN '2025-06-01' AND '2025-09-30'
                  AND ci1.CI_SERVICE_NO IS NOT NULL AND ci1.CI_SERVICE_NO != '' AND ci1.CI_SERVICE_NO != '0' AND ci1.CI_SERVICE_NO NOT LIKE '0000%'
                  AND cs1.CS_UTI_APP_AMT >= 10000 
                  AND cs2.CS_UTI_APP_AMT >= 10000
                ORDER BY total_approved DESC
                LIMIT 50;
            """
            cursor.execute(query_family)
            res_family = cursor.fetchall()
            family_file = os.path.join(output_dir, f"new_14_family_sharing_{ts}.csv")
            with open(family_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['service_no', 'member_1', 'relation_1', 'member_2', 'relation_2', 'admission_date', 'hospital_1', 'hospital_2', 'approved_amt_1', 'approved_amt_2', 'total_approved'])
                for r in res_family:
                    writer.writerow([r['service_no'], r['member_1'], r['relation_1'], r['member_2'], r['relation_2'], r['admission_date'], r['hospital_1'], r['hospital_2'], r['approved_amt_1'], r['approved_amt_2'], r['total_approved']])
            print(f"  ✓ Saved {len(res_family)} records to {os.path.basename(family_file)}")

            # 3. Demographic Mismatch (Pattern 8)
            print("\nExtracting Pattern 8 (Demographic Mismatch) - Fast...")
            query_mismatch = """
                SELECT 
                    ci.CI_SEX AS gender,
                    rm.RM_RELATION_NAME AS relationship,
                    om.OM_OFFICE_NAME AS hospital_name,
                    om.OM_OFFICE_CITY AS city,
                    ci.CI_BENEFICIARY_NAME AS beneficiary_name,
                    ci.CI_PATIENT_NAME AS patient_name,
                    DATE(ci.CI_ADMISSION_DATE) AS admission_date,
                    cs.CS_NET_CLAIM_AMT AS claimed_amount,
                    cs.CS_UTI_APP_AMT AS approved_amount,
                    (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) AS deducted_amount
                FROM claim_submission cs
                JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
                LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
                LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
                WHERE cs.CS_CFA_DATE BETWEEN '2025-06-01' AND '2025-09-30'
                  AND (
                    (ci.CI_SEX = 'M' AND rm.RM_RELATION_NAME IN ('Wife', 'Mother', 'Daughter', 'Sister'))
                    OR (ci.CI_SEX = 'F' AND rm.RM_RELATION_NAME IN ('Husband', 'Father', 'Son', 'Brother'))
                  )
                  AND cs.CS_UTI_APP_AMT >= 20000
                ORDER BY cs.CS_UTI_APP_AMT DESC
                LIMIT 50;
            """
            cursor.execute(query_mismatch)
            res_mismatch = cursor.fetchall()
            mismatch_file = os.path.join(output_dir, f"new_15_demographic_mismatch_{ts}.csv")
            with open(mismatch_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['gender', 'relationship', 'hospital_name', 'city', 'beneficiary_name', 'patient_name', 'admission_date', 'claimed_amount', 'approved_amount', 'deducted_amount'])
                for r in res_mismatch:
                    writer.writerow([r['gender'], r['relationship'], r['hospital_name'], r['city'], r['beneficiary_name'], r['patient_name'], r['admission_date'], r['claimed_amount'], r['approved_amount'], r['deducted_amount']])
            print(f"  ✓ Saved {len(res_mismatch)} records to {os.path.basename(mismatch_file)}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
