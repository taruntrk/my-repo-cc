# ECHS Module 20 Forensic Analysis Summary (2021–2026)

This document serves as the final saved summary of the forensic audit reporting configuration for Module 20: Budget Impact & Leakage Estimation.

---

## 1. Key Metrics & Financial Results (FY 2021–2026)
* **Total Claims Scanned:** 19,845,384 claims
* **Total Claimed Budget:** ₹36,261.44 Cr
* **Total Approved ECHS Budget:** ₹32,649.03 Cr
* **Prevented Leakage (Audit Deductions):** ₹3,612.41 Cr (intercepted savings)
* **Realized Leakage (Approved Fraud):** ₹3,225.01 Cr (**9.88% slippage rate** of the approved budget)

### Granular 8-Pattern Breakdown:
1. **Corporate Overbilling:** ₹22.25 Cr realized leakage across 15 high-volume private hospital chains.
2. **Ping-Pong Readmissions:** ₹60.03 Cr realized leakage from discharging/admitting same patients within 48 hours.
3. **Weekend Emergency Surge:** ₹3,097.47 Cr realized leakage via elective procedures booked on weekends.
4. **Superman Surgeon:** ₹6.56 Cr realized leakage from single doctors billed for >15 surgeries per day.
5. **Threshold Avoiding (₹99k Trick):** ₹22.97 Cr realized leakage from bills priced exactly at ₹99,000–₹99,999 to bypass CFA approvals.
6. **Individual Card Sharing:** ₹4.82 Cr realized leakage (same-day multi-hospital admission under single card ID).
7. **Family Card Sharing:** ₹8.44 Cr realized leakage (simultaneous dependant abuse under same service number).
8. **Demographic Mismatch:** ₹37.99 Cr realized leakage from impossible profiles (e.g. Male registered as Wife or Mother).

---

## 2. Saved Forensic Deliverables (PDF paths)
* **Executive Leakage Report (HTML/WeasyPrint PDF):** `/home/tarun/Downloads/CC/echs_analysis/module_20/final_report/ECHS_Module20_Leakage_Report_*.pdf`
* **Main Budget Leakage Report (ReportLab PDF):** `/home/tarun/Downloads/CC/echs_analysis/module_20/reports/ECHS_Module20_Budget_Leakage_Report.pdf`
* **Forensic Explanations Guide (Hindi/English PDF):** `/home/tarun/Downloads/CC/echs_analysis/module_20/final_explanation/ECHS_Fraud_Explanations.pdf`

---

## 3. Core Database Detection Logic
* **Pattern 6 (Card-Sharing):** Self-join on `card_id` matching same `admission_date` but different `hospital_id`.
* **Pattern 7 (Family Sharing):** Self-join on `service_no` matching same `admission_date` but different patient names.
* **Pattern 8 (Demographics Mismatch):** Matches gender against impossible relationships: `(gender='M' AND relationship IN ('Wife', 'Mother', 'Daughter'))` OR `(gender='F' AND relationship IN ('Husband', 'Father', 'Son'))`.
