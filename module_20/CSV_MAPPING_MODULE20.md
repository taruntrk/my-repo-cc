# ECHS Module 20: PDF to CSV Data Mapping Guide

This document traces the exact data flow from the generated forensic PDF report back to the raw CSV files stored in the `new_data/` directory.

## 1. Executive Summary & KPIs
* **Data Displayed:** Total Claims Scanned, Total Leakage Deducted, Deduction Rate.
* **Underlying CSV:** `new_data/new_01a_overall_leakage_summary_*.csv`
* **Python Variable:** `p01`

## 2. Annual Expenditure Trend
* **Data Displayed:** The year-by-year budget trend chart (FY2021 to FY2026).
* **Underlying CSV:** `new_data/new_02a_annual_expenditure_trend_*.csv`
* **Python Variable:** `p02`

## 3. Pattern 1: Corporate Hospital Overbilling
* **Data Displayed:** Table 1.1 — Top Private Hospitals by Deduction Volume (Top 15 outliers shown, 50 evaluated).
* **Underlying CSV:** `new_data/new_04a_hospital_leakage_summary_*.csv`
* **Python Variable:** `p04a`

## 4. Pattern 2: Macro Analytics
### A. Regional Demographics
* **Data Displayed:** Table 2.2 — Geographical Anomaly Breakdown (Command-wise leakage).
* **Underlying CSV:** `new_data/new_05a_regional_deduction_breakdown_*.csv`
* **Python Variable:** `p05a`

### B. Gender Demographics
* **Data Displayed:** The Gender & Dependents vulnerability pie-chart.
* **Underlying CSV:** `new_data/new_08a_gender_relation_summary_*.csv`
* **Python Variable:** `p08a`

## 5. Pattern 3: Itemized Procedure Deviations
* **Data Displayed:** Tables displaying outliers for Package Double-Billing, Antibiotic Abuse, and Unjustified Charges.
* **Underlying CSV:** `new_data/new_07_targeted_itemized_deductions_*.csv` *(Note: This CSV contains the full 1.46 Million row dataset)*
* **Python Variable:** `p07`

## 6. Pattern 4: Extended Length of Stay (LoS)
* **Data Displayed:** Table P2 — Top Instances of Extended Hospital Stays (> 10 Days).
* **Underlying CSV:** `new_data/new_08_los_bed_blocking_abuse_*.csv` *(Note: Contains all 838 true database cases)*
* **Python Variable:** `p08_los`

## 7. Pattern 5: Ping-Pong Admissions
* **Data Displayed:** Table P3 — Top Cases of Split-Package Readmissions (Within 48 Hrs).
* **Underlying CSV:** `new_data/new_09_ping_pong_admissions_*.csv` *(Note: Contains all 500 true database cases)*
* **Python Variable:** `p09_pingpong`

## 8. Pattern 6: Weekend Admission Surge
* **Data Displayed:** Table P4 — Facilities with Highest Non-Working Day Admission Rates.
* **Underlying CSV:** `new_data/new_10_weekend_surge_abuse_*.csv` *(Note: Aggregates the 1.32 Million weekend admissions)*
* **Python Variable:** `p10_weekend`

## 9. Pattern 7: High-Volume Provider (Superman)
* **Data Displayed:** Table P5 — Top Treating Doctors by Abnormal Volume (>15 Procedures/Day).
* **Underlying CSV:** `new_data/new_11_superman_surgeon_*.csv` *(Note: Contains all 17,374 abnormal procedures)*
* **Python Variable:** `p11_superman`

## 10. Pattern 8: Threshold Avoiding Bills
* **Data Displayed:** Table P6 — Split Bills Designed to Evade Approval Ceilings.
* **Underlying CSV:** `new_data/new_12_threshold_avoiding_*.csv` *(Note: Contains all 2,856 threshold-avoiding bills)*
* **Python Variable:** `p12_threshold`

---
> **Developer Note:** The `generate_module20_report_html.py` script automatically loads the *most recently generated* CSV for each pattern using a `glob` wildcard search. If you wish to update the report with fresh data, simply re-run the extraction scripts (`extract_module20_data.py` and `extract_phase3_patterns.py`) to generate new timestamped CSVs in the `new_data/` folder.
