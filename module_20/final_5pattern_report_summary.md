# ECHS Module 20 Forensic Analysis 5-Pattern Summary (2021–2026)

This document contains the consolidated results of the ECHS Module 20 forensic leakage detection based on the new **5-Pattern Behavioral Taxonomy** from 100% of the claims database (4,401,708 rows scanned).

---

## 1. Key Metrics & Financial Results (Consolidated)

*   **Total Claims Scanned:** 4,401,708 claims
*   **Total Base ECHS Approved Budget:** ₹32,649.04 Cr
*   **Total Prevented Leakage (Deductions):** ₹3,612.41 Cr (intercepted savings)

### **Behavioral Taxonomy Summary Table**

| Pattern ID & Behavioral Category | Flagged Cases | Total Claimed (Cr) | Realized Leakage (Approved Cr) | % of ECHS Approved Budget |
| :--- | :---: | :---: | :---: | :---: |
| **Pattern 1: Beneficiary & Dependency Abuse** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*1a. Card Sharing (Concurrent Admissions)* | 11,137 pairs | ₹161.1992 Cr | ₹118.7812 Cr | 0.3638% |
| &nbsp;&nbsp;&nbsp;&nbsp;*1b. Demographic Relationship Mismatches* | 4,221 claims | ₹30.4055 Cr | ₹24.3962 Cr | 0.0747% |
| &nbsp;&nbsp;&nbsp;&nbsp;*1c. Deceased Beneficiary Lazarus Billing* | 524 claims | ₹0.8452 Cr | ₹0.6425 Cr | 0.0020% |
| **Pattern 2: Systematic Provider Abuse & Collusion** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*2a. Hospital Audit Leakage Ranking* | 19,845,384 claims | ₹36261.4404 Cr | ₹32649.0364 Cr | 100.0000% |
| &nbsp;&nbsp;&nbsp;&nbsp;*2b. Referral Collusion Doctor Rings* | 1,111 rings (338,280 claims) | ₹3125.3824 Cr | ₹2700.7436 Cr | 8.2720% |
| **Pattern 3: Doctor-Level & Clinical Anomaly** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*3a. Superman Surgeons (>=15 surgeries/day)* | 2,193 days (47,433 claims) | ₹445.9941 Cr | ₹265.9742 Cr | 0.8146% |
| **Pattern 4: Claim Manipulation & Billing Evasion** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*4a. CFA Threshold Avoidance (₹99k-99.9k)* | 8,146 claims | ₹81.0528 Cr | ₹68.1289 Cr | 0.2087% |
| &nbsp;&nbsp;&nbsp;&nbsp;*4b. Duplicate Claims (Same patient/amt <=48h)* | 336,512 pairs | ₹534.4805 Cr | ₹351.0236 Cr | 1.0751% |
| **Pattern 5: Temporal Surge & Referral Bypass** | | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;*5a. Weekend Emergency Surge (Sat/Sun)* | 830,866 claims | ₹6181.7782 Cr | ₹4751.7582 Cr | 14.5541% |
| &nbsp;&nbsp;&nbsp;&nbsp;*5b. Month-End Billing Spikes* | 5,975 spikes | - | ₹229.0579 Cr | 0.7016% |

---

## 2. Saved Forensic Deliverables (CSV Paths under data_2/)

* **Pattern 1:**
  - Card Sharing: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1a_card_sharing/pat1a_card_sharing_details.csv`
  - Demographic Mismatch: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1b_demographic_mismatch/pat1b_demographic_mismatch_details.csv`
  - Deceased Beneficiary: `data_2/pattern_1_beneficiary_abuse/sub_pattern_1c_deceased_beneficiary/pat1c_deceased_beneficiary_details.csv`
* **Pattern 2:**
  - Hospital Leakage: `data_2/pattern_2_provider_abuse/sub_pattern_2a_hospital_leakage_ranking/pat2a_hospital_leakage_ranking.csv`
  - Referral Collusion: `data_2/pattern_2_provider_abuse/sub_pattern_2b_referral_collusion_rings/pat2b_referral_collusion_rings.csv`
* **Pattern 3:**
  - Superman Surgeon: `data_2/pattern_3_doctor_anomaly/sub_pattern_3a_superman_surgeon/pat3a_superman_surgeon_details.csv`
* **Pattern 4:**
  - CFA Threshold: `data_2/pattern_4_claim_manipulation/sub_pattern_4a_threshold_avoidance/pat4a_threshold_avoidance_details.csv`
  - Duplicate Bills: `data_2/pattern_4_claim_manipulation/sub_pattern_4b_duplicate_claims/pat4b_duplicate_claims_details.csv`
* **Pattern 5:**
  - Weekend emergency: `data_2/pattern_5_temporal_surge/sub_pattern_5a_weekend_emergency_surge/pat5a_weekend_emergency_surge.csv`
  - Month-End Spike: `data_2/pattern_5_temporal_surge/sub_pattern_5b_monthend_spike/pat5b_monthend_spike_analysis.csv`

---

## 3. Core Refactoring Summary
1. **Consolidation:** The ECHS forensic taxonomy has been streamlined from 8 chaotic leakage tags into 5 behavioral classifications.
2. **Exhaustive Scope:** Removed all `LIMIT` constraints from extraction. Fallback engines now parse 100% of the 1.38 GB claims file.
3. **Audit Nomenclature:** Normalised output files with systematic prefixes (e.g., `pat1a_`, `pat2a_`, `pat5b_`) for complete audit traceability.
