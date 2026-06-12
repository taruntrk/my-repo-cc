# ECHS Module 20: 5-Pattern Complete Data Extraction Plan (2021–2026)

This document contains the step-by-step extraction plan for all 5 Consolidated Fraud and Leakage Patterns. We will create a separate folder for each pattern and extract comprehensive combined sheets detailing the anomalous cases.

---

## Folder Structure to be Created
We will create these folders under `/home/tarun/Downloads/CC/echs_analysis/module_20/`:
* `pattern_1_beneficiary_abuse/`
* `pattern_2_provider_abuse/`
* `pattern_3_doctor_anomaly/`
* `pattern_4_claim_manipulation/`
* `pattern_5_temporal_surge/`

---

## Detailed Column & Schema Specification for Each CSV

### **1. Pattern 1: Beneficiary & Dependency Abuse (Card/Profile Misuse)**
We will extract **3 detailed sheets** into the `pattern_1_beneficiary_abuse/` folder.

#### **A. Card Sharing Details (`pattern_1_beneficiary_abuse/card_sharing_details.csv`)**
* **Goal:** Identify single card IDs admitted to multiple hospitals on the same day.
* **Columns to Extract:**
  1. `card_id` (Smart Card ID)
  2. `admission_date` (Date of Admissions)
  3. `patient_name` (Patient Name)
  4. `hospital_1_id` (First Hospital ID)
  5. `hospital_1_name` (First Hospital Name)
  6. `hospital_1_city` (First Hospital City)
  7. `hospital_2_id` (Second Hospital ID)
  8. `hospital_2_name` (Second Hospital Name)
  9. `hospital_2_city` (Second Hospital City)
  10. `claim_1_id` (First Claim ID)
  11. `claim_2_id` (Second Claim ID)
  12. `claim_1_amt` (Claimed Amount 1)
  13. `claim_2_amt` (Claimed Amount 2)
  14. `approved_1_amt` (Approved Amount 1)
  15. `approved_2_amt` (Approved Amount 2)
  16. `ailment_1` (Ailment 1)
  17. `ailment_2` (Ailment 2)
  18. `realized_leakage` (Approved amount representing fraud)
* **SQL Query Logic:** Self-join `claim_intimation` `ci1` and `ci2` on `ci1.CI_CARD_ID = ci2.CI_CARD_ID` where `ci1.CI_ADMISSION_DATE = ci2.CI_ADMISSION_DATE` AND `ci1.CI_HOSPITAL_ID != ci2.CI_HOSPITAL_ID`.

#### **B. Demographic Mismatch Details (`pattern_1_beneficiary_abuse/demographic_mismatch_details.csv`)**
* **Goal:** Identify gender and relationship discrepancies (impossible profiles).
* **Columns to Extract:**
  1. `card_id` (Smart Card ID)
  2. `beneficiary_name` (Registered Beneficiary Name)
  3. `patient_name` (Patient Name)
  4. `gender` (Registered Gender - M/F)
  5. `relationship` (Relationship - Wife, Mother, Daughter, Husband, Father, etc.)
  6. `claim_id` (Claim ID)
  7. `admission_date` (Admission Date)
  8. `hospital_name` (Hospital Name)
  9. `claimed_amount` (Claimed Amount)
  10. `approved_amount` (Approved Amount / Realized Leakage)
  11. `anomaly_type` (Male as Female Relation / Female as Male Relation)
* **SQL Query Logic:** Join `claim_intimation` with `relation_master` where `(CI_SEX = 'M' AND RM_RELATION_NAME IN ('Wife', 'Mother', 'Daughter', 'Sister'))` OR `(CI_SEX = 'F' AND RM_RELATION_NAME IN ('Husband', 'Father', 'Son', 'Brother'))`.

#### **C. Deceased Beneficiary Details (`pattern_1_beneficiary_abuse/deceased_beneficiary_details.csv`)**
* **Goal:** Identify claims billed after the beneficiary's recorded date of death.
* **Columns to Extract:**
  1. `card_id` (Smart Card ID)
  2. `patient_name` (Patient Name)
  3. `date_of_death` (Date of Death in system)
  4. `claim_id` (Claim ID)
  5. `admission_date` (Admission Date)
  6. `discharge_date` (Discharge Date)
  7. `hospital_name` (Hospital Name)
  8. `treating_doctor` (Doctor Name)
  9. `claimed_amount` (Claimed Amount)
  10. `approved_amount` (Approved Amount / Realized Leakage)
* **SQL Query Logic:** Join `claim_intimation` and `claim_submission` where `ci.CI_ADMISSION_DATE > cs.CS_DOD`.

---

### **2. Pattern 2: Systematic Provider Abuse & Collusion (Hospital-Level)**
We will extract **2 detailed sheets** into the `pattern_2_provider_abuse/` folder.

#### **A. Hospital Leakage Ranking (`pattern_2_provider_abuse/hospital_leakage_ranking.csv`)**
* **Goal:** Identify and rank empanelled hospitals by total claim count, deduction rates, and realized leakage.
* **Columns to Extract:**
  1. `hospital_id` (Hospital ID)
  2. `hospital_name` (Hospital Name)
  3. `city` (CGHS City)
  4. `state` (State)
  5. `hosp_type` (NABH/Non-NABH, Private/Public)
  6. `total_claims` (Total claims 2021-2026)
  7. `total_claimed_cr` (Total Claimed in Cr)
  8. `total_approved_cr` (Total Approved in Cr)
  9. `total_deducted_cr` (Total Deducted in Cr)
  10. `deduction_pct` (Deduction Rate %)
  11. `realized_leakage_cr` (Estimated realized leakage)
* **SQL Query Logic:** Aggregate sums of claims, claimed, and approved amounts from `settlement_stat` grouped by hospital ID.

#### **B. Referral Collusion Rings (`pattern_2_provider_abuse/referral_collusion_rings.csv`)**
* **Goal:** Identify repeating hospital-doctor-patient rings that channel claims.
* **Columns to Extract:**
  1. `hospital_name` (Hospital Name)
  2. `treating_doctor` (Doctor Name)
  3. `num_claims` (Total claims generated)
  4. `num_distinct_patients` (Number of unique patients treated)
  5. `total_claimed_lakh` (Total Claimed in Lakhs)
  6. `total_approved_lakh` (Total Approved in Lakhs)
  7. `realized_leakage_lakh` (Approved leakage)
* **SQL Query Logic:** Group `claim_submission` and `claim_intimation` by `CI_HOSPITAL_ID` and `CS_TREAT_DOCT`, count unique `CI_BENF_ID`.

---

### **3. Pattern 3: Doctor-Level & Clinical Anomaly (Doctor-Level)**
We will extract **1 detailed sheet** into the `pattern_3_doctor_anomaly/` folder.

#### **A. Superman Surgeon Details (`pattern_3_doctor_anomaly/superman_surgeon_details.csv`)**
* **Goal:** Identify doctors billed for $\ge 15$ surgeries on a single calendar date.
* **Columns to Extract:**
  1. `doctor_name` (Doctor Name)
  2. `admission_date` (Date of surgery)
  3. `hospital_name` (Hospital Name)
  4. `surgeries_performed` (Surgeries in that day)
  5. `total_claimed_lakh` (Total Claimed)
  6. `total_approved_lakh` (Total Approved / Realized Leakage)
* **SQL Query Logic:** Group `claim_submission` by `CS_TREAT_DOCT` and `CS_ADMISSION_DATE`, filter for surgery counts $\ge 15$.

---

### **4. Pattern 4: Claim Manipulation & Billing Evasion (Claim-Level)**
We will extract **2 detailed sheets** into the `pattern_4_claim_manipulation/` folder.

#### **A. Threshold Avoidance Details (`pattern_4_claim_manipulation/threshold_avoidance_details.csv`)**
* **Goal:** Capture bills priced exactly between ₹99,000 and ₹99,999 to avoid manual CFA vetting.
* **Columns to Extract:**
  1. `claim_id` (Claim ID)
  2. `hospital_name` (Hospital Name)
  3. `patient_name` (Patient Name)
  4. `admission_date` (Admission Date)
  5. `ailment` (Procedure/Ailment code)
  6. `claimed_amount` (Claimed amount)
  7. `approved_amount` (Approved amount / Realized Leakage)
  8. `treating_doctor` (Doctor Name)
* **SQL Query Logic:** Filter `claim_submission` where `CS_NET_CLAIM_AMT` is between `99000` and `99999`.

#### **B. Duplicate Claims Details (`pattern_4_claim_manipulation/duplicate_claims_details.csv`)**
* **Goal:** Find identical/duplicate bills (same patient, same hospital, same amount, within 48 hours).
* **Columns to Extract:**
  1. `patient_name` (Patient Name)
  2. `card_id` (Card ID)
  3. `hospital_name` (Hospital Name)
  4. `claim_id_1` (First Claim ID)
  5. `claim_id_2` (Second Claim ID)
  6. `admission_date_1` (First Admission Date)
  7. `admission_date_2` (Second Admission Date)
  8. `claimed_amount` (Claimed Amount)
  9. `approved_amount` (Approved Amount / Realized Leakage)
* **SQL Query Logic:** Self-join `claim_submission` on `CS_BENF_ID` and `CS_NET_CLAIM_AMT` where dates differ by $\le 2$ days.

---

### **5. Pattern 5: Temporal Surge & Referral Bypass (Temporal Patterns)**
We will extract **2 detailed sheets** into the `pattern_5_temporal_surge/` folder.

#### **A. Weekend Emergency Surge (`pattern_5_temporal_surge/weekend_emergency_surge.csv`)**
* **Goal:** Identify elective surgeries admitted as emergencies on Saturday/Sunday.
* **Columns to Extract:**
  1. `claim_id` (Claim ID)
  2. `hospital_name` (Hospital Name)
  3. `patient_name` (Patient Name)
  4. `admission_date` (Admission Date)
  5. `day_of_week` (Saturday/Sunday)
  6. `ailment` (Procedure/Ailment code)
  7. `claimed_amount` (Claimed Amount)
  8. `approved_amount` (Approved Amount / Realized Leakage)
* **SQL Query Logic:** Filter `claim_intimation` where `DAYOFWEEK(CI_ADMISSION_DATE) IN (1, 7)` and `CI_REF_TYPE_ID = 'Emergency'`.

#### **B. Month-End Spike Analysis (`pattern_5_temporal_surge/monthend_spike_analysis.csv`)**
* **Goal:** Capture billing spikes in the final 3 days of each month.
* **Columns to Extract:**
  1. `hospital_name` (Hospital Name)
  2. `month_year` (Month/Year)
  3. `normal_days_avg_claims` (Average claims per day during days 1-27)
  4. `monthend_days_avg_claims` (Average claims per day during final 3 days)
  5. `spike_ratio` (Ratio showing spike)
  6. `extra_monthend_approved_lakh` (Excess approved leakage)
* **SQL Query Logic:** Group claims by day of month and hospital to compute average daily claim counts.
