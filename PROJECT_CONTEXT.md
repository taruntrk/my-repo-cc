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
