# ECHS Fraud Analytics — Project Context & Conversation Summary
**Date:** June 5, 2026  
**Prepared by:** Kiro AI (conversation with Tarun)

---

## 1. Project Overview

**ECHS** = Ex-Servicemen Contributory Health Scheme  
**Organization:** IIT Kanpur × ECHS Directorate  
**Purpose:** Fraud detection & budget leakage analysis on ECHS healthcare claims database  
**Database:** ECHS Production DB on `samar.iitk.ac.in` — 26+ million records  
**Connection:** Direct SSH via paramiko (no tunnel needed)

| | Primary | Secondary (Tarun's) |
|---|---|---|
| SSH User | `echs_aman` | `echs_akash` |
| SSH Pass | `aman@2026` | `Akash@2026` |
| DB User | `aman` | `akash` |
| DB Pass | `aman@2026` | `Akash@2026` |
| DB Name | `ECHS` | `ECHS` |

---

## 2. Project Structure

```
/home/tarun/Downloads/CC/echs_analysis/
├── module_11/                  ← Identity Fraud Detection (DONE)
│   ├── data/                   ← 25 CSV files (fraud data)
│   ├── queries/                ← point11_fraud_detection_queries.sql
│   ├── reports/                ← ECHS_Module11_Identity_Fraud_Report.pdf
│   └── generate_module11_report.py
│
├── module_20/                  ← Budget Leakage Analysis (IN PROGRESS)
│   ├── queries/                ← point20_budget_leakage_queries.sql (FIXED)
│   ├── extract_scripts/        ← 6 individual extract scripts (OLD queries)
│   ├── extract_module20_data.py      ← Master extract script (UPDATED)
│   ├── extract_module20_fresh.py     ← NEW: runs 3 fresh queries
│   ├── generate_module20_report.py   ← PDF generator (53KB, ready)
│   └── reports/                ← ECHS_Module20_Budget_Leakage_Report.pdf
│
├── data-tarun/module_20/       ← Extracted CSVs for Module 20
├── ECHS_schema_full.sql        ← Full DB schema
├── ECHS_schema_only.sql        ← Schema without data
├── echs_db_metadata.json       ← All table metadata (527KB)
└── Point11_Fraud_Detection_Complete_Data.json  ← Module 11 JSON (8MB)
```

---

## 3. Module 11 — Identity Fraud Detection (COMPLETED)

### Status: ✅ DONE

### What was built:
- 10 fraud pattern SQL queries on `claim_intimation` + `claim_submission` tables
- 8 patterns returned data, 2 returned zero results
- All data extracted to CSV with full descriptive info
- PDF report generated: `ECHS_Module11_Identity_Fraud_Report.pdf`

### Results:
- **Total Cases:** 4,006 flagged (500 per pattern)
- **Financial Exposure:** ₹796.67 Crores (estimated)
- **Analysis Period:** 2021–2026 (last 5 years)

### 8 Fraud Patterns Detected:

| # | Pattern | Severity | Cases |
|---|---------|----------|-------|
| 01 | Duplicate Card IDs | CRITICAL | 500 |
| 02 | Simultaneous Admissions | CRITICAL | 500 |
| 03 | Duplicate Bill Numbers | HIGH | 500 |
| 04 | Mobile Number Rings | HIGH | 500 |
| 05 | UID (Aadhaar) Duplication | CRITICAL | 500 |
| 06 | Post-Death Claims (Lazarus) | CRITICAL | 500 |
| 07 | Chronic Stay (90+ days) | HIGH | 506 |
| 08 | High Frequency Claims (10+) | HIGH | 500 |

### Patterns with NO data:
- Pattern 09: Impossible Dependent Claims → 0 results
- Pattern 10: Doctor Teleportation → 0 results (but CSV exists with some data)

### Module 11 CSV files (in `module_11/data/`):
```
01_Duplicate_Card_IDs.csv        (533 KB)
02_Simultaneous_Admissions.csv   (138 KB)
03_Duplicate_Bill_Numbers.csv    (2.2 MB)
04_Mobile_Number_Rings.csv       (431 KB)
05_UID_Duplication.csv           (444 KB)
06_Post_Death_Claims_Lazarus.csv (122 KB)
07_Chronic_Stay_Forever_Patient.csv (99 KB)
08_High_Frequency_Claims.csv     (185 KB)
10_Doctor_Teleportation.csv      (1.5 MB)
+ several older/anecdotal CSVs
```

### Module 11 Data Structure (every CSV has):
- Hospital ID, Name, City, State
- Service Number, Card Number, Beneficiary Name, Rank, Service Type
- Patient Name, Age, Gender, Relationship
- Claim ID, Admission Date, Discharge Date, Stay Duration
- Bill Number, Claimed Amount, Approved Amount
- Treating Doctor, Ailment, Claim Stage/Status

### Known Issue — Hospital Names "Unknown":
- `CI_HOSPITAL_ID` (e.g., `fortis@D1`) doesn't match `office_master.OM_OFFICE_ID`
- **Workaround used:** `CI_CR_OFFICE_ID` (not `CI_HOSPITAL_ID`) → matches `OM_OFFICE_ID` ✅
- Note in schema: "Use `CI_CR_OFFICE_ID`, NOT `CI_HOSPITAL_ID`"

### Module 11 Execution Time (actual log):
```
Query 01 (Duplicate Cards):    4 min 57 sec
Query 02 (Simultaneous):       0 min 58 sec
Query 03 (Duplicate Bills):    3 min 46 sec
Query 04 (Mobile Rings):       4 min 49 sec
Query 05 (UID Duplication):    1 min 04 sec
Query 06 (Post-Death):         3 min 23 sec
Query 07 (Chronic Stay):       2 min 43 sec
Total:                         ~28 minutes
```

### Report Fixes Applied:
- Pattern numbering gap fixed: was 1,2,3,4,5,8 → now 1,2,3,4,5,6
- HTML tags visible in PDF → fixed with inline Paragraph styling
- Currency "n796.67" → "₹796.67" fixed
- Pattern 2 amount columns (all zeros) → auto-hidden

---

## 4. Module 20 — Budget Leakage Analysis (IN PROGRESS)

### Status: ⚠️ Partially Done — Data extracted, queries fixed, ready to re-run

### Focus:
- Module 11 = **WHO** is committing identity fraud
- Module 20 = **WHERE** is budget leaking (hospital billing deductions)

### Primary Table: `settlement_stat`
```sql
SS_YEAR, SS_MONTH, SS_FY_YEAR     -- time dimensions
SS_REGION_ID, SS_OFFICE_ID        -- location (hospital)
SS_PAT_TYPE_ID, SS_ENTITY_ID      -- patient type
SS_GENDER, SS_RELATION_ID         -- demographics
SS_ROOM_CATG                       -- room category
SS_CLAIM_CNT                       -- number of claims
SS_CLAIM_AMT                       -- total claimed amount
SS_APPR_AMT                        -- approved amount
SS_DED_AMT                         -- deducted amount (leakage)
```

### Module 20 existing CSVs (already extracted, in `data-tarun/module_20/`):
```
overall_leakage_summary.csv        ✅ Good
annual_expenditure_trend.csv       ✅ Good (FY 2021-2025)
hospital_type_nabh_leakage.csv     ⚠️ Type codes only (M,N,1,2...)
hospital_leakage_summary.csv       ✅ Good (hospital names present)
regional_deduction_breakdown.csv   ⚠️ Broken — "Region 29", "Region 27" (no names)
fraud_projection_summary.csv       ✅ Good
```

### Key Numbers from Existing Data:
- **Total Claims:** 19.8 Crore (FY 2021-2025)
- **Total Claimed:** ₹36,261 Crores
- **Total Deducted:** ₹3,612 Crores
- **Deduction Rate:** 9.96%
- **Worst Hospital:** VIJAY HOSPITAL [ID: 3149] — 34% deduction rate, ₹149 Cr deducted
- **Worst Region:** JAIPUR (Region 8) — 17.09% deduction rate
- **Worst Type:** Type M hospitals — 23.82% deduction rate

### Annual Trend:
| FY | Claims | Claimed (Cr) | Deduction % |
|----|--------|--------------|-------------|
| 2021 | 24.3L | 4163 | 11.39% |
| 2022 | 35.0L | 6039 | 9.23% |
| 2023 | 53.3L | 9088 | 8.66% |
| 2024 | 52.7L | 10351 | 10.07% |
| 2025 | 33.1L | 6618 | 11.36% (partial year) |

---

## 5. Module 20 Query Issues Found & Fixed

### Problem 1: CAST AS UNSIGNED (risky)
```sql
-- OLD (wrong):
LEFT JOIN office_master om ON CAST(ss.SS_OFFICE_ID AS UNSIGNED) = CAST(om.OM_OFFICE_ID AS UNSIGNED)

-- FIXED (Module 11 pattern):
LEFT JOIN office_master om ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
```

### Problem 2: `ecs_region` table — incomplete data
```sql
-- OLD (broken — Region 29, Region 27 etc.):
LEFT JOIN ecs_region er ON CAST(ss.SS_REGION_ID AS UNSIGNED) = CAST(er.ER_REGION_ID AS UNSIGNED)

-- FIXED (Module 11 proven chain):
LEFT JOIN office_master om       ON ss.SS_OFFICE_ID = om.OM_OFFICE_ID
LEFT JOIN cghs_region_master crm ON om.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
LEFT JOIN state_master sm        ON crm.CRM_STATE_ID = sm.SM_STATE_ID
```

### Problem 3: Missing related data
- Senior said: "3-4 tables ka data mix karo"
- Meaning: Don't just pull numbers — pull hospital name, city, state, type in same query
- Fixed in Q04: added `city`, `state`, `pincode`, `nabl_status` columns
- Added Q07: claim-level detail from `claim_intimation` + `claim_submission`
- Added Q08: gender + relationship breakdown from `relation_master`

---

## 6. Module 20 — Final 8 Queries (in `queries/point20_budget_leakage_queries.sql`)

| Query | Name | Tables Used |
|-------|------|-------------|
| Q01 | Overall Leakage Summary | settlement_stat |
| Q02 | Annual Expenditure Trend | settlement_stat |
| Q03 | Hospital Type + NABH Leakage | settlement_stat + office_master |
| Q04 | Hospital-wise Leakage Detail | settlement_stat + office_master + cghs_region_master + state_master |
| Q05 | Regional Breakdown (FIXED) | settlement_stat + office_master + cghs_region_master + state_master |
| Q06 | Fraud Projections | settlement_stat |
| Q07 | Claim-level Detail (Top 25 Hospitals) | claim_intimation + claim_submission + office_master + cghs_region_master + state_master |
| Q08 | Gender + Relation Leakage | settlement_stat + relation_master |

---

## 7. Module 20 JOIN Chain (Correct — from Schema)

```
settlement_stat.SS_OFFICE_ID
    → office_master.OM_OFFICE_ID          (string match, no CAST)
        → office_master.OM_OFFICE_CGHS_CITY_ID
            → cghs_region_master.CRM_CITY_ID
                → cghs_region_master.CRM_STATE_ID
                    → state_master.SM_STATE_ID
```

Key column names confirmed from schema:
- `office_master.OM_OFFICE_CGHS_CITY_ID` (NOT `OM_CGHS_CITY_ID`)
- `cghs_region_master.CRM_CITY_ID`, `CRM_CITY_NAME`, `CRM_STATE_ID`
- `state_master.SM_STATE_ID`, `SM_STATE_NAME`

---

## 8. Module 20 — Pending Work

### What needs to be done:
1. **SSH tunnel start** karo (port 3307)
2. **Run extraction script:**
   ```bash
   python3 /home/tarun/Downloads/CC/echs_analysis/module_20/extract_module20_fresh.py
   ```
   This runs 3 queries and saves:
   - `regional_deduction_breakdown.csv` (re-run with fixed join)
   - `high_deduction_hospital_claims.csv` (new)
   - `gender_relation_leakage.csv` (new)

3. **OR run full master script** for all 8 queries:
   ```bash
   python3 /home/tarun/Downloads/CC/echs_analysis/module_20/extract_module20_data.py
   ```

4. **Then regenerate PDF report:**
   ```bash
   python3 /home/tarun/Downloads/CC/echs_analysis/module_20/generate_module20_report.py
   ```

### Estimated time: 15–22 minutes total

---

## 9. Key Database Tables Reference

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `claim_intimation` | Individual claim records | `CI_INTIMATION_ID`, `CI_SERVICE_NO`, `CI_CARD_ID`, `CI_CR_OFFICE_ID`, `CI_ADMISSION_DATE` |
| `claim_submission` | Bill/amount details | `CS_INTIMATION_ID`, `CS_NET_CLAIM_AMT`, `CS_UTI_APP_AMT`, `CS_DOD`, `CS_BILL_NO` |
| `settlement_stat` | Monthly aggregated stats | `SS_FY_YEAR`, `SS_OFFICE_ID`, `SS_CLAIM_AMT`, `SS_APPR_AMT`, `SS_DED_AMT` |
| `office_master` | Hospital details | `OM_OFFICE_ID`, `OM_OFFICE_NAME`, `OM_HOSP_TYPE`, `OM_NABH`, `OM_OFFICE_CGHS_CITY_ID` |
| `cghs_region_master` | City/region names | `CRM_CITY_ID`, `CRM_CITY_NAME`, `CRM_STATE_ID` |
| `state_master` | State names | `SM_STATE_ID`, `SM_STATE_NAME` |
| `benf_master_live` | Beneficiary master | `BM_SERVICE_NO`, `BM_DOB`, `BM_FORCE_TYPE` |
| `relation_master` | Relationship types | `RM_RELATION_ID`, `RM_RELATION_DESC` |
| `rank_master` | Rank names | `RM_RANK_ID`, `RM_RANK_NAME` |
| `service_type_master` | Army/Navy/AF etc. | `STM_SERVICE_ID`, `STM_SERVICE_NAME` |

---

## 10. Important Notes

- **Never use `CI_HOSPITAL_ID`** — it has short codes like `fortis@D1` that don't match `office_master`. Always use `CI_CR_OFFICE_ID`.
- **FY 2025 is partial year** — lower claim count (-36% YoY) is expected, not actual decline.
- **`ecs_region` table is incomplete** — many regions have no name. Use `cghs_region_master` chain instead.
- **CAST AS UNSIGNED is risky** — use direct string match for ID joins.
- All amounts in DB are in **rupees (raw)**. Divide by `100000` for Lakhs, `10000000` for Crores.

---

## 11. Report Style Guide (Both Modules)

```
Color Scheme:
  NAVY   #1a2744  → Headers, titles, table headers
  GOLD   #c8a84b  → Accents, pattern labels, cover page
  RED    #cc2222  → CRITICAL severity
  ORANGE #d46a00  → HIGH severity
  GREEN  #1a6e1a  → Success/low risk

Typography:
  Body:   9.5pt Helvetica, 14pt leading
  Tables: 7pt Helvetica
  H1:     16pt Helvetica-Bold (Gold)
  H2:     12pt Helvetica-Bold (Navy)
  Margins: 20mm all sides

Cover Page: Navy background + Gold bands (top/bottom)
Inner pages: header/footer with page number
```

---

*Last updated: June 5, 2026 by Kiro AI*


---

# SESSION 2 UPDATE — June 6, 2026

## Summary of Everything Done This Session

### Step 1 — Module 20 first run (old scripts)
Pehle `extract_module20_data.py` jaisi scripts se 7/8 queries run ki gayi `settlement_stat` pe.  
7 CSVs extract hue, Pattern 07 (individual claims) mein error tha.

**CSVs extracted (first run, `module_20/data/`):**
```
01_overall_leakage_summary_20260606_111109.csv       (1 row — system-wide totals)
02_annual_expenditure_trend_20260606_111118.csv       (5 rows — FY 2021-2025)
03_hospital_type_nabh_leakage_20260606_111123.csv    (type codes M,N,1,2 etc.)
04_hospital_leakage_summary_20260606_111128.csv      (432KB — hospital-wise, GOOD DATA)
05_regional_deduction_breakdown_20260606_111149.csv  (region names fixed via cghs_region_master)
06_fraud_projection_summary_20260606_111155.csv      (projections)
08_gender_relation_leakage_20260606_112156.csv       (gender/relation breakdown)
```
Pattern 07 (individual claims for top hospitals) — **FAILED**, CSV not created.

---

### Step 2 — Problem Identified: Data Comparison
Module 11 CSVs vs Module 20 CSVs compare karne pe problem clear hua:

| | Module 11 CSVs | Module 20 CSVs (old) |
|---|---|---|
| Patient name | ✅ | ❌ |
| Doctor name | ✅ | ❌ |
| Card/Service number | ✅ | ❌ |
| Ailment | ✅ | ❌ |
| Admission/Discharge | ✅ | ❌ |
| Individual claim rows | ✅ | ❌ (sirf aggregated totals) |

**Root cause:** Purani scripts sirf `settlement_stat` use karti thin jo pre-aggregated table hai — individual records hote hi nahi usme.

---

### Step 3 — Scripts Rewritten (`module_20/queries/`)
Har pattern ko `_a` (summary totals) + `_b` (individual claim detail) mein split kiya.

**`_a` queries** → `settlement_stat` + joins → aggregated hospital/region totals  
**`_b` queries** → `claim_intimation` + `claim_submission` + joins → individual claims with full patient/doctor detail (exactly Module 11 jaisa)

**8 scripts written/rewritten:**
```
pattern_01_overall_leakage.py      → 01a system totals  + 01b top 500 claims (all hospitals)
pattern_02_annual_trend.py         → 02a FY-wise totals + 02b top 500 claims (year-wise)
pattern_03_hospital_type_nabh.py   → 03a type+NABH totals + 03b claims from Type M/N/H hospitals
pattern_04_hospital_leakage.py     → 04a hospital totals + 04b claims from top 25 hospitals
pattern_05_regional_breakdown.py   → 05a region totals (proper city+state names) + 05b claims from top 3 regions
pattern_06_fraud_projections.py    → 06a financial projections + 06b highest individual deduction claims
pattern_07_high_deduction_claims.py → 07a top 25 hospital summary + 07b individual claims (500 rows)
pattern_08_gender_relation.py      → 08a gender+relation totals (⚠ _b not yet added)
```

**Pattern 04 logic (two-step):**
1. First query: get top 25 hospital IDs from `settlement_stat`
2. Second query: fetch individual claims from `claim_intimation` WHERE hospital IN (top 25 IDs)

Same two-step approach for patterns 05 (top 3 regions) and 07.

**`_b` columns (same as Module 11):**
```
hospital_id, hospital_name, city, state, hosp_type, nabh_status,
claim_id, service_number, card_number, beneficiary_name, patient_name,
age, gender, relationship, admission_date, discharge_date, stay_days,
ailment, treating_doctor, bill_number, claimed_amount, approved_amount,
deducted_amount, deduction_pct, claim_stage, claim_status
```

---

### Step 4 — What Got Extracted (Second Partial Run)
Only pattern_01 ran successfully (01a CSV created):
```
01a_overall_leakage_summary_20260606_113147.csv   (1 row — totals only, _b errored)
```
Remaining patterns NOT run yet — scripts ready but execution pending.

---

## Current State of `module_20/data/`

```
01_overall_leakage_summary_*.csv        ← old (totals only)
01a_overall_leakage_summary_*.csv       ← new _a run (totals only)
02_annual_expenditure_trend_*.csv       ← old
03_hospital_type_nabh_leakage_*.csv     ← old (type codes, no names)
04_hospital_leakage_summary_*.csv       ← old (432KB, hospital names present)
05_regional_deduction_breakdown_*.csv   ← old (region names present)
06_fraud_projection_summary_*.csv       ← old
08_gender_relation_leakage_*.csv        ← old
```
**Missing (not yet extracted):**
- All `_b` (individual claims) CSVs — `01b`, `02b`, `03b`, `04b`, `05b`, `06b`, `07b`
- Pattern `07` CSV (both _a and _b)

---

## Pending Work

### 1. Run all rewritten scripts (PRIMARY TASK):
```bash
cd /home/tarun/Downloads/CC/echs_analysis
for s in module_20/queries/pattern_0*.py; do echo "=== $s ==="; python3 $s; done
```
Expected output per script: `_a` CSV + `_b` CSV in `module_20/data/`  
Estimated time: ~25-35 minutes total

### 2. Fix pattern_08 — add `_b` individual claims split (minor)

### 3. Regenerate PDF report after fresh CSVs:
```bash
python3 module_20/generate_module20_report.py
```
Note: `generate_module20_report.py` was written for old CSV names — may need updating to pick up new `_a`/`_b` filenames.

---

## Files NOT to Delete

```
module_20/queries/pattern_01_*.py → pattern_08_*.py   ← REWRITTEN (use these, not old scripts)
module_20/queries/point20_budget_leakage_queries.sql  ← keep for reference
module_20/data/*.csv                                   ← all extracted data
module_20/generate_module20_report.py                  ← PDF generator (53KB)
module_20/extract_scripts/                             ← OLD individual scripts (reference only)
module_20/extract_module20_complete.py                 ← OLD master script (reference)
module_11/                                             ← COMPLETED, don't touch
```

*Last updated: June 6, 2026 by Kiro AI*

---

# SESSION 3 UPDATE — June 6, 2026 (continuation)

## Old PDF Report Analysis (reports/Module_20.pdf)

Purani report mein exactly 5 queries thi — sab `settlement_stat` se (aggregated, no individual claims):

| Query | Content |
|---|---|
| Q20a | Annual Expenditure & Deduction Trend (FY 2013-2025) |
| Q20b | Budget Leakage by Hospital Type & NABH Status |
| Q20c | Overall Leakage Summary & Fraud Projections |
| Q20d | Top 25 Hospitals Priority Audit List |
| Q20e | Regional Deduction Breakdown |

**Key findings from old report:**
- Total deducted: ₹5,735 Cr (FY 2013-2025)
- VIJAY HOSPITAL [3149]: 34% deduction rate — worst
- PARK HOSPITAL chain: 7 units, ₹437 Cr combined deductions
- Region 6 (Chennai): 19.13% deduction rate — highest
- Type M hospitals: 25.96% deduction rate
- Type N hospitals: 23.39% deduction rate

## DB Reality Check (June 6, 2026)

| Metric | Value |
|---|---|
| settlement_stat rows | 30.85 lakh |
| settlement_stat FY range | 2013–2025 (2026 nahi hai) |
| claim_intimation (last 5yr) | 2.6 crore rows |
| Claims WITH deduction (2021-2026) | 75.6 lakh rows |
| Hospitals with deductions | 4,188 |

**Year-wise breakdown (claims with deduction):**
- 2021: 7.95 lakh, 2022: 10.42 lakh, 2023: 13.22 lakh
- 2024: 15.52 lakh, 2025: 19.17 lakh, 2026: 9.28 lakh

## Script Architecture (Final Decision)

8 scripts, har ek mein:
- `_a` query → `settlement_stat` FY 2021-2025, aggregated totals (no limit)
- `_b` query → `claim_intimation + claim_submission` joins, YEAR 2021-2026, individual claims

**_b columns (Module 11 jaisa):**
`hospital_id, hospital_name, city, state, hosp_type, nabh_status, claim_id, service_number, card_number, beneficiary_name, rank, service_type, patient_name, age, gender, relationship, admission_date, discharge_date, stay_days, ailment, treating_doctor, bill_number, claimed_amount, approved_amount, deducted_amount, deduction_pct, claim_stage, claim_status`

**Filters per `_b` script:**
- 01b: saare claims with deduction
- 02b: saare claims, year-wise sort
- 03b: Type M/N/H/0 hospitals only
- 04b: top 50 hospitals (by total deduction)
- 05b: top 10 regions
- 06b: claims with >=50% deduction rate
- 07b: top 50 hospitals (same focus as 04b)
- 08b: saare claims, gender+relation sort

## Bug Found & Root Cause

### Problem: `_b` queries return empty output

**Symptom:** `run_query` returns -1 rows, query completes in 0.05-0.3 sec (too fast)

**Root cause identified:** `IN ('3149', '367', ...)` — single quotes around hospital IDs in the IN clause **conflict with single quotes** used around DB password in the mysql command:
```
mysql -u aman -p'aman@2026' ECHS -B
```
Shell interprets the single quotes in `IN ('3149')` as closing the password quote → mysql command breaks silently.

**Fix:** Remove single quotes from IDs in IN clause — use integers directly:
```python
# WRONG:
ids_str = ', '.join(f"'{h}'" for h in ids)
# CORRECT:
ids_str = ', '.join(str(h) for h in ids)
```

**Note:** `CI_CR_OFFICE_ID` is `varchar(6)` in schema but MySQL will auto-cast integers in IN clause for string comparison — this works fine.

### Other fixes applied this session:
1. `run_query(client, sql, label)` → `run_query(sql, label)` — fresh SSH connection per query call
2. `load_dotenv()` → `load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))` — explicit path
3. Removed top-level SSH client from `main()` — each `run_query` call makes its own connection

## Current State of Scripts

- `pattern_04_hospital_leakage.py` — **FIXED** (ids_str uses str(h), fresh connection, correct dotenv path)
- `pattern_01,02,03,05,06,07,08` — **PARTIALLY FIXED** (fresh connection + dotenv fix done, but ids_str fix NOT yet applied to scripts that use IN clause — 05 and 07)

## What Still Needs to Be Done

### 1. Apply ids_str fix to pattern_05 and pattern_07
In `pattern_05_regional_breakdown.py` and `pattern_07_high_deduction_claims.py`:
```python
# Change this line:
ids_str = ', '.join(f"'{r}'" for r in ids)  # or f"'{h}'"
# To:
ids_str = ', '.join(str(x) for x in ids)
```

### 2. Fix remaining scripts that still have old `run_query(client, sql, label)` signature
Scripts 01,02,03,05,06,07,08 still have broken `run_query` from regex fixes — need clean rewrite like pattern_04.

### 3. Run scripts ONE BY ONE, get permission before each:
Order: pattern_04 → pattern_01 → pattern_02 → pattern_03 → pattern_05 → pattern_06 → pattern_07 → pattern_08

### 4. After all CSVs extracted → regenerate PDF report

## Run Command
```bash
cd /home/tarun/Downloads/CC/echs_analysis
python3 module_20/queries/pattern_04_hospital_leakage.py
```

## Files Location
- Scripts: `module_20/queries/pattern_0*.py`
- Data output: `module_20/data/`
- Old PDF: `reports/Module_20.pdf`
