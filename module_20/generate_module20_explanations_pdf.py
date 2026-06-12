import os
import time
from datetime import date

try:
    from weasyprint import HTML
except ImportError:
    print("ERROR: weasyprint not installed. Please run: pip install weasyprint")
    exit(1)

BASE = os.path.dirname(os.path.abspath(__file__))
FINAL_EXP_DIR = os.path.join(BASE, "final_explanation")
os.makedirs(FINAL_EXP_DIR, exist_ok=True)

today_str = date.today().strftime("%B %Y")
PDF_OUT = os.path.join(FINAL_EXP_DIR, "ECHS_Fraud_Explanations.pdf")

NAV = "#1a2744"
GOLD = "#c9a84c"

CSS_STR = f"""
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:Arial,Helvetica,sans-serif; font-size:10pt; color:#222; line-height:1.6; background:#fff; margin:0; }}

@page {{
    size:A4; margin:20mm 15mm 18mm 15mm;
    @top-left   {{ content:"ECHS FRAUD ANALYTICS — FORENSIC EXPLANATIONS GUIDE (MODULE 20)";
                  font-family:Arial; font-size:7pt; font-weight:700; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @top-right  {{ content:"IIT Kanpur | Page " counter(page);
                  font-family:Arial; font-size:7.5pt; color:#555;
                  border-bottom:1px solid #ccc; padding-bottom:4px; vertical-align:bottom; }}
    @bottom-left  {{ content:"RESTRICTED — For internal presentation and executive review.";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
    @bottom-right {{ content:"Generated: {today_str}";
                    font-family:Arial; font-size:7pt; color:#555; border-top:1px solid #ddd; padding-top:3px; }}
}}

.cover {{ text-align:center; padding:40px 20px; background:{NAV}; color:#fff; border-bottom:6px solid {GOLD}; margin:-20mm -15mm 30px -15mm; }}
.cover-title {{ font-size:22pt; font-weight:900; letter-spacing:1px; margin-bottom:10px; }}
.cover-sub {{ font-size:12pt; font-weight:300; color:#ddd; }}

.container {{ padding:0 10px; }}
h1 {{ font-size:15pt; font-weight:900; color:{NAV}; text-transform:uppercase; border-bottom:2px solid {GOLD}; padding-bottom:5px; margin:30px 0 15px 0; }}
h2 {{ font-size:12pt; font-weight:800; color:#c0392b; margin:20px 0 10px 0; }}
h3 {{ font-size:11pt; font-weight:700; color:{NAV}; margin:15px 0 5px 0; }}

p {{ margin-bottom:12px; text-align:justify; }}
.highlight {{ background:#fff3cd; padding:2px 4px; font-weight:700; color:#856404; }}

.card {{ background:#f8f9fa; border-left:4px solid {NAV}; padding:15px; margin-bottom:20px; }}
.card-title {{ font-weight:800; font-size:11.5pt; margin-bottom:8px; color:{NAV}; display:flex; align-items:center; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
.card-text {{ font-size:9.5pt; color:#444; line-height:1.5; }}
.metric-row {{ margin-top: 10px; padding-top: 8px; border-top: 1px dashed #ccc; display: flex; gap: 15px; font-size: 9pt; }}
.metric-val {{ font-weight: bold; color: #c0392b; }}
.metric-ok {{ font-weight: bold; color: #27ae60; }}

ul {{ margin-left:20px; margin-bottom:15px; }}
li {{ margin-bottom:8px; font-size:9.5pt; }}

.conclusion-box {{ background:{NAV}; color:#fff; padding:20px; text-align:center; margin-top:40px; border-radius:4px; border:2px solid {GOLD}; }}
.conclusion-text {{ font-size:11pt; font-style:italic; font-weight:600; line-height:1.5; }}
"""

def generate_explainer():
    print("Generating Module 20 Explanations PDF...")
    
    H = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS_STR}</style></head><body>
    <div class="cover">
        <div class="cover-title">MODULE 20 FORENSIC LEAKAGE SYSTEM</div>
        <div class="cover-sub">Forensic Explanations of Prevented vs. Realized Budget Leakage</div>
    </div>
    
    <div class="container">
        <p>This document provides the executive explanations guide for the Module 20 forensic leakage analysis. It details the conceptual shift from audit savings to realized losses and breaks down the top 8 high-impact behavioral patterns with Hindi translations, policy references, and technical SQL logic.</p>
        
        <h1>1. Key Terminology &amp; Definitions</h1>
        <p>To align with senior-level reporting standards, we clearly differentiate between intercepted savings and actual losses:</p>
        <ul>
            <li><b>Prevented Leakage (Audit Deductions):</b> The amount ECHS successfully intercepted and deducted from claims during the bill verification phase (totaling <b>₹3,612.41 Cr</b>). This represents actual savings, meaning this money was never paid out of ECHS accounts.</li>
            <li><b>Realized Leakage (Approved Fraud):</b> The wrong/fraudulent amount that got approved and paid by ECHS under suspicious behavioral patterns (such as package splitting, doctor cloning, and weekend referral bypass) because the audit checks did not block them in real-time (totaling <b>₹3,225.01 Cr</b>, representing a <b>9.88%</b> slippage rate of the total approved budget). This represents direct financial loss to the ECHS budget.</li>
        </ul>
        
        <h1>2. Forensic Explanations of the 8 Core Patterns</h1>
        
        <!-- PATTERN 1 -->
        <div class="card">
            <div class="card-title">Pattern 1: Corporate Hospital Overbilling (Vijay &amp; Park Chains)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Multi-specialty private hospital chains ya specific high-volume single hospitals system ko abuse karte hain by systematically overbilling ECHS. Yeh surgeries, procedures, medicines aur clinical packages ke rates ko agreement limits se bahut zyada dikha kar bill submit karte hain.</p>
                <p><b>Real-Life Example (Hindi):</b> Ek bada private hospital chain (jaise Park Hospital) standard surgical treatments ka package rate inflate karke bill banta hai. Jab audit hota hai, to pata chalta hai ki unke pure chain ne milkar excess billing ki thi jo audit cut ho jati hai. Vijay Hospital [ID 3149] ka check karne par unka deduction rate anomalous (34.00%) tha, yaani unke har ₹100 ke bill me se ₹34 reject ho raha tha.</p>
                <p><b>Policy Violation:</b> Empanelment MoU and pre-agreed ECHS/CGHS tariff package rates guideline ka direct violation.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Humne hospital leakage summary dataset check kiya jahan unique hospital name with ID code (<code>hospital_name_with_id</code>) ko absolute deductions amount (<code>total_deducted_lakh</code>) aur percentage deduction (<code>deduction_pct</code>) ke hisab se sort aur rank kiya.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹34.41 Cr</b> (Top 15)</div>
                    <div>Prevented Leakage: <span class="metric-ok">₹11.20 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹22.25 Cr Slipped</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 2 -->
        <div class="card">
            <div class="card-title">Pattern 2: Ping-Pong Admissions (Split-Package Abuse)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Jab ek patient ko multiple procedures ki zaroorat hoti hai, to hospital package cost boundaries bypass karne ke liye single admission me sab treatment nahi karta. Woh patient ko discharge karke 48 ghante ke andar fir se admit dikha deta hai taaki double package limits ECHS se extract ho sakein.</p>
                <p><b>Real-Life Example (Hindi):</b> Patient ko appendicitis aur urinary stone dono ka treatment chahiye. Hospital ek hi baar me dono surgical procedures karne ke bajaye, appendix removal karke discharge karta hai aur next day hi stone operation ke liye fir se admit dikha deta hai, taaki do alag-alag treatment package payouts claim kar sake.</p>
                <p><b>Policy Violation:</b> Package Splitting and Unbundling rules under ECHS guidelines.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Window function <code>LEAD</code> use karke humne unique patient (<code>CI_SERVICE_NO</code> aur <code>CI_BENEFICIARY_NAME</code>) ke sequential admissions tracking ki aur discharge date se next admission date ka gap check kiya: <code>DATEDIFF(next_admission_date, discharge_date) BETWEEN 0 AND 2</code> days.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹60.03 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹0.00 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹60.03 Cr Slipped (100% loss)</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 3 -->
        <div class="card">
            <div class="card-title">Pattern 3: Weekend / Holiday Surge Admissions (Polyclinic Referral Bypass)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Hospital planned / elective procedures ko jaan-बूझकर Friday night, Saturday ya Sunday ko admit dikhate hain jab regional referral polyclinic staff closed/skeleton staff mode me hota hai. Aisa karke wo normal screening checks ko bypass karke direct emergency bypass use kar lete hain.</p>
                <p><b>Real-Life Example (Hindi):</b> Ek patient ki planned cataract surgery honi thi, par hospital use Saturday ko admit dikhata hai emergency route se taaki polyclinic referral verification officer bill bypass karke seedhe bill submission clear kar sake.</p>
                <p><b>Policy Violation:</b> Out-of-hours admissions referral guidelines aur emergency admission verification checks.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> MySQL function <code>DAYOFWEEK(CI_ADMISSION_DATE) IN (1, 6, 7)</code> check kiya (Sunday=1, Friday=6, Saturday=7) aur un hospitals ko highlight kiya jinka weekend admission and subsequent deduction rates abnormal level par the.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹4,449.07 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹1,351.61 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹3,097.47 Cr Slipped</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 4 -->
        <div class="card">
            <div class="card-title">Pattern 4: Doctor Cloning (Superman Surgeon Pattern)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Hospital claims portal par single main specialist surgeon ke name par ek hi din me clinically impossible number of surgeries (jaise 15-20 bypass surgeries) document kar deta hai. Asal me ya to junior/untrained staff surgeries kar rahe hote hain, ya fir bills fabricated (fake paper entries) hote hain.</p>
                <p><b>Real-Life Example (Hindi):</b> Ek senior cardiologist ke profile se ek hi din me 18 complex bypass surgeries portal par billed dikhai jati hain. Ek doctor ke liye physical and clinical terms me itni surgeries single day me karna namumkin hai.</p>
                <p><b>Policy Violation:</b> Surgeon credential verification standards aur clinical practice limits.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Treatment doctor column (<code>CS_TREAT_DOCT</code>) aur admission date (<code>DATE(CS_SUB_DATE)</code>) par grouping lagai aur filters apply kiye jahan clean doctor entries aggregate counts <code>COUNT(*) >= 15</code> per day perform kar rahi thin.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹6.56 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹0.00 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹6.56 Cr Slipped (100% loss)</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 5 -->
        <div class="card">
            <div class="card-title">Pattern 5: Threshold Avoiding (The ₹99k Trick)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> ECHS rules ke anusaar ₹1 Lakh ya usse bada bill hone par dynamic pre-authorisation mandatory hoti hai jo higher authorities (CFA - Competent Financial Authority) verify karte hain. Is checking zone se bachne ke liye hospitals intentionally bills ko ₹99,000 se ₹99,999 ke range me split/limit kar dete hain taaki direct billing release ho jaye.</p>
                <p><b>Real-Life Example (Hindi):</b> Gallstone removal procedure ka actual bill ₹1,15,000 banna chahiye tha, par hospital use janbujhkar system limits ke niche ₹99,850 ka banata hai taaki dynamic pre-approval checks automatic pass-through ho jayein.</p>
                <p><b>Policy Violation:</b> Delegation of Financial Powers Rule (DFPR) bypass and split-billing evasion code.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Submitted claim values <code>CS_NET_CLAIM_AMT</code> check kiya jahan values exactly <code>BETWEEN 99000 AND 99999</code> limit me falls karti hain aur specific hospital per-year repeat cases counts count <code>COUNT(*) > 10</code> exceed kar raha ho.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹28.42 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹5.44 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹22.97 Cr Slipped</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 6 -->
        <div class="card">
            <div class="card-title">Pattern 6: Individual Card Sharing (Same-Day Multi-Hospital Admissions)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Ek hi beneficiary card (Card ID) ko geographically distant hospitals me same day use kiya jata hai admissions and treatments ke liye. Yeh direct impersonation (identity theft) ko represent karta hai.</p>
                <p><b>Real-Life Example (Hindi):</b> Ek card (Card ID: PT0046184) ke beneficiary (J K SINGH) ko Patna ke Jeevak Heart Hospital aur Patna ke ASG Hospital me same day (2018-04-06) admit dikhaya gaya. ECHS ne dono claims approve kar diye bina geographic overlap check kiye.</p>
                <p><b>Policy Violation:</b> Identity verification failure and ECHS Smart Card guidelines violation.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Database queries using self-join on <code>card_id</code> with filters: same <code>admission_date</code> but different <code>hospital_id</code>.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹4.82 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹0.00 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹4.82 Cr Slipped (100% loss)</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 7 -->
        <div class="card">
            <div class="card-title">Pattern 7: Family Card Sharing (Simultaneous Dependant Abuse)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Service member ke multiple dependents (jaise Son, Wife, Spouse) same day alag-alag hospitals me admit ho jate hain high-value procedures ke liye. Yeh organized card sharing abuse ko show karta hai.</p>
                <p><b>Real-Life Example (Hindi):</b> Same Service Number (01124788) ke do dependents (Son/Daughter) ko different hospital chains (Livasa Hosp and Ivy Health) me same day (2017-11-06) admit kiya gaya, aur large amount (₹3.20 Lakhs+) ECHS se approve karwaya gaya.</p>
                <p><b>Policy Violation:</b> Collusive beneficiary sharing and dependent claims validation rules.</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Self-join queries on <code>service_no</code> matching same <code>admission_date</code> but different patient names (<code>beneficiary_name</code>) and different hospital codes.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹8.44 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹0.00 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹8.44 Cr Slipped (100% loss)</span></div>
                </div>
            </div>
        </div>

        <!-- PATTERN 8 -->
        <div class="card">
            <div class="card-title">Pattern 8: Demographic &amp; Relation Mismatch (Gender-Relationship Conflict)</div>
            <div class="card-text">
                <p><b>Kaise Fraud hota hai:</b> Patients ke demographics (Gender) aur primary beneficiary ke relationship code (e.g. Wife, Mother) me impossible contradiction hoti hai (jaise: patient registered with gender 'Male' but relationship 'Wife' or 'Mother').</p>
                <p><b>Real-Life Example (Hindi):</b> Claims me registered patient ka gender Male 'M' dikhaya gaya par relation field 'Mother' ya 'Wife' listed thi (jaise Fortis Escorts Hospital, Amritsar me Kashmir Kaur ka relation Mother but gender Male listed tha).</p>
                <p><b>Policy Violation:</b> Eligibility criteria checking and demographic verification standard operating procedures (SOP).</p>
                <p><b>Data se kaise identify kiya (Hindi):</b> Filtered query matching impossible pairs: <code>(gender='M' AND relationship IN ('Wife', 'Mother', 'Daughter'))</code> OR <code>(gender='F' AND relationship IN ('Husband', 'Father', 'Son'))</code>.</p>
                <div class="metric-row">
                    <div>Claimed: <b>₹37.99 Cr</b></div>
                    <div>Prevented Leakage: <span class="metric-ok">₹0.00 Cr</span></div>
                    <div>Realized Leakage: <span class="metric-val">₹37.99 Cr Slipped (100% loss)</span></div>
                </div>
            </div>
        </div>

        <div class="conclusion-box">
            <div class="conclusion-text">
                "By differentiating between Prevented Leakage (₹3,612.41 Cr saved) and Realized Leakage (₹3,225.01 Cr slipped), this forensic guide provides the clear evidence needed to implement hard pre-payment rules on split billing, surgeon volumes, and weekend emergency admissions."
            </div>
        </div>
    </div>
    </body>
    </html>
    """
    
    HTML(string=H, base_url=BASE).write_pdf(PDF_OUT)
    print(f"✅ Explanations PDF successfully generated at: {PDF_OUT}")

if __name__ == "__main__":
    generate_explainer()
