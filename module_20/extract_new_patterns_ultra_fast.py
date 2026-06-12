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
            print("\nExtracting Pattern 6 (Individual Card-Sharing) - Ultra Fast...")
            # Step 1: Find card IDs with same-day multi-hospital admissions
            find_cards_query = """
                SELECT 
                    ci.CI_CARD_ID AS card_id, 
                    DATE(ci.CI_ADMISSION_DATE) AS adm_date, 
                    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) AS hosp_count
                FROM claim_intimation ci
                WHERE ci.CI_INTIMATION_ID BETWEEN 8000000 AND 9999999
                  AND ci.CI_CARD_ID IS NOT NULL 
                  AND ci.CI_CARD_ID != '' 
                  AND ci.CI_CARD_ID != '0' 
                  AND ci.CI_CARD_ID NOT LIKE '0000%'
                GROUP BY ci.CI_CARD_ID, DATE(ci.CI_ADMISSION_DATE)
                HAVING hosp_count > 1
                LIMIT 50;
            """
            cursor.execute(find_cards_query)
            cards_list = cursor.fetchall()
            print(f"  Found {len(cards_list)} potential card-sharing instances. Fetching details...")
            
            card_rows = []
            for instance in cards_list:
                card_id = instance['card_id']
                adm_date = instance['adm_date']
                
                # Fetch details for this card ID and date
                details_query = """
                    SELECT 
                        ci.CI_BENEFICIARY_NAME AS beneficiary_name,
                        om.OM_OFFICE_NAME AS hospital_name,
                        cs.CS_UTI_APP_AMT AS approved_amt
                    FROM claim_intimation ci
                    JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
                    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
                    WHERE ci.CI_CARD_ID = %s 
                      AND DATE(ci.CI_ADMISSION_DATE) = %s
                """
                cursor.execute(details_query, (card_id, adm_date))
                details = cursor.fetchall()
                
                if len(details) >= 2:
                    hosp1 = details[0]['hospital_name']
                    hosp2 = details[1]['hospital_name']
                    amt1 = float(details[0]['approved_amt'] or 0)
                    amt2 = float(details[1]['approved_amt'] or 0)
                    beneficiary = details[0]['beneficiary_name']
                    
                    card_rows.append([
                        card_id,
                        beneficiary,
                        str(adm_date),
                        hosp1,
                        hosp2,
                        amt1,
                        amt2,
                        amt1 + amt2
                    ])
            
            # Sort by total approved descending
            card_rows.sort(key=lambda x: x[7], reverse=True)
            
            card_file = os.path.join(output_dir, f"new_13_card_sharing_{ts}.csv")
            with open(card_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['card_id', 'beneficiary_name', 'admission_date', 'hospital_1', 'hospital_2', 'approved_amt_1', 'approved_amt_2', 'total_approved'])
                for r in card_rows:
                    writer.writerow(r)
            print(f"  ✓ Saved {len(card_rows)} records to {os.path.basename(card_file)}")
            
            # 2. Family Sharing (Pattern 7)
            print("\nExtracting Pattern 7 (Family Simultaneous Admissions) - Ultra Fast...")
            # Step 1: Find service numbers with same-day multi-hospital admissions for different card IDs
            find_families_query = """
                SELECT 
                    ci.CI_SERVICE_NO AS service_no, 
                    DATE(ci.CI_ADMISSION_DATE) AS adm_date, 
                    COUNT(DISTINCT ci.CI_CARD_ID) AS card_count,
                    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) AS hosp_count
                FROM claim_intimation ci
                WHERE ci.CI_INTIMATION_ID BETWEEN 8000000 AND 9999999
                  AND ci.CI_SERVICE_NO IS NOT NULL 
                  AND ci.CI_SERVICE_NO != '' 
                  AND ci.CI_SERVICE_NO != '0' 
                  AND ci.CI_SERVICE_NO NOT LIKE '0000%'
                GROUP BY ci.CI_SERVICE_NO, DATE(ci.CI_ADMISSION_DATE)
                HAVING card_count > 1 AND hosp_count > 1
                LIMIT 50;
            """
            cursor.execute(find_families_query)
            families_list = cursor.fetchall()
            print(f"  Found {len(families_list)} potential family-sharing instances. Fetching details...")
            
            family_rows = []
            for instance in families_list:
                service_no = instance['service_no']
                adm_date = instance['adm_date']
                
                # Fetch details for this service number and date
                details_query = """
                    SELECT 
                        ci.CI_BENEFICIARY_NAME AS beneficiary_name,
                        rm.RM_RELATION_NAME AS relationship,
                        om.OM_OFFICE_NAME AS hospital_name,
                        cs.CS_UTI_APP_AMT AS approved_amt
                    FROM claim_intimation ci
                    JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
                    LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
                    LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
                    WHERE ci.CI_SERVICE_NO = %s 
                      AND DATE(ci.CI_ADMISSION_DATE) = %s
                """
                cursor.execute(details_query, (service_no, adm_date))
                details = cursor.fetchall()
                
                if len(details) >= 2:
                    m1 = details[0]['beneficiary_name']
                    r1 = details[0]['relationship'] or 'Self'
                    m2 = details[1]['beneficiary_name']
                    r2 = details[1]['relationship'] or 'Spouse'
                    h1 = details[0]['hospital_name']
                    h2 = details[1]['hospital_name']
                    amt1 = float(details[0]['approved_amt'] or 0)
                    amt2 = float(details[1]['approved_amt'] or 0)
                    
                    family_rows.append([
                        service_no,
                        m1,
                        r1,
                        m2,
                        r2,
                        str(adm_date),
                        h1,
                        h2,
                        amt1,
                        amt2,
                        amt1 + amt2
                    ])
            
            # Sort by total approved descending
            family_rows.sort(key=lambda x: x[10], reverse=True)
            
            family_file = os.path.join(output_dir, f"new_14_family_sharing_{ts}.csv")
            with open(family_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['service_no', 'member_1', 'relation_1', 'member_2', 'relation_2', 'admission_date', 'hospital_1', 'hospital_2', 'approved_amt_1', 'approved_amt_2', 'total_approved'])
                for r in family_rows:
                    writer.writerow(r)
            print(f"  ✓ Saved {len(family_rows)} records to {os.path.basename(family_file)}")

            # 3. Demographic Mismatch (Pattern 8)
            print("\nExtracting Pattern 8 (Demographic Mismatch)...")
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
                WHERE ci.CI_INTIMATION_ID BETWEEN 8000000 AND 9999999
                  AND (
                    (ci.CI_SEX = 'M' AND rm.RM_RELATION_NAME IN ('Wife', 'Mother', 'Daughter', 'Sister'))
                    OR (ci.CI_SEX = 'F' AND rm.RM_RELATION_NAME IN ('Husband', 'Father', 'Son', 'Brother'))
                  )
                  AND cs.CS_UTI_APP_AMT >= 30000
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
