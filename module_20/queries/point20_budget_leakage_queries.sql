-- =====================================================================
-- ECHS MODULE 20: BUDGET LEAKAGE & EXPENDITURE ANALYSIS
-- =====================================================================
-- Analysis Period : FY 2021 - FY 2025
-- Database        : ECHS Production
-- Tables Used     : settlement_stat, office_master, cghs_region_master,
--                   state_master, relation_master, claim_intimation,
--                   claim_submission
-- JOIN Pattern    : Module 11 proven chain
--                   office_master.OM_OFFICE_CGHS_CITY_ID = cghs_region_master.CRM_CITY_ID
--                   cghs_region_master.CRM_STATE_ID = state_master.SM_STATE_ID
-- =====================================================================


-- =====================================================================
-- QUERY 01: OVERALL LEAKAGE SUMMARY
-- =====================================================================
SELECT
    SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                    AS total_claimed_cr,
    ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                    AS total_approved_cr,
    ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                    AS total_deducted_cr,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
FROM settlement_stat ss
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025;


-- =====================================================================
-- QUERY 02: ANNUAL EXPENDITURE TREND (Year-on-Year)
-- NOTE: FY 2025 is partial year — lower claim count is expected.
-- =====================================================================
WITH annual_stats AS (
    SELECT
        SS_FY_YEAR        AS fiscal_year,
        SUM(SS_CLAIM_CNT) AS total_claims,
        SUM(SS_CLAIM_AMT) AS total_claimed,
        SUM(SS_APPR_AMT)  AS total_approved,
        SUM(SS_DED_AMT)   AS total_deducted
    FROM settlement_stat
    WHERE SS_FY_YEAR BETWEEN 2021 AND 2025
    GROUP BY SS_FY_YEAR
)
SELECT
    fiscal_year,
    total_claims,
    ROUND(total_claimed  / 10000000.0, 2)                                                       AS total_claimed_cr,
    ROUND(total_approved / 10000000.0, 2)                                                       AS total_approved_cr,
    ROUND(total_deducted / 10000000.0, 2)                                                       AS total_deducted_cr,
    ROUND(total_deducted * 100.0 / total_claimed, 2)                                            AS deduction_pct,
    ROUND(
        (total_claimed - LAG(total_claimed) OVER (ORDER BY fiscal_year)) * 100.0
        / LAG(total_claimed) OVER (ORDER BY fiscal_year)
    , 2)                                                                                         AS yoy_growth_pct
FROM annual_stats
ORDER BY fiscal_year;


-- =====================================================================
-- QUERY 03: LEAKAGE BY HOSPITAL TYPE & NABH STATUS
-- Tables: settlement_stat + office_master + cghs_region_master + state_master
-- =====================================================================
SELECT
    COALESCE(om.OM_HOSP_TYPE, 'Unknown')                            AS hosp_type_code,
    COALESCE(om.OM_NABH, 'N')                                       AS nabh_status,
    COUNT(DISTINCT ss.SS_OFFICE_ID)                                 AS num_hospitals,
    SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                    AS total_claimed_cr,
    ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                    AS total_approved_cr,
    ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                    AS total_deducted_cr,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
FROM settlement_stat ss
LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
GROUP BY om.OM_HOSP_TYPE, om.OM_NABH
ORDER BY deduction_pct DESC;


-- =====================================================================
-- QUERY 04: HOSPITAL-WISE LEAKAGE SUMMARY
-- Tables: settlement_stat + office_master + cghs_region_master + state_master
-- Full related data: hospital name, city, state, type, NABH + all amounts
-- =====================================================================
SELECT
    ss.SS_OFFICE_ID                                                 AS hospital_id,
    COALESCE(om.OM_OFFICE_NAME, 'Unknown')                         AS hospital_name,
    COALESCE(om.OM_OFFICE_CITY, '')                                AS hospital_city_direct,
    COALESCE(crm.CRM_CITY_NAME, '')                                AS cghs_city,
    COALESCE(sm.SM_STATE_NAME, '')                                  AS state,
    COALESCE(om.OM_HOSP_TYPE, '')                                   AS hosp_type_code,
    COALESCE(om.OM_NABH, 'N')                                       AS nabh_status,
    COALESCE(om.OM_NABL, 'N')                                       AS nabl_status,
    om.OM_OFFICE_PIN                                                AS pincode,
    SUM(ss.SS_CLAIM_CNT)                                            AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 100000.0, 2)                      AS total_claimed_lakh,
    ROUND(SUM(ss.SS_APPR_AMT)  / 100000.0, 2)                      AS total_approved_lakh,
    ROUND(SUM(ss.SS_DED_AMT)   / 100000.0, 2)                      AS total_deducted_lakh,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)   AS deduction_pct
FROM settlement_stat ss
LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
GROUP BY
    ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_OFFICE_CITY,
    crm.CRM_CITY_NAME, sm.SM_STATE_NAME,
    om.OM_HOSP_TYPE, om.OM_NABH, om.OM_NABL, om.OM_OFFICE_PIN
ORDER BY total_deducted_lakh DESC;


-- =====================================================================
-- QUERY 05: REGIONAL DEDUCTION BREAKDOWN
-- Tables: settlement_stat + office_master + cghs_region_master + state_master
-- Fix: uses Module 11 proven chain instead of broken ecs_region table
-- =====================================================================
SELECT
    ss.SS_REGION_ID                                                         AS region_id,
    COALESCE(crm.CRM_CITY_NAME, CONCAT('Region ', ss.SS_REGION_ID))        AS region_name,
    COALESCE(sm.SM_STATE_NAME, '')                                          AS state_name,
    COUNT(DISTINCT ss.SS_OFFICE_ID)                                         AS num_hospitals,
    SUM(ss.SS_CLAIM_CNT)                                                    AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                            AS total_claimed_cr,
    ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                            AS total_approved_cr,
    ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                            AS total_deducted_cr,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)           AS deduction_pct
FROM settlement_stat ss
LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
GROUP BY ss.SS_REGION_ID, crm.CRM_CITY_NAME, sm.SM_STATE_NAME
ORDER BY total_deducted_cr DESC;


-- =====================================================================
-- QUERY 06: FRAUD PROJECTION SUMMARY
-- =====================================================================
SELECT
    ROUND(SUM(SS_CLAIM_AMT) / 10000000.0, 2)                AS total_claimed_cr,
    ROUND(SUM(SS_DED_AMT)   / 10000000.0, 2)                AS total_deducted_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.30, 2)         AS conservative_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.50, 2)         AS moderate_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.75, 2)         AS aggressive_fraud_cr,
    ROUND((SUM(SS_DED_AMT) / 10000000.0) * 0.60, 2)         AS ai_interception_cr
FROM settlement_stat
WHERE SS_FY_YEAR BETWEEN 2021 AND 2025;


-- =====================================================================
-- QUERY 07: CLAIM-LEVEL DETAIL FOR TOP 25 HIGH-DEDUCTION HOSPITALS
-- Tables: claim_intimation + claim_submission + office_master
--         + cghs_region_master + state_master
-- Senior requirement: related data se individual claim detail bhi nikalo
-- =====================================================================
SELECT
    ci.CI_CR_OFFICE_ID                                                              AS hospital_id,
    COALESCE(om.OM_OFFICE_NAME, 'Unknown')                                         AS hospital_name,
    COALESCE(om.OM_OFFICE_CITY, crm.CRM_CITY_NAME, '')                            AS city,
    COALESCE(sm.SM_STATE_NAME, '')                                                  AS state,
    COALESCE(om.OM_HOSP_TYPE, '')                                                   AS hosp_type,
    COALESCE(om.OM_NABH, 'N')                                                       AS nabh_status,
    ci.CI_INTIMATION_ID                                                             AS claim_id,
    ci.CI_SERVICE_NO                                                                AS service_number,
    ci.CI_BENEFICIARY_NAME                                                          AS beneficiary_name,
    ci.CI_PATIENT_NAME                                                              AS patient_name,
    ci.CI_AGE                                                                       AS age,
    ci.CI_SEX                                                                       AS gender,
    ci.CI_ADMISSION_DATE                                                            AS admission_date,
    cs.CS_DOD                                                                       AS discharge_date,
    DATEDIFF(COALESCE(cs.CS_DOD, CURDATE()), ci.CI_ADMISSION_DATE)                AS stay_days,
    ci.CI_ADM_AILMENT                                                               AS ailment,
    cs.CS_TREAT_DOCT                                                                AS treating_doctor,
    cs.CS_BILL_NO                                                                   AS bill_number,
    cs.CS_NET_CLAIM_AMT                                                             AS claimed_amount,
    cs.CS_UTI_APP_AMT                                                               AS approved_amount,
    (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT)                                     AS deducted_amount,
    ROUND(
        (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) * 100.0
        / NULLIF(cs.CS_NET_CLAIM_AMT, 0)
    , 2)                                                                             AS deduction_pct,
    ci.CI_INT_STAGE                                                                 AS claim_stage,
    ci.CI_INT_STATUS                                                                AS claim_status
FROM claim_intimation ci
JOIN  claim_submission cs  ON ci.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
LEFT JOIN office_master om       ON ci.CI_CR_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
WHERE ci.CI_CR_DATE >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
    AND cs.CS_NET_CLAIM_AMT > 0
    AND (cs.CS_NET_CLAIM_AMT - cs.CS_UTI_APP_AMT) > 0
    AND ci.CI_CR_OFFICE_ID IN (
        SELECT ss.SS_OFFICE_ID
        FROM settlement_stat ss
        WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
        GROUP BY ss.SS_OFFICE_ID
        ORDER BY SUM(ss.SS_DED_AMT) DESC
        LIMIT 25
    )
ORDER BY deducted_amount DESC
LIMIT 500;


-- =====================================================================
-- QUERY 08: GENDER + RELATIONSHIP BREAKDOWN OF DEDUCTIONS
-- Tables: settlement_stat + relation_master
-- Who is driving the most deductions — self, spouse, children?
-- =====================================================================
SELECT
    ss.SS_GENDER                                                            AS gender,
    COALESCE(rm.RM_RELATION_DESC, ss.SS_RELATION_ID)                       AS relationship,
    SUM(ss.SS_CLAIM_CNT)                                                    AS total_claims,
    ROUND(SUM(ss.SS_CLAIM_AMT) / 10000000.0, 2)                            AS total_claimed_cr,
    ROUND(SUM(ss.SS_APPR_AMT)  / 10000000.0, 2)                            AS total_approved_cr,
    ROUND(SUM(ss.SS_DED_AMT)   / 10000000.0, 2)                            AS total_deducted_cr,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2)           AS deduction_pct
FROM settlement_stat ss
LEFT JOIN relation_master rm ON ss.SS_RELATION_ID = rm.RM_RELATION_ID
WHERE ss.SS_FY_YEAR BETWEEN 2021 AND 2025
GROUP BY ss.SS_GENDER, ss.SS_RELATION_ID, rm.RM_RELATION_DESC
ORDER BY total_deducted_cr DESC;
