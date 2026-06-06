# Module 11: Identity Fraud & Duplicate Claim Detection Analysis — Technical Documentation

## Overview
Module 11 is designed to detect physical identity fraud, ghost billing, synthetic identity creation, and over-utilisation within the ECHS (Ex-Servicemen Contributory Health Scheme) database. The framework processes over 26 million records from the last five years (FY 2021–2026) to generate high-fidelity, actionable insights.

---

## Database Tables Utilized
The module relies on the following core ECHS database tables:
1. **`beneficiary_details`**: Contains demographic information, ECHS card numbers, mobile numbers, Aadhaar (UID), and service numbers of the beneficiaries.
2. **`claim_intimation` (`ci`)**: The primary table recording the start of a hospital admission or OPD visit. Key fields include `CI_CR_DATE` (creation date), `CI_DATE_OF_ADMISSION`, and `CI_PATIENT_TYPE`.
3. **`claim_submission` (`cs`)**: Contains the financial data submitted by hospitals, including `CS_GR_CLAIM_AMT` (Gross Claimed Amount) and `CS_UTI_APP_AMT` (Approved Amount), as well as bill/invoice numbers (`CS_HOSP_BILL_NO`).
4. **`office_master` (`om`)**: Holds metadata about empanelled hospitals, including hospital names and geographical locations.

---

## Detailed Pattern Breakdown

### Check 1: Duplicate Card IDs
* **What it Detects**: A single ECHS card number linked to 3 or more different service numbers (primary ex-serviceman identifiers). This indicates severe physical identity fraud where cards are cloned or shared across unrelated families.
* **Tables Used**: `beneficiary_details`
* **Data Fields**: `card_no`, `service_no`
* **Output Metrics**: Card Number, Number of Linked Service IDs, List of Service IDs.

### Check 2: Simultaneous Admissions
* **What it Detects**: The same beneficiary (same ECHS card) admitted to two different hospitals within a 7-day overlapping window. This is a physical impossibility and strongly indicates "ghost billing" where hospitals use a patient's credentials without them actually being present.
* **Tables Used**: `claim_intimation`, `office_master`
* **Data Fields**: `CI_CARD_NO`, `CI_DATE_OF_ADMISSION`, `CI_CR_OFFICE_ID`
* **Output Metrics**: Beneficiary Card, First Hospital, Second Hospital, Admission Dates, Gap in Days (absolute value).

### Check 3: Duplicate Bill Numbers
* **What it Detects**: Identical invoice/bill numbers resubmitted for multiple distinct claims. This represents direct double-billing fraud by the hospital administration.
* **Tables Used**: `claim_intimation`, `claim_submission`, `office_master`
* **Data Fields**: `CS_HOSP_BILL_NO`, `CS_GR_CLAIM_AMT`
* **Output Metrics**: Bill Number, Hospital Name, Number of Times Submitted, Total Claimed Amount associated with the duplicated bills.

### Check 4: Mobile Number Rings
* **What it Detects**: A single mobile number registered across 5 or more completely unrelated ECHS cards (different service numbers). This typically maps to coordinated "fraud agent" rings managing multiple beneficiaries' profiles to siphon funds.
* **Tables Used**: `beneficiary_details`
* **Data Fields**: `mob_no`, `card_no`
* **Output Metrics**: Phone Number, Count of Linked Cards. (Data is split into "Real Numbers" and "Dummy Numbers" e.g., 9999999999).

### Check 5: UID (Aadhaar) Duplication
* **What it Detects**: The exact same 12-digit Aadhaar UID registered under multiple distinct service numbers. Since Aadhaar is biometrically unique, duplication indicates synthetic identity creation.
* **Tables Used**: `beneficiary_details`
* **Data Fields**: `uid_no`, `card_no`
* **Output Metrics**: UID Number, Count of Occurrences.

### Check 6: High Frequency Claims
* **What it Detects**: Beneficiaries with a statistically anomalous number of claims over the 5-year period. The threshold is calculated dynamically using the Interquartile Range (IQR) method (Q3 + 1.5 × IQR), identifying those filing an outlier volume of claims (e.g., 13+ claims).
* **Tables Used**: `claim_intimation`
* **Data Fields**: `CI_CARD_NO`, `CI_INTIMATION_ID`
* **Output Metrics**: Card Number, Total Claims, Median/Q3 context, Statistical Threshold used.

---

## Report Generation Architecture
The final PDF (`ECHS_Identity_Fraud_Report_YYYYMMDD_HHMMSS.pdf`) is generated using a custom Python script leveraging **HTML** and **WeasyPrint**:
* **Input**: Aggregated `.csv` files dumped by the pattern queries.
* **Logic**: Python parses the CSV data, calculates Total Financial Exposure, sorts tables to highlight highest financial risk, and dynamically embeds findings into an HTML template.
* **Rendering**: The HTML uses CSS variables (Navy/Gold scheme), CSS grid layouts, and strict pagination (A4 size, `page-break-before`) to render an immutable, audit-ready PDF.
