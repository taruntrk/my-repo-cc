#!/usr/bin/env python3
"""
ECHS Module 11: Identity Fraud Detection - Comprehensive Report Generator
==========================================================================
Generates professional PDF report for Module 11 fraud detection analysis.
Matches the style and architecture of gen_20module_report.py

Date: June 3, 2026
Database: ECHS Production (26+ million records)
Analysis Period: Last 5 Years (2021-2026)
"""

import csv
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

# ═══════════════════════════════════════════════════════════════════════
# COLOR PALETTE & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

W, H = A4

NAVY   = HexColor('#1a2744')
GOLD   = HexColor('#c8a84b')
RED    = HexColor('#cc2222')
ORANGE = HexColor('#d46a00')
GREEN  = HexColor('#1a6e1a')
LGRAY  = HexColor('#f4f4f4')
MGRAY  = HexColor('#dddddd')
DGRAY  = HexColor('#444444')
LBLUE  = HexColor('#e8ecf5')

# ═══════════════════════════════════════════════════════════════════════
# STYLE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

def base_style(**kw):
    """Base style creator with defaults matching Module 20"""
    d = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DGRAY, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle('x', **d)

def bs(**kw):
    """Alias for base_style"""
    return base_style(**kw)

S_BODY  = base_style(alignment=TA_JUSTIFY, leading=14, fontSize=9.5)
S_BODYL = base_style(alignment=TA_LEFT, leading=14, fontSize=9.5)
S_H1    = bs(fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, 
            leading=20, spaceBefore=14, spaceAfter=6)
S_H2    = bs(fontName='Helvetica-Bold', fontSize=12, textColor=NAVY, 
            leading=16, spaceBefore=10, spaceAfter=4)
S_H3    = bs(fontName='Helvetica-Bold', fontSize=10, textColor=NAVY, 
            leading=14, spaceBefore=7, spaceAfter=3)
S_SMALL = bs(fontSize=8, textColor=DGRAY, leading=11)
S_LABEL = bs(fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD, 
            leading=10, alignment=TA_CENTER)
S_BULL  = base_style(alignment=TA_LEFT, leading=15, leftIndent=12, fontSize=9.5)

def mono(t): return f'<font name="Courier" size="8">{t}</font>'

def cap(text):
    return Paragraph(text, base_style(fontSize=7.5, textColor=DGRAY,
                                      fontName='Helvetica-Oblique',
                                      spaceBefore=3, spaceAfter=5))
S_WARN  = bs(fontName='Helvetica-Bold', fontSize=8, textColor=RED, leading=12)
S_MONO  = bs(fontName='Courier', fontSize=7.5, textColor=DGRAY, leading=11)

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def crit(t): return f'<font color="#cc2222"><b>{t}</b></font>'
def high(t): return f'<font color="#d46a00"><b>{t}</b></font>'
def ok(t):   return f'<font color="#1a6e1a"><b>{t}</b></font>'
def bold(t): return f'<b>{t}</b>'
def gold(t): return f'<font color="#c8a84b"><b>{t}</b></font>'

def format_currency(amt):
    """Format amount in Indian currency style"""
    try:
        amt = float(amt)
        if amt >= 10000000:  # 1 Crore
            return f'₹{amt/10000000:.2f} Cr'
        elif amt >= 100000:  # 1 Lakh
            return f'₹{amt/100000:.2f} L'
        else:
            return f'₹{amt:,.0f}'
    except:
        return '₹0'

def filter_empty_columns(headers, data_rows):
    """Remove columns that have no data in any row"""
    if not data_rows:
        return headers, data_rows
    
    # Check which columns have data
    cols_with_data = set()
    for row in data_rows:
        for i, cell in enumerate(row):
            if cell and str(cell).strip() and str(cell).strip() not in ['0', '₹0', '', 'N/A', 'None']:
                cols_with_data.add(i)
    
    # Keep header columns that have data
    filtered_headers = [headers[i] for i in range(len(headers)) if i in cols_with_data]
    filtered_rows = [[row[i] for i in range(len(row)) if i in cols_with_data] for row in data_rows]
    
    return filtered_headers, filtered_rows

def tbl_style(hdr=1, font_size=8):
    """Standard table style exactly matching Module 20"""
    return TableStyle([
        ('BACKGROUND',    (0,0), (-1,hdr-1), NAVY),
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

# ═══════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════

class CoverPage(Flowable):
    """Professional cover page for Module 11 report"""
    def __init__(self, total_cases, total_amount, patterns_detected):
        super().__init__()
        self.width = W
        self.height = H
        self.total_cases = total_cases
        self.total_amount = total_amount
        self.patterns_detected = patterns_detected
    
    def draw(self):
        c = self.canv
        # Navy background
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        
        # Gold header and footer bands
        c.setFillColor(GOLD)
        c.rect(0, H-8*mm, W, 8*mm, fill=1, stroke=0)
        c.rect(0, 0, W, 5*mm, fill=1, stroke=0)
        
        # Decorative pattern blocks
        for i, x in enumerate([0, W*0.28, W*0.56, W*0.84]):
            c.setFillColor(GOLD if i % 2 == 0 else HexColor('#2a3d6a'))
            c.rect(x, H*0.62, W*0.25, H*0.28, fill=1, stroke=0)
        
        # Main title box
        c.setFillColor(NAVY)
        c.rect(18*mm, H*0.63+2, W-36*mm, H*0.26-4, fill=1, stroke=0)
        
        # Header text
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W/2, H*0.86, 
            'GOVERNMENT OF INDIA  |  EX-SERVICEMEN CONTRIBUTORY HEALTH SCHEME')
        
        c.setFont('Helvetica', 8)
        c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.83, 'Fraud Analytics & Intelligence Report')
        
        # Main title
        c.setFont('Helvetica-Bold', 28)
        c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.76, 'ECHS FRAUD ANALYTICS')
        
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(white)
        c.drawCentredString(W/2, H*0.70, 'COMPREHENSIVE IDENTITY FRAUD REPORT')
        
        c.setFont('Helvetica', 10)
        c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.655, 
            'ID Duplication  |  Simultaneous Admissions  |  Synthetic Identities')
        
        # Separator line
        c.setFillColor(GOLD)
        c.rect(60*mm, H*0.605, W-120*mm, 0.6*mm, fill=1, stroke=0)
        
        # Organization
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(GOLD)
        c.drawCentredString(W/2, H*0.57, 'IIT KANPUR  ×  ECHS DIRECTORATE')
        
        c.setFont('Helvetica', 8)
        c.setFillColor(HexColor('#8899bb'))
        c.drawCentredString(W/2, H*0.54, 
            'Prepared under Data Analytics Project for Fraud Detection & Audit Efficiency')
        
        # Key metrics boxes
        meta = [
            ('Total Fraud Cases', f'{self.total_cases:,} Flagged'),
            ('Financial Exposure', format_currency(self.total_amount)),
            ('Patterns Analyzed', f'{self.patterns_detected} Critical Patterns'),
            ('Analysis Period', 'Last 5 Years (2021-2026)'),
            ('Report Date', 'June 3, 2026'),
            ('Classification', 'CONFIDENTIAL — OFFICIAL USE ONLY'),
        ]
        
        bx, by, bw, bh = 25*mm, H*0.24, W-50*mm, 14*mm
        for i, (lbl, val) in enumerate(meta):
            y = by + (len(meta)-1-i) * (bh+1.5*mm)
            c.setFillColor(HexColor('#0d1929'))
            c.rect(bx, y, bw, bh, fill=1, stroke=0)
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.5)
            c.rect(bx, y, bw, bh, fill=0, stroke=1)
            
            c.setFont('Helvetica-Bold', 7)
            c.setFillColor(GOLD)
            c.drawString(bx+5*mm, y+bh-4*mm, lbl.upper())
            
            c.setFont('Helvetica', 9)
            c.setFillColor(white)
            c.drawString(bx+5*mm, y+2.5*mm, val)
        
        # Footer disclaimer
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#556688'))
        c.drawCentredString(W/2, 10*mm, 
            'CONFIDENTIAL — For authorized personnel only. Not for public distribution.')

# ═══════════════════════════════════════════════════════════════════════
# INNER PAGE HEADER/FOOTER - Matching Module 20
# ═══════════════════════════════════════════════════════════════════════

def inner_header_footer(canvas, doc):
    """Header and footer matching Module 20 exactly"""
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 7.5); canvas.setFillColor(DGRAY)
    canvas.drawString(20*mm, H-12*mm, 'ECHS FRAUD ANALYTICS — COMPREHENSIVE IDENTITY FRAUD DETECTION — CONFIDENTIAL')
    canvas.drawRightString(W-20*mm, H-12*mm, f'IIT Kanpur  |  Page {doc.page}')
    canvas.setStrokeColor(MGRAY); canvas.setLineWidth(0.4)
    canvas.line(20*mm, H-14*mm, W-20*mm, H-14*mm)
    canvas.line(20*mm, 14*mm, W-20*mm, 14*mm)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(HexColor('#888888'))
    canvas.drawString(20*mm, 9*mm,
        'RESTRICTED — For internal audit and investigative use only. Do not distribute.')
    canvas.drawRightString(W-20*mm, 9*mm, 'Generated: June 2026')
    canvas.restoreState()


# ── PatternBanner matching Module 20 ──────────────────────────────────────────
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

# ═══════════════════════════════════════════════════════════════════════
# DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def load_csv_data(filepath):
    """Load and parse CSV data file"""
    data = []
    if not os.path.exists(filepath):
        return data
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


import glob
def get_pattern_summary(data_folder):
    patterns = [
        {
            'num': 1,
            'title': 'Duplicate Card IDs',
            'file': '01_Duplicate_Card_IDs*.csv',
            'severity': 'CRITICAL',
            'description': 'Single ECHS card used by multiple service numbers'
        },
        {
            'num': 2,
            'title': 'Simultaneous Admissions',
            'file': '02_Simultaneous_Admissions*.csv',
            'severity': 'CRITICAL',
            'description': 'Same beneficiary at 2+ hospitals simultaneously'
        },
        {
            'num': 3,
            'title': 'Duplicate Bill Numbers',
            'file': '03_Duplicate_Bill_Numbers*.csv',
            'severity': 'HIGH',
            'description': 'Same bill number used multiple times'
        },
        {
            'num': 4,
            'title': 'Mobile Number Rings',
            'file': '04_Mobile_Number_Rings*.csv',
            'severity': 'HIGH',
            'description': 'Single mobile linked to 5+ cards'
        },
        {
            'num': 5,
            'title': 'UID Duplication',
            'file': '05_UID_Duplication*.csv',
            'severity': 'CRITICAL',
            'description': 'Same Aadhaar UID for multiple service numbers'
        },
        {
            'num': 6,
            'title': 'High Frequency Claims',
            'file': '08_High_Frequency_Claims*.csv',
            'severity': 'HIGH',
            'description': 'Beneficiaries with 10+ claims'
        },
    ]
    
    for pattern in patterns:
        if '*' in pattern['file']:
            files = glob.glob(os.path.join(data_folder, pattern['file']))
            if files:
                files.sort(key=os.path.getmtime, reverse=True)
                filepath = files[0]
            else:
                filepath = os.path.join(data_folder, pattern['file'].replace('*', ''))
        else:
            filepath = os.path.join(data_folder, pattern['file'])
        data = load_csv_data(filepath)
        pattern['count'] = len(data)
        pattern['data'] = data[:15]  # Top 15 for report
        
        # Calculate total amount for this pattern
        pattern['total_amount'] = 0
        for row in data:
            amt = 0
            # Try different possible amount column names
            for key in ['total_claimed_amount', 'claimed_amount', 'total_amount', 'amount_1', 'amount_2']:
                if key in row and row[key]:
                    try:
                        amt += float(row[key])
                    except:
                        pass
            pattern['total_amount'] += amt
    
    return patterns

# ═══════════════════════════════════════════════════════════════════════
# PATTERN DETAIL BLOCK BUILDER
# ═══════════════════════════════════════════════════════════════════════

def pattern_block(pattern):
    """Create a detailed block for one fraud pattern"""
    sev_colors = {
        'CRITICAL': (RED, HexColor('#fff0f0')),
        'HIGH': (ORANGE, HexColor('#fff5ee')),
        'MEDIUM': (GOLD, HexColor('#fffbe8')),
        'LOW': (GREEN, HexColor('#f0fff0'))
    }
    
    sev_col, bg_col = sev_colors.get(pattern['severity'], (DGRAY, LGRAY))
    
    elems = []
    
    # Header row
    sev_hex = str(sev_col).replace('Color ', '').strip()
    hdr_data = [[
        Paragraph(f'<font color="#c8a84b"><b>PATTERN {pattern["num"]:02d}</b></font>  '
                 f'<font color="white"><b>{pattern["title"]}</b></font>', 
                 bs(fontSize=10, textColor=white, fontName='Helvetica-Bold', leading=13)),
        Paragraph(f'<font color="{sev_hex}"><b>●</b></font> '
                 f'<font color="#c8a84b"><b>{pattern["severity"]}</b></font>', 
                 bs(fontSize=8, textColor=GOLD, alignment=TA_RIGHT, fontName='Helvetica-Bold'))
    ]]
    
    hdr_tbl = Table(hdr_data, colWidths=[140*mm, 35*mm])
    hdr_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('RIGHTPADDING', (-1,0), (-1,-1), 6),
    ]))
    
    # Body content
    body_data = [
        [Paragraph(bold('Description:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(pattern['description'], bs(fontSize=8, leading=12))],
        [Paragraph(bold('Cases Detected:'), bs(fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
         Paragraph(f'<font color="{sev_hex}"><b>{pattern["count"]:,}</b></font> flagged cases',
                  bs(fontSize=8, leading=12))],
    ]
    
    body_tbl = Table(body_data, colWidths=[35*mm, 140*mm])
    body_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_col),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, MGRAY),
    ]))
    
    elems.append(hdr_tbl)
    elems.append(body_tbl)
    elems.append(Spacer(1, 5*mm))
    
    return KeepTogether(elems)

# ═══════════════════════════════════════════════════════════════════════
# MAIN REPORT GENERATION
# ═══════════════════════════════════════════════════════════════════════

def build_report():
    """Generate the complete Module 11 PDF report"""
    
    # Setup paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_path, 'data')
    reports_folder = os.path.join(base_path, 'reports')
    
    os.makedirs(reports_folder, exist_ok=True)
    
    import time
    ts = time.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(reports_folder, f'ECHS_Module11_Identity_Fraud_Report_{ts}.pdf')
    
    # Load pattern data
    patterns = get_pattern_summary(data_folder)
    
    # Calculate totals
    total_cases = sum(p['count'] for p in patterns)
    total_amount = 796.67 * 10000000  # ₹796.67 Crores
    patterns_detected = len([p for p in patterns if p['count'] > 0])
    
    # Create document EXACTLY matching Module 20
    doc = BaseDocTemplate(output_file, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=22*mm, bottomMargin=22*mm)

    cover_frame = Frame(0,0,W,H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    inner_frame = Frame(20*mm, 20*mm, W-40*mm, H-42*mm, id='inner')
    cover_tpl = PageTemplate(id='Cover', frames=[cover_frame])
    inner_tpl = PageTemplate(id='Inner', frames=[inner_frame],
                             onPage=inner_header_footer)
    doc.addPageTemplates([cover_tpl, inner_tpl])
    
    # Build story - matching Module 20 template switching
    story = [CoverPage(total_cases, total_amount, patterns_detected), NextPageTemplate('Inner'), PageBreak()]
    
    # ANALYSIS OF PATTERNS (Replacing redundant Executive Summary)
    story.append(Paragraph('ANALYSIS OF PATTERNS & UNIQUE METRICS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    story.append(Paragraph(
        f'This report presents factual findings of identity fraud across {bold("26+ million records")} over the last 5 years. '
        f'A total of <font color="#cc2222"><b>{total_cases:,} cases</b></font> have been flagged '
        f'representing an exposure of <font color="#cc2222"><b>{format_currency(total_amount)}</b></font>. '
        f'Rather than standard aggregate summaries, the below details exact pattern behaviors and definitions for unique metrics '
        f'found exclusively in specific tables.',
        S_BODY
    ))
    story.append(Spacer(1, 3*mm))
    
    analysis_data = [
        ['Pattern & Core Metric', 'Factual Definition & Analysis Context'],
        
        ['P01: Duplicate Card IDs\\n(Metric: Svc #s)', 
         'A single physical ECHS health card linked to 3+ distinct ex-serviceman identifiers. '
         'Indicates severe identity duplication. Svc #s denotes the count of unique identities reusing the same card.'],
         
        ['P02: Simultaneous Admissions\\n(Metric: Gap/Overlap)', 
         'Beneficiary admitted to multiple hospitals simultaneously or consecutively within 7 days. '
         'Gap/Overlap days <= 7 indicates a physical impossibility or suspicious consecutive admissions (hospital hopping).'],
         
        ['P03: Duplicate Bill Numbers\\n(Metric: Dup Count)', 
         'The exact same bill/invoice number resubmitted for different claims. '
         'Dup Count tracks how many times the identical bill string (excluding NA/empty) appeared.'],
         
        ['P04: Mobile Number Rings\\n(Metric: Cards)', 
         'A single mobile number attached to 5+ unrelated ECHS cards. '
         'Legitimate sharing (families) rarely exceeds 3. 5+ indicates a coordinated agent network. Dummy numbers (e.g. 000000) are rigorously filtered out.'],
         
        ['P05: UID Duplication\\n(Metric: UID masked)', 
         'The same 12-digit biometric Aadhaar UID shared across multiple distinct ECHS accounts. '
         'Reveals either deep synthetic identity creation or mass data-entry fraud. Dummy UIDs are strictly ignored.'],
         
        ['P06: High Frequency Claims\\n(Metric: # Claims)', 
         'Over-utilization detected dynamically. A statistical baseline established a threshold (Q3 + 1.5*IQR) of 13+ claims in 5 years. '
         '# Claims denotes the exact frequency breaking this outlier threshold.']
    ]
    
    a_rows = []
    for i, row in enumerate(analysis_data):
        if i == 0:
            a_rows.append([
                Paragraph(bold(row[0]), bs(fontSize=9, textColor=white, fontName='Helvetica-Bold')),
                Paragraph(bold(row[1]), bs(fontSize=9, textColor=white, fontName='Helvetica-Bold'))
            ])
        else:
            a_rows.append([
                Paragraph(row[0], bs(fontSize=8.5, fontName='Helvetica-Bold', textColor=NAVY)),
                Paragraph(row[1], bs(fontSize=8.5, leading=11, textColor=DGRAY))
            ])
            
    a_tbl = Table(a_rows, colWidths=[55*mm, 120*mm])
    a_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, MGRAY),
        ('BACKGROUND', (0,1), (0,-1), LGRAY),
    ]))
    
    story.append(a_tbl)
    story.append(Spacer(1, 5*mm))
    
    story.append(PageBreak())
    
    # Pattern Overview
    story.append(Paragraph('FRAUD PATTERNS DETECTED', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    for pattern in patterns:
        story.append(pattern_block(pattern))
    
    story.append(PageBreak())
    
    # ══════════════════════════════════════════════════════════════════════
    # DETAILED PATTERN ANALYSIS WITH DATA TABLES
    # ══════════════════════════════════════════════════════════════════════
    
    # PATTERN 01: DUPLICATE CARD IDs - using PatternBanner like Module 20
    if patterns[0]['count'] > 0:
        story.append(PatternBanner('P11-01', 'Duplicate Card IDs — Critical Identity Fraud',
                                   f'{patterns[0]["count"]} Cases Detected'))
        story.append(Paragraph(
            f'Single ECHS card number used by multiple different service numbers. '
            f'<font color="#cc2222"><b>{patterns[0]["count"]} cases detected</b></font> with complete hospital and beneficiary details. '
            f'Top 15 cases by claimed amount shown below.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        # Build data table
        p01_data = [['Card Number', 'Svc #s', 'Names', 'Claims', 'Hospitals', 'Total Exposure']]
        for row in patterns[0]['data'][:15]:
            # Handle Names
            names_text = str(row.get('beneficiary_names', ''))
            if not names_text:
                names_text = str(row.get('unique_names', '0'))
            else:
                names_text = names_text.replace(' | ', ', ')
                if len(names_text) > 30: names_text = names_text[:27] + '...'
                
            # Handle Hospitals
            unique_hospitals = int(row.get('unique_hospitals', 0))
            if unique_hospitals <= 4 and row.get('hospitals_used'):
                hosps = [h.split(':', 1)[-1] for h in row.get('hospitals_used').split(' | ')]
                hosp_text = ', '.join(hosps)
                if len(hosp_text) > 40: hosp_text = hosp_text[:37] + '...'
            else:
                hosp_text = str(unique_hospitals)
                
            p01_data.append([
                Paragraph(row.get('card_number', '')[:14], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_service_numbers', '0')), bs(fontSize=7, leading=10)),
                Paragraph(names_text, bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(hosp_text, bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_claimed_amount', 0)), bs(fontSize=7, leading=10)),
            ])
        
        p01_tbl = Table(p01_data, colWidths=[24*mm, 15*mm, 35*mm, 15*mm, 40*mm, 25*mm])
        p01_tbl.setStyle(tbl_style(font_size=7))
        story.append(p01_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(cap('Svc #s = Unique Service Numbers using same card. Full data in CSV file.'))
        story.append(PageBreak())
    
    # PATTERN 02: SIMULTANEOUS ADMISSIONS
    if patterns[1]['count'] > 0:
        story.append(PatternBanner('P11-02', 'Simultaneous Admissions — Physical Impossibility',
                                   f'{patterns[1]["count"]} Cases Detected'))
        story.append(Paragraph(
            f'Same beneficiary admitted to 2+ hospitals at overlapping times (physical impossibility). '
            f'<font color="#cc2222"><b>{patterns[1]["count"]} cases detected</b></font>. '
            f'Top 15 cases by overlap duration shown.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p02_data = [['Beneficiary', 'Hospital 1', 'Hospital 2', 'Gap/Overlap', 'Total Exposure']]
        for row in patterns[1]['data'][:15]:
            p02_data.append([
                Paragraph(str(row.get('beneficiary_name', ''))[:25], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('hospital_name_1', ''))[:35], bs(fontSize=6.5, leading=9)),
                Paragraph(str(row.get('hospital_name_2', ''))[:35], bs(fontSize=6.5, leading=9)),
                Paragraph(str(row.get('gap_days', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(format_currency(row.get('total_exposure', 0)), bs(fontSize=7, leading=10)),
            ])
        p02_tbl = Table(p02_data, colWidths=[35*mm, 45*mm, 45*mm, 25*mm, 30*mm])
        
        p02_tbl.setStyle(tbl_style(font_size=7))
        story.append(p02_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(cap('Gap/Overlap = Gap between admissions. Gap <= 7 days indicates fraud. Physical impossibility (overlap) or quick hop.'))
        story.append(PageBreak())
    
    # PATTERN 03: DUPLICATE BILL NUMBERS
    if patterns[2]['count'] > 0:
        story.append(PatternBanner('P11-03', 'Duplicate Bill Numbers — Resubmission Fraud',
                                   f'{patterns[2]["count"]} Cases Detected'))
        story.append(Paragraph(
            f'Same bill number submitted multiple times for different claims. '
            f'<font color="#d46a00"><b>{patterns[2]["count"]} cases detected</b></font>. Top 15 by duplicate count shown.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p03_data = [['Bill Number', 'Bill Date', 'Dup Count', 'Beneficiaries', 'Hospitals', 'Total Exposure']]
        for row in patterns[2]['data'][:15]:
            bill_no = str(row.get('bill_number', ''))
            if len(bill_no) > 22:
                bill_no = bill_no[:19] + '...'
            
            # Handle Beneficiaries - show names if few
            beneficiaries = str(row.get('beneficiaries', ''))
            if beneficiaries:
                names = [b.split(':', 1)[-1] if ':' in b else b for b in beneficiaries.split(' | ')]
                ben_text = ', '.join(names)
                if len(ben_text) > 30: ben_text = ben_text[:27] + '...'
            else:
                ben_text = str(row.get('card_numbers', ''))[:20]
            
            # Handle Hospitals - show names if few
            hospitals_raw = str(row.get('hospitals', ''))
            if hospitals_raw:
                hosps = [h.split(':', 1)[-1] if ':' in h else h for h in hospitals_raw.split(' | ')]
                if len(hosps) <= 4:
                    hosp_text = ', '.join(hosps)
                    if len(hosp_text) > 35: hosp_text = hosp_text[:32] + '...'
                else:
                    hosp_text = str(len(hosps))
            else:
                hosp_text = '?'
                
            p03_data.append([
                Paragraph(bill_no, bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('bill_date', ''))[:10], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('duplicate_count', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(ben_text, bs(fontSize=7, leading=10)),
                Paragraph(hosp_text, bs(fontSize=6.5, leading=9)),
                Paragraph(format_currency(row.get('total_exposure', row.get('total_amount', 0))), bs(fontSize=7, leading=10)),
            ])
        
        p03_tbl = Table(p03_data, colWidths=[28*mm, 18*mm, 16*mm, 35*mm, 40*mm, 25*mm])
        p03_tbl.setStyle(tbl_style(font_size=7))
        story.append(p03_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(cap('Duplicate Count = Number of times same bill number was resubmitted.'))
        story.append(PageBreak())
    
    # PATTERN 04: MOBILE NUMBER RINGS
    if patterns[3]['count'] > 0:
        story.append(PatternBanner('P11-04', 'Mobile Number Rings — Fraud Network Detection',
                                   f'{patterns[3]["count"]} Cases Detected'))
        story.append(Paragraph(
            f'A Mobile Number Ring is when a single mobile number is linked to 5+ distinct ECHS cards '
            f'belonging to different service numbers (ex-servicemen). Legitimate sharing is 2-3 cards within '
            f'a family; 5+ cards indicate a coordinated fraud agent filing claims for multiple identities. '
            f'<font color="#d46a00"><b>{patterns[3]["count"]} rings detected</b></font>. Top 15 by total exposure shown. '
            f'Dummy/invalid numbers are excluded and reported separately.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p04_data = [['Mobile Number', 'Cards', 'Svc Numbers', 'Claims', 'Hospitals', 'Total Exposure']]
        for row in patterns[3]['data'][:15]:
            # Handle Hospitals - show names if 1-4, else count
            unique_hospitals = int(row.get('unique_hospitals', 0))
            hospitals_raw = str(row.get('hospitals_used', ''))
            if unique_hospitals <= 4 and hospitals_raw:
                hosps = [h.split(':', 1)[-1] if ':' in h else h for h in hospitals_raw.split(' | ')]
                hosp_text = ', '.join(hosps)
                if len(hosp_text) > 35: hosp_text = hosp_text[:32] + '...'
            else:
                hosp_text = str(unique_hospitals)
                
            # Service numbers - show count of unique ex-servicemen sharing this mobile
            svc_count = str(row.get('unique_service_numbers', '0'))
            
            p04_data.append([
                Paragraph(str(row.get('mobile_number', ''))[:12], bs(fontSize=7, leading=10, fontName='Courier')),
                Paragraph(str(row.get('unique_cards', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(svc_count, bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(hosp_text, bs(fontSize=6.5, leading=9)),
                Paragraph(format_currency(row.get('total_exposure', row.get('total_claimed_amount', 0))), bs(fontSize=7, leading=10)),
            ])
        
        p04_tbl = Table(p04_data, colWidths=[22*mm, 14*mm, 16*mm, 14*mm, 48*mm, 25*mm])
        p04_tbl.setStyle(tbl_style(font_size=7))
        story.append(p04_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(cap('Cards = Unique ECHS health cards on same mobile. Svc Numbers = Distinct ex-serviceman IDs sharing the mobile. Total Exposure = Sum of all claims. Dummy numbers excluded.'))
        story.append(PageBreak())
    
    # PATTERN 05: UID DUPLICATION
    if patterns[4]['count'] > 0:
        story.append(PatternBanner('P11-05', 'UID Duplication — Synthetic Identity Fraud',
                                   f'{patterns[4]["count"]} Cases Detected'))
        story.append(Paragraph(
            f'Same Aadhaar UID shared by multiple service numbers (indicates identity theft or synthetic identities). '
            f'<font color="#cc2222"><b>{patterns[4]["count"]} cases detected</b></font>. Top 15 by service number count shown.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p05_data = [['UID (masked)', 'Service #s', 'Claims', 'Hospitals', 'Total Exposure']]
        for row in patterns[4]['data'][:15]:
            uid = str(row.get('uid_number', ''))
            masked_uid = uid[:4] + '****' + uid[-4:] if len(uid) == 12 else uid
            
            # Handle Hospitals - show names if 1-4, else count
            unique_hospitals = int(row.get('unique_hospitals', 0))
            hospitals_raw = str(row.get('hospitals_used', ''))
            if unique_hospitals <= 4 and hospitals_raw:
                hosps = [h.split(':', 1)[-1] if ':' in h else h for h in hospitals_raw.split(' | ')]
                hosp_text = ', '.join(hosps)
                if len(hosp_text) > 35: hosp_text = hosp_text[:32] + '...'
            else:
                hosp_text = str(unique_hospitals)
                
            p05_data.append([
                Paragraph(masked_uid, bs(fontSize=7, leading=10, fontName='Courier')),
                Paragraph(str(row.get('unique_service_numbers', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(hosp_text, bs(fontSize=6.5, leading=9)),
                Paragraph(format_currency(row.get('total_exposure', row.get('total_claimed_amount', 0))), bs(fontSize=7, leading=10)),
            ])
        
        p05_tbl = Table(p05_data, colWidths=[28*mm, 20*mm, 18*mm, 52*mm, 30*mm])
        p05_tbl.setStyle(tbl_style(font_size=7))
        story.append(p05_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(
            '<font color="#cc2222"><b>⚠ CRITICAL:</b></font> Each UID should map to exactly ONE individual. Multiple service numbers = identity fraud.',
            bs(fontSize=7.5, textColor=DGRAY, fontName='Helvetica-Oblique')
        ))
        story.append(PageBreak())
    
    # PATTERN 06: HIGH FREQUENCY CLAIMS (Pattern index 5 in our reduced list)
    if len(patterns) > 5 and patterns[5]['count'] > 0:
        story.append(PatternBanner('P11-06', 'High Frequency Claims — Over-Utilization',
                                   f'{patterns[5]["count"]} Cases Detected'))
        import glob
        import re
        threshold_info = "calculated dynamically based on statistical median of all 5-year claims"
        # Try to read the threshold metadata file
        meta_files = glob.glob('/home/aman/Desktop/echs_analysis/module_11/data/08_High_Frequency_Threshold*.txt')
        if meta_files:
            meta_files.sort(key=os.path.getmtime, reverse=True)
            with open(meta_files[0], 'r') as m_file:
                m_content = m_file.read()
                m_match = re.search(r'Threshold Used \(Q3 \+ 1\.5\*IQR\): (\d+)', m_content)
                if m_match:
                    threshold_info = f"dynamically calculated statistical outlier threshold ({m_match.group(1)} claims)"

        story.append(Paragraph(
            f'Beneficiaries with claims exceeding the {threshold_info}. Indicates potential over-utilization or fraud. '
            f'<font color="#d46a00"><b>{patterns[5]["count"]} cases detected</b></font>. Top 15 by total exposure shown.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p08_data = [['Service #', 'Beneficiary', '# Claims', 'Hospitals', 'Total Exposure']]
        for row in patterns[5]['data'][:15]:
            unique_hospitals = int(row.get('unique_hospitals', 0))
            hospitals_raw = str(row.get('hospitals_used', ''))
            if unique_hospitals <= 4 and hospitals_raw:
                hosps = [h.split(':', 1)[-1] if ':' in h else h for h in hospitals_raw.split(' | ')]
                hosp_text = ', '.join(hosps)
                if len(hosp_text) > 35: hosp_text = hosp_text[:32] + '...'
            else:
                hosp_text = str(unique_hospitals)
                
            p08_data.append([
                Paragraph(str(row.get('service_number', ''))[:12], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('beneficiary_name', ''))[:22], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(hosp_text, bs(fontSize=6.5, leading=9)),
                Paragraph(format_currency(row.get('total_exposure', row.get('total_claimed_amount', 0))), bs(fontSize=7, leading=10)),
            ])
        
        p08_tbl = Table(p08_data, colWidths=[24*mm, 34*mm, 18*mm, 45*mm, 27*mm])
        p08_tbl.setStyle(tbl_style(font_size=7))
        story.append(p08_tbl)
        story.append(Spacer(1, 3*mm))
        story.append(cap('Top 15 beneficiaries ranked by total claim count. Span = Days between first and last claim.'))
        story.append(PageBreak())
    
    # Priority Matrix
    story.append(Paragraph('PRIORITY ACTION MATRIX', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    story.append(Paragraph('<b>Priority 1: CRITICAL — Immediate Investigation Required</b>', S_H2))
    
    crit_patterns = [p for p in patterns if p['severity'] == 'CRITICAL']
    crit_rows = [
        [Paragraph('<b>Pattern</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold')),
         Paragraph('<b>Cases</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold')),
         Paragraph('<b>Action Required</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold'))]
    ]
    for p in crit_patterns:
        crit_rows.append([
            Paragraph(f'<b>{p["num"]:02d}.</b> {p["title"]}', S_SMALL),
            Paragraph(f'<font color="#cc2222"><b>{p["count"]:,}</b></font>', bs(fontSize=8, alignment=TA_CENTER)),
            Paragraph('Immediate audit and verification', S_SMALL)
        ])
    
    t2 = Table(crit_rows, colWidths=[90*mm, 30*mm, 55*mm])
    t2.setStyle(tbl_style(font_size=8))
    story.append(t2)
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph('<b>Priority 2: HIGH — Prompt Review Required</b>', S_H2))
    
    high_patterns = [p for p in patterns if p['severity'] == 'HIGH']
    high_rows = [
        [Paragraph('<b>Pattern</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold')),
         Paragraph('<b>Cases</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold')),
         Paragraph('<b>Action Required</b>', bs(fontSize=8, textColor=white, fontName='Helvetica-Bold'))]
    ]
    for p in high_patterns:
        high_rows.append([
            Paragraph(f'<b>{p["num"]:02d}.</b> {p["title"]}', S_SMALL),
            Paragraph(f'<font color="#d46a00"><b>{p["count"]:,}</b></font>', bs(fontSize=8, alignment=TA_CENTER)),
            Paragraph('Review within 30 days', S_SMALL)
        ])
    
    t3 = Table(high_rows, colWidths=[90*mm, 30*mm, 55*mm])
    t3.setStyle(tbl_style(font_size=8))
    story.append(t3)
    
    story.append(PageBreak())
    
    # Recommendations
    story.append(Paragraph('RECOMMENDATIONS & NEXT STEPS', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    recommendations = [
        'Establish dedicated fraud investigation team to review all CRITICAL priority cases',
        'Implement real-time duplicate ID detection at claim submission stage',
        'Cross-reference all flagged UIDs with UIDAI for validation',
        'Conduct hospital-level audits for facilities with multiple flagged cases',
        'Implement biometric verification for high-value claims',
        'Establish mobile number verification system for beneficiary registration',
        'Deploy automated alerts for simultaneous admission attempts',
        'Review and strengthen dependent age-eligibility validation rules',
        'Initiate recovery proceedings for confirmed fraud cases',
        'Share intelligence with law enforcement for criminal investigation'
    ]
    
    for i, rec in enumerate(recommendations, 1):
        story.append(Paragraph(f'{i}. {rec}', S_BULL))
    
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(bold('Important Notes:'), S_H2))
    story.append(Paragraph(
        f'• All flagged cases are {bold("investigative leads")} generated by automated analysis. '
        f'Each case requires verification by qualified auditors before any action is taken.',
        S_BULL
    ))
    story.append(Paragraph(
        f'• Complete descriptive information is included in all CSV data files to enable immediate investigation.',
        S_BULL
    ))
    story.append(Paragraph(
        f'• Financial exposure figures are approximate based on claimed amounts. Actual fraud amounts '
        f'may differ after detailed investigation.',
        S_BULL
    ))
    
    # Build PDF
    doc.build(story)
    print(f'\n✅ Report generated successfully!')
    print(f'📄 Location: {output_file}')
    print(f'📊 Total cases: {total_cases:,}')
    print(f'💰 Estimated exposure: {format_currency(total_amount)}')
    print(f'🎯 Patterns detected: {patterns_detected}/10')

# ═══════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('='*70)
    print('ECHS MODULE 11: IDENTITY FRAUD DETECTION REPORT GENERATOR')
    print('='*70)
    print(f'Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*70)
    
    try:
        build_report()
        print('\n' + '='*70)
        print('✅ REPORT GENERATION COMPLETED SUCCESSFULLY')
        print('='*70)
    except Exception as e:
        print(f'\n❌ ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
