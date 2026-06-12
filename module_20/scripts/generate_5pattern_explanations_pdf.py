import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

BASE = "/home/tarun/Downloads/CC/echs_analysis/module_20"
EXP_DIR = os.path.join(BASE, "new_explanation")
os.makedirs(EXP_DIR, exist_ok=True)

PDF_OUT = os.path.join(EXP_DIR, "ECHS_5_Pattern_Fraud_Explanations.pdf")
today_str = datetime.today().strftime("%B %d, %Y")

W, H = A4

# Color Palette
NAVY = HexColor('#1a2744')
GOLD = HexColor('#c8a84b')
RED = HexColor('#cc2222')
GREEN = HexColor('#1a6e1a')
LGRAY = HexColor('#f4f4f4')
MGRAY = HexColor('#dddddd')
DGRAY = HexColor('#333333')

# Typography Styles
def base_style(**kw):
    d = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DGRAY, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle('x', **d)

S_BODY = base_style(alignment=TA_JUSTIFY, leading=14, fontSize=9.5)
S_BODY_L = base_style(alignment=TA_LEFT, leading=14, fontSize=9.5)
S_TITLE = base_style(fontName='Helvetica-Bold', fontSize=18, textColor=white, leading=22, alignment=TA_CENTER)
S_SUBTITLE = base_style(fontName='Helvetica-Oblique', fontSize=10, textColor=GOLD, leading=14, alignment=TA_CENTER)
S_H1 = base_style(fontName='Helvetica-Bold', fontSize=13, textColor=NAVY, leading=17, spaceBefore=15, spaceAfter=8)
S_H2 = base_style(fontName='Helvetica-Bold', fontSize=10.5, textColor=NAVY, leading=14, spaceBefore=10, spaceAfter=4)
S_BULL = base_style(alignment=TA_LEFT, leading=14, leftIndent=12, fontSize=9)
S_CARD_TITLE = base_style(fontName='Helvetica-Bold', fontSize=10, textColor=NAVY, leading=13)
S_CARD_DESC = base_style(fontName='Helvetica-Oblique', fontSize=8.5, textColor=DGRAY, leading=12, spaceAfter=6)

S_WHAT_IS = base_style(alignment=TA_LEFT, leading=13, fontSize=8.5)
S_WHAT_IS_NOT = base_style(alignment=TA_LEFT, leading=13, fontSize=8.5)

# Decoration Callbacks
def draw_decorations(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setStrokeColor(HexColor('#ccc'))
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, H - 15*mm, W - 15*mm, H - 15*mm)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(HexColor("#555"))
    canvas.drawString(15*mm, H - 13*mm, "ECHS FRAUD ANALYTICS — 5-PATTERN FORENSIC EXPLANATIONS GUIDE")
    canvas.drawRightString(W - 15*mm, H - 13*mm, f"IIT Kanpur | Page {doc.page}")
    
    # Footer
    canvas.line(15*mm, 18*mm, W - 15*mm, 18*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(HexColor("#555"))
    canvas.drawString(15*mm, 13*mm, "RESTRICTED — For internal presentation and executive audit review.")
    canvas.drawRightString(W - 15*mm, 13*mm, f"Generated: {today_str}")
    canvas.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=22*mm,
        bottomMargin=22*mm
    )
    
    flowables = []
    
    # 1. Header Banner Box
    title_p = Paragraph("ECHS 5-PATTERN FORENSIC LEAKAGE SYSTEM", S_TITLE)
    sub_p = Paragraph("Hinglish Explanations of Fraud Patterns &amp; Auditing Recommendations", S_SUBTITLE)
    
    banner_data = [[title_p], [sub_p]]
    banner_table = Table(banner_data, colWidths=[W - 30*mm])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,1), (-1,1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEBELOW', (0,1), (-1,1), 4, GOLD),
    ]))
    flowables.append(banner_table)
    flowables.append(Spacer(1, 6*mm))
    
    # Intro Paragraph
    intro_txt = (
        "This explanations guide details the <b>5-Pattern Behavioral Taxonomy</b> implemented for "
        "ECHS Module 20 forensic leakage detection. It provides clear, executive-level definitions of each "
        "fraud mechanism (<b>Kya Hai</b>) vs. normal clinical behavior (<b>Kya Nahi Hai</b>) along with "
        "verified case counts and financial statistics."
    )
    flowables.append(Paragraph(intro_txt, S_BODY))
    flowables.append(Spacer(1, 4*mm))
    
    # Section 1
    flowables.append(Paragraph("1. Key Words Aur Definitions (Hinglish)", S_H1))
    
    term_1 = (
        "• <b>Prevented Leakage (Audit Deductions):</b> Yeh woh paisa hai jo ECHS ne bills verification "
        "ke dauran pakad kar kaat liya (total <b>₹3,612.41 Cr</b>). Yeh actual savings hai, yaani yeh paise "
        "hospitals ko nahi diye gaye."
    )
    term_2 = (
        "• <b>Realized Leakage (Approved Fraud):</b> Yeh woh amount hai jo suspicious patterns hone ke "
        "bawajood system me auto-approve ho gaya aur hospitals ko pay kar diya gaya (total <b>₹3,225.01 Cr</b>). "
        "Yeh ECHS budget ka direct financial loss hai."
    )
    flowables.append(Paragraph(term_1, S_BULL))
    flowables.append(Paragraph(term_2, S_BULL))
    flowables.append(Spacer(1, 4*mm))
    
    # Section 2
    flowables.append(Paragraph("2. 5 Fraud Patterns Ki Detailed Explanation", S_H1))
    
    def make_card(title, desc, sub_patterns):
        card_content = []
        card_content.append(Paragraph(title, S_CARD_TITLE))
        card_content.append(Paragraph(desc, S_CARD_DESC))
        
        for sp_title, what_is, what_is_not, stats_str in sub_patterns:
            card_content.append(Paragraph(f"<b>{sp_title}</b>", S_H2))
            
            w_text = f'<font color="#cc2222"><b>Kya Hai:</b></font> {what_is}'
            card_content.append(Paragraph(w_text, S_WHAT_IS))
            
            wn_text = f'<font color="#1a6e1a"><b>Kya Nahi Hai:</b></font> {what_is_not}'
            card_content.append(Paragraph(wn_text, S_WHAT_IS_NOT))
            
            if stats_str:
                card_content.append(Paragraph(f'<font color="#1a2744"><b>Data Metrics:</b></font> {stats_str}', S_WHAT_IS))
                
            card_content.append(Spacer(1, 1*mm))
            
        card_table = Table([[card_content]], colWidths=[W - 32*mm])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LGRAY),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINELEFT', (0,0), (-1,-1), 4, NAVY),
        ]))
        return KeepTogether([card_table, Spacer(1, 4*mm)])
        
    # --- Pattern 1 ---
    p1_subs = [
        ("1a. Card Sharing (Concurrent Admissions)", 
         "Ek hi smart card ko multiple families share karti hain aur same day do alag-alag hospitals me admissions/treatments ke liye use karti hain.",
         "Yeh genuine medical transfers ya emergency shifting nahi hai jahan patient ek hospital se dusre hospital proper documentation se shifted hota hai.",
         "<b>11,137 pairs</b> of concurrent admissions | <b>₹118.78 Cr</b> Realized Leakage"),
         
        ("1b. Demographic Profile Mismatch", 
         "Identity chupani ya non-entitled logon ka treatment bill karne ke liye gender-relationship conflict code daalna (e.g. Male cardholder listed as 'Wife').",
         "Yeh database entry ki simple spelling ya single clerical key-press error nahi hai.",
         "<b>4,221 claims</b> mismatch | <b>₹24.40 Cr</b> Realized Leakage"),
         
        ("1c. Deceased Beneficiary Lazarus Billing", 
         "Cardholder ki death ho chuki hai par card active hai, aur death date ke baad ki hospital admissions bill ho rahi hain.",
         "Yeh death bed treatment ya critical emergency bills nahi hain jo patient ki death se pehle perform hue.",
         "<b>524 claims</b> | <b>₹0.64 Cr</b> Realized Leakage")
    ]
    flowables.append(make_card("Pattern 1: Beneficiary & Dependency Abuse", 
                               "Smart cards ke profile data me falsification ya details lend karke non-entitled members ko bill karna.", p1_subs))
                               
    # --- Pattern 2 ---
    p2_subs = [
        ("2a. Hospital Audit Leakage Ranking", 
         "Kuch empanelled hospitals systematically packages rates ko expand karte hain, jisse inka bill audit me har baar 25%+ reject hota hai.",
         "Yeh pre-agreed rates ya emergency categories ke generic standard deductions nahi hain.",
         "<b>4,000 hospitals ranked</b> | <b>₹32,649.04 Cr</b> total approved ECHS budget scanned"),
         
        ("2b. Referral Collusion Rings (Doctor-Hospital Loop)", 
         "Ek single doctor aur hospital ka referral ring, jo same patients ko multiple times high-value claims loop me daalta hai (Index > 2.0).",
         "Yeh dialysis, chemo, ya genuine chronic care treatments ke cycles nahi hain.",
         "<b>1,111 doctor-hospital rings</b> detected (338,280 claims loop) | <b>₹2,700.74 Cr</b> approved")
    ]
    flowables.append(make_card("Pattern 2: Systematic Provider Abuse & Collusion", 
                               "Hospitals dwara systematic overbilling karna ya fake referral networks run karna.", p2_subs))
                               
    # --- Pattern 3 ---
    p3_subs = [
        ("3a. Superman Surgeons (Surgeon Cloning)", 
         "Senior specialist doctor ke credentials misuse karna aur unke name par ek hi din me 15+ complex surgeries bill karna (clinically impossible).",
         "OPD clinic visits me 15 se 20 normal checks karna surgeon cloning nahi hai; yeh theatre (OT) operation fraud hai.",
         "<b>2,193 doctor-days</b> flagged (47,433 claims) | <b>₹265.97 Cr</b> approved")
    ]
    flowables.append(make_card("Pattern 3: Doctor-Level & Clinical Anomaly", 
                               "Surgeons ke clinic credentials ka misuse karke phantom ya cloned billing karna.", p3_subs))
                               
    # --- Pattern 4 ---
    p4_subs = [
        ("4a. CFA Threshold Avoidance (₹99k Trick)", 
         "₹1 Lakh ke manual review vetting block se bachne ke liye bill values ko intentionally ₹99,000 se ₹99,999 me split/limit karna.",
         "Yeh package price change ya random clinical billing cost fluctuation nahi hai.",
         "<b>8,146 claims</b> exactly in this range | <b>₹68.13 Cr</b> Realized Leakage"),
         
        ("4b. Duplicate Claims (Split Billing)", 
         "Same patient, same hospital aur same amount ka bill 48 hours ke andar do baar upload karke double payment nikalna.",
         "Multi-stage clinical step invoicing nahi hai jahan details separate code se aati hain.",
         "<b>336,512 duplicate pairs</b> | <b>₹351.02 Cr</b> Realized Leakage")
    ]
    flowables.append(make_card("Pattern 4: Claim Manipulation & Billing Evasion", 
                               "Audits aur financial powers validation limits se bachne ke liye tricks use karna.", p4_subs))
                               
    # --- Pattern 5 ---
    p5_subs = [
        ("5a. Weekend Emergency Surge", 
         "Polyclinic referral letters se bachne ke liye planned elective admissions ko Friday/Saturday/Sunday emergency routes par dikhana.",
         "Trauma, sudden heart attacks, ya real emergency cases ke weekend admissions nahi hain.",
         "<b>830,866 claims</b> weekend admissions | <b>₹4,751.76 Cr</b> Realized Leakage"),
         
        ("5b. Month-End Billing Spikes", 
         "Month ke last 3 days me hospital billing me massive spike dikhana (Ratio > 1.5) taaki monthly targets meet kiye ja sakein.",
         "Yeh winter/monsoon diseases seasonality ke peaks nahi hain.",
         "<b>5,975 spikes</b> flagged | <b>₹229.06 Cr</b> leakage")
    ]
    flowables.append(make_card("Pattern 5: Temporal Surge & Referral Bypass", 
                               "Bypass channels aur month-end target billing periods ka time abuse karna.", p5_subs))
    
    # Section 3: Summary Table
    flowables.append(Paragraph("3. Fraud Ka Financial Impact Aur Audit Ki Recommendations", S_H1))
    
    table_data = [
        [
            Paragraph("<b>Pattern</b>", base_style(fontName='Helvetica-Bold', fontSize=8, textColor=white)),
            Paragraph("<b>Fraud Type</b>", base_style(fontName='Helvetica-Bold', fontSize=8, textColor=white)),
            Paragraph("<b>Cases Flagged</b>", base_style(fontName='Helvetica-Bold', fontSize=8, textColor=white, alignment=TA_CENTER)),
            Paragraph("<b>Leakage (Cr)</b>", base_style(fontName='Helvetica-Bold', fontSize=8, textColor=white, alignment=TA_CENTER)),
            Paragraph("<b>Audit Action</b>", base_style(fontName='Helvetica-Bold', fontSize=8, textColor=white))
        ],
        [
            Paragraph("1a", base_style(fontSize=8)),
            Paragraph("Card Sharing Concurrent", base_style(fontSize=8)),
            Paragraph("11,137 pairs", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹118.78 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Mandatory biometric scans at entry.", base_style(fontSize=8))
        ],
        [
            Paragraph("1b", base_style(fontSize=8)),
            Paragraph("Demographic Mismatch", base_style(fontSize=8)),
            Paragraph("4,221 claims", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹24.40 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Hard validations on gender relationship.", base_style(fontSize=8))
        ],
        [
            Paragraph("1c", base_style(fontSize=8)),
            Paragraph("Lazarus Post-Death Billing", base_style(fontSize=8)),
            Paragraph("524 claims", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹0.64 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Real-time integration with Death registry.", base_style(fontSize=8))
        ],
        [
            Paragraph("2b", base_style(fontSize=8)),
            Paragraph("Collusion Rings", base_style(fontSize=8)),
            Paragraph("1,111 rings", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹2,700.74 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Audit doctor-hospital referral pairs.", base_style(fontSize=8))
        ],
        [
            Paragraph("3a", base_style(fontSize=8)),
            Paragraph("Superman Surgeon", base_style(fontSize=8)),
            Paragraph("2,193 days", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹265.97 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Verify surgeons via AEBAS attendance.", base_style(fontSize=8))
        ],
        [
            Paragraph("4a", base_style(fontSize=8)),
            Paragraph("CFA Threshold Avoidance", base_style(fontSize=8)),
            Paragraph("8,146 claims", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹68.13 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Audit claims priced ₹95k-99.9k.", base_style(fontSize=8))
        ],
        [
            Paragraph("4b", base_style(fontSize=8)),
            Paragraph("Duplicate Billing", base_style(fontSize=8)),
            Paragraph("336,512 pairs", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹351.02 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Deduplication block for 72-hour window.", base_style(fontSize=8))
        ],
        [
            Paragraph("5a", base_style(fontSize=8)),
            Paragraph("Weekend Emergency", base_style(fontSize=8)),
            Paragraph("830,866 claims", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹4,751.76 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Audit weekend emergency justifications.", base_style(fontSize=8))
        ],
        [
            Paragraph("5b", base_style(fontSize=8)),
            Paragraph("Month-End billing spike", base_style(fontSize=8)),
            Paragraph("5,975 spikes", base_style(fontSize=8, alignment=TA_CENTER)),
            Paragraph("₹229.06 Cr", base_style(fontSize=8, alignment=TA_CENTER, textColor=RED)),
            Paragraph("Audit final week claims for spike hospitals.", base_style(fontSize=8))
        ]
    ]
    
    t_summary = Table(table_data, colWidths=[12*mm, 42*mm, 25*mm, 22*mm, 79*mm])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, MGRAY),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    flowables.append(KeepTogether([t_summary, Spacer(1, 5*mm)]))
    
    # Conclusion Box
    con_p = Paragraph(
        "\"Differentiating between Prevented Leakage (₹3,612.41 Cr saved) and Realized Leakage "
        "(₹3,225.01 Cr slipped) is key. This Hinglish forensic guide provides senior executives "
        "with clear audit evidence to enforce stricter rules.\"",
        base_style(fontName='Helvetica-Oblique', fontSize=9, textColor=white, leading=13, alignment=TA_CENTER)
    )
    
    con_table = Table([[con_p]], colWidths=[W - 30*mm])
    con_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 2, GOLD),
    ]))
    flowables.append(KeepTogether([con_table]))
    
    doc.build(flowables, onFirstPage=draw_decorations, onLaterPages=draw_decorations)
    print(f"✅ ReportLab ECHS 5-Pattern Explanations PDF successfully generated at: {PDF_OUT}")

if __name__ == '__main__':
    build_pdf()
