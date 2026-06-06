# ECHS Module 11 Identity Fraud Report - Complete Explanation

## 📊 **WHAT THIS REPORT DOES**

This report analyzes **5 years of ECHS claims data (2021-2026)** to detect **identity-related fraud patterns**. It examines **26+ million claim records** to find cases where:
- People are using fake or stolen identities
- Single cards are being shared by multiple people  
- Beneficiaries are being admitted to multiple hospitals at the same time (physically impossible)
- Same bills are being submitted multiple times
- Fraud rings are operating using common contact numbers

### **Purpose**
- Detect systematic identity fraud in ECHS claims
- Provide actionable intelligence for fraud investigators
- Estimate financial exposure from fraudulent claims
- Enable immediate recovery and enforcement actions

---

## 📅 **DATA ANALYZED**

### **Time Period**
- **5 Years**: 2021 to 2026 (Last 5 years from current date)
- **Total Records**: 26+ million claims analyzed
- **Analysis Date**: June 3, 2026

### **Data Sources (Database Tables)**

1. **`claim_intimation`** (Primary table)
   - Contains all claim basic information
   - Links to beneficiaries, patients, hospitals

2. **`claim_submission`** (Financial data)
   - Contains claim amounts, bill details
   - Death dates, discharge dates

3. **`office_master`** (Hospital information)
   - Hospital names, addresses, locations

4. **`cghs_region_master`** (Geographic data)
   - City names, regions

5. **`state_master`** (Geographic data)
   - State names and codes

6. **`relation_master`** (Relationship types)
   - Patient relationship to beneficiary

7. **`service_master`** (Service types)
   - Army, Navy, Air Force, etc.

8. **`rank_master`** (Military ranks)
   - Rank descriptions

---

## 🔍 **6 FRAUD PATTERNS DETECTED**

### **PATTERN 01: Duplicate Card IDs** [CRITICAL]

**What it detects**: Single ECHS card number used by multiple different service numbers

**Example Case**:
- Card: `000001724273`
- Used by: **2 different service numbers** (6285365 and 6285365Y)
- Total Claims: 157 claims
- Money Involved: ₹7.19 Crores claimed

**Why it's fraud**: Each ECHS card should belong to ONLY ONE beneficiary. If multiple people are using the same card, it means:
- Card cloning
- Identity theft
- Sharing of legitimate cards for fraudulent claims

**Columns in Data**:
- `card_number`: The ECHS card ID being misused
- `unique_service_numbers`: How many different people are using this card
- `unique_names`: How many different beneficiary names
- `total_claims`: Total number of claims made
- `unique_hospitals`: How many hospitals involved
- `total_claimed_amount`: Total money claimed
- `total_approved_amount`: Total money approved/paid
- `service_numbers`: List of all service numbers using this card
- `beneficiary_names`: List of all names claiming with this card
- `hospitals_used`: List of hospitals where card was used
- `fraud_span_days`: Number of days the fraud has been going on

---

### **PATTERN 02: Simultaneous Admissions** [CRITICAL]

**What it detects**: Same beneficiary admitted to 2 or more hospitals at the exact same time

**Example Logic**:
- Person A admitted to Hospital X on Jan 1, 2024
- Person A also admitted to Hospital Y on Jan 1, 2024
- **Physically impossible** - one person cannot be in two places!

**Why it's fraud**:
- Identity theft - someone else using the person's card
- Card sharing between family/friends
- Collusion between hospitals

**Columns in Data**:
- `service_number`: The beneficiary's service ID
- `card_number`: ECHS card number
- `beneficiary_name`: Name of card holder
- `claim_id_1`, `claim_id_2`: The two overlapping claims
- `admission_date_1`, `admission_date_2`: Admission dates at both hospitals
- `discharge_date_1`, `discharge_date_2`: Discharge dates
- `hospital_1`, `hospital_2`: Hospital IDs
- `hospital_name_1`, `hospital_name_2`: Hospital names
- `city_1`, `city_2`: Cities of hospitals
- `overlap_days`: How many days the admissions overlapped
- `amount_1`, `amount_2`: Claim amounts at each hospital

---

### **PATTERN 03: Duplicate Bill Numbers** [HIGH]

**What it detects**: Same bill number submitted multiple times for different claims

**Example Case**:
- Bill Number: `BG120260078` 
- Date: March 11, 2024
- Submitted: **94 times** (same bill!)
- Total Amount: ₹11.05 Lakhs

**Why it's fraud**:
- Hospitals recycling authentic bills
- Submitting photocopies of same bill
- System bypass to claim multiple times

**Columns in Data**:
- `bill_number`: The hospital bill number being reused
- `bill_date`: Date on the bill
- `duplicate_count`: How many times this bill was submitted
- `total_amount`: Total money claimed using this bill
- `total_approved`: Total approved/paid
- `claim_ids`: All claim IDs using this bill
- `beneficiaries`: All beneficiaries claiming with this bill
- `card_numbers`: All cards used
- `hospitals`: Hospitals that submitted the bill
- `locations`: Geographic locations
- `admission_dates`: All admission dates

---

### **PATTERN 04: Mobile Number Rings** [HIGH]

**What it detects**: Single mobile number linked to 5 or more different ECHS cards

**Example Case**:
- Mobile: `0000000000`
- Linked Cards: **2,667 different cards**
- Service Numbers: 2,652 people
- Total Claims: 4,476 claims
- Amount: ₹10.07 Crores

**Why it's fraud**: Fraud rings use a central mobile number as contact for all fake identities
- Organized fraud network
- Single person managing multiple fake identities
- Coordination point for fraudulent activities

**Columns in Data**:
- `mobile_number`: The phone number used as common contact
- `unique_cards`: How many different cards linked
- `unique_service_numbers`: How many different beneficiaries
- `total_claims`: Total claims from this ring
- `unique_hospitals`: Hospitals involved
- `total_claimed_amount`: Money claimed
- `card_numbers`: List of all cards
- `beneficiaries`: List of all beneficiaries
- `hospitals_used`: Hospitals where claims made
- `locations`: Geographic spread
- `first_claim_date`, `last_claim_date`: Activity period
- **Span (days)**: How long the fraud ring has been operating

---

### **PATTERN 05: UID Duplication (Synthetic Identities)** [CRITICAL]

**What it detects**: Same Aadhaar UID (12-digit number) used by multiple different service numbers

**Example Case**:
- UID: `8374****7138` (masked for privacy)
- Used by: **605 different service numbers**
- Cards: 679 different cards
- Claims: 1,355 claims
- Amount: ₹29.36 Lakhs

**Why it's fraud**: Each Aadhaar UID is UNIQUE to one person
- Synthetic identities created using stolen/fake UIDs
- Identity theft
- Impossible biometric matches

**Columns in Data**:
- `uid_number`: The Aadhaar UID being misused (partially masked)
- `unique_service_numbers`: How many fake profiles using this UID
- `unique_cards`: How many cards involved
- `total_claims`: Claims made using this UID
- `unique_hospitals`: Hospitals involved
- `total_claimed_amount`: Money claimed
- `total_approved_amount`: Money approved
- `beneficiaries`: List of names using same UID
- `card_numbers`: Cards involved
- `hospitals_used`: Where fraud occurred
- `locations`: Geographic distribution

---

### **PATTERN 06: High Frequency Claims** [HIGH]

**What it detects**: Beneficiaries making 10 or more claims in the 5-year period

**Example Case**:
- Service Number: `8654T`
- Beneficiary: B B SRIVASTAVA
- Total Claims: **1,008 claims** in 5 years
- Hospitals Used: 5 different hospitals
- Amount: ₹22.46 Lakhs
- Average per claim: ₹2,228
- Active Period: 1,714 days

**Why it's suspicious**:
- Abnormally high utilization
- Possible collusion with hospitals
- Unnecessary procedures
- Card sharing with family/friends

**Columns in Data**:
- `service_number`: Beneficiary's service ID
- `card_number`: ECHS card
- `beneficiary_name`: Name of cardholder
- `service_type`: Army/Navy/Air Force
- `rank_col`: Military rank
- `total_claims`: Number of claims made
- `unique_hospitals`: How many hospitals visited
- `years_with_claims`: Years active
- `unique_patients`: Different patients treated (if family)
- `first_claim_date`, `last_claim_date`: Activity period
- `fraud_span_days`: Days between first and last claim
- `total_claimed_amount`: Total money claimed
- `total_approved_amount`: Total approved
- `avg_claim_amount`: Average per claim
- `hospitals_used`: List of hospitals
- `locations_used`: Cities visited
- `patients_treated`: List of patients
- `contact_mobile`: Contact number
- `address`: Address on file

---

## 💰 **FINANCIAL IMPACT**

### **Summary**
- **Total Cases Flagged**: 3,000 cases
- **Estimated Financial Exposure**: ₹796.67 Crores
- **Critical Cases**: 1,500 cases (requiring immediate action)
- **High Priority Cases**: 1,500 cases (urgent review)

### **Pattern-wise Breakdown**
| Pattern | Cases | Severity |
|---------|-------|----------|
| Duplicate Card IDs | 500 | CRITICAL |
| Simultaneous Admissions | 500 | CRITICAL |
| UID Duplication | 500 | CRITICAL |
| Duplicate Bill Numbers | 500 | HIGH |
| Mobile Number Rings | 500 | HIGH |
| High Frequency Claims | 500 | HIGH |

---

## 📋 **COLUMN MEANINGS - DETAILED EXPLANATION**

### **Beneficiary Information Columns**
- **`service_number`**: Unique ID for ex-serviceman (e.g., 8654T, IC55489K)
- **`card_number`**: ECHS card number (e.g., 000001724273)
- **`beneficiary_name`**: Name of the ex-serviceman or dependent
- **`service_type`**: Branch of service (Army/Navy/Air Force/CAPF)
- **`rank_col`**: Military rank (e.g., Sepoy, Subedar, Major)

### **Patient Information Columns**
- **`patient_name`**: Name of person receiving treatment
- **`patient_age`**: Age of patient
- **`patient_gender`**: Male/Female
- **`relationship_code`**: Code for relationship (SEL=Self, WIF=Wife, SON=Son, etc.)
- **`relationship`**: Full relationship description

### **Hospital Information Columns**
- **`hospital_id`**: Hospital identifier code
- **`hospital_name`**: Full name of hospital
- **`hospital_location`**: City, State
- **`hospital_address`**: Full address
- **`city_1`, `city_2`**: Cities (for simultaneous admissions)

### **Claim Information Columns**
- **`claim_id`**: Unique claim identifier (intimation ID)
- **`admission_date`**: Date patient was admitted
- **`discharge_date`**: Date patient was discharged (or death date)
- **`stay_duration_days`**: Length of hospital stay
- **`bill_number`**: Hospital bill number
- **`bill_date`**: Date on hospital bill
- **`ailment`**: Disease/condition treated
- **`treating_doctor`**: Doctor who treated patient
- **`room_type`**: Type of room (general/semi-private/private)

### **Financial Columns**
- **`claimed_amount`**: Amount hospital is asking for
- **`approved_amount`**: Amount ECHS approved to pay
- **`total_claimed_amount`**: Sum of all claimed amounts
- **`total_approved_amount`**: Sum of all approved amounts
- **`avg_claim_amount`**: Average amount per claim

### **Fraud Indicator Columns**
- **`unique_service_numbers`**: Count of different beneficiaries
- **`unique_cards`**: Count of different ECHS cards
- **`unique_names`**: Count of different names
- **`unique_hospitals`**: Count of different hospitals
- **`duplicate_count`**: How many times duplicated
- **`overlap_days`**: Days of overlapping admissions
- **`fraud_span_days`**: Days from first to last fraud incident

### **Status Columns**
- **`claim_stage`**: Processing stage of claim
- **`claim_status`**: Current status (approved/pending/rejected)

### **Contact Information Columns**
- **`contact_mobile`**: Beneficiary mobile number
- **`address`**: Beneficiary address

### **Geographic Columns**
- **`locations`**: Cities and states involved
- **`cities_visited`**: List of cities where claims made

---

## ⚠️ **PRIORITY ACTIONS REQUIRED**

### **Priority 1: CRITICAL (Immediate Investigation)**
1. **Duplicate Card IDs** - 500 cases → Audit and freeze cards
2. **Simultaneous Admissions** - 500 cases → Verify identity immediately
3. **UID Duplication** - 500 cases → Cross-check with UIDAI

### **Priority 2: HIGH (Review within 30 days)**
4. **Duplicate Bill Numbers** - 500 cases → Hospital audit
5. **Mobile Number Rings** - 500 cases → Investigate fraud networks
6. **High Frequency Claims** - 500 cases → Verify medical necessity

---

## 📂 **OUTPUT FILES**

All data is available in CSV format:
- `01_Duplicate_Card_IDs.csv`
- `02_Simultaneous_Admissions.csv`
- `03_Duplicate_Bill_Numbers.csv`
- `04_Mobile_Number_Rings.csv`
- `05_UID_Duplication.csv`
- `08_High_Frequency_Claims.csv`

Plus comprehensive JSON file:
- `Point11_Fraud_Detection_Complete_Data.json`

---

## 🎯 **HOW TO USE THIS REPORT**

### **For Investigators**
1. Start with CRITICAL patterns (01, 02, 05)
2. Review top 15 cases in each pattern
3. Use complete CSV files for detailed analysis
4. Cross-reference with hospital records
5. Initiate recovery proceedings

### **For Auditors**
1. Verify flagged cases with source documents
2. Conduct hospital-level audits
3. Check biometric records for UID cases
4. Validate bill authenticity
5. Document findings for enforcement

### **For Management**
1. Review financial exposure estimates
2. Prioritize resource allocation
3. Monitor investigation progress
4. Implement preventive measures
5. Report to higher authorities

---

## ⚖️ **IMPORTANT DISCLAIMERS**

1. **Investigative Leads**: All flagged cases are potential fraud indicators, not confirmed fraud. Each requires verification before action.

2. **Financial Estimates**: Exposure amounts are based on claimed amounts. Actual fraud may differ after investigation.

3. **Data Completeness**: 100% descriptive information included - no additional database queries needed for initial investigation.

4. **Confidentiality**: This report contains sensitive personal and financial information. Restricted to authorized personnel only.

---

**Report Generated By**: IIT Kanpur - ECHS Fraud Analytics Division  
**Analysis Date**: June 3, 2026  
**Classification**: CONFIDENTIAL - OFFICIAL USE ONLY
