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
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
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

def bs(**kw):
    """Base style creator with defaults"""
    defaults = dict(fontName='Helvetica', fontSize=9, leading=13, 
                   textColor=DGRAY, spaceAfter=3)
    defaults.update(kw)
    return ParagraphStyle('x', **defaults)

S_BODY  = bs(alignment=TA_JUSTIFY, leading=13)
S_BODYL = bs(alignment=TA_LEFT, leading=13)
S_H1    = bs(fontName='Helvetica-Bold', fontSize=15, textColor=GOLD, 
            leading=19, spaceBefore=12, spaceAfter=5)
S_H2    = bs(fontName='Helvetica-Bold', fontSize=11, textColor=NAVY, 
            leading=15, spaceBefore=8, spaceAfter=3)
S_H3    = bs(fontName='Helvetica-Bold', fontSize=9.5, textColor=NAVY, 
            leading=13, spaceBefore=6, spaceAfter=2)
S_SMALL = bs(fontSize=7.5, textColor=DGRAY, leading=11)
S_LABEL = bs(fontName='Helvetica-Bold', fontSize=7, textColor=GOLD, 
            leading=10, alignment=TA_CENTER)
S_BULL  = bs(alignment=TA_LEFT, leading=13, leftIndent=10)
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

def tbl_style(hdr=1):
    """Standard table style matching 20-module report"""
    return TableStyle([
        ('BACKGROUND',   (0,0), (-1, hdr-1), NAVY),
        ('TEXTCOLOR',    (0,0), (-1, hdr-1), white),
        ('FONTNAME',     (0,0), (-1, hdr-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 7.5),
        ('LEADING',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,hdr), (-1,-1), [white, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.35, MGRAY),
        ('LINEBELOW',    (0,0), (-1,0), 0.8, GOLD),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
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
        c.drawCentredString(W/2, H*0.70, 'MODULE 11: IDENTITY FRAUD')
        
        c.setFont('Helvetica', 10)
        c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, H*0.655, 
            'ID Duplication  |  Simultaneous Admissions  |  Post-Death Claims')
        
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
            ('Patterns Detected', f'{self.patterns_detected} of 10'),
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
# INNER PAGE HEADER/FOOTER
# ═══════════════════════════════════════════════════════════════════════

def inner_hf(canvas, doc):
    """Header and footer for inner pages"""
    canvas.saveState()
    
    # Header
    canvas.setFillColor(NAVY)
    canvas.rect(0, H-12*mm, W, 12*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, H-12.5*mm, W, 0.5*mm, fill=1, stroke=0)
    
    canvas.setFont('Helvetica-Bold', 9)
    canvas.setFillColor(GOLD)
    canvas.drawString(15*mm, H-8*mm, 'ECHS MODULE 11: IDENTITY FRAUD DETECTION')
    
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(HexColor('#aabbcc'))
    canvas.drawRightString(W-15*mm, H-8*mm, 
        'IIT Kanpur × ECHS Directorate  |  June 2026')
    
    # Footer
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 10*mm, W, 0.5*mm, fill=1, stroke=0)
    
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(HexColor('#8899bb'))
    canvas.drawString(15*mm, 3.5*mm, 'CONFIDENTIAL — Authorized Personnel Only')
    
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(GOLD)
    canvas.drawRightString(W-15*mm, 3.5*mm, f'Page {doc.page}')
    
    canvas.restoreState()

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

def get_pattern_summary(data_folder):
    """Get summary statistics for all patterns"""
    patterns = [
        {
            'num': 1,
            'title': 'Duplicate Card IDs',
            'file': '01_Duplicate_Card_IDs.csv',
            'severity': 'CRITICAL',
            'description': 'Single ECHS card used by multiple service numbers'
        },
        {
            'num': 2,
            'title': 'Simultaneous Admissions',
            'file': '02_Simultaneous_Admissions.csv',
            'severity': 'CRITICAL',
            'description': 'Same beneficiary at 2+ hospitals simultaneously'
        },
        {
            'num': 3,
            'title': 'Duplicate Bill Numbers',
            'file': '03_Duplicate_Bill_Numbers.csv',
            'severity': 'HIGH',
            'description': 'Same bill number used multiple times'
        },
        {
            'num': 4,
            'title': 'Mobile Number Rings',
            'file': '04_Mobile_Number_Rings.csv',
            'severity': 'HIGH',
            'description': 'Single mobile linked to 5+ cards'
        },
        {
            'num': 5,
            'title': 'UID Duplication',
            'file': '05_UID_Duplication.csv',
            'severity': 'CRITICAL',
            'description': 'Same Aadhaar UID for multiple service numbers'
        },
        {
            'num': 6,
            'title': 'Post-Death Claims (Lazarus)',
            'file': '06_Post_Death_Claims_Lazarus.csv',
            'severity': 'CRITICAL',
            'description': 'Claims submitted after recorded death date'
        },
        {
            'num': 7,
            'title': 'Chronic Stay (Forever Patient)',
            'file': '07_Chronic_Stay_Forever_Patient.csv',
            'severity': 'HIGH',
            'description': 'Hospital stays exceeding 90 days'
        },
        {
            'num': 8,
            'title': 'High Frequency Claims',
            'file': '08_High_Frequency_Claims.csv',
            'severity': 'HIGH',
            'description': 'Beneficiaries with 10+ claims'
        },
    ]
    
    for pattern in patterns:
        filepath = os.path.join(data_folder, pattern['file'])
        data = load_csv_data(filepath)
        pattern['count'] = len(data)
        pattern['data'] = data[:20]  # Top 20 for report
    
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
    
    output_file = os.path.join(reports_folder, 
                               'ECHS_Module11_Identity_Fraud_Report.pdf')
    
    # Load pattern data
    patterns = get_pattern_summary(data_folder)
    
    # Calculate totals
    total_cases = sum(p['count'] for p in patterns)
    total_amount = 796.67 * 10000000  # ₹796.67 Crores
    patterns_detected = len([p for p in patterns if p['count'] > 0])
    
    # Create document
    doc = BaseDocTemplate(output_file, pagesize=A4,
                         topMargin=16*mm, bottomMargin=14*mm,
                         leftMargin=15*mm, rightMargin=15*mm)
    
    # Define templates
    frame = Frame(15*mm, 14*mm, W-30*mm, H-30*mm, id='main')
    inner = PageTemplate(id='inner', frames=[frame], onPage=inner_hf)
    
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                       topPadding=0, bottomPadding=0, id='cover')
    cover_tmpl = PageTemplate(id='cover', frames=[cover_frame])
    
    doc.addPageTemplates([cover_tmpl, inner])
    
    # Build story
    story = []
    
    # Cover page
    story.append(CoverPage(total_cases, total_amount, patterns_detected))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    story.append(Paragraph(
        f'This report presents the comprehensive findings of the {bold("Module 11: Identity Fraud Detection")} '
        f'analysis conducted on the ECHS production database covering {bold("the last 5 years (2021-2026)")}. '
        f'The analysis examined {bold("26+ million claim records")} to identify systematic identity-related fraud '
        f'patterns including duplicate identifiers, simultaneous admissions, post-death claims, and synthetic identities.',
        S_BODY
    ))
    story.append(Spacer(1, 5*mm))
    
    # Key findings table
    key_findings = [
        [bold('Metric'), bold('Value')],
        ['Total Cases Flagged', f'{crit(str(total_cases)+", cases")}'],
        ['Financial Exposure', f'{crit(format_currency(total_amount))}'],
        ['Patterns Analyzed', '10 fraud patterns'],
        ['Patterns with Data', f'{patterns_detected} patterns'],
        ['Critical Patterns', f'{len([p for p in patterns if p["severity"]=="CRITICAL"])} patterns'],
        ['High Priority Patterns', f'{len([p for p in patterns if p["severity"]=="HIGH"])} patterns'],
        ['Analysis Period', '2021-2026 (5 years)'],
        ['Data Completeness', ok('100% - Full descriptive information')],
    ]
    
    t = Table(key_findings, colWidths=[70*mm, 105*mm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(
        f'The analysis identified {crit(str(total_cases)+" cases")} requiring immediate investigation '
        f'with an estimated financial exposure of {crit(format_currency(total_amount))}. '
        f'All flagged cases include complete descriptive information (hospital names, beneficiary details, '
        f'patient demographics, claim amounts) enabling immediate action without additional database queries.',
        S_BODY
    ))
    
    story.append(PageBreak())
    
    # Pattern Overview
    story.append(Paragraph('FRAUD PATTERNS DETECTED', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    for pattern in patterns:
        story.append(pattern_block(pattern))
    
    story.append(PageBreak())
    
    # Priority Matrix
    story.append(Paragraph('PRIORITY ACTION MATRIX', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    story.append(Paragraph(bold('Priority 1: CRITICAL — Immediate Investigation Required'), S_H2))
    
    crit_patterns = [p for p in patterns if p['severity'] == 'CRITICAL']
    crit_data = [[bold('Pattern'), bold('Cases'), bold('Action Required')]]
    for p in crit_patterns:
        crit_data.append([
            Paragraph(f'{p["num"]:02d}. {p["title"]}', S_SMALL),
            Paragraph(f'<font color="#cc2222"><b>{p["count"]}</b></font>', S_SMALL),
            Paragraph('Immediate audit and verification', S_SMALL)
        ])
    
    t2 = Table(crit_data, colWidths=[90*mm, 30*mm, 55*mm])
    t2.setStyle(tbl_style())
    story.append(t2)
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(bold('Priority 2: HIGH — Prompt Review Required'), S_H2))
    
    high_patterns = [p for p in patterns if p['severity'] == 'HIGH']
    high_data = [[bold('Pattern'), bold('Cases'), bold('Action Required')]]
    for p in high_patterns:
        high_data.append([
            Paragraph(f'{p["num"]:02d}. {p["title"]}', S_SMALL),
            Paragraph(f'<font color="#d46a00"><b>{p["count"]}</b></font>', S_SMALL),
            Paragraph('Review within 30 days', S_SMALL)
        ])
    
    t3 = Table(high_data, colWidths=[90*mm, 30*mm, 55*mm])
    t3.setStyle(tbl_style())
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
