# ECHS Module 20: Pipeline Audit & Correction Report

This report documents the requirements ignored, bugs introduced, and dataset completeness issues encountered during the development of the ECHS Module 20 pipeline, along with the corrective actions taken.

---

## 1. Summary of Issues & Gaps

| Area | What was Ignored / Done Poorly | Impact | Corrective Action Taken |
| :--- | :--- | :--- | :--- |
| **Dataset Completeness (Forensic Claims Data)** | Focused only on aggregated summary files. Ignored the large-scale, raw claim-level detail files (e.g., the `04b_hospital_all_claims` dataset containing lakhs of forensic records). | Left the forensic team without the actual detailed data needed for audits. | Fixed the query pipeline to extract both summary stats AND detailed claim records. |
| **Subquery LIMIT Bug (Query 7)** | Attempted to run nested subquery with `LIMIT` inside the `IN` clause: `IN (SELECT ... LIMIT 25)`. | Query 7 (`high_deduction_hospital_claims`) failed with `ERROR 1235 (42000)`. | Refactored Python logic to fetch IDs first, then formatted them dynamically into the query. |
| **Incorrect Column Names (Query 8)** | Used `rm.RM_RELATION_DESC` instead of the actual schema column `rm.RM_RELATION_NAME`. | Query 8 (`gender_relation_leakage`) failed with `ERROR 1054 (42S22)`. | Corrected the column reference to `RM_RELATION_NAME`. |
| **Unresolved Region Master Join (Query 5)** | Left `om.OM_CGHS_CITY_ID` inside the query in `extract_module20_data.py`. | Query 5 (`regional_deduction_breakdown`) failed with `ERROR 1054 (42S22)`. | Corrected to `om.OM_OFFICE_CGHS_CITY_ID`. |

---

## 2. Detailed Breakdown of Failures

### A. Missing Detailed Claims ("Bhut Data" Requirement)
* **What went wrong:** The senior developer's legacy data folder contained massive files (e.g., `04b_hospital_all_claims_*.csv` with size >298 MB) containing actual claim IDs, patient names, diagnoses, admission dates, and doctor names. In contrast, our initial scripts only extracted summaries (~8-30 rows each) for ReportLab PDF compilation, completely ignoring the investigator's requirement for raw forensic claims list.
* **Resolution:** The extraction pipeline `extract_module20_data.py` now runs all 8 queries, successfully capturing both summaries and high-deduction hospital claim-level details.

### B. MySQL Nested Subquery Limitation
* **What went wrong:** The subquery:
  ```sql
  AND ci.CI_CR_OFFICE_ID IN (
      SELECT ss.SS_OFFICE_ID FROM settlement_stat ss ... LIMIT 25
  )
  ```
  failed because MySQL CLI does not support `LIMIT` within an `IN` subquery.
* **Resolution:** Replaced the static nested subquery with a two-step Python workflow:
  1. Fetch the Top 25 hospital IDs.
  2. Dynamically substitute the resolved IDs into the main query using `IN ({ids})`.

### C. Schema Mismatch Bugs
* **What went wrong:** Incorrect column references (`RM_RELATION_DESC` and `OM_CGHS_CITY_ID`) were included in the SQL queries, showing a lack of testing against the actual database schema.
* **Resolution:** Query columns updated to `RM_RELATION_NAME` and `OM_OFFICE_CGHS_CITY_ID` respectively.

---

## 3. Current Pipeline Status

The extraction pipeline is now **100% functional**:
1. All **8/8 queries** execute without errors.
2. The complete set of CSV files (both summaries and claim-level details) are saved in `/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20/`.
3. The PDF report successfully generates using these dynamic files and is synchronized with the central repository `/home/tarun/Downloads/CC/echs_analysis/reports/Module_20.pdf`.
