-- ==============================================================================
-- ECHS Forensic Analytics & Pipeline Automation (Module 20)
-- Finalized Query Pack with Safe Key Joins
-- ==============================================================================

-- Query A: Annual Expenditure Trend
-- Sourced for Page 3: Annual Expenditure & Deduction Trend
SELECT 
    SS_FY_YEAR AS fiscal_year,
    SUM(SS_CLAIM_CNT) AS total_claims,
    SUM(SS_CLAIM_AMT) AS total_claimed_amount,
    SUM(SS_APPR_AMT) AS total_approved_amount,
    SUM(SS_DED_AMT) AS total_deducted_amount,
    ROUND(SUM(SS_DED_AMT) * 100.0 / SUM(SS_CLAIM_AMT), 2) AS deduction_pct
FROM settlement_stat
WHERE SS_FY_YEAR BETWEEN 2013 AND 2025
GROUP BY SS_FY_YEAR
ORDER BY SS_FY_YEAR;


-- Query B: Hospital Type + NABH Leakage
-- Sourced for Page 4: Budget Leakage by Hospital Type & NABH Status
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
LEFT JOIN office_master om 
    ON CAST(ss.SS_OFFICE_ID AS UNSIGNED) = CAST(om.OM_OFFICE_ID AS UNSIGNED)
WHERE ss.SS_FY_YEAR BETWEEN 2013 AND 2025
GROUP BY om.OM_HOSP_TYPE, om.OM_NABH
ORDER BY deduction_pct DESC;


-- Query C: Top 25 Hospitals by Deduction
-- Sourced for Page 5: Priority Audit List
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
LEFT JOIN office_master om 
    ON CAST(ss.SS_OFFICE_ID AS UNSIGNED) = CAST(om.OM_OFFICE_ID AS UNSIGNED)
WHERE ss.SS_FY_YEAR BETWEEN 2013 AND 2025
GROUP BY ss.SS_OFFICE_ID, om.OM_OFFICE_NAME, om.OM_HOSP_TYPE, om.OM_NABH
ORDER BY total_deducted_amount DESC
LIMIT 25;


-- Query D: Regional Deduction Breakdown
-- Sourced for Page 6: Regional Deduction Breakdown
SELECT 
    ss.SS_REGION_ID AS region_id,
    COALESCE(er.ER_REGION_NAME, CONCAT('Region ', ss.SS_REGION_ID)) AS region_name,
    COUNT(DISTINCT ss.SS_OFFICE_ID) AS num_hospitals,
    SUM(ss.SS_CLAIM_CNT) AS total_claims,
    SUM(ss.SS_CLAIM_AMT) AS total_claimed_amount,
    SUM(ss.SS_APPR_AMT) AS total_approved_amount,
    SUM(ss.SS_DED_AMT) AS total_deducted_amount,
    ROUND(SUM(ss.SS_DED_AMT) * 100.0 / SUM(ss.SS_CLAIM_AMT), 2) AS deduction_pct
FROM settlement_stat ss
LEFT JOIN ecs_region er 
    ON CAST(ss.SS_REGION_ID AS UNSIGNED) = CAST(er.ER_REGION_ID AS UNSIGNED)
WHERE ss.SS_FY_YEAR BETWEEN 2013 AND 2025
GROUP BY ss.SS_REGION_ID, er.ER_REGION_NAME
ORDER BY total_deducted_amount DESC;


-- Query E: Overall Leakage & Fraud Estimates
-- Sourced for Page 2: Executive Summary & Page 7: Fraud Projections
SELECT 
    SUM(SS_CLAIM_CNT) AS total_claims,
    SUM(SS_CLAIM_AMT) AS total_claimed_amount,
    SUM(SS_APPR_AMT) AS total_approved_amount,
    SUM(SS_DED_AMT) AS total_deducted_amount,
    ROUND(SUM(SS_DED_AMT) * 100.0 / SUM(SS_CLAIM_AMT), 2) AS deduction_pct
FROM settlement_stat
WHERE SS_FY_YEAR BETWEEN 2013 AND 2025;
