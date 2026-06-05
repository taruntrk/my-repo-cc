# Module 12: Hospital Specialty Misuse & Service Empanelment Analysis — Technical Documentation

## Overview
Module 12 investigates empanelment scope creep, hospital specialty misuse, and high-deduction anomalous behaviors among ECHS-empanelled facilities. The analysis ensures that hospitals are only billing for services they are legally licensed and equipped to provide over the FY 2021–2026 period.

---

## Database Tables Utilized
The module relies on the following core ECHS database tables:
1. **`claim_intimation` (`ci`)**: The entry point for claims. The critical field `CI_PATIENT_TYPE = 'I'` is used to filter exclusively for Inpatient (IPD) admissions.
2. **`claim_submission` (`cs`)**: Stores the financial details, heavily relying on `CS_GR_CLAIM_AMT` (amount claimed by the hospital) and `CS_UTI_APP_AMT` (amount finally approved by ECHS).
3. **`office_master` (`om`)**: Holds hospital master data. Critical fields include `OM_HOSP_TYPE` (e.g., '1' for Hospital, '3' for Dental/Labs), `OM_HOSP_TYPES` (text description), and `OM_NABH` ('Y' or 'N' for accreditation).
4. **`empanel_hospital_service` (`ehs`)**: Maps a hospital (`EHS_OFFICE_ID`) to its empaneled service facilities. Includes validation dates (`EHS_TO_DATE`).
5. **`empanel_facility` (`ef`)**: The lookup table detailing the names of the empaneled services (e.g., "General Medicine", "Cardiology", "Intensive Care Unit Adult (ICU)").

---

## Detailed Pattern Breakdown

### Check 1: Specialty Category Billing Fraud (IPD)
* **What it Detects**: Identifies "Type-3" facilities—specifically dental clinics, diagnostic laboratories, and polyclinics—that are illicitly billing for inpatient (IPD) admissions. Since these facilities lack the infrastructure for overnight admissions, all such claims represent a severe policy violation.
* **Tables Used**: `claim_intimation`, `office_master`, `claim_submission`
* **Filtering Logic**: `om.OM_HOSP_TYPE IN ('3', '4', '7')` AND `ci.CI_PATIENT_TYPE = 'I'`.
* **Output Metrics**: Hospital Name, Type, State, IPD Claims, Claimed Amt, Ded. %.

### Check 2: NABH Accreditation & High Deduction Anomalies
* **What it Detects**: Evaluates the gap between claimed amounts and approved amounts (deduction percentage). NABH-accredited facilities should theoretically adhere to strict billing guidelines and show low deductions. Hospitals with an NABH status but an overall deduction rate exceeding 15% are flagged for predatory over-billing or unbundled charging.
* **Tables Used**: `claim_intimation`, `office_master`, `claim_submission`
* **Filtering Logic**: `om.OM_NABH = 'Y'` AND overall `deduction_pct > 15.0`.
* **Output Metrics**: Hospital Name, Claims, Claimed (Lakh), Approved (Lakh), Ded. %.

### Check 3: Services Outside Empaneled Scope
* **What it Detects**: Cross-references the actual IPD claims filed against the official ECHS empanelment registry. It flags hospitals filing IPD claims that do not possess any empanelled service containing terms like "IPD", "Indoor", or "Inpatient".
* **Tables Used**: `claim_intimation`, `office_master`, `empanel_hospital_service`, `empanel_facility`, `claim_submission`
* **Filtering Logic**: The `GROUP_CONCAT` of all empaneled services per hospital is checked. If it `NOT LIKE '%IPD%'` and `NOT LIKE '%Indoor%'`, the hospital is flagged.
* **Output Metrics**: Hospital Name, IPD Claims, Claimed Amt, Empaneled Services List.

### Check 4: Year-over-Year Billing Spike by Hospital
* **What it Detects**: Calculates the total claim amounts filed by a hospital in the previous year vs. the current year. Identifies facilities showing an explosive (>100%) annual growth in revenue, which often signals an aggressive change in billing tactics or newly established fraud operations.
* **Tables Used**: `claim_intimation`, `claim_submission`, `office_master`
* **Filtering Logic**: `curr_yr_amt > prev_yr_amt * 2` (100% Growth).
* **Output Metrics**: Prev Yr Amt, Curr Yr Amt, Amt Growth %, Claims Growth %.

### Check 5: High-Value Claims at Low-Tier Facilities
* **What it Detects**: Highlights Type-3 and low-tier specialist facilities submitting individual claims with an exceptionally high value (e.g., > ₹1,000,000 / 1 Lakh). This suggests massive bill fabrication or upcoding for out-patient procedures.
* **Tables Used**: `claim_intimation`, `claim_submission`, `office_master`
* **Filtering Logic**: `cs.CS_GR_CLAIM_AMT > 100000` AND `om.OM_HOSP_TYPE IN ('3', '4', '7')`.
* **Output Metrics**: High Val Claims, Max Single Claim, Total Claimed.

---

## Report Generation Architecture
The final PDF (`ECHS_Hospital_Specialty_Misuse_Report_YYYYMMDD_HHMMSS.pdf`) mirrors the established reporting framework standard:
* **Total Exposure Calculation**: Accurately aggregates the financial exposure across all flagged facilities in Indian Rupees (₹ Crores/Lakhs).
* **High-Fidelity PDF Generation**: The `generate_module12_report.py` script filters outliers (e.g., ignoring 0-value claims), handles missing database constraints (converting `NULL` empanelled entries to "No Empaneled Services"), and injects professional `Navy/Gold` CSS styling dynamically before rendering the HTML into a secure, RESTRICTED PDF via WeasyPrint.
