# ECHS Module 20: 5-Pattern CSV Extraction & Database Design

This document details the CSV file structure designed to support the **5 Consolidated ECHS Fraud and Leakage Patterns** for the FY 2021–2026 data.

---

### **Pattern 1: Beneficiary & Dependency Abuse (Card/Profile Misuse)**
We will extract **4 CSV files** for this pattern to isolate card abuse and profile discrepancies:

1. **`pat1_beneficiary_misuse_summary.csv`**
   - *Purpose:* Overall aggregates for Pattern 1 to populate KPI dashboard blocks.
   - *Columns:* `total_flagged_claims`, `total_claimed_cr`, `total_approved_cr`, `total_deducted_cr`, `realized_leakage_cr`.
   - *Source Tables:* `claim_intimation`, `claim_submission`, `relation_master`.
2. **`pat1_card_sharing_detail.csv`**
   - *Purpose:* Multi-hospital admissions under the same card ID on the same day.
   - *Columns:* `card_id`, `admission_date`, `patient_name`, `num_hospitals`, `hospitals_visited` (concatenated string), `total_claimed_lakh`, `total_approved_lakh`, `realized_leakage_lakh`.
   - *Source Tables:* Self-join on `claim_intimation` and `claim_submission` where `CI_CARD_ID` is same but `CI_HOSPITAL_ID` is different.
3. **`pat1_demographic_mismatch_detail.csv`**
   - *Purpose:* Gender and relationship conflicts (e.g., Male listed as Wife/Mother).
   - *Columns:* `card_id`, `patient_name`, `gender`, `relationship`, `total_claims`, `total_claimed_lakh`, `total_approved_lakh`, `realized_leakage_lakh`.
   - *Source Tables:* `claim_intimation` and `relation_master` where gender and relationship are mismatched.
4. **`pat1_deceased_beneficiary_claims.csv`**
   - *Purpose:* Claims billed after a beneficiary's date of death.
   - *Columns:* `card_id`, `patient_name`, `date_of_death`, `claim_id`, `admission_date`, `claimed_amount`, `approved_amount`, `realized_leakage`.
   - *Source Tables:* `claim_intimation` joined with `claim_submission` where `CI_ADMISSION_DATE > CS_DOD`.

---

### **Pattern 2: Systematic Provider Abuse & Collusion (Hospital-Level)**
We will extract **3 CSV files** to track hospital-level inflation and network collusion:

1. **`pat2_provider_abuse_summary.csv`**
   - *Purpose:* Overall metrics for Pattern 2.
   - *Columns:* `total_flagged_hospitals`, `total_claims`, `total_claimed_cr`, `total_approved_cr`, `realized_leakage_cr`.
   - *Source Tables:* `settlement_stat`, `office_master`.
2. **`pat2_hospital_leakage_detail.csv`**
   - *Purpose:* Top hospitals ranked by total approved leakage and high deduction rates.
   - *Columns:* `hospital_id`, `hospital_name`, `city`, `nabh_status`, `total_claims`, `total_claimed_lakh`, `total_approved_lakh`, `total_deducted_lakh`, `deduction_pct`, `realized_leakage_lakh`.
   - *Source Tables:* `settlement_stat` joined with `office_master` and `cghs_region_master`.
3. **`pat2_referral_collusion_detail.csv`**
   - *Purpose:* Hospital-doctor-patient co-occurrence clusters showing collusion circles.
   - *Columns:* `hospital_name`, `doctor_name`, `num_claims`, `num_distinct_beneficiaries`, `total_claimed_lakh`, `total_approved_lakh`, `realized_leakage_lakh`.
   - *Source Tables:* `claim_intimation` and `claim_submission` grouped by doctor and hospital.

---

### **Pattern 3: Doctor-Level & Clinical Anomaly (Doctor-Level)**
We will extract **2 CSV files** to monitor doctor billing behavior:

1. **`pat3_doctor_anomaly_summary.csv`**
   - *Purpose:* Overall metrics for Pattern 3.
   - *Columns:* `total_flagged_doctors`, `total_claims`, `total_claimed_cr`, `total_approved_cr`, `realized_leakage_cr`.
   - *Source Tables:* `claim_submission`.
2. **`pat3_superman_surgeon_detail.csv`**
   - *Purpose:* Single doctor performing $\ge 15$ surgeries in a day.
   - *Columns:* `doctor_name`, `admission_date`, `hospital_name`, `surgeries_performed`, `total_claimed_lakh`, `total_approved_lakh`, `realized_leakage_lakh`.
   - *Source Tables:* `claim_submission` joined with `office_master`, grouped by doctor and date.

---

### **Pattern 4: Claim Manipulation & Billing Evasion (Claim-Level)**
We will extract **3 CSV files** to track individual billing bypass techniques:

1. **`pat4_claim_manipulation_summary.csv`**
   - *Purpose:* Overall metrics for Pattern 4.
   - *Columns:* `total_flagged_claims`, `total_claimed_cr`, `total_approved_cr`, `realized_leakage_cr`.
   - *Source Tables:* `claim_submission`.
2. **`pat4_threshold_avoidance_detail.csv`**
   - *Purpose:* ECHS CFA threshold bypass (bills priced exactly at ₹99,000–₹99,999).
   - *Columns:* `hospital_name`, `claim_id`, `admission_date`, `claimed_amount`, `approved_amount`, `realized_leakage`.
   - *Source Tables:* `claim_submission` joined with `office_master` where `CS_NET_CLAIM_AMT` is in the target range.
3. **`pat4_duplicate_claims_detail.csv`**
   - *Purpose:* Duplicate or near-duplicate claims.
   - *Columns:* `patient_name`, `hospital_name`, `claim_id_1`, `claim_id_2`, `admission_date`, `ailment`, `claimed_amount_1`, `claimed_amount_2`, `realized_leakage`.
   - *Source Tables:* Self-join on `claim_submission` where patient and ailment are same but claim IDs differ.

---

### **Pattern 5: Temporal Surge & Referral Bypass (Temporal Patterns)**
We will extract **3 CSV files** to track time-based spikes:

1. **`pat5_temporal_surge_summary.csv`**
   - *Purpose:* Overall metrics for Pattern 5.
   - *Columns:* `total_weekend_claims`, `total_weekday_claims`, `weekend_claimed_cr`, `weekend_approved_cr`, `realized_leakage_cr`.
   - *Source Tables:* `claim_intimation`.
2. **`pat5_weekend_emergency_surge_detail.csv`**
   - *Purpose:* Elective procedures performed on weekends via emergency route.
   - *Columns:* `hospital_name`, `claim_id`, `patient_name`, `admission_date`, `day_of_week`, `ailment`, `claimed_amount`, `approved_amount`, `realized_leakage`.
   - *Source Tables:* `claim_intimation` joined with `claim_submission` where admission is Saturday/Sunday and referral is marked 'Emergency'.
3. **`pat5_monthend_spike_detail.csv`**
   - *Purpose:* Surges in billing in the final 3 days of each month.
   - *Columns:* `hospital_name`, `month_year`, `avg_weekday_admissions`, `avg_monthend_admissions`, `spike_ratio`, `total_approved_lakh`, `realized_leakage_lakh`.
   - *Source Tables:* `claim_intimation` grouped by month and hospital.
