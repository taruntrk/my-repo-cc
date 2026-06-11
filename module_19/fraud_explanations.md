# ECHS Forensic Fraud & Policy Abuse Explanations

This document provides a simplified breakdown of the 10 forensic patterns identified in the ECHS Module 19 audit. It explains how each fraud works, followed by a simple real-life example in Hindi, the corresponding policy rule violation, and the database columns/logic used to identify it.

---

### Pattern 1: High Deduction (Systemic Overbilling)
- **Kaise Fraud hota hai:** Hospitals ECHS ke mandated CGHS rates se zyada billing kar dete hain (tests, medicines aur surgical packages ke rates badha kar). Woh bill me extra unapproved charges jod dete hain is umeed me ki check karte waqt automated checks se kuch pass ho jaye.
- **Real-Life Example (Hindi):** Ek simple Appendix surgery ka government rate ₹30,000 fixed hai. Lekin hospital ECHS ko ₹65,000 ka bill bhejta hai, jisme ₹15,000 sutures ke aur ₹8,000 recovery room ke alag se laga deta hai jo ki package me pehle se shamil the. Auditor checks ke dauran ₹35,000 reject (deduct) kar deta hai aur sirf ₹30,000 approve karta hai.
- **Policy Violation:** Hospital ne pre-agreed ECHS tariff rate agreement policy ka seedha violation kiya, bundle package items ko alag se double-bill karke.
- **Data se kaise identify kiya (Hindi):** Humne submitted bills ke table (`claim_submission`) se final **Billed Amount (CS_GR_CLAIM_AMT)** aur **Approved Amount (CS_UTI_APP_AMT)** ko check kiya. Jahan deduction percentage `((Billed Amount - Approved Amount) / Billed Amount) > 0.50` (yaani 50% se zyada) tha, un claims ko flag kiya.

---

### Pattern 2: Room Upgrade Fraud (Entitlement Misuse)
- **Kaise Fraud hota hai:** Hospital patient ke ECHS card entitlement (jaise General Ward) se bade room category (jaise Private Ward) me use admit dikha kar bill bhejta hai, kyunki high-tier rooms me surgical package charges aur room rent dono bohot zyada hote hain.
- **Real-Life Example (Hindi):** Patient ka card sirf General Ward bed ke liye valid hai, par hospital use Private Ward me admit kar deta hai aur room charge ₹2,000/night ki jagah ₹10,000/night ECHS se claim karta hai, saath hi surgery ka private-room level package lagata hai.
- **Policy Violation:** Hospital ne patient ke room entitlement rule ka violation kiya aur bina authorization ke category badhai taaki zyada surgical rates claim ho sakein.
- **Data se kaise identify kiya (Hindi):** Humne claims table (`claim_intimation`) ke **Entitled Room Type (CI_CARD_ROOM_TYPE)** (patient ki card limit room category, jaise GEN/General or SPR/Semi-Private) aur **Billed Room Type (CI_ROOM_TYPE_ID)** (hospital dwara bill kiya gaya room category, jaise PRI/Private) columns ko compare kiya. Jahan dono match nahi hue (`Entitled Room Type != Billed Room Type`), un claims ko check kiya.

---

### Pattern 3: Ghost Admissions (In-Patient Department Paper Fraud)
- **Kaise Fraud hota hai:** Hospital bina kisi registered bed ya physical admission ke sirf paper par fake admission bills banata hai aur database portal ke loopholes ka fayda utha kar portal me bina valid Hospital ID dale bill pass-through karwa leta hai.
- **Real-Life Example (Hindi):** Hospital ECHS database me ek fake bill submit karta hai jisme dikhaya jata hai ki ek patient 5 din tak dengue ke liye admit tha, par bill me hospital ka ID blank chhod diya jata. Patient asal me apne ghar me tha aur unhe pata bhi nahi tha ki unke card se fraud billing hui hai.
- **Policy Violation:** Hospital ne registration aur physical admission verification rules ka bypass kiya aur paper-only billing submit ki.
- **Data se kaise identify kiya (Hindi):** Humne claims table (`claim_intimation`) me check kiya jahan unique **Hospital ID (CI_HOSPITAL_ID)** column empty ya NULL tha, par fir bhi bill table me **Billed Amount (CS_GR_CLAIM_AMT)** zero se bada tha, jisse bina registered hospital ke hi payment clear ho rahi thi.

---

### Pattern 4: Y-Flag Bypass (Non-Empanelled Abuse)
- **Kaise Fraud hota hai:** Jo hospitals ECHS ke partners nahi hain (non-empanelled), woh routine planned surgeries (jaise knee joint replacement) ko "emergency treatment" (Y-Flag) ke roop me submit karte hain taaki unhe bina referral ke direct ECHS payments mil sakein.
- **Real-Life Example (Hindi):** Ek non-empanelled private hospital kisi patient ki planned knee replacement surgery (jo emergency nahi thi) karta hai aur portal par 'Y-Flag' (Emergency) tick kar deta hai taaki standard rates bypass karke unhe direct ₹1.5 Lakhs ka payment mil sake.
- **Policy Violation:** Hospital ne non-empanelled emergency exception policy ka misuse kiya aur planned elective procedure ko emergency dikhaya.
- **Data se kaise identify kiya (Hindi):** Humne claims table (`claim_intimation`) me check kiya jahan **Non-Empanelled Hospital Flag (CI_NONEMP_FLG)** ki value `'Y'` (Yes) thi, aur un claims ko check kiya jinki cost planned packages se matches karti thi.

---

### Pattern 5: U-Flag Anomaly (Blind Spot Exploitation)
- **Kaise Fraud hota hai:** Jab kisi hospital ka operational status unverified ya blocked (U-Flag) hota hai, fir bhi portal ki system errors ke karan unki billing processing aur payments pass ho jati hain bina quality verify hue.
- **Real-Life Example (Hindi):** Ek diagnostic lab ka license expire ho chuka hai aur wo ECHS portal par 'Unverified' marked hai. Lab high-end MRI scan ka bill bhejti hai aur portal ke check filter bypass hone ki wajah se payment receive kar leti hai.
- **Policy Violation:** Hospital status validation aur portal security policies ka bypass hua, jiske chalte ek blocked/unverified facility ko payment release ho gayi.
- **Data se kaise identify kiya (Hindi):** Humne claims table (`claim_intimation`) me status check kiya jahan **Non-Empanelled Hospital Flag (CI_NONEMP_FLG)** ki value `'U'` (Unverified) register thi, aur checking filter laga kar un anomalies ko dhunda jo bina system verification ke clear ho gaye.

---

### Pattern 6: In-Patient Department (IPD) Reversal (Out-Patient Department (OPD) Disguised as IPD)
- **Kaise Fraud hota hai:** Hospital simple Out-Patient Department (OPD) checkup ya day-care tests ke liye aaye patient ko paper par 24-hour In-Patient Department (IPD) admission dikha deta hai, kyunki IPD package payouts OPD se bohot zyada hote hain.
- **Real-Life Example (Hindi):** Patient sirf 1 ghante ke routine eye check-up ke liye jata hai, par hospital patient ko file par 24 ghante ke liye room rent aur clinical monitoring ke sath admit dikha deta hai aur saste check-up ki jagah bada IPD package claim karta hai.
- **Policy Violation:** Hospital ne treatment classification policy ka violation kiya, outpatient consultations ko IPD admission me convert karke overbilling karne ke liye.
- **Data se kaise identify kiya (Hindi):** Humne claims table (`claim_intimation`) ke **Patient Type (CI_PATIENT_TYPE)** (Out-Patient vs In-Patient) aur **Hospital ID (CI_HOSPITAL_ID)** columns ko process kiya. Humne un hospitals ko filter kiya jinka total In-Patient IPD volume (`SUM(IF(Patient Type = 'I'))`) unke Out-Patient OPD volume (`SUM(IF(Patient Type = 'O'))`) se abnormal roop se zyada tha.

---

### Pattern 7: Unlisted Procedures (Bypassing Price Caps)
- **Kaise Fraud hota hai:** CGHS rules standard procedures ke liye rates fix karte hain. Hospital un standard procedures ko custom ya "unlisted" (NMI codes) likh kar bill bhejte hain taaki price ceilings bypass karke manchaha rate claim kar sakein.
- **Real-Life Example (Hindi):** Hospital standard kidney stone removal surgery karta hai (jiska government rate ₹25,000 fixed hai), lekin bill me procedure code ki jagah custom "NMI" code daal kar ₹80,000 charge kar deta hai.
- **Policy Violation:** CGHS/ECHS fixed price cap policy ko bypass kiya gaya, standard procedure ko non-standard code me category change karke.
- **What is NMI (Non-Medical Item / Unlisted):** NMI ka matlab hai jo items ya procedures government ki rate list me registered nahi hain. Hospitals standard treatments ko NMI dikha dete hain taaki portal ke price checks/caps bypass ho sakein aur manchaha charge bill kiya ja sake.
- **Data se kaise identify kiya (Hindi):** Humne sub-table `unlisted_procedure` ke **Unlisted Procedure Name (UP_PROCEDURE)** column ko scan kiya aur check kiya jahan standard rate list bypass karke **Unlisted Total Cost (UP_TOTAL_COST)** zero se badi thi.

---

### Pattern 8: The Bait & Switch (Prior Approval Inflation)
- **Kaise Fraud hota hai:** Hospital treatment ke liye ECHS polyclinic se approval lene ke liye shuruat me bohot sasta estimate deta hai. Par admission ke baad bill me arbitrary extra charges ya complications dikha kar final bill ko bohot bada kar deta hai.
- **Real-Life Example (Hindi):** Hospital gallstone surgery ke liye shuru me ₹40,000 ka estimate dekar polyclinic se approval le leta hai. Par surgery ke baad final bill ₹1.2 Lakhs bhej deta hai, yeh bol kar ki procedure mushkil tha aur extra disposable items use/bill hue.
- **Policy Violation:** Hospital ne pre-authorization cost guidelines ka violation kiya, approval process ko circumvent karne ke liye initial estimation ko manipulate kiya.
- **Data se kaise identify kiya (Hindi):** Humne claims table ke prior approval estimated amount **Approved Estimate (CI_APPROX_COST)** aur submission table ke final submitted bill **Billed Amount (CS_GR_CLAIM_AMT)** columns ko compare kiya. Jahan final bill estimate se zyada tha (`Billed Amount > Approved Estimate`), unhe flag kiya.

---

### Pattern 9: Stay Extension Farming
- **Kaise Fraud hota hai:** Hospital patient ko theek hone ke baad bhi be-wajah kai dino tak bed par rakh kar discharge delay karta hai taaki ECHS se daily room rent, routine doctor round fees, aur nursing charges claim kiye ja sakein.
- **Real-Life Example (Hindi):** Ek patient minor procedure ke baad 2 din me fully recover ho jata hai, par hospital use 6 din extra admit rakhta hai taaki daily room rent, routine saline drip aur extra nursing charges bill kar sake.
- **Policy Violation:** Hospital ne clinical stay and medical necessity guideline policy ka violation kiya, bina medical reason ke patient ko admit rakhne ke liye.
- **Data se kaise identify kiya (Hindi):** Humne `stay_extension` table me checking ki. Humne patient ke **Expected Discharge Date (CI_EXP_DOD)** aur hospital ke delayed proposed/approved discharge dates (**Proposed Discharge Date (SE_PROPOSE_DOD)** / **Approved Discharge Date (SE_APPROVED_DOD)**) ke bich difference (DATEDIFF) nikala. Is calculated duration se extra days identify kiye.

---

### Pattern 10: Emergency Gateway Bypass
- **Kaise Fraud hota hai:** Routine aur planned surgeries (jaise cataract ya bypass) jinke liye pehle se referral aur polyclinic approval lena zaroori hota hai, hospital unhe "Emergency" (E-Flag) route se submit kar deta hai taaki bina kisi referral ke check-post bypass ho jaye.
- **Real-Life Example (Hindi):** Hospital routine cataract surgery (jo 2 hafte pehle se planned thi) ko "Emergency" declare karke process karta hai, taaki polyclinic ke checks se na guzarna pade aur billing seedhe post-facto pass ho jaye.
- **Policy Violation:** Hospital ne mandatory referral aur pre-authorization policy ko bypass kiya, normal elective procedures ko fake emergency claim route me bhej kar.
- **Data se kaise identify kiya (Hindi):** Humne claims table ke **Referral Type ID (CI_REF_TYPE_ID)** ko check kiya jahan iski value `'E'` (Emergency bypass) save thi, aur **Ailment Description (CI_ADM_AILMENT)** me planned procedures ke keywords match kiye.
