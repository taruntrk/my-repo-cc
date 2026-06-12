# ECHS Forensic Budget Impact & Leakage Explanations (Module 20)

This document provides a detailed forensic breakdown of the leakage and behavioral fraud patterns analyzed in the ECHS Module 20 audit. It explains how each pattern works, accompanied by a real-life example in Hindi, the specific ECHS/CGHS policy violation, and the technical database schema logic used to identify it.

---

### **Important Concept: Prevented Leakage vs. Realized Leakage**
Before reviewing the patterns, it is critical to distinguish between two types of financial metrics:
1. **Prevented Leakage (Audit Deductions):** The **₹3,612.41 Cr** that ECHS audits successfully caught and deducted from bills. This represents **savings**—money that was saved and never went out of ECHS accounts.
2. **Realized Leakage (Approved Fraud):** The wrong/fraudulent amount that got approved and paid by ECHS under suspicious behavioral patterns (such as package splitting, doctor cloning, and weekend referral bypass) because the audit checks did not block them in real-time. This represents the **actual financial loss (leakage)** to the ECHS budget.

---

### Pattern 1: Corporate Hospital Overbilling (Park Chain & Vijay Hospital)
- **Kaise Fraud hota hai:** Multi-specialty private hospital chains ya specific high-volume single hospitals system ko abuse karte hain by systematically overbilling ECHS. Yeh surgeries, procedures, medicines aur clinical packages ke rates ko agreement limits se bahut zyada dikha kar bill submit karte hain.
- **Real-Life Example (Hindi):** Ek bada private hospital chain (jaise Park Hospital) standard surgical treatments ka package rate inflate karke bill banta hai. Jab audit hota hai, to pata chalta hai ki unke pure chain ne milkar excess billing ki thi jo audit cut ho jati hai. Vijay Hospital [ID 3149] ka check karne par unka deduction rate anomalous (34.00%) tha, yaani unke har ₹100 ke bill me se ₹34 reject ho raha tha (₹11.20 Cr caught, ₹22.25 Cr approved and slipped).
- **Policy Violation:** Empanelment MoU and pre-agreed ECHS tariff package rates guideline ka direct violation.
- **Data se kaise identify kiya (Hindi):** Humne hospital leakage summary dataset check kiya jahan unique hospital name with ID code (`hospital_name_with_id`) ko absolute deductions amount (`total_deducted_lakh`) aur percentage deduction (`deduction_pct`) ke hisab se sort aur rank kiya.

---

### Pattern 2: Ping-Pong Admissions (Split-Package Abuse)
- **Kaise Fraud hota hai:** Jab ek patient ko multiple procedures ki zaroorat hoti hai, to hospital package cost boundaries bypass karne ke liye single admission me sab treatment nahi karta. Woh patient ko discharge karke 48 ghante ke andar fir se admit dikha deta hai taaki double package limits ECHS se extract ho sakein. ECHS ne in admissions par **₹60.03 Cr** approve kiya jo direct loss/leakage hai.
- **Real-Life Example (Hindi):** Patient ko appendicitis aur urinary stone dono ka treatment chahiye. Hospital ek hi baar me dono surgical procedures karne ke bajaye, appendix removal karke discharge karta hai aur next day hi stone operation ke liye fir se admit dikha deta hai, taaki do alag-alag treatment package payouts claim kar sake.
- **Policy Violation:** Package Splitting and Unbundling rules under ECHS guidelines.
- **Data se kaise identify kiya (Hindi):** Window function `LEAD` use karke humne unique patient (`CI_SERVICE_NO` aur `CI_BENEFICIARY_NAME`) ke sequential admissions tracking ki aur discharge date se next admission date ka gap check kiya: `DATEDIFF(next_admission_date, discharge_date) BETWEEN 0 AND 2` days.

---

### Pattern 3: Weekend / Holiday Surge Admissions (The Friday Hustle)
- **Kaise Fraud hota hai:** Hospital planned / elective procedures ko jaan-बूझकर Friday night, Saturday ya Sunday ko admit dikhate hain jay regional referral polyclinic staff closed/skeleton staff mode me hota hai. Aisa karke wo normal screening checks ko bypass karke direct emergency bypass use kar lete hain. ECHS ने is pattern me **₹3,097.47 Cr** ki claims approve kar di jo realized leakage hai.
- **Real-Life Example (Hindi):** Ek patient ki planned cataract surgery honi thi, par hospital use Saturday ko admit dikhata hai emergency route se taaki polyclinic referral verification officer bill bypass karke seedhe bill submission clear kar sake.
- **Policy Violation:** Out-of-hours admissions referral guidelines aur emergency admission verification checks.
- **Data se kaise identify kiya (Hindi):** MySQL function `DAYOFWEEK(CI_ADMISSION_DATE) IN (1, 6, 7)` check kiya (Sunday=1, Friday=6, Saturday=7) aur un hospitals ko highlight kiya jinka weekend admission and subsequent deduction rates abnormal level par the.

---

### Pattern 4: Doctor Cloning (Superman Surgeon Pattern)
- **Kaise Fraud hota hai:** Hospital claims portal par single main specialist surgeon ke name par ek hi din me clinically impossible number of surgeries (jaise 15-20 bypass surgeries) document kar deta hai. Asal me ya to junior/untrained staff surgeries kar rahe hote hain, ya fir bills fabricated (fake paper entries) hote hain. ECHS ne **₹6.56 Cr** approved kiya on these impossible surgeon days.
- **Real-Life Example (Hindi):** Ek senior cardiologist ke profile se ek hi din me 18 complex bypass surgeries portal par billed dikhai jati hain. Ek doctor ke liye physical and clinical terms me itni surgeries single day me karna namumkin hai.
- **Policy Violation:** Surgeon credential verification standards aur clinical practice limits.
- **Data se kaise identify kiya (Hindi):** Treatment doctor column (`CS_TREAT_DOCT`) aur admission date (`DATE(CS_SUB_DATE)`) par grouping lagai aur filters apply kiye jahan clean doctor entries aggregate counts `COUNT(*) >= 15` per day perform kar rahi thin.

---

### Pattern 5: Threshold Avoiding (The ₹99k Trick)
- **Kaise Fraud hota hai:** ECHS rules ke anusaar ₹1 Lakh ya usse bada bill hone par dynamic pre-authorisation mandatory hoti hai jo higher authorities (CFA - Competent Financial Authority) verify karte hain. Is checking zone se bachne ke liye hospitals intentionally bills ko ₹99,000 se ₹99,999 ke range me split/limit kar dete hain taaki direct billing release ho jaye. ECHS ne is bypass scheme me **₹22.97 Cr** approve kiya.
- **Real-Life Example (Hindi):** Gallstone removal procedure ka actual bill ₹1,15,000 banna chahiye tha, par hospital use janbujhkar system limits ke niche ₹99,850 ka banata hai taaki dynamic pre-approval checks automatic pass-through ho jayein.
- **Policy Violation:** Delegation of Financial Powers Rule (DFPR) bypass and split-billing evasion code.
- **Data se kaise identify kiya (Hindi):** Submitted claim values `CS_NET_CLAIM_AMT` check kiya jahan values exactly `BETWEEN 99000 AND 99999` limit me falls karti hain aur specific hospital per-year repeat cases counts count `COUNT(*) > 10` exceed kar raha ho.

---

### Pattern 6: Individual Card Sharing (Same-Day Multi-Hospital Admissions)
- **Kaise Fraud hota hai:** Ek hi beneficiary card (Card ID) ko geographically distant hospitals me same day use kiya jata hai admissions and treatments ke liye. Yeh direct impersonation (identity theft) ko represent karta hai, kyunki ek person same day do alag-alag cities ya locations me admit nahi ho sakta. ECHS ne in cases par **₹4.82 Cr** approve kiya jo fully realized leakage hai.
- **Real-Life Example (Hindi):** Ek card (Card ID: PT0046184) ke beneficiary (J K SINGH) ko Patna ke Jeevak Heart Hospital aur Patna ke ASG Hospital me same day (2018-04-06) admit dikhaya gaya. ECHS ne dono claims approve kar diye bina geographic overlap check kiye.
- **Policy Violation:** Identity verification failure and ECHS Smart Card guidelines violation.
- **Data se kaise identify kiya (Hindi):** Database queries using self-join on `card_id` with filters: same `admission_date` but different `hospital_id`.

---

### Pattern 7: Family Card Sharing (Simultaneous Dependant Abuse)
- **Kaise Fraud hota hai:** Service member ke multiple dependents (jaise Son, Wife, Spouse) same day alag-alag hospitals me admit ho jate hain high-value procedures ke liye. Yeh local healthcare providers ke collusive billing pattern ya organized card sharing abuse ko show karta hai. ECHS ne is simultaneous abuse pattern me **₹8.44 Cr** approve kiya.
- **Real-Life Example (Hindi):** Same Service Number (01124788) ke do dependents (Son/Daughter) ko different hospital chains (Livasa Hosp and Ivy Health) me same day (2017-11-06) admit kiya gaya, aur large amount (₹3.20 Lakhs+) ECHS se approve karwaya gaya.
- **Policy Violation:** Collusive beneficiary sharing and dependent claims validation rules.
- **Data se kaise identify kiya (Hindi):** Self-join queries on `service_no` matching same `admission_date` but different patient names (`beneficiary_name`) and different hospital codes.

---

### Pattern 8: Demographic & Relation Mismatch (Gender-Relationship Conflict)
- **Kaise Fraud hota hai:** Patients ke demographics (Gender) aur primary beneficiary ke relationship code (e.g. Wife, Mother, Daughter) me impossible contradiction hoti hai (jaise: patient registered with gender 'Male' but relationship 'Wife' or 'Mother'). Is data mismatch ko ignores karke hospitals claim pass-through karwa dete hain. ECHS ne is type ke 17,205 claims me **₹37.99 Cr** approve kiya.
- **Real-Life Example (Hindi):** Claims me registered patient ka gender Male 'M' dikhaya gaya par relation field 'Mother' ya 'Wife' listed thi (jaise Fortis Escorts Hospital, Amritsar me Kashmir Kaur ka relation Mother but gender Male listed tha). ECHS systems ne data checks bypass kar diye aur full approval clear kiya.
- **Policy Violation:** Eligibility criteria checking and demographic verification standard operating procedures (SOP).
- **Data se kaise identify kiya (Hindi):** Filtered query matching impossible pairs: `(gender='M' AND relationship IN ('Wife', 'Mother', 'Daughter'))` OR `(gender='F' AND relationship IN ('Husband', 'Father', 'Son'))`.
