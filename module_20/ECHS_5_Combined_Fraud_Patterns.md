# ECHS Module 20: 5 Consolidated Fraud & Leakage Patterns

This document outlines the **5 Consolidated Fraud and Leakage Patterns** created by mapping and merging all categories and sub-items from `ECHS_Fraud_Leakage_Patterns.docx`.

---

### **Overview of the 5 Combined Patterns**

1. **Pattern 1: Beneficiary & Dependency Abuse (Card/Profile Misuse)**
2. **Pattern 2: Systematic Provider Abuse & Collusion (Hospital-Level & Network Fraud)**
3. **Pattern 3: Doctor-Level & Clinical Anomaly (Doctor-Level)**
4. **Pattern 4: Claim Manipulation & Billing Evasion (Claim-Level)**
5. **Pattern 5: Temporal Surge & Referral Bypass (Temporal Patterns)**

---

### **Detailed Mapping & Breakdown of All Sub-Items**

#### **Pattern 1: Beneficiary & Dependency Abuse (Card/Profile Misuse)**
* **Sub-items covered from DOCX:**
  - *Excessive utilization compared to peers* (Beneficiary-Level)
  - *Hospital shopping* - multiple hospitals in short period (Beneficiary-Level)
  - *Repeat procedures in clinically unlikely intervals* (Beneficiary-Level)
  - *Claims after beneficiary death* (Beneficiary-Level)
  - *Unusual claim growth year-over-year* (Beneficiary-Level)
  - *High-cost patient outliers* (Beneficiary-Level)
  - *Multiple service numbers linked to same beneficiary/family* (Dependency/Card Misuse)
  - *Dependent appearing under multiple memberships* (Dependency/Card Misuse)
  - *Shared contact details across many beneficiaries* (Dependency/Card Misuse)
  - *Duplicate beneficiary records* (Dependency/Card Misuse)
  - *Demographic Mismatch* (e.g. Male registered as Wife or Mother)
* **Real-Life Example (Hindi):** Ek hi beneficiary multiple cards banwa kar alag-alag hospitals se ek hi time par treatment claim karta hai (Hospital shopping), ya patient ke expire hone ke baad bhi unke card se medicines and treatment continue bill hoti rehti hai.
* **Policy Violation:** Direct violation of ECHS Smart Card eligibility guidelines and beneficiary identity verification protocols.
* **Database Logic:** 
  - Self-join on `claim_intimation` where `CI_CARD_ID` matches but `CI_ADMISSION_DATE` is identical and `CI_HOSPITAL_ID` is different.
  - Matches `CI_SEX = 'M'` against `RM_RELATION_NAME IN ('Wife', 'Mother', 'Daughter')`.

---

#### **Pattern 2: Systematic Provider Abuse & Collusion (Hospital-Level & Network Fraud)**
* **Sub-items covered from DOCX:**
  - *High claim amount outlier hospitals* (Hospital-Level)
  - *Package upcoding* (Hospital-Level)
  - *Unusual approval rates* (Hospital-Level)
  - *Consistently high UTI cuts/deductions* (Hospital-Level)
  - *Inflated diagnostics and investigations* (Hospital-Level)
  - *Excessive admissions compared to peers* (Hospital-Level)
  - *Procedure mix anomalies* (Hospital-Level)
  - *Hospital-doctor-beneficiary referral loops* (Network Fraud)
  - *Clusters of beneficiaries using same providers* (Network Fraud)
  - *Organized claim generation networks* (Network Fraud)
  - *Provider collusion patterns* (Network Fraud)
* **Real-Life Example (Hindi):** Kisi specific hospital chain me achanak certain costly surgeries (jaise Angioplasty) ke numbers abnormal levels par badh jaate hain (Procedure mix anomaly/excessive admissions) aur ek hi patient-doctor group ke beech lagatar claims rotate hote hain (Referral loops).
* **Policy Violation:** Empanelment MoU, billing codes, and pre-agreed ECHS tariff package rates guideline violation.
* **Database Logic:** 
  - Scan `hosp_exp_det` for outlier package rate billing where `HED_CLAIM_AMOUNT > HED_ACT_RATE` by more than 50%.
  - Detect referral clusters where `CI_HOSPITAL_ID`, `CS_TREAT_DOCT`, and `CI_BENF_ID` have high repeating co-occurrences.

---

#### **Pattern 3: Doctor-Level & Clinical Anomaly (Doctor-Level)**
* **Sub-items covered from DOCX:**
  - *Procedure frequency outliers* (Doctor-Level)
  - *Excessive diagnostics ordered by provider* (Doctor-Level)
  - *Unusually high admission recommendations* (Doctor-Level)
  - *High-cost treatment bias* (Doctor-Level)
  - *Superman Surgeon* (Single doctor conducting $\ge 15$ surgeries in a day)
* **Real-Life Example (Hindi):** Ek hi treating doctor daily clinic hours me 20-30 patients ki surgeries/investigations prescribe aur perform dikhata hai jo ki impossible hai (Doctor Cloning / Superman Surgeon).
* **Policy Violation:** MCI Code of Medical Ethics and ECHS professional billing guidelines.
* **Database Logic:** 
  - Group `claim_submission` by `CS_TREAT_DOCT` and `CS_ADMISSION_DATE`, filtering for count of surgeries (`CS_INTIMATION_ID`) $\ge 15$.

---

#### **Pattern 4: Claim Manipulation & Billing Evasion (Claim-Level)**
* **Sub-items covered from DOCX:**
  - *Exact duplicate claims* (Claim-Level)
  - *Near-duplicate claims* (Claim-Level)
  - *Split billing / Threshold Avoiding* (Claim-Level)
  - *Inflated billing* (Claim-Level)
  - *Ineligible reimbursement items* (Claim-Level)
  - *Suspicious resubmissions after rejection* (Claim-Level)
* **Real-Life Example (Hindi):** CFA vetting audit bypass karne ke liye (jo ₹1 Lakh se upar hota hai) ek hi admission treatment bill ko ₹99,800 aur ₹40,000 ke do separate bills (split-billing) me split karke auto-approval route me bheja jata hai.
* **Policy Violation:** Splitting of bills to evade financial delegation of powers (CFA vetting thresholds).
* **Database Logic:** 
  - Filter `claim_submission` where `CS_NET_CLAIM_AMT` is between `99000` and `99999` and group by hospital to find anomalies.
  - Self-join on `claim_submission` for duplicate `CS_INTIMATION_ID` or same patient, same hospital, within 48 hours.

---

#### **Pattern 5: Temporal Surge & Referral Bypass (Temporal Patterns)**
* **Sub-items covered from DOCX:**
  - *Month-end spikes* (Temporal Patterns)
  - *Financial year-end spikes* (Temporal Patterns)
  - *Holiday-period anomalies* (Temporal Patterns)
  - *Sudden claim bursts after policy changes* (Temporal Patterns)
  - *Weekend elective surges* (Scheduling surgeries on weekends via emergency route to bypass referral checks)
* **Real-Life Example (Hindi):** Month-end aur financial year-end par target complete karne ke liye hospital elective procedures ko achanak badha deta hai, ya phir Friday night ko checkup bypass karne ke liye "emergency route" se elective surgery show karke admit kiya jata hai.
* **Policy Violation:** Emergency bypass guidelines and referral validation protocols.
* **Database Logic:** 
  - Filter `claim_intimation` where `DAYOFWEEK(CI_ADMISSION_DATE) IN (1, 7)` (Sunday and Saturday) and `CI_REF_TYPE_ID` is marked as 'Emergency'.

---

### **Calculated Metrics & Analytics Integration**
The remaining sections from the DOCX (**8. Budget Impact Metrics** and **9. Predictive Analytics**) will be generated as part of our dashboard KPIs and forecasting outputs:
- **Fraud Leakage % & Recoverable Leakage** (Standard KPIs on cover and summary pages)
- **Hospital and Beneficiary Risk Scores** (Calculated based on weightages of Patterns 1-5)
- **Claim Expenditure Forecasting & Future Budget Requirement Estimation** (Time series analysis integrated into the report)
