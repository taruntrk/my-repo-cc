# Module 20 Report - Quick Reference Card

## 📄 Report Details

**File:** `ECHS_Module20_Budget_Leakage_Report.pdf`
**Location:** `/home/tarun/Downloads/CC/echs_analysis/module_20/reports/`
**Status:** ✅ PRODUCTION-READY

---

## 📊 Statistics (FY 2021-2025)

| Metric | Value |
|--------|-------|
| **Total Claims Analyzed** | 1.98+ Crore claims |
| **Financial Exposure (Claimed)** | ₹36,261.45 Crores |
| **Budget Leakage Blocked** | ₹3,612.41 Crores |
| **Overall Deduction Rate** | 9.96% |
| **Analysis Period** | 2021-2025 (5 years) |
| **Key Risk Signals Mapped** | 6 critical risk categories |

---

## 🔍 Six Key Risk Signals

### Signal 01: Deduction Rate Reversal (FY 2024–2025)
- **Type:** CRITICAL
- **Description:** Reversal of historical decline, climbing to 11.36% in FY 2025.
- **Action:** Restore pre-auth rules for claims >₹1 Lakh.

### Signal 02: Park Hospital Chain Concentration
- **Type:** CRITICAL
- **Description:** Multiple Park chain units dominate the absolute deduction list, carrying ₹437 Cr in leakage.
- **Action:** Corporate-level empanelment audit.

### Signal 03: Vijay Hospital Overbilling
- **Type:** CRITICAL
- **Description:** ECHS ID 3149 has an anomalous 34.00% deduction rate (₹149 Cr deducted).
- **Action:** Immediate IPD and discharge summary investigation.

### Signal 04: Facility Type M & N Leakage
- **Type:** CRITICAL
- **Description:** Type M (25.96% deduction) and Type N (23.39% deduction) exceed double the system average.
- **Action:** Mandatory quality audits and renegotiated empanelment terms.

### Signal 05: Regional Fraud Hotspots (Chennai / Jaipur)
- **Type:** HIGH
- **Description:** Chennai Region 6 (19.13%) and Jaipur Region 8 (15.08%) exhibit severe leakage.
- **Action:** Deploy Regional Audit Task Force.

### Signal 06: Quality Accreditation Compliance Gap
- **Type:** HIGH
- **Description:** Non-NABH Type 1 hospitals have 9.87% deduction rate vs 8.24% for accredited facilities.
- **Action:** Transition to mandatory NABH empanelment requirements.

---

## 🎨 Report Design

### Color Scheme
- **Navy Blue (#1a2744):** Primary headers, titles, and table headers
- **Gold (#c8a84b):** Accent panels and pattern badges
- **Red (#cc2222):** Critical severity markings
- **Orange (#d46a00):** High severity markings
- **Green (#1a6e1a):** Low risk / compliance indicators

### Typography
- **Body Text:** 9.5pt Helvetica (14pt leading)
- **Tables:** 7pt - 8pt Helvetica
- **Headers:** 16pt (H1), 12pt (H2), 10pt (H3)
- **Margins:** 20mm margins on all sides

---

## 📑 Report Structure

1. **Cover Page** - Premium Navy/Gold layout with key metric summaries
2. **Executive Summary** - Core narrative analysis, dynamic metrics, and key risk summary table
3. **Annual Expenditure & Trend (Q20a)** - Claims growth, expenditure values, and YoY growth table
4. **Leakage by Hospital Type & NABH (Q20b)** - Empanelment category breakdown table and quality observations
5. **Priority Audit List (Q20d)** - Top 25 hospitals ranked by absolute deductions and target summaries
6. **Regional Breakdown (Q20e)** - ECHS Command-level leakage rates and geographic findings table
7. **Leakage Projections & Strategic Recommendations (Q20c)** - Conservative, moderate, and aggressive projections table followed by policy recommendations

---

## 🔧 How to Regenerate

To run the report generation script and compile the PDF:

```bash
cd /home/tarun/Downloads/CC/echs_analysis/module_20
python3 generate_module20_report.py
```

**Output:** `reports/ECHS_Module20_Budget_Leakage_Report.pdf`

---

## ✅ Quality Checklist

- [x] All amounts correctly converted to Lakhs/Crores based on ECHS standards
- [x] Rupee symbol (`₹`) renders correctly on all platforms
- [x] No HTML tags visible in the compiled PDF output
- [x] Colors and borders render with print-ready precision
- [x] Top 25 hospitals sorted by absolute deduction amount
- [x] Professional cover page matching Module 11 style guide
- [x] Dynamic data loading from CSVs with safe historical fallbacks

---

## 📋 Data Sources

Loaded dynamically from CSV files in `/home/tarun/Downloads/CC/echs_analysis/data-tarun/module_20/`:
- `overall_leakage_summary.csv`
- `annual_expenditure_trend.csv`
- `hospital_type_nabh_leakage.csv`
- `hospital_leakage_summary.csv`
- `regional_deduction_breakdown.csv`
- `fraud_projection_summary.csv`

---

*Prepared by ECHS Fraud Analytics Team - IIT Kanpur*
*Module 20: Budget Impact & Leakage Analysis*
