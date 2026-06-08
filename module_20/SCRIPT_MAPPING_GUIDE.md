# ECHS Fraud Analytics: Script Mapping & Audit Guide
This document serves as a guide to explain the technical purpose, analysis connection, and usage status of each script in **Module 20 (Budget Impact & Leakage Analysis)**.

---

## 📂 Directories Reorganized
To keep the new workspace clean and separate from old testing scripts:
* **Production Scripts Location:** `/home/tarun/Downloads/CC/echs_analysis/module_20/new_queries/`
* **Production CSV Data Location:** `/home/tarun/Downloads/CC/echs_analysis/module_20/new_data/`

---

## 📊 Complete Script Mapping Table

| Script Name (Old vs. New) | What the Script Does (Kya Karti Hai) | Connection to Leakage Analysis (Report Connection) | Status & Usage (Use Karenge Ki Nahi?) |
| :--- | :--- | :--- | :--- |
| **Pattern 01**<br>`pattern_01_overall_leakage.py`<br>→ `new_pattern_01_overall_leakage.py` | Calculates system-wide overall leakage metrics and streams overall high-deduction claims (>= 25k). | Establishes overall leakage rates and provides a listing of the worst leakage claims nationwide. | **ACTIVE:** The new script streams **659,564 claims** without limits to `new_data/`. Old script was useless due to `LIMIT 500`. |
| **Pattern 02**<br>`pattern_02_annual_trend.py`<br>→ `new_pattern_02_annual_trend.py` | Computes Year-on-Year expenditure growth trends and streams annual top-deduction claims (>= 20k). | Shows if budget leakage is escalating over time and tracks year-wise worst offenders. | **ACTIVE:** The new script streams **766,652 claims** without limits to `new_data/`. Old script was useless due to `LIMIT 500`. |
| **Pattern 03**<br>`pattern_03_hospital_type_nabh.py`<br>→ `new_pattern_03_hospital_type_nabh.py` | Groups deductions by hospital type and NABH accreditation, streaming all claims for types M, N, H, 0 (>= 10k). | Proves whether unaccredited facilities show higher audit failure/rejection rates. | **ACTIVE:** The new script streams **175,448 claims** without limits to `new_data/`. Old script was useless due to `LIMIT 5000`. |
| **Pattern 04**<br>`pattern_04_hospital_leakage.py`<br>→ `new_pattern_04_hospital_leakage.py` | Extracts **100% of historical claims** (since 2021) for the **Top 50 worst-performing hospitals**. | Pinpoints the exact hospitals driving the highest rejection amounts, exposing overbilling clusters. | **ACTIVE:** Streams **953,195 claims** directly to `new_data/`. Replaces the old, crashed script. |
| **Pattern 05**<br>`pattern_05_regional_breakdown.py`<br>→ `new_pattern_05_regional_breakdown.py` | Extracts **100% of claims** for the **Top 10 highest-deduction regional commands** (duplicate-free). | Exposes geographic fraud rings and regional command hotspots (e.g., Chennai, Delhi commands). | **ACTIVE:** Streams **4,401,707 claims** to `new_data/`. Replaces the old script which caused Cartesian duplication. |
| **Pattern 06**<br>`pattern_06_fraud_projections.py` | Computes financial projections showing how much money could be saved by deploying an AI monitoring system. | Provides the "Return on Investment (ROI)" business case for senior management to justify fraud detection tools. | **USELESS (Do Not Use):** The projection scenarios (30%, 50%, 75%) are fixed mathematical models already written into the report. Running this query again is redundant. |
| **Pattern 07**<br>`pattern_07_high_deduction_claims.py`<br>→ `new_pattern_07_high_deductions.py` | Performs a **two-step streaming extraction** of itemized lines (procedures/drugs) where claim deduction was >= 50k. | Shows exactly which procedures (e.g., "stent", "ICU stay", "implants") are being overbilled and rejected by auditors. | **ACTIVE:** Streams **1,463,130 itemized lines** to `new_data/`. Replaces the old script which had a `LIMIT 5000` cap. |
| **Pattern 08**<br>`pattern_08_gender_relation.py`<br>→ `new_pattern_08_gender_relation.py` | Extracts patient demographic data (gender/relation) for all claims with deductions >= 10,000 INR. | Investigates identity misuse (e.g., card-sharing by dependents) by checking if spouse/children claims drive anomalous rejections. | **ACTIVE:** Streams **1,137,393 claims** directly to `new_data/`. Replaces the old script which had a `LIMIT 5000` cap. |

---

## 💡 Quick Summary for Senior Management
* **Old Py Scripts:** **Useless/Deprecated.** They were built for small testing samples (`LIMIT 500` / `LIMIT 5000`) and cause memory crashes on full production runs.
* **New Py Scripts (Prefix `new_` in `new_queries/`):** **Active & Production-Grade.** They use streaming (line-by-line file writing) and smart database indexing to pull the complete dataset without crashing your system.
* **Analysis Goal:** By running the New scripts (01, 02, 03, 04, 05, 07, 08), we extract a complete forensic view of leakage:
  1. **How much overall leakage?** (Overall national baseline - Pattern 01)
  2. **Is it getting worse?** (YoY Trends - Pattern 02)
  3. **Which facility types are worse?** (NABH vs Non-NABH - Pattern 03)
  4. **Who is billing?** (Top 50 worst hospitals - Pattern 04)
  5. **Where is it happening?** (Top 10 worst regional commands - Pattern 05)
  6. **What is being billed?** (Specific procedure-level rejections - Pattern 07)
  7. **Who is the beneficiary?** (Demographic breakdown of dependents - Pattern 08)
