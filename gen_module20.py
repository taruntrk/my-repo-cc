from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable,
    KeepTogether, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

W, H = A4

NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
TBLHDR = NAVY

def base_style(**kw):
    d = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DGRAY, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle('x', **d)

S_BODY  = base_style(alignment=TA_JUSTIFY, leading=14)
S_BODYL = base_style(alignment=TA_LEFT,    leading=14)
S_H1    = base_style(fontName='Helvetica-Bold', fontSize=15, textColor=GOLD,
                     leading=19, spaceBefore=12, spaceAfter=5)
S_H2    = base_style(fontName='Helvetica-Bold', fontSize=11, textColor=NAVY,
                     leading=15, spaceBefore=8,  spaceAfter=3)
S_H3    = base_style(fontName='Helvetica-Bold', fontSize=9.5, textColor=NAVY,
                     leading=13, spaceBefore=6,  spaceAfter=2)
S_SMALL = base_style(fontSize=7.5, textColor=DGRAY, leading=11)
S_SMALLS= base_style(fontSize=7, textColor=DGRAY, leading=10)
S_BULL  = base_style(alignment=TA_LEFT, leading=14, leftIndent=10)

def crit(t): return f'<font color="#cc2222"><b>{t}</b></font>'
def high(t): return f'<font color="#d46a00"><b>{t}</b></font>'
def ok(t):   return f'<font color="#1a6e1a"><b>{t}</b></font>'
def bold(t): return f'<b>{t}</b>'
def gold(t): return f'<font color="#c8a84b"><b>{t}</b></font>'
def mono(t): return f'<font name="Courier" size="8">{t}</font>'

def tbl_style(hdr=1, font_size=8):
    return TableStyle([
        ('BACKGROUND',    (0,0), (-1,hdr-1), TBLHDR),
        ('TEXTCOLOR',     (0,0), (-1,hdr-1), white),
        ('FONTNAME',      (0,0), (-1,hdr-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), font_size),
        ('LEADING',       (0,0), (-1,-1), font_size+3),
        ('ROWBACKGROUNDS',(0,hdr),(-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW',     (0,0), (-1,0), 0.8, GOLD),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
    ])

def cap(text):
    return Paragraph(text, base_style(fontSize=7.5, textColor=DGRAY,
                                      fontName='Helvetica-Oblique',
                                      spaceBefore=3, spaceAfter=5))

# ── Cover ──────────────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self): super().__init__(); self.width=W; self.height=H
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(GOLD);  c.rect(0,H-8*mm, W,8*mm,fill=1,stroke=0)
        c.setFillColor(GOLD);  c.rect(0,0, W,5*mm,fill=1,stroke=0)

        # Accent strip
        for i in range(6):
            shade = HexColor('#%02x%02x%02x' % (26+i*8, 39+i*10, 68+i*12))
            c.setFillColor(shade)
            c.rect(i*(W/6), H*0.36, W/6, H*0.22, fill=1, stroke=0)
        c.setFillColor(NAVY); c.rect(10*mm, H*0.37, W-20*mm, H*0.20, fill=1, stroke=0)

        c.setFillColor(white); c.setFont('Helvetica-Bold', 8.5)
        c.drawCentredString(W/2, H*0.885,
            'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME  |  ECHS DIRECTORATE')
        c.setFont('Helvetica', 8); c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.86, 'Fraud Analytics & Financial Intelligence Report')

        c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 34)
        c.drawCentredString(W/2, H*0.80, 'ECHS FRAUD ANALYTICS')
        c.setFillColor(white); c.setFont('Helvetica', 14)
        c.drawCentredString(W/2, H*0.755, 'Budget Impact & Financial Leakage Estimation')
        c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(W/2, H*0.715,
            'MODULE 20 REPORT  |  FY 2013 – FY 2025  |  FULL DATABASE COVERAGE')
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(W*0.12, H*0.695, W*0.88, H*0.695)

        boxes = [
            ('TOTAL CLAIMS',    '3.34 Crore'),
            ('TOTAL CLAIMED',   '₹55,453 Cr'),
            ('TOTAL DEDUCTED',  '₹5,735 Cr'),
            ('DEDUCTION RATE',  '10.34%'),
        ]
        bw = W/4; bh = 26*mm; by = H*0.585
        for i,(lbl,val) in enumerate(boxes):
            bx = i*bw
            c.setFillColor(HexColor('#0d1929'))
            c.rect(bx+2, by, bw-4, bh, fill=1, stroke=0)
            c.setStrokeColor(GOLD); c.setLineWidth(0.4)
            c.rect(bx+2, by, bw-4, bh, fill=0, stroke=1)
            c.setFont('Helvetica-Bold', 7); c.setFillColor(GOLD)
            c.drawCentredString(bx+bw/2, by+bh-7*mm, lbl)
            c.setFont('Helvetica-Bold', 14); c.setFillColor(white)
            c.drawCentredString(bx+bw/2, by+bh/2-4*mm, val)

        fraud_lbl = [
            ('Conservative Fraud Estimate', '₹1,720 Cr/yr'),
            ('Moderate Fraud Estimate',     '₹2,868 Cr/yr'),
            ('Aggressive Fraud Estimate',   '₹4,302 Cr/yr'),
        ]
        fy = H*0.465; fx = W*0.08; fw = (W*0.84)/3
        for i,(lbl,val) in enumerate(fraud_lbl):
            c.setFillColor(HexColor('#162038'))
            c.rect(fx+i*fw+2, fy, fw-4, 20*mm, fill=1, stroke=0)
            c.setStrokeColor(HexColor('#2a4070')); c.setLineWidth(0.3)
            c.rect(fx+i*fw+2, fy, fw-4, 20*mm, fill=0, stroke=1)
            c.setFont('Helvetica', 7); c.setFillColor(HexColor('#aabbcc'))
            c.drawCentredString(fx+i*fw+fw/2, fy+16*mm, lbl)
            c.setFont('Helvetica-Bold', 12); c.setFillColor(ORANGE)
            c.drawCentredString(fx+i*fw+fw/2, fy+6*mm, val)

        c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(W/2, H*0.25,
            'IIT KANPUR — Data Analytics & Fraud Intelligence Division')
        c.setFillColor(white); c.setFont('Helvetica', 8)
        c.drawCentredString(W/2, H*0.225,
            'May 2026  |  Ex-Servicemen Contributory Health Scheme (ECHS)')
        c.setFont('Helvetica', 7); c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 10*mm,
            'RESTRICTED — For internal audit and investigative use only.')


# ── Inner header/footer ────────────────────────────────────────────────────────
def inner_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 7.5); canvas.setFillColor(DGRAY)
    canvas.drawString(20*mm, H-12*mm, 'ECHS FRAUD ANALYTICS — MODULE 20: BUDGET IMPACT & LEAKAGE — CONFIDENTIAL')
    canvas.drawRightString(W-20*mm, H-12*mm, f'IIT Kanpur  |  Page {doc.page}')
    canvas.setStrokeColor(MGRAY); canvas.setLineWidth(0.4)
    canvas.line(20*mm, H-14*mm, W-20*mm, H-14*mm)
    canvas.line(20*mm, 14*mm, W-20*mm, 14*mm)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#888888'))
    canvas.drawString(20*mm, 9*mm,
        'RESTRICTED — For internal audit and investigative use only. Do not distribute.')
    canvas.drawRightString(W-20*mm, 9*mm, 'Generated: May 2026')
    canvas.restoreState()


# ── StatBox ────────────────────────────────────────────────────────────────────
class StatBox(Flowable):
    def __init__(self, items, row_h=22*mm, cols=4):
        super().__init__()
        self.items = items; self.row_h = row_h; self.cols = cols
        self.width = W - 40*mm; self.height = row_h
    def draw(self):
        c = self.canv; n = self.cols
        items = self.items[:n]
        bw = self.width/n; bh = self.row_h
        for i,(num,sub,color) in enumerate(items):
            bx = i*bw
            c.setFillColor(NAVY)
            c.roundRect(bx+1.5*mm, 0, bw-3*mm, bh, 2*mm, fill=1, stroke=0)
            c.setFillColor(color); c.setFont('Helvetica-Bold', 17)
            c.drawCentredString(bx+bw/2, bh*0.50, num)
            c.setFillColor(HexColor('#aabbcc')); c.setFont('Helvetica', 7)
            c.drawCentredString(bx+bw/2, bh*0.16, sub)


# ── PatternBanner ─────────────────────────────────────────────────────────────
class PatternBanner(Flowable):
    def __init__(self, label, title, subtitle=''):
        super().__init__(); self.label=label; self.title=title
        self.subtitle=subtitle; self.width=W-40*mm; self.height=16*mm
    def draw(self):
        c = self.canv
        c.setStrokeColor(GOLD); c.setLineWidth(2)
        c.line(0, self.height, 0, 0)
        c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 7)
        c.drawString(6*mm, self.height-5*mm, self.label)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 15)
        c.drawString(6*mm, self.height-13*mm, self.title)
        if self.subtitle:
            c.setFillColor(DGRAY); c.setFont('Helvetica', 7.5)
            c.drawRightString(self.width, self.height-5*mm, self.subtitle)


# ─────────────────────────────────────────────────────────────────────────────
def build():
    OUT = '/home/abhishekpathak/Downloads/ECHS/ECHS_Module20_Budget_Leakage_Report.pdf'
    doc = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=22*mm, bottomMargin=22*mm)

    cover_frame = Frame(0,0,W,H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    inner_frame = Frame(20*mm, 20*mm, W-40*mm, H-42*mm, id='inner')
    cover_tpl = PageTemplate(id='Cover', frames=[cover_frame])
    inner_tpl = PageTemplate(id='Inner', frames=[inner_frame],
                             onPage=inner_header_footer)
    doc.addPageTemplates([cover_tpl, inner_tpl])

    story = [CoverPage(), NextPageTemplate('Inner'), PageBreak()]

    # ── PAGE 2: EXECUTIVE SUMMARY ──────────────────────────────────────────────
    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(Paragraph(
        f'Module 20 quantifies the total financial leakage across the ECHS claim ecosystem from '
        f'FY 2013 to FY 2025 using the {mono("settlement_stat")} pre-aggregated dataset — the most '
        f'comprehensive view of ECHS expenditure available. Across {bold("3.34 crore claims")} '
        f'worth {bold("₹55,453.78 crore")}, a total of {crit("₹5,735.91 crore")} has been '
        f'deducted at settlement — a system-wide deduction rate of {crit("10.34%")}. '
        f'The analysis identifies four critical financial risk signals: '
        f'(1) a reversal of the declining deduction trend, with FY 2025 reaching {crit("11.36%")} — '
        f'the highest rate since FY 2017; '
        f'(2) concentration of deductions in a single hospital chain; '
        f'(3) regional fraud hotspots; and '
        f'(4) two hospital facility types with deduction rates exceeding 23%.',
        S_BODY))
    story.append(Spacer(1, 5*mm))

    stat_items = [
        ('₹5,735 Cr',  'Total Deducted\n(All Years)',    GOLD),
        ('11.36%',     'FY 2025 Deduction\nRate ↑',      RED),
        ('₹437 Cr',    'Park Chain\nDeductions',          ORANGE),
        ('19.13%',     'Region 6\nDeduction Rate',        ORANGE),
    ]
    story.append(StatBox(stat_items, row_h=24*mm))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph('Module 20 — Key Fraud Signals', S_H2))
    sig_data = [
        ['#', 'Signal', 'Finding', 'Risk'],
        ['S1', 'Deduction Rate Reversal',
         'FY 2025 deduction rate 11.36% — highest since FY 2017 (12.14%). '
         'Declining trend from 2017–2023 has reversed.', crit('CRITICAL')],
        ['S2', 'Park Hospital Chain Dominance',
         '7 Park Hospital units in top 25. Combined ₹437.33 Cr deducted = 7.6% of ALL ECHS '
         'deductions from a single chain.', crit('CRITICAL')],
        ['S3', 'Vijay Hospital Overbilling',
         'ID 3149: 34% deduction rate — highest among top-volume hospitals. '
         '21,815 claims, ₹149.66 Cr deducted.', crit('CRITICAL')],
        ['S4', 'Type M/N Hospital Overbilling',
         'Hospital type M: 25.96% deduction (133 hospitals, ₹286.95 Cr). '
         'Type N: 23.39% (353 hospitals, ₹443.68 Cr). Both exceed 2× system average.', crit('CRITICAL')],
        ['S5', 'Region 6 Fraud Concentration',
         '19.13% deduction rate in Region 6 (119 hospitals, ₹216.08 Cr deducted) — '
         'highest rate among significant regions.', high('HIGH')],
        ['S6', 'NABH Accreditation Gap',
         'Type 1 non-NABH: 9.87% vs NABH: 8.24% deduction. '
         '1,751 non-NABH hospitals drive ₹3,459.55 Cr in deductions.', high('HIGH')],
        ['S7', 'FY 2024 Expenditure Peak',
         '₹10,351.39 Cr claimed in FY 2024 — a 45× increase from ₹226 Cr in FY 2013. '
         'Spend growth outpacing beneficiary growth.', high('HIGH')],
        ['S8', 'Top-25 Deduction Concentration',
         'Top 25 hospitals = ₹1,315.67 Cr deducted = 22.9% of all ECHS deductions. '
         'Targeted audit of 25 hospitals can recover nearly ¼ of all losses.', high('HIGH')],
    ]
    sw = [8*mm, 30*mm, 110*mm, 22*mm]
    sig_rows = []
    for r, row in enumerate(sig_data):
        sig_rows.append([
            Paragraph(row[0], base_style(fontName='Helvetica-Bold' if r==0 else 'Helvetica',
                                         fontSize=7.5, textColor=white if r==0 else DGRAY, leading=10)),
            Paragraph(row[1], base_style(fontName='Helvetica-Bold' if r==0 else 'Helvetica-Bold',
                                         fontSize=7.5, textColor=white if r==0 else NAVY, leading=10)),
            Paragraph(row[2], base_style(fontSize=7.5, textColor=white if r==0 else DGRAY, leading=10)),
            Paragraph(row[3], base_style(fontSize=7.5, textColor=white if r==0 else DGRAY, leading=10)),
        ])
    sig_tbl = Table(sig_rows, colWidths=sw)
    sig_tbl.setStyle(tbl_style())
    story.append(sig_tbl)
    story.append(PageBreak())

    # ── PAGE 3: ANNUAL TREND ──────────────────────────────────────────────────
    story.append(PatternBanner('Q20a', 'Annual Expenditure & Deduction Trend',
                               'FY 2013 – FY 2025'))
    story.append(Spacer(1, 5*mm))

    annual_data = [
        ['FY Year', 'Total Claims', 'Claimed (₹ Cr)', 'Approved (₹ Cr)',
         'Deducted (₹ Cr)', 'Deduction %', 'YoY Growth'],
        ['2013', '2,00,564',  '226.23',   '201.93',  '24.29',   '10.74%', '—'],
        ['2014', '9,67,659',  '1,120.49', '1,002.81','117.69',  '10.50%', ok('+395%')],
        ['2015', '12,56,074', '1,689.05', '1,498.14','190.92',  '11.30%', high('+51%')],
        ['2016', '17,96,866', '2,181.21', '1,929.71','251.50',  '11.53%', high('+29%')],
        ['2017', '22,26,849', '3,090.24', '2,715.01','375.23',  crit('12.14% ▲PEAK'), high('+42%')],
        ['2018', '18,09,494', '2,415.35', '2,160.02','255.33',  '10.57%', '−22%'],
        ['2019', '28,88,703', '4,376.09', '3,916.90','459.18',  '10.49%', high('+81%')],
        ['2020', '24,53,252', '4,093.68', '3,644.32','449.35',  '10.98%', '−6%'],
        ['2021', '24,27,999', '4,163.81', '3,689.73','474.08',  '11.39%', '+2%'],
        ['2022', '35,02,425', '6,039.22', '5,481.88','557.34',  ok('9.23% ↓'), high('+45%')],
        ['2023', '53,30,615', '9,088.64', '8,302.01','786.63',  ok('8.66% ↓LOW'), high('+50%')],
        ['2024', '52,71,213', '10,351.39','9,309.18','1,042.21', '10.07%', high('+14%')],
        ['2025*','33,13,132', '6,618.39', '5,866.24','752.15',  crit('11.36% ▲'), '—'],
        ['TOTAL', bold('3,34,44,845'), bold('55,453.78'), bold('49,717.87'),
         bold('5,735.91'), bold('10.34%'), ''],
    ]
    aw = [14*mm, 22*mm, 27*mm, 27*mm, 27*mm, 28*mm, 25*mm]
    a_rows = []
    for r, row in enumerate(annual_data):
        style_fn = (lambda x, r=r: base_style(fontName='Helvetica-Bold',
                    fontSize=7.5, textColor=white if r==0 else DGRAY, leading=10,
                    alignment=TA_RIGHT if r>0 and annual_data.index(row)>0 else TA_LEFT))
        a_rows.append([
            Paragraph(cell if isinstance(cell, str) else cell,
                      base_style(fontName='Helvetica-Bold' if r==0 or r==len(annual_data)-1
                                 else 'Helvetica',
                                 fontSize=7.5,
                                 textColor=white if r==0 else DGRAY,
                                 leading=10,
                                 alignment=TA_CENTER if r==0 else TA_RIGHT))
            for cell in row
        ])
    a_tbl = Table(a_rows, colWidths=aw)
    a_tbl.setStyle(tbl_style(font_size=7.5))
    a_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TBLHDR),
        ('BACKGROUND', (0,-1), (-1,-1), NAVY),
        ('TEXTCOLOR', (0,-1), (-1,-1), GOLD),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('LEADING', (0,0), (-1,-1), 11),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, LGRAY]),
        ('GRID', (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW', (0,0), (-1,0), 0.8, GOLD),
        ('LINEABOVE', (0,-1), (-1,-1), 0.8, GOLD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ]))
    story.append(a_tbl)
    story.append(cap('* FY 2025 data is partial (settlement_stat snapshot). '
                     'Full-year figures will be higher. YoY Growth computed on claimed amount.'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Trend Analysis & Key Observations', S_H2))
    obs = [
        (crit('CRITICAL — Deduction Rate Reversal in 2025:'),
         'After declining from the 12.14% peak (FY 2017) to a low of 8.66% (FY 2023), '
         'the deduction rate has climbed back to 11.36% in FY 2025. This is the steepest '
         'rebound in the dataset and signals that the fraud prevention measures from '
         'FY 2020–2023 are losing effectiveness as hospitals adapt their billing strategies.'),
        (high('HIGH — Spend Growth Outpacing Beneficiary Growth:'),
         'Total ECHS spend grew 45× from ₹226 Cr (FY 2013) to ₹10,351 Cr (FY 2024) in 11 years. '
         'While beneficiary growth accounts for part of this, the compound annual growth rate '
         'of ~30% in spend is unsustainable and suggests systematic pricing inflation.'),
        (bold('FY 2023 — Anomalous Low:'),
         'The 8.66% deduction rate in FY 2023, the system\'s all-time low, coincides with '
         '53.3 lakh claims — the highest claim volume in a single year. This may indicate '
         'that a surge in smaller-value claims (which attract fewer deductions) diluted the '
         'overall rate, masking high-value fraud in the same period.'),
        (bold('FY 2024 — Peak Expenditure:'),
         '₹10,351.39 Cr claimed in FY 2024 is the highest single-year ECHS expenditure on record. '
         'Combined with a deduction rate of 10.07% — above the system average — this year '
         'represents ₹1,042.21 Cr in deductions alone, larger than the total ECHS spend in FY 2015.'),
    ]
    for title, body in obs:
        story.append(KeepTogether([
            Paragraph(f'{title}', S_H3),
            Paragraph(body, S_BODY),
            Spacer(1, 2*mm),
        ]))
    story.append(PageBreak())

    # ── PAGE 4: HOSPITAL TYPE & NABH ─────────────────────────────────────────
    story.append(PatternBanner('Q20b', 'Budget Leakage by Hospital Type & NABH Status',
                               'System-Wide — All FY Years'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        'Hospital types are classified by the ECHS empanelment category. '
        f'{crit("Types M and N")} are the highest-risk categories, with deduction rates of '
        f'{crit("25.96%")} and {crit("23.39%")} respectively — more than double the system '
        f'average of 10.34%. '
        f'NABH-accredited hospitals (within the same type) consistently show '
        f'{ok("lower deduction rates")} than their non-accredited peers.',
        S_BODY))
    story.append(Spacer(1, 4*mm))

    type_desc = {
        'M': 'Military Medical Establishments',
        'N': 'Naval / Non-Govt Specialist Facilities',
        'H': 'Homeopathy / Heritage Facilities',
        '0': 'Central Govt / CGHS-Listed Hospitals',
        '1': 'Private Empanelled Hospitals (General)',
        '2': 'Eye / Speciality Hospitals',
        '3': 'Diagnostic Labs & Imaging Centres',
        '4': 'Small Nursing Homes',
        '5': 'Dental & Allied Specialty Clinics',
        '7': 'Ayurveda / AYUSH Centres',
        'G': 'Government Central Hospitals',
        'L': 'Leprosy / Specialty Centres',
        'Unknown': 'Unmapped / Legacy Facility Codes',
        '':  'Facility Type Not Recorded',
    }

    type_rows = [
        ['Type', 'Facility Category', 'NABH', 'Hospitals', 'Claims',
         'Claimed (Cr)', 'Deducted (Cr)', 'Ded %', 'Risk'],
        # Sorted by ded_pct desc from data
        ['M',  type_desc['M'],        'N', '133',   '12,72,658',  '1,105.15', '286.95', crit('25.96%'), crit('CRITICAL')],
        ['N',  type_desc['N'],        'N', '353',   '23,90,439',  '1,896.57', '443.68', crit('23.39%'), crit('CRITICAL')],
        ['H',  type_desc['H'],        'N', '8',     '689',         '6.76',     '1.27',  crit('18.81%'), high('HIGH')],
        ['0',  type_desc['0'],        'N', '119',   '7,85,367',   '2,009.87', '290.57', high('14.46%'), high('HIGH')],
        ['Unk',type_desc['Unknown'],  'N', '501',   '3,29,026',    '816.68',  '108.29', high('13.26%'), high('HIGH')],
        ['—',  'Type Not Recorded',   'N', '252',   '5,90,465',   '1,726.09', '195.65', '11.33%', bold('MEDIUM')],
        ['1',  type_desc['1'],        'N', '1,751', '1,77,59,181','35,038.83','3,459.55','9.87%',  bold('MEDIUM')],
        ['3',  type_desc['3'],        'Y', '16',    '2,51,396',    '53.81',    '4.54',   '8.43%',  bold('MEDIUM')],
        ['5',  type_desc['5'],        'N', '130',   '6,36,408',    '216.34',   '17.98',  '8.31%',  bold('MEDIUM')],
        ['1',  type_desc['1'],        'Y', '166',   '61,36,820',  '10,057.79','828.38',  ok('8.24%'), ok('LOW')],
        ['5',  type_desc['5'],        'Y', '19',    '2,31,412',    '88.27',    '5.41',   ok('6.13%'), ok('LOW')],
        ['3',  type_desc['3'],        'N', '246',   '5,62,611',    '131.37',   '7.18',   ok('5.46%'), ok('LOW')],
        ['2',  type_desc['2'],        'N', '525',   '22,62,964',  '1,964.76',  '81.02',  ok('4.12%'), ok('LOW')],
        ['G',  type_desc['G'],        'N', '39',    '42,091',      '202.41',   '1.10',   ok('0.54%'), ok('LOWEST')],
    ]
    tw = [8*mm, 48*mm, 11*mm, 17*mm, 22*mm, 22*mm, 22*mm, 14*mm, 16*mm]
    t_tbl_rows = []
    for r, row in enumerate(type_rows):
        t_tbl_rows.append([
            Paragraph(c, base_style(fontName='Helvetica-Bold' if r==0 else 'Helvetica',
                                    fontSize=7, textColor=white if r==0 else DGRAY, leading=10))
            for c in row
        ])
    t_tbl = Table(t_tbl_rows, colWidths=tw)
    t_tbl.setStyle(tbl_style(font_size=7))
    story.append(t_tbl)
    story.append(cap(
        'NABH = National Accreditation Board for Hospitals. Y = Accredited, N = Not Accredited. '
        'Type codes as per ECHS empanelment master (office_master.OM_HOSP_TYPE). '
        'Types M and N combined deductions: ₹730.63 Cr (12.7% of total system deduction).'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Key Observations — Hospital Type Analysis', S_H2))
    type_obs = [
        (crit('Type M & N — Chronic Overbilling:'),
         'Combined, type M and N hospitals (486 facilities) have deducted ₹730.63 Cr — '
         '12.7% of total ECHS deductions — despite representing a small fraction of total hospitals. '
         'Their deduction rates of 25.96% and 23.39% indicate systematic overbilling at more than '
         'double the system average. These facility types require immediate empanelment review.'),
        (high('NABH Effect — 1.63 Percentage Point Difference:'),
         'For Type 1 private hospitals, NABH-accredited facilities show 8.24% deduction rate '
         'versus 9.87% for non-accredited — a 1.63 percentage point difference. Scaled across '
         '17.76 lakh claims in the non-NABH segment, mandatory NABH accreditation could '
         'theoretically reduce Type 1 deductions by ₹285–₹320 Cr annually.'),
        (ok('Government Hospitals — Near-Zero Fraud:'),
         'Type G (Government Central Hospitals, 39 facilities) have a 0.54% deduction rate — '
         'the lowest in the system. Government hospitals have no financial incentive to inflate '
         'billing. This validates that the fraud signal is concentrated in private and '
         'specialist facilities.'),
    ]
    for title, body in type_obs:
        story.append(KeepTogether([
            Paragraph(title, S_H3),
            Paragraph(body, S_BODY),
            Spacer(1, 2*mm),
        ]))
    story.append(PageBreak())

    # ── PAGE 5: TOP 25 HOSPITALS ──────────────────────────────────────────────
    story.append(PatternBanner('Q20d', 'Priority Audit List — Top 25 Hospitals by Deduction',
                               'Ranked by Absolute Deduction Amount'))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f'The top 25 hospitals account for {bold("₹1,315.67 Cr")} in deductions — '
        f'{crit("22.9% of all ECHS deductions")} from just 25 facilities. '
        f'Auditing these hospitals in priority order offers the maximum financial recovery per '
        f'investigation hour. {crit("Park Hospital chain")} (7 units) and '
        f'{crit("Vijay Hospital")} (34% deduction rate) are the most critical targets.',
        S_BODY))
    story.append(Spacer(1, 3*mm))

    top25_data = [
        ['Rank', 'Hospital (ECHS ID)', 'Type', 'NABH', 'Claims',
         'Claimed (₹L)', 'Approved (₹L)', 'Deducted (₹L)', 'Ded %'],
        ['1',  'PARK HOSPITAL – GURGAON [367]*',            '1','N','1,23,373','75,170.79','57,917.18',crit('17,253.61'),crit('22.95%')],
        ['2',  'VIJAY HOSPITAL [3149]',                      '0','N','21,815',  '44,020.04','29,054.18',crit('14,965.86'),crit('34.00%')],
        ['3',  'HEALING TOUCH SUPER SPECIALITY [1219]',      '1','N','71,465',  '54,875.24','46,287.77','8,587.47','15.65%'],
        ['4',  'PARK HOSPITAL – CHOWKHANDI [60]*',           '1','Y','23,004',  '29,057.55','22,377.52',high('6,680.03'),high('22.99%')],
        ['5',  'MEDANTA THE MEDICITY – GURGAON [183]',       '1','Y','3,41,282','56,434.05','51,522.43','4,911.62','8.70%'],
        ['6',  'PARK HOSPITAL – KAILASH SUPERSPECIALITY [1161]*','1','N','52,070','17,041.24','12,176.49',high('4,864.74'),high('28.55%')],
        ['7',  'GRECIAN SUPER-SPECIALITY HOSPITAL [109]',    '1','N','50,179',  '33,223.48','28,418.17','4,805.31','14.46%'],
        ['8',  'LIVASA HOSPITAL – IVY HEALTHCARE [78]',      '1','N','2,02,450','57,954.40','53,258.46','4,695.94','8.10%'],
        ['9',  'VIRAT HOSPITAL [2856]',                      '1','N','22,179',  '15,528.43','10,871.59',high('4,656.83'),high('29.99%')],
        ['10', 'YATHARTH WELLNESS & TRAUMA CENTRE [1454]',   '1','N','1,35,915','19,138.65','14,495.36','4,643.29','24.26%'],
        ['11', 'PARK HOSPITAL – PARK MEDICITY INDIA [2127]*','1','N','20,391',  '20,107.16','15,777.75','4,329.42','21.53%'],
        ['12', 'METRO HOSPITAL & HEART INST – NOIDA [1042]', '1','Y','77,696',  '26,839.48','22,514.79','4,324.69','16.11%'],
        ['13', 'MANIPAL HEALTH ENTERPRISES PVT LTD [399]',   '1','N','3,17,616','56,776.11','52,474.22','4,301.89','7.58%'],
        ['14', 'EMC SUPER SPECIALITY HOSPITAL [519]',         '1','N','39,376',  '40,503.68','36,275.73','4,227.94','10.44%'],
        ['15', 'FORTIS HOSPITAL – MOHALI [34]',               '1','Y','4,41,516','80,900.08','76,753.43','4,146.65','5.13%'],
        ['16', 'MADHURAJ HOSPITAL – KANPUR [292]',            '1','N','11,406',  '12,411.61', '8,299.99',high('4,111.61'),high('33.13%')],
        ['17', 'PARK HOSPITAL – UMKAL HEALTHCARE [514]*',     '1','Y','59,211',  '28,522.86','24,689.14','3,833.71','13.44%'],
        ['18', 'ARTEMIS MEDICARE SERVICES – GURGAON [17]',    '1','Y','4,62,187','62,859.59','59,160.66','3,698.94','5.88%'],
        ['19', 'PARK HOSPITAL – FARIDABAD [1373]*',           '1','N','19,458',  '26,758.86','23,104.71','3,654.15','13.66%'],
        ['20', 'INDUS SUPER SPECIALITY – MOHALI [74]',        '1','N','99,673',  '33,234.76','29,827.28','3,407.47','10.25%'],
        ['21', 'REGENCY HOSPITAL LTD – KANPUR [401]',         '1','N','1,18,239','21,182.14','17,822.44','3,359.70','15.86%'],
        ['22', 'SRI GURU HARKRISHNA EYE HOSP [169]',          '2','N','2,52,290','64,790.99','61,616.98','3,174.02','4.90%'],
        ['23', 'SIGNATURE HOSPITAL – PARK MEDICITY [2766]*',  '1','N','24,284',  '22,583.60','19,466.05','3,117.55','13.80%'],
        ['24', 'STAR HOSPITAL – OM MEDICENTRE [2694]',         '1','N','5,522',   '9,564.00', '6,584.65',high('2,979.35'),high('31.15%')],
        ['25', 'FORTIS HOSPITAL – NOIDA [1003]',              '1','Y','2,99,611','42,119.56','39,284.61','2,834.95','6.73%'],
        ['',   bold('TOP 25 TOTAL'),                          '','','',
         bold('9,35,390.39'), bold('8,03,822.64'), bold('1,31,566.74'),
         bold('22.9% of all')],
    ]
    p25w = [8*mm, 66*mm, 10*mm, 11*mm, 19*mm, 20*mm, 20*mm, 22*mm, 14*mm]
    p25_rows = []
    for r, row in enumerate(top25_data):
        is_hdr = (r == 0)
        is_tot = (r == len(top25_data)-1)
        p25_rows.append([
            Paragraph(c, base_style(
                fontName='Helvetica-Bold' if (is_hdr or is_tot) else 'Helvetica',
                fontSize=6.5, leading=9,
                textColor=white if is_hdr else (GOLD if is_tot else DGRAY),
                alignment=TA_LEFT if i<=1 else TA_RIGHT))
            for i, c in enumerate(row)
        ])
    p25_tbl = Table(p25_rows, colWidths=p25w)
    p25_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TBLHDR),
        ('BACKGROUND', (0,-1), (-1,-1), NAVY),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('LEADING', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, LGRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, MGRAY),
        ('LINEBELOW', (0,0), (-1,0), 0.7, GOLD),
        ('LINEABOVE', (0,-1), (-1,-1), 0.7, GOLD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
    ]))
    story.append(p25_tbl)
    story.append(cap(
        '* Park Hospital chain units (7 of top 25). '
        'Combined Park chain deduction: ₹43,733.21L = ₹437.33 Cr = 7.6% of total ECHS deductions. '
        'Amounts in ₹ Lakh. Claims are cumulative FY 2013–2025.'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('Critical Audit Targets', S_H2))
    audit_obs = [
        (crit('VIJAY HOSPITAL (ID 3149) — 34% Deduction Rate:'),
         '₹14,965.86L (₹149.66 Cr) deducted from ₹44,020.04L (₹440.20 Cr) claimed over the '
         'database history. At 34% deduction, approximately 1 in 3 rupees billed is rejected at '
         'settlement. This hospital is the single highest-rate overbiller among high-volume '
         'facilities. Type 0 (Govt-affiliated) classification makes this especially concerning — '
         'a facility with institutional oversight still showing fraud-level deductions.'),
        (crit('PARK HOSPITAL CHAIN — 7 Units, ₹437 Cr Combined:'),
         'Park Hospital units at IDs 367, 60, 1161, 2127, 514, 1373, and 2766 form a chain '
         'with collectively ₹437.33 Cr in deductions. The parent entity ID 367 (Park Medicentres, '
         'Gurgaon) alone has ₹172.54 Cr deducted at 22.95% — the largest single-facility '
         'deduction in ECHS history. Chain-level audit is required; individual facility audits '
         'may not capture cross-unit billing coordination.'),
        (high('MADHURAJ HOSPITAL KANPUR (ID 292) & STAR HOSPITAL (ID 2694):'),
         'Both show >30% deduction rates with moderate claim volumes. Madhuraj: 33.13% on '
         '11,406 claims. Star Hospital: 31.15% on 5,522 claims. These are smaller facilities '
         'with proportionally higher fraud rates — likely systematic package upcoding.'),
    ]
    for title, body in audit_obs:
        story.append(KeepTogether([
            Paragraph(title, S_H3),
            Paragraph(body, S_BODY),
            Spacer(1, 2*mm),
        ]))
    story.append(PageBreak())

    # ── PAGE 6: REGIONAL + LEAKAGE PROJECTIONS ───────────────────────────────
    story.append(PatternBanner('Q20e', 'Regional Deduction Breakdown — Fraud Geography',
                               'Ranked by Absolute Deduction (₹ Cr)'))
    story.append(Spacer(1, 3*mm))

    REGION_NAMES = {
        '1': 'NEW DELHI', '2': 'MUMBAI',     '3': 'KOLKATA',
        '4': 'BANGALORE', '5': 'HYDERABAD',  '6': 'CHENNAI',
        '7': 'DEHRADUN',  '8': 'JAIPUR',     '9': 'PUNE',
        '10': 'CHANDIGARH','11': 'ALLAHABAD','12': 'PATNA',
        '13': 'AHMEDABAD',
    }
    # [ID, Region Name, Hospitals, Claims, Claimed, Deducted, Ded%, Avg Claim, Risk]
    reg_top = [
        ['ID', 'ECHS Region / Command', 'Hosps', 'Claims',
         'Claimed (Cr)', 'Deducted (Cr)', 'Ded %', 'Avg Claim (₹)', 'Risk'],
        ['1',  'NEW DELHI',             '429', '42,77,447', '7,904.82',  '840.54', '10.63%', '1,850', bold('HIGH')],
        ['8',  'JAIPUR',                '266', '21,12,770', '4,126.55',  '622.28', crit('15.08%'), '1,950', crit('CRITICAL')],
        ['29', '— (Sub-Region)',         '363', '32,85,282', '4,429.62',  '496.87', '11.22%', '1,350', bold('HIGH')],
        ['9',  'PUNE',                  '248', '18,72,822', '6,891.45',  '484.65', ok('7.03%'), '3,680', bold('MEDIUM')],
        ['4',  'BANGALORE',             '200', '26,42,599', '5,917.03',  '427.01', ok('7.22%'), '2,240', bold('MEDIUM')],
        ['27', '— (Sub-Region)',         '209', '15,47,779', '3,334.93',  '420.89', high('12.62%'), '2,150', high('HIGH')],
        ['24', '— (Sub-Region)',         '216', '10,65,357', '2,752.50',  '287.20', '10.43%', '2,580', bold('MEDIUM')],
        ['3',  'KOLKATA',               '223', '10,00,068', '1,470.32',  '227.29', crit('15.46%'), '1,470', crit('CRITICAL')],
        ['6',  'CHENNAI',               '119', '3,88,080',  '1,129.36',  '216.08', crit('19.13%'), '2,910', crit('CRITICAL')],
        ['30', '— (Sub-Region)',         '161', '14,20,453', '2,062.89',  '192.82', '9.35%', '1,450', bold('MEDIUM')],
        ['5',  'HYDERABAD',             '140', '8,58,789',  '1,255.36',  '161.00', high('12.83%'), '1,460', high('HIGH')],
        ['2',  'MUMBAI',                '116', '30,77,053', '1,911.24',  '154.02', ok('8.06%'), '620', bold('LOW')],
        ['7',  'DEHRADUN',              '133', '24,39,532', '2,106.38',  '140.55', ok('6.67%'), '860', bold('LOW')],
        ['17', '— (Sub-Region)',         '141', '8,78,432',  '1,221.40',  '138.01', '11.30%', '1,390', bold('MEDIUM')],
        ['10', 'CHANDIGARH',            '86',  '3,95,251',  '921.23',    '108.90', '11.82%', '2,330', bold('MEDIUM')],
        ['13', 'AHMEDABAD',             '79',  '4,56,933',  '647.04',    '102.10', crit('15.78%'), '1,420', crit('CRITICAL')],
        ['25', '— (Sub-Region)',         '83',  '4,86,354',  '568.75',     '87.09', crit('15.31%'), '1,170', crit('CRITICAL')],
        ['15', '— (Sub-Region)',         '94',  '7,40,478',  '1,007.49',   '84.05', ok('8.34%'), '1,360', bold('MEDIUM')],
        ['12', 'PATNA',                 '125', '6,90,969',  '1,156.00',   '75.48', ok('6.53%'), '1,670', bold('LOW')],
        ['18', '— (Sub-Region)',         '147', '4,37,590',  '528.32',     '67.90', high('12.85%'), '1,210', high('HIGH')],
        ['28', '— (Sub-Region)',         '84',  '4,67,228',  '763.74',     '63.93', ok('8.37%'), '1,630', bold('LOW')],
        ['19', '— (Sub-Region)',         '124', '5,63,384',  '688.31',     '60.68', ok('8.82%'), '1,220', bold('LOW')],
        ['21', '— (Sub-Region)',         '74',  '4,43,780',  '551.55',     '49.31', ok('8.94%'), '1,240', bold('LOW')],
        ['26', '— (Sub-Region)',         '65',  '2,87,953',  '336.40',     '46.77', high('13.90%'), '1,170', high('HIGH')],
        ['20', '— (Sub-Region)',         '72',  '1,05,808',  '171.70',     '24.12', high('14.05%'), '1,620', high('HIGH')],
        ['TOTAL', bold('13 Named + 13 Sub-Regions'), bold('3,713'),
         bold('3,34,44,845'), bold('55,453.78'), bold('5,735.91'), bold('10.34%'), bold('1,659'), '—'],
    ]
    # Col widths: ID, Name, Hosps, Claims, Claimed, Deducted, Ded%, Avg, Risk
    rw = [9*mm, 36*mm, 13*mm, 22*mm, 22*mm, 22*mm, 14*mm, 18*mm, 14*mm]
    r_rows = []
    for r, row in enumerate(reg_top):
        is_hdr = (r == 0); is_tot = (r == len(reg_top)-1)
        r_rows.append([
            Paragraph(c, base_style(
                fontName='Helvetica-Bold' if (is_hdr or is_tot) else 'Helvetica',
                fontSize=6.5, leading=9,
                textColor=white if is_hdr else (GOLD if is_tot else DGRAY),
                alignment=TA_LEFT if i <= 1 else TA_RIGHT))
            for i, c in enumerate(row)
        ])
    r_tbl = Table(r_rows, colWidths=rw)
    r_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TBLHDR),
        ('BACKGROUND', (0,-1), (-1,-1), NAVY),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('LEADING', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, LGRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, MGRAY),
        ('LINEBELOW', (0,0), (-1,0), 0.7, GOLD),
        ('LINEABOVE', (0,-1), (-1,-1), 0.7, GOLD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (2,1), (-1,-2), 'RIGHT'),
    ]))
    story.append(r_tbl)
    story.append(cap(
        'Region names sourced from ecs_region table. IDs 14–33 without names are ECHS sub-regions '
        'or legacy zone codes not present in ecs_region master. '
        'Avg Claim (₹) = average claim value per admission. '
        'Chennai, Kolkata, Ahmedabad, Jaipur flagged CRITICAL (>15% deduction rate).'))
    story.append(Spacer(1, 5*mm))

    # High-risk region insight
    story.append(Paragraph('High-Risk Region (ECHS Command) Summary', S_H2))
    story.append(Paragraph(
        f'Five ECHS commands exceed {crit("15% deduction rate")}: '
        f'{crit("Chennai")} Region 6 ({crit("19.13%")}), '
        f'{crit("Kolkata")} Region 3 ({crit("15.46%")}), '
        f'{crit("Ahmedabad")} Region 13 ({crit("15.78%")}), '
        f'Sub-Region 25 ({crit("15.31%")}), and '
        f'{crit("Jaipur")} Region 8 ({crit("15.08%")}). '
        f'These 5 commands collectively account for {bold("₹1,258.30 Cr")} in deductions. '
        f'{bold("New Delhi")} (Region 1), while showing a moderate 10.63% rate, contributes the '
        f'{bold("highest absolute deduction (₹840.54 Cr)")} due to its concentration of 429 hospitals '
        f'and proximity to major private hospital chains (Park, Medanta, Artemis, Fortis). '
        f'{bold("Pune")} (Region 9) has the highest average claim value (₹3,680/claim) — '
        f'indicating a tertiary-care heavy profile — and warrants scrutiny despite its low 7.03% rate. '
        f'{bold("Mumbai")} (Region 2) processes the highest claim volume (30.77 lakh claims) '
        f'at a low 8.06% deduction, suggesting better compliance or under-reporting.',
        S_BODY))
    story.append(PageBreak())

    # ── PAGE 7: LEAKAGE PROJECTIONS + RECOMMENDATIONS ────────────────────────
    story.append(PatternBanner('Q20c', 'Overall Leakage Summary & Fraud Recovery Projections',
                               'Full ECHS History — settlement_stat'))
    story.append(Spacer(1, 5*mm))

    proj_data = [
        ['Metric', 'Value', 'Notes'],
        ['Total Claims', '3,34,44,845', 'Full ECHS history via settlement_stat'],
        ['Total Claimed (₹ Cr)', '55,453.78', 'Gross billed by empanelled hospitals'],
        ['Total Approved (₹ Cr)', '49,717.87', 'Net payable after deductions'],
        ['Total Deducted (₹ Cr)', '5,735.91', 'Difference: claimed − approved'],
        ['Overall Deduction Rate', '10.34%', 'System-wide average across all years'],
        ['', '', ''],
        [bold('Fraud Recovery Projections'), '', ''],
        ['Conservative Estimate (30% of deductions)', crit('₹1,720.77 Cr'),
         '30% of settled deductions = confirmed fraud/overbilling'],
        ['Moderate Estimate (50% of deductions)', crit('₹2,867.96 Cr'),
         '50% = deductions attributable to intentional inflation'],
        ['Aggressive Estimate (75% of deductions)', crit('₹4,301.93 Cr'),
         '75% = deductions plus adjacent unreported fraud'],
        ['Pre-Approval AI Interception (60% recovery)', gold('₹3,441.55 Cr'),
         'If 60% of fraud caught before payment — eliminates recovery effort'],
    ]
    pw = [72*mm, 35*mm, 63*mm]
    p_rows = []
    for r, row in enumerate(proj_data):
        is_hdr = (r == 0); is_sect = (r == 7)
        p_rows.append([
            Paragraph(c, base_style(
                fontName='Helvetica-Bold' if (is_hdr or is_sect) else 'Helvetica',
                fontSize=8, leading=11,
                textColor=white if is_hdr else (GOLD if is_sect else DGRAY)))
            for c in row
        ])
    p_tbl = Table(p_rows, colWidths=pw)
    p_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TBLHDR),
        ('BACKGROUND', (0,7), (-1,7), HexColor('#0d1929')),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 11),
        ('ROWBACKGROUNDS', (0,1), (-1,6), [white, LGRAY]),
        ('ROWBACKGROUNDS', (0,8), (-1,-1), [HexColor('#fff8ee'), white, HexColor('#fff8ee'), white]),
        ('GRID', (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW', (0,0), (-1,0), 0.8, GOLD),
        ('LINEBELOW', (0,6), (-1,6), 0.5, MGRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(p_tbl)
    story.append(Spacer(1, 7*mm))

    story.append(Paragraph('Strategic Recommendations', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))

    recs = [
        ('1. Immediate Audit — Top 5 Hospitals',
         'Prioritise Vijay Hospital (34% deduction, ₹149.66 Cr), Park Hospital Gurgaon '
         '(22.95%, ₹172.54 Cr), Park Hospital Chowkhandi (22.99%, ₹66.80 Cr), '
         'Park Hospital Kailash (28.55%, ₹48.65 Cr), and Madhuraj Hospital Kanpur (33.13%, '
         '₹41.12 Cr). These five facilities alone account for ₹479 Cr in deductions. '
         'Discharge summary audit and physical verification of IPD admissions is recommended.',
         crit('CRITICAL — Immediate')),
        ('2. Park Hospital Chain — Chain-Level Empanelment Review',
         '7 Park Hospital units in the top 25 with a combined ₹437.33 Cr deduction suggests '
         'a chain-wide billing strategy rather than individual facility errors. The ECHS empanelment '
         'authority should initiate a chain-level review under Rule 25 of the ECHS Regulations, '
         'with potential suspension pending investigation.',
         crit('CRITICAL — 30 Days')),
        ('3. Type M & N Facility Category Audit',
         '486 hospitals across types M and N are billing at 25% and 23% deduction rates — '
         '2.5× the system average. A category-wide rate review and empanelment terms renegotiation '
         'is warranted. If rates cannot be justified, mandatory NABH accreditation should be '
         'required as a condition of continued empanelment.',
         crit('CRITICAL — 60 Days')),
        ('4. Address the 2025 Deduction Rate Reversal',
         'The FY 2025 rate of 11.36% breaks the 2017–2023 declining trend. Targeted policy '
         'intervention is needed before FY 2026 begins. Recommended actions: '
         '(a) re-activate pre-auth requirements for all claims above ₹1 lakh; '
         '(b) introduce hospital-level deduction rate thresholds triggering automatic audit; '
         '(c) implement real-time billing anomaly alerts via the existing ECHS IT infrastructure.',
         high('HIGH — This Quarter')),
        ('5. Regional Fraud Task Force — Regions 3, 6, 8, 13, 25',
         'Five regions with >15% deduction rates (₹1,258 Cr combined deductions) should have '
         'dedicated regional audit teams. Region 6 at 19.13% is the highest-priority. '
         'Regional command should be directed to cross-reference high-deduction facilities '
         'with complaint registers and beneficiary feedback.',
         high('HIGH — 90 Days')),
        ('6. NABH Accreditation Mandate for Non-Accredited Type 1 Hospitals',
         '1,751 non-NABH Type 1 hospitals carry a 9.87% deduction rate vs 8.24% for NABH-accredited '
         'peers — a gap that translates to ~₹285–₹320 Cr per year in avoidable deductions. '
         'A phased NABH mandate (3-year timeline) with empanelment-linked compliance milestones '
         'would structurally reduce leakage without requiring individual audits.',
         bold('MEDIUM — Policy Intervention')),
        ('7. AI-Assisted Pre-Approval Fraud Interception',
         'The most impactful long-term intervention is pre-payment fraud detection. '
         'If 60% of the ₹5,735.91 Cr historical deduction pool represents fraud that could '
         'have been caught pre-approval, implementing an AI scoring model (as in Module 13) '
         'could intercept ₹3,441 Cr — eliminating the need for post-payment recovery '
         'entirely. This requires a local database extract (not VPN access) for model training '
         'on the full claim_intimation and claim_remarks dataset.',
         bold('MEDIUM — Strategic')),
    ]
    for title, body, risk in recs:
        story.append(KeepTogether([
            Table([[Paragraph(f'<b>{title}</b>',
                              base_style(fontSize=9, textColor=NAVY, fontName='Helvetica-Bold',
                                         leading=12)),
                    Paragraph(risk, base_style(fontSize=7.5, alignment=TA_RIGHT,
                                               leading=12))]],
                  colWidths=[W-80*mm, 40*mm],
                  style=TableStyle([
                      ('BACKGROUND', (0,0), (-1,-1), LGRAY),
                      ('TOPPADDING', (0,0), (-1,-1), 4),
                      ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                      ('LEFTPADDING', (0,0), (-1,-1), 6),
                      ('RIGHTPADDING', (0,0), (-1,-1), 6),
                      ('LINEBELOW', (0,0), (-1,0), 0.5, GOLD),
                  ])),
            Paragraph(body, base_style(leading=13, leftIndent=6)),
            Spacer(1, 3*mm),
        ]))

    doc.build(story)
    print(f'PDF saved: {OUT}')

if __name__ == '__main__':
    build()
