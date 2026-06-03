-- =====================================================================
-- ECHS MODULE 11: IDENTITY FRAUD DETECTION - SQL QUERIES
-- =====================================================================
-- Analysis Period: Last 5 Years (2021-2026)
-- Database: ECHS Production Database
-- Total Patterns: 10 Fraud Detection Patterns
-- =====================================================================

-- =====================================================================
-- PATTERN 01: DUPLICATE CARD IDs
-- Description: Single ECHS card number used by multiple different service numbers
-- Severity: CRITICAL
-- =====================================================================

SELECT 
    ci.CI_CARD_ID as card_number,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_BENEFICIARY_NAME) as unique_names,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
    MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
    MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
    DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    SUM(cs.CS_UTI_APP_AMT) as total_approved_amount,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
    GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as claim_ids
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_CARD_ID IS NOT NULL
    AND ci.CI_CARD_ID != ''
    AND LENGTH(ci.CI_CARD_ID) > 5
GROUP BY ci.CI_CARD_ID
HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) > 1
ORDER BY total_claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 02: SIMULTANEOUS ADMISSIONS  
-- Description: Same beneficiary admitted to 2+ hospitals at overlapping times
-- Severity: CRITICAL
-- =====================================================================

SELECT 
    a.CI_SERVICE_NO as service_number,
    a.CI_BENEFICIARY_NAME as beneficiary_name,
    a.CI_INTIMATION_ID as claim_id_1,
    a.CI_ADMISSION_DATE as admission_date_1,
    cs1.CS_DOD as discharge_date_1,
    a.CI_CR_OFFICE_ID as hospital_id_1,
    om1.OM_OFFICE_NAME as hospital_1,
    CONCAT(crm1.CRM_CITY_NAME, ', ', sm1.SM_STATE_NAME) as city_1,
    b.CI_INTIMATION_ID as claim_id_2,
    b.CI_ADMISSION_DATE as admission_date_2,
    cs2.CS_DOD as discharge_date_2,
    b.CI_CR_OFFICE_ID as hospital_id_2,
    om2.OM_OFFICE_NAME as hospital_2,
    CONCAT(crm2.CRM_CITY_NAME, ', ', sm2.SM_STATE_NAME) as city_2,
    DATEDIFF(
        LEAST(COALESCE(cs1.CS_DOD, CURDATE()), COALESCE(cs2.CS_DOD, CURDATE())),
        GREATEST(a.CI_ADMISSION_DATE, b.CI_ADMISSION_DATE)
    ) as overlap_days,
    cs1.CS_NET_CLAIM_AMT as amount_1,
    cs2.CS_NET_CLAIM_AMT as amount_2,
    a.CI_PATIENT_NAME as patient_name,
    a.CI_AGE as age,
    a.CI_SEX as gender
FROM claim_intimation a
JOIN claim_intimation b ON a.CI_SERVICE_NO = b.CI_SERVICE_NO
    AND a.CI_INTIMATION_ID < b.CI_INTIMATION_ID
    AND a.CI_CR_OFFICE_ID != b.CI_CR_OFFICE_ID
LEFT JOIN claim_submission cs1 ON a.CI_INTIMATION_ID = cs1.CS_INTIMATION_ID
LEFT JOIN claim_submission cs2 ON b.CI_INTIMATION_ID = cs2.CS_INTIMATION_ID
LEFT JOIN office_master om1 ON a.CI_CR_OFFICE_ID = om1.OM_OFFICE_ID
LEFT JOIN office_master om2 ON b.CI_CR_OFFICE_ID = om2.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm1 ON om1.OM_CGHS_CITY_ID = crm1.CRM_CITY_ID
LEFT JOIN cghs_region_master crm2 ON om2.OM_CGHS_CITY_ID = crm2.CRM_CITY_ID
LEFT JOIN state_master sm1 ON crm1.CRM_STATE_ID = sm1.SM_STATE_ID
LEFT JOIN state_master sm2 ON crm2.CRM_STATE_ID = sm2.SM_STATE_ID
WHERE a.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND b.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND (
        (a.CI_ADMISSION_DATE BETWEEN b.CI_ADMISSION_DATE 
            AND COALESCE(cs2.CS_DOD, DATE_ADD(b.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
        OR
        (b.CI_ADMISSION_DATE BETWEEN a.CI_ADMISSION_DATE 
            AND COALESCE(cs1.CS_DOD, DATE_ADD(a.CI_ADMISSION_DATE, INTERVAL 30 DAY)))
    )
ORDER BY overlap_days DESC, amount_1 DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 03: DUPLICATE BILL NUMBERS
-- Description: Same bill number submitted multiple times for different claims
-- Severity: HIGH
-- =====================================================================

SELECT 
    cs.CS_BILL_NO as bill_number,
    COUNT(*) as duplicate_count,
    SUM(cs.CS_NET_CLAIM_AMT) as total_amount,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_SERVICE_NO, ':', ci.CI_BENEFICIARY_NAME) 
        ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as beneficiaries,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
    GROUP_CONCAT(ci.CI_INTIMATION_ID ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as claim_ids,
    GROUP_CONCAT(DISTINCT ci.CI_ADMISSION_DATE ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as admission_dates,
    GROUP_CONCAT(DISTINCT ci.CI_CARD_ID SEPARATOR ', ') as card_numbers
FROM claim_submission cs
JOIN claim_intimation ci ON cs.CS_INTIMATION_ID = ci.CI_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE cs.CS_SUB_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_BILL_NO IS NOT NULL
    AND cs.CS_BILL_NO != ''
    AND LENGTH(cs.CS_BILL_NO) > 3
GROUP BY cs.CS_BILL_NO
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, total_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 04: MOBILE NUMBER RINGS
-- Description: Single mobile number linked to 5+ unrelated cards/service numbers
-- Severity: HIGH
-- =====================================================================

SELECT 
    ci.CI_MOBILE as mobile_number,
    COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
    MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
    MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
    DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    SUM(cs.CS_UTI_APP_AMT) as total_approved_amount,
    GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ', ') as card_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ', ') as service_numbers,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_MOBILE IS NOT NULL
    AND ci.CI_MOBILE != ''
    AND LENGTH(ci.CI_MOBILE) = 10
GROUP BY ci.CI_MOBILE
HAVING COUNT(DISTINCT ci.CI_CARD_ID) >= 5
ORDER BY unique_cards DESC, total_claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 05: UID DUPLICATION
-- Description: Same Aadhaar UID shared by multiple service numbers (synthetic identities)
-- Severity: CRITICAL
-- =====================================================================

SELECT 
    ci.CI_UID_NUMBER as uid_number,
    COUNT(DISTINCT ci.CI_SERVICE_NO) as unique_service_numbers,
    COUNT(DISTINCT ci.CI_CARD_ID) as unique_cards,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
    MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
    MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
    DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    SUM(cs.CS_UTI_APP_AMT) as total_approved_amount,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ', ') as service_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_CARD_ID ORDER BY ci.CI_CARD_ID SEPARATOR ', ') as card_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_BENEFICIARY_NAME ORDER BY ci.CI_SERVICE_NO SEPARATOR ' | ') as names,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_UID_NUMBER IS NOT NULL
    AND ci.CI_UID_NUMBER != ''
    AND LENGTH(ci.CI_UID_NUMBER) = 12
GROUP BY ci.CI_UID_NUMBER
HAVING COUNT(DISTINCT ci.CI_SERVICE_NO) > 1
ORDER BY unique_service_numbers DESC, total_claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 06: POST-DEATH CLAIMS (LAZARUS)
-- Description: Claims submitted AFTER recorded date of death
-- Severity: CRITICAL
-- =====================================================================

SELECT 
    ci.CI_INTIMATION_ID as claim_id,
    ci.CI_SERVICE_NO as service_number,
    ci.CI_CARD_ID as card_number,
    ci.CI_BENEFICIARY_NAME as beneficiary_name,
    ci.CI_PATIENT_NAME as patient_name,
    ci.CI_AGE as age,
    ci.CI_SEX as gender,
    ci.CI_RELATION_ID as relation_code,
    rm.RM_RELATION_DESC as relationship,
    cs.CS_DOD as death_date_in_claim,
    ci.CI_ADMISSION_DATE as admission_date,
    cs.CS_SUB_DATE as claim_submission_date,
    DATEDIFF(ci.CI_ADMISSION_DATE, cs.CS_DOD) as days_after_death_admission,
    DATEDIFF(cs.CS_SUB_DATE, cs.CS_DOD) as days_after_death_submission,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    cs.CS_UTI_APP_AMT as approved_amount,
    ci.CI_CR_OFFICE_ID as hospital_id,
    om.OM_OFFICE_NAME as hospital_name,
    CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as location,
    cs.CS_TREAT_DOCT as treating_doctor,
    ci.CI_ADM_AILMENT as ailment,
    ci.CI_INT_STAGE as claim_stage,
    ci.CI_INT_STATUS as claim_status
FROM claim_intimation ci
JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_DOD IS NOT NULL
    AND (
        ci.CI_ADMISSION_DATE > cs.CS_DOD
        OR cs.CS_SUB_DATE > DATE_ADD(cs.CS_DOD, INTERVAL 90 DAY)
    )
ORDER BY days_after_death_admission DESC, claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 07: CHRONIC STAY (FOREVER PATIENT)
-- Description: Hospital stays exceeding 90 days continuously
-- Severity: HIGH
-- =====================================================================

SELECT 
    ci.CI_SERVICE_NO as service_number,
    ci.CI_CARD_ID as card_number,
    ci.CI_BENEFICIARY_NAME as beneficiary_name,
    ci.CI_PATIENT_NAME as patient_name,
    ci.CI_AGE as age,
    ci.CI_SEX as gender,
    ci.CI_RELATION_ID as relation_code,
    rm.RM_RELATION_DESC as relationship,
    ci.CI_INTIMATION_ID as claim_id,
    ci.CI_ADMISSION_DATE as admission_date,
    cs.CS_DOD as discharge_date,
    DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) as stay_duration_days,
    ci.CI_CR_OFFICE_ID as hospital_id,
    om.OM_OFFICE_NAME as hospital_name,
    CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as location,
    ci.CI_ADM_AILMENT as ailment,
    ci.CI_ROOM_TYPE_ID as room_type,
    cs.CS_TREAT_DOCT as treating_doctor,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    cs.CS_UTI_APP_AMT as approved_amount,
    ci.CI_INT_STAGE as claim_stage,
    ci.CI_INT_STATUS as claim_status
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_ADMISSION_DATE IS NOT NULL
    AND DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE) > 90
ORDER BY stay_duration_days DESC, claimed_amount DESC
LIMIT 506;

-- =====================================================================
-- PATTERN 08: HIGH FREQUENCY CLAIMS
-- Description: Beneficiaries with 10+ claims in the analysis period
-- Severity: HIGH
-- =====================================================================

SELECT 
    ci.CI_SERVICE_NO as service_number,
    ci.CI_CARD_ID as card_number,
    ci.CI_BENEFICIARY_NAME as beneficiary_name,
    ci.CI_SERVICE_TYPE as service_type_code,
    stm.STM_SERVICE_NAME as service_type,
    ci.CI_SERVICE_RANK as rank_code,
    rm_rank.RM_RANK_NAME as rank_name,
    COUNT(DISTINCT ci.CI_INTIMATION_ID) as total_claims,
    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as unique_hospitals,
    COUNT(DISTINCT YEAR(ci.CI_ADMISSION_DATE)) as years_with_claims,
    COUNT(DISTINCT ci.CI_PATIENT_NAME) as unique_patients,
    MIN(ci.CI_ADMISSION_DATE) as first_claim_date,
    MAX(ci.CI_ADMISSION_DATE) as last_claim_date,
    DATEDIFF(MAX(ci.CI_ADMISSION_DATE), MIN(ci.CI_ADMISSION_DATE)) as fraud_span_days,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    SUM(cs.CS_UTI_APP_AMT) as total_approved_amount,
    AVG(cs.CS_NET_CLAIM_AMT) as avg_claim_amount,
    ci.CI_MOBILE as contact_mobile,
    ci.CI_ADDRESS1 as address,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals_used,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as locations,
    GROUP_CONCAT(DISTINCT ci.CI_PATIENT_NAME ORDER BY ci.CI_PATIENT_NAME SEPARATOR ' | ') as patients_treated
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
LEFT JOIN service_type_master stm ON ci.CI_SERVICE_TYPE = stm.STM_SERVICE_ID
LEFT JOIN rank_master rm_rank ON ci.CI_SERVICE_RANK = rm_rank.RM_RANK_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
GROUP BY ci.CI_SERVICE_NO, ci.CI_CARD_ID, ci.CI_BENEFICIARY_NAME,
         ci.CI_SERVICE_TYPE, ci.CI_SERVICE_RANK, ci.CI_MOBILE, ci.CI_ADDRESS1,
         stm.STM_SERVICE_NAME, rm_rank.RM_RANK_NAME
HAVING COUNT(DISTINCT ci.CI_INTIMATION_ID) >= 10
ORDER BY total_claims DESC, total_claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 09: IMPOSSIBLE DEPENDENT CLAIMS
-- Description: Claims for dependents who shouldn't be eligible (age, relationship issues)
-- Severity: HIGH
-- =====================================================================

SELECT 
    ci.CI_INTIMATION_ID as claim_id,
    ci.CI_SERVICE_NO as service_number,
    ci.CI_CARD_ID as card_number,
    ci.CI_BENEFICIARY_NAME as beneficiary_name,
    ci.CI_PATIENT_NAME as patient_name,
    ci.CI_AGE as patient_age,
    ci.CI_SEX as patient_gender,
    ci.CI_RELATION_ID as relation_code,
    rm.RM_RELATION_DESC as relationship,
    YEAR(CURDATE()) - YEAR(bm.BM_DOB) as beneficiary_age,
    ci.CI_ADMISSION_DATE as admission_date,
    cs.CS_DOD as discharge_date,
    cs.CS_NET_CLAIM_AMT as claimed_amount,
    cs.CS_UTI_APP_AMT as approved_amount,
    ci.CI_CR_OFFICE_ID as hospital_id,
    om.OM_OFFICE_NAME as hospital_name,
    CONCAT(crm.CRM_CITY_NAME, ', ', sm.SM_STATE_NAME) as location,
    cs.CS_TREAT_DOCT as treating_doctor,
    ci.CI_MOBILE as contact_mobile,
    ci.CI_ADM_AILMENT as ailment,
    CASE 
        WHEN ci.CI_RELATION_ID = 'SON' AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15) 
            THEN 'Son older than possible'
        WHEN ci.CI_RELATION_ID = 'DAU' AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15) 
            THEN 'Daughter older than possible'
        WHEN ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25 
            THEN 'Dependent over age limit (25)'
        WHEN ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) + 15) 
            THEN 'Wife age inconsistent'
        ELSE 'Age relationship mismatch'
    END as issue_type
FROM claim_intimation ci
LEFT JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN benf_master_live bm ON ci.CI_SERVICE_NO = bm.BM_SERVICE_NO 
    AND ci.CI_SERVICE_TYPE = bm.BM_FORCE_TYPE
LEFT JOIN relation_master rm ON ci.CI_RELATION_ID = rm.RM_RELATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND ci.CI_RELATION_ID IS NOT NULL
    AND ci.CI_RELATION_ID != 'SEL'
    AND (
        (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > 25)
        OR (ci.CI_RELATION_ID IN ('SON', 'DAU') AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) - 15))
        OR (ci.CI_RELATION_ID = 'WIF' AND CAST(ci.CI_AGE AS UNSIGNED) > (YEAR(CURDATE()) - YEAR(bm.BM_DOB) + 15))
    )
ORDER BY claimed_amount DESC, patient_age DESC
LIMIT 500;

-- =====================================================================
-- PATTERN 10: DOCTOR TELEPORTATION
-- Description: Same doctor treating patients at geographically distant hospitals on same day
-- Severity: HIGH
-- =====================================================================

SELECT 
    cs.CS_TREAT_DOCT as doctor_name,
    DATE(ci.CI_ADMISSION_DATE) as treatment_date,
    COUNT(DISTINCT ci.CI_CR_OFFICE_ID) as number_of_hospitals,
    COUNT(*) as number_of_patients,
    COUNT(DISTINCT crm.CRM_CITY_ID) as number_of_cities,
    GROUP_CONCAT(DISTINCT CONCAT(ci.CI_CR_OFFICE_ID, ':', om.OM_OFFICE_NAME) 
        ORDER BY ci.CI_CR_OFFICE_ID SEPARATOR ' | ') as hospitals,
    GROUP_CONCAT(DISTINCT CONCAT(crm.CRM_CITY_NAME, '-', sm.SM_STATE_NAME) 
        ORDER BY crm.CRM_CITY_NAME SEPARATOR ' | ') as cities,
    GROUP_CONCAT(DISTINCT ci.CI_PATIENT_NAME ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as patients_treated,
    GROUP_CONCAT(DISTINCT ci.CI_SERVICE_NO ORDER BY ci.CI_SERVICE_NO SEPARATOR ', ') as service_numbers,
    GROUP_CONCAT(DISTINCT ci.CI_INTIMATION_ID ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as claim_ids,
    GROUP_CONCAT(DISTINCT TIME(ci.CI_ADMISSION_DATE) ORDER BY ci.CI_ADMISSION_DATE SEPARATOR ', ') as treatment_times,
    SUM(cs.CS_NET_CLAIM_AMT) as total_claimed_amount,
    SUM(cs.CS_UTI_APP_AMT) as total_approved_amount
FROM claim_intimation ci
JOIN claim_submission cs ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_TREAT_DOCT IS NOT NULL
    AND cs.CS_TREAT_DOCT != ''
    AND LENGTH(cs.CS_TREAT_DOCT) > 3
GROUP BY cs.CS_TREAT_DOCT, DATE(ci.CI_ADMISSION_DATE)
HAVING COUNT(DISTINCT ci.CI_CR_OFFICE_ID) >= 2
    AND COUNT(DISTINCT crm.CRM_CITY_ID) >= 2
ORDER BY number_of_hospitals DESC, number_of_cities DESC, total_claimed_amount DESC
LIMIT 500;

-- =====================================================================
-- END OF MODULE 11 FRAUD DETECTION QUERIES
-- =====================================================================
-- Note: Use CI_CR_OFFICE_ID from claim_intimation and join with 
--       office_master.OM_OFFICE_ID to get hospital names.
--       Do NOT use CI_HOSPITAL_ID as it is not unique.
-- =====================================================================
