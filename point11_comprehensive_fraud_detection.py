import paramiko
import csv
import datetime
import json

# Database credentials
SSH_HOST = 'samar.iitk.ac.in'
SSH_PORT = 22
SSH_USER = 'echs_aman'
SSH_PASS = 'aman@2026'

DB_USER = 'aman'
DB_PASS = 'aman@2026'
DB_NAME = 'ECHS'

# All comprehensive fraud detection queries for Point 11
queries = {
    "01_Duplicate_Card_IDs": """
        SELECT 
            ci.CI_CARD_ID as card_number,
            COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
            COUNT(DISTINCT ci.CI_BENEFICIARY_NAME) as unique_names,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
            COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as service_numbers,
            GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME ORDER BY ci.CI_BENEFICIARY_NAME SEPARATOR ' | ') as beneficiary_names,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
            GROUP_CONCAT(DISTINCT CONCAT(COALESCE(crm.CRM_CITY_NAME,'?'), '-', COALESCE(sm.SM_STATE_NAME,'?')) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
            GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as all_claim_ids,
            MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
            MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
            DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_CARD_ID IS NOT NULL
            AND ci.CI_CARD_ID != ''
        GROUP BY ci.CI_CARD_ID
        HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) >= 3
        ORDER BY total_claimed_amount DESC;
    """,
    
    "02_Simultaneous_Admissions": """
        SELECT 
            a.CI_SERVICE_NO as service_number,
            a.CI_CARD_ID as card_number,
            a.CI_BENEFICIARY_NAME as beneficiary_name,
            a.CI_INTIMATION_ID as claim_id_1,
            a.CI_ADMISSION_DATE as admission_date_1,
            COALESCE(cs1.CS_DOD, 'Still Admitted') as discharge_date_1,
            a.CI_CR_OFFICE_ID as hospital_id_1,
            om1.OM_OFFICE_NAME as hospital_name_1,
            CONCAT(COALESCE(crm1.CRM_CITY_NAME,'?'), ', ', COALESCE(sm1.SM_STATE_NAME,'?')) as city_1,
            b.CI_INTIMATION_ID as claim_id_2,
            b.CI_ADMISSION_DATE as admission_date_2,
            COALESCE(cs2.CS_DOD, 'Still Admitted') as discharge_date_2,
            b.CI_CR_OFFICE_ID as hospital_id_2,
            om2.OM_OFFICE_NAME as hospital_name_2,
            CONCAT(COALESCE(crm2.CRM_CITY_NAME,'?'), ', ', COALESCE(sm2.SM_STATE_NAME,'?')) as city_2,
            DATEDIFF(
                LEAST(COALESCE(cs1.CS_DOD, CURDATE()), COALESCE(cs2.CS_DOD, CURDATE())),
                GREATEST(a.CI_ADMISSION_DATE, b.CI_ADMISSION_DATE)
            ) as overlap_days,
            COALESCE(cs1.CS_NET_CLAIM_AMT, 0) as amount_1,
            COALESCE(cs2.CS_NET_CLAIM_AMT, 0) as amount_2,
            COALESCE(cs1.CS_UTI_APP_AMT, 0) as approved_1,
            COALESCE(cs2.CS_UTI_APP_AMT, 0) as approved_2
        FROM claim_intimation a
        JOIN claim_intimation b ON a.CI_SERVICE_NO = b.CI_SERVICE_NO
            AND a.CI_INTIMATION_ID < b.CI_INTIMATION_ID
            AND a.CI_CR_OFFICE_ID != b.CI_CR_OFFICE_ID
        LEFT JOIN claim_submission cs1 ON a.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
        LEFT JOIN claim_submission cs2 ON b.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
        LEFT JOIN office_master om1 ON a.CI_CR_OFFICE_ID = om1.OM_OFFICE_ID
        LEFT JOIN office_master om2 ON b.CI_CR_OFFICE_ID = om2.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm1 ON om1.OM_OFFICE_CGHS_CITY_ID = crm1.CRM_CITY_ID
        LEFT JOIN cghs_region_master crm2 ON om2.OM_OFFICE_CGHS_CITY_ID = crm2.CRM_CITY_ID
        LEFT JOIN state_master sm1 ON crm1.CRM_STATE_ID = sm1.SM_STATE_ID
        LEFT JOIN state_master sm2 ON crm2.CRM_STATE_ID = sm2.SM_STATE_ID
        WHERE a.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND b.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND (
                (a.CI_ADMISSION_DATE BETWEEN b.CI_ADMISSION_DATE AND COALESCE(cs2.CS_DOD, DATE_ADD(b.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
                OR
                (b.CI_ADMISSION_DATE BETWEEN a.CI_ADMISSION_DATE AND COALESCE(cs1.CS_DOD, DATE_ADD(a.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
            )
        ORDER BY a.CI_SERVICE_NO, a.CI_ADMISSION_DATE
        LIMIT 500;
    """,
    
    "03_Duplicate_Bill_Numbers": """
        SELECT 
            cs.CS_BILL_NO as bill_number,
            cs.CS_BILL_DATE as bill_date,
            COUNT(*) as duplicate_count,
            SUM(cs.CS_NET_CLAIM_AMT) as total_amount,
            SUM(cs.CS_UTI_APP_AMT) as total_approved,
            GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_INTIMATION_ID SEPARATOR ' | ') as claim_ids,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
            GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_numbers,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
            GROUP_CONCAT(DISTINCT ci.CI_ADMISSION_DATE ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as admission_dates
        FROM claim_submission cs
        JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE cs.CS_SUB_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_BILL_NO IS NOT NULL
            AND cs.CS_BILL_NO != ''
        GROUP BY cs.CS_BILL_NO, cs.CS_BILL_DATE
        HAVING COUNT(*) > 1
        ORDER BY duplicate_count DESC, total_amount DESC
        LIMIT 500;
    """,
    
    "04_Mobile_Number_Rings": """
        SELECT 
            ci.CI_MOBILE as mobile_number,
            COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
            COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
            COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_numbers,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
            MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
            MAX(ci.CI_ADMISSION_DATE) as last_claim_date
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
        ORDER BY unique_cards DESC, total_claimed_amount DESC
        LIMIT 500;
    """,
    
    "05_UID_Duplication": """
        SELECT 
            ci.CI_UID_NUMBER as uid_number,
            COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
            COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
            COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
            GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ' | ') as card_numbers,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
            MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
            MAX(ci.CI_ADMISSION_DATE) as last_claim_date
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_UID_NUMBER IS NOT NULL
            AND ci.CI_UID_NUMBER != ''
            AND LENGTH(ci.CI_UID_NUMBER) = 12
            AND ci.CI_UID_NUMBER NOT IN ('000000000000', '999999999999', '123456789012', '111111111111')
        GROUP BY ci.CI_UID_NUMBER
        HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) > 1
        ORDER BY unique_service_numbers DESC, total_claimed_amount DESC
        LIMIT 500;
    """,
    
    "06_Post_Death_Claims_Lazarus": """
        SELECT 
            ci.CI_INTIMATION_ID as claim_id,
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            ci.CI_PATIENT_NAME as patient_name,
            ci.CI_AGE as patient_age,
            ci.CI_SEX as patient_gender,
            ci.CI_RELATION_ID as relationship_code,
            rm.RM_RELATION_NAME as relationship,
            cs.CS_DOD as death_date_in_claim,
            ci.CI_ADMISSION_DATE as admission_date,
            cs.CS_SUB_DATE as claim_submission_date,
            DATEDIFF(ci.CI_ADMISSION_DATE, cs.CS_DOD) as days_after_death_admission,
            DATEDIFF(cs.CS_SUB_DATE, cs.CS_DOD) as days_after_death_submission,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) as claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) as approved_amount,
            ci.CI_CR_OFFICE_ID as hospital_id,
            om.OM_OFFICE_NAME as hospital_name,
            CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as hospital_location,
            ci.CI_ADM_AILMENT as ailment,
            ci.CI_INT_STAGE as claim_stage,
            ci.CI_INT_STATUS as claim_status,
            cs.CS_TREAT_DOCT as treating_doctor
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_DOD IS NOT NULL
            AND (
                ci.CI_ADMISSION_DATE > cs.CS_DOD
                OR cs.CS_SUB_DATE > DATE_ADD(cs.CS_DOD, INTERVAL 90 DAY)
            )
        ORDER BY days_after_death_admission DESC
        LIMIT 500;
    """,
    
    "07_Chronic_Stay_Forever_Patient": """
        SELECT 
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            ci.CI_PATIENT_NAME as patient_name,
            ci.CI_AGE as patient_age,
            ci.CI_SEX as patient_gender,
            ci.CI_RELATION_ID as relationship_code,
            rm.RM_RELATION_NAME as relationship,
            ci.CI_INTIMATION_ID as claim_id,
            ci.CI_ADMISSION_DATE as admission_date,
            cs.CS_DOD as discharge_date,
            DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) as stay_duration_days,
            ci.CI_CR_OFFICE_ID as hospital_id,
            om.OM_OFFICE_NAME as hospital_name,
            CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as hospital_location,
            om.OM_OFFICE_ADD1 as hospital_address,
            ci.CI_ROOM_TYPE_ID as room_type,
            ci.CI_ADM_AILMENT as ailment,
            cs.CS_TREAT_DOCT as treating_doctor,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) as claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) as approved_amount,
            ci.CI_INT_STAGE as claim_stage,
            ci.CI_INT_STATUS as claim_status
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_ADMISSION_DATE IS NOT NULL
            AND DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) > 90
        ORDER BY stay_duration_days DESC
        LIMIT 500;
    """,
    
    "08_High_Frequency_Claims": """
        SELECT 
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            sm_svc.sm_desc as service_type,
            rm.rm_rank_def as rank_col,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
            COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
            COUNT(DISTINCT YEAR(ci.CI_ADMISSION_DATE)) as years_with_claims,
            COUNT(DISTINCT ci.CI_PATIENT_NAME) as unique_patients,
            MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
            MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
            DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            ROUND(AVG(cs.CS_NET_CLAIM_AMT), 2) as avg_claim_amount,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown')) ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations_used,
            GROUP_CONCAT(DISTINCT ci.CI_PATIENT_NAME ORDER BY ci.CI_PATIENT_NAME SEPARATOR ' | ') as patients_treated,
            ci.CI_MOBILE as contact_mobile,
            ci.CI_ADDRESS1 as address
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN service_master sm_svc ON ci.CI_SERVICE_TYPE = sm_svc.sm_code
        LEFT JOIN rank_master rm ON ci.CI_SERVICE_RANK = rm.rm_rank_id AND ci.CI_SERVICE_TYPE = rm.rm_service_code
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
        GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME, sm_svc.sm_desc, rm.rm_rank_def, ci.CI_MOBILE, ci.CI_ADDRESS1
        HAVING COUNT(DISTINCT ci.CI_INTIMATION_ID) >= 10
        ORDER BY total_claims DESC, total_claimed_amount DESC
        LIMIT 500;
    """,
    
    "09_Impossible_Dependent_Claims": """
        SELECT 
            ci.CI_INTIMATION_ID as claim_id,
            ci.CI_SERVICE_NO as service_number,
            ci.CI_CARD_ID as card_number,
            ci.CI_BENEFICIARY_NAME as beneficiary_name,
            ci.CI_PATIENT_NAME as patient_name,
            ci.CI_SEX as patient_gender,
            ci.CI_RELATION_ID as relationship_code,
            rm.RM_RELATION_NAME as relationship,
            ci.CI_AGE as patient_age,
            ci.CI_ADMISSION_DATE as admission_date,
            cs.CS_DOD as discharge_date,
            COALESCE(cs.CS_NET_CLAIM_AMT, 0) as claimed_amount,
            COALESCE(cs.CS_UTI_APP_AMT, 0) as approved_amount,
            ci.CI_CR_OFFICE_ID as hospital_id,
            om.OM_OFFICE_NAME as hospital_name,
            CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as hospital_location,
            ci.CI_ADM_AILMENT as ailment,
            cs.CS_TREAT_DOCT as treating_doctor,
            ci.CI_MOBILE as contact_mobile,
            ci.CI_INT_STAGE as claim_stage,
            ci.CI_INT_STATUS as claim_status,
            CASE 
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25 THEN 'Dependent over age limit (>25)'
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) < 0 THEN 'Invalid negative age'
                WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 50 THEN 'Age too high for dependent'
                WHEN ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) < 18 THEN 'Wife age too young'
                WHEN ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > 100 THEN 'Wife age too old'
                ELSE 'Age relationship inconsistency'
            END as issue_type
        FROM claim_intimation ci
        LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND ci.CI_RELATION_ID IS NOT NULL
            AND ci.CI_RELATION_ID != 'SEL'
            AND ci.CI_AGE IS NOT NULL
            AND (
                (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25)
                OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) < 18)
                OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > 100)
            )
        ORDER BY claimed_amount DESC
        LIMIT 500;
    """,
    
    "10_Doctor_Teleportation": """
        SELECT 
            cs.CS_TREAT_DOCT as doctor_name,
            DATE(ci.CI_ADMISSION_DATE) as treatment_date,
            COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as number_of_hospitals,
            COUNT(DISTINCT ci.CI_INTIMATION_ID) as number_of_patients,
            COUNT(DISTINCT crm.CRM_CITY_ID) as number_of_cities,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', COALESCE(om.OM_OFFICE_NAME, 'Unknown'), ' [', crm.CRM_CITY_NAME, ']') ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_and_locations,
            GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as cities_visited,
            GROUP_CONCAT(DISTINCT CONCAT(ci.CI_INTIMATION_ID, ':', ci.CI_PATIENT_NAME) ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ' | ') as patients_treated,
            GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as service_numbers,
            COALESCE(SUM(cs.CS_NET_CLAIM_AMT), 0) as total_claimed_amount,
            COALESCE(SUM(cs.CS_UTI_APP_AMT), 0) as total_approved_amount,
            MIN(ci.CI_ADMISSION_DATE) as first_treatment_time,
            MAX(ci.CI_ADMISSION_DATE) as last_treatment_time
        FROM claim_intimation ci
        JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
        LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
        LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
        LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
        WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            AND cs.CS_TREAT_DOCT IS NOT NULL
            AND cs.CS_TREAT_DOCT != ''
            AND cs.CS_TREAT_DOCT != 'NA'
        GROUP BY cs.CS_TREAT_DOCT, DATE(ci.CI_ADMISSION_DATE)
        HAVING COUNT(DISTINCT ci.CI_CR_OFFICE_ID) >= 2
            AND COUNT(DISTINCT crm.CRM_CITY_ID) >= 2
        ORDER BY number_of_hospitals DESC, total_claimed_amount DESC
        LIMIT 500;
    """
}

def run_mysql_query(client, query):
    """Execute a MySQL query via SSH and return the result."""
    mysql_cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -e "{query}"'
    stdin, stdout, stderr = client.exec_command(mysql_cmd, timeout=600)
    
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    
    # Filter out password warning
    err_lines = [l for l in err.splitlines() if 'Using a password' not in l and l.strip()]
    if err_lines:
        print(f"  [WARNING] {' | '.join(err_lines)[:200]}")
    
    return out

def main():
    print(f"\n{'='*80}")
    print(f"ECHS Point 11 Comprehensive Fraud Detection Analysis")
    print(f"Execution Start Time: {datetime.datetime.now()}")
    print(f"{'='*80}\n")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to SSH server: {SSH_HOST}...")
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
        print("✓ Connected successfully.\n")
        
        results_summary = {}
        all_data = {}
        
        for idx, (name, query) in enumerate(queries.items(), 1):
            print(f"\n[{idx}/{len(queries)}] Executing: {name}")
            print(f"Time: {datetime.datetime.now()}")
            print("-" * 80)
            
            try:
                # Execute query
                start_time = datetime.datetime.now()
                result = run_mysql_query(client, query.replace('"', '\\"').replace('\n', ' '))
                end_time = datetime.datetime.now()
                
                if result and result.strip():
                    # Save to CSV
                    filename = f"{name}.csv"
                    lines = result.splitlines()
                    
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for line in lines:
                            writer.writerow(line.split('\t'))
                    
                    # Store in memory for JSON
                    all_data[name] = {
                        'filename': filename,
                        'rows': len(lines) - 1,  # Excluding header
                        'query_time': str(end_time - start_time),
                        'data': []
                    }
                    
                    # Parse data for JSON
                    if len(lines) > 1:
                        headers = lines[0].split('\t')
                        for line in lines[1:]:
                            values = line.split('\t')
                            all_data[name]['data'].append(dict(zip(headers, values)))
                    
                    # Print summary
                    print(f"✓ Query completed in {end_time - start_time}")
                    print(f"✓ Records found: {len(lines) - 1}")
                    print(f"✓ Saved to: {filename}")
                    
                    # Show preview
                    print("\nPreview (first 3 records):")
                    for i, line in enumerate(lines[:4]):
                        if i == 0:
                            print(f"  HEADERS: {line.replace(chr(9), ' | ')}")
                        else:
                            print(f"  Row {i}: {line.replace(chr(9), ' | ')[:150]}...")
                    
                    if len(lines) > 4:
                        print(f"  ... and {len(lines) - 4} more records")
                    
                    results_summary[name] = {
                        'status': 'success',
                        'records': len(lines) - 1,
                        'file': filename,
                        'query_time': str(end_time - start_time)
                    }
                else:
                    print(f"⚠ No data returned")
                    results_summary[name] = {
                        'status': 'no_data',
                        'records': 0
                    }
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                results_summary[name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Save comprehensive JSON report
        json_filename = 'Point11_Fraud_Detection_Complete_Data.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'execution_time': datetime.datetime.now().isoformat(),
                'total_patterns': len(queries),
                'summary': results_summary,
                'data': all_data
            }, f, indent=2, default=str)
        
        print(f"\n{'='*80}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"\nExecution Summary:")
        print(f"  Total Patterns Analyzed: {len(queries)}")
        print(f"  Successful: {sum(1 for r in results_summary.values() if r['status'] == 'success')}")
        print(f"  No Data: {sum(1 for r in results_summary.values() if r['status'] == 'no_data')}")
        print(f"  Errors: {sum(1 for r in results_summary.values() if r['status'] == 'error')}")
        print(f"\nTotal Records Found:")
        for name, info in results_summary.items():
            if info['status'] == 'success':
                print(f"  {name}: {info['records']} records")
        
        print(f"\n✓ All data saved to individual CSV files")
        print(f"✓ Comprehensive JSON report: {json_filename}")
        print(f"\nEnd Time: {datetime.datetime.now()}")
        
    except Exception as e:
        print(f"\n✗ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\n✓ SSH connection closed.")

if __name__ == "__main__":
    main()
