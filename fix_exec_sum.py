with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

# 1. Update Cover Page to remove Module 11 mentions
cover_old_1 = "c.drawCentredString(W/2, H*0.70, 'MODULE 11: IDENTITY FRAUD')"
cover_new_1 = "c.drawCentredString(W/2, H*0.70, 'COMPREHENSIVE IDENTITY FRAUD REPORT')"
if cover_old_1 in content:
    content = content.replace(cover_old_1, cover_new_1)
    
inner_old = "canvas.drawString(20*mm, H-12*mm, 'ECHS FRAUD ANALYTICS — MODULE 11: IDENTITY FRAUD DETECTION — CONFIDENTIAL')"
inner_new = "canvas.drawString(20*mm, H-12*mm, 'ECHS FRAUD ANALYTICS — COMPREHENSIVE IDENTITY FRAUD DETECTION — CONFIDENTIAL')"
if inner_old in content:
    content = content.replace(inner_old, inner_new)

# 2. Update Executive Summary to be more analytical and factual
exec_old = """    # Executive Summary
    story.append(Paragraph('EXECUTIVE SUMMARY', S_H1))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=6))
    
    story.append(Paragraph(
        f'This report presents the comprehensive findings of the {bold("Module 11: Identity Fraud Detection")} '
        f'analysis conducted on the ECHS production database covering {bold("the last 5 years (2021-2026)")}. '
        f'The analysis examined {bold("26+ million claim records")} to identify systematic identity-related fraud '
        f'patterns including duplicate identifiers, simultaneous admissions, synthetic identities, and coordinated fraud rings. '
        f'{bold("Six critical patterns")} were analyzed with complete descriptive information for immediate action.',
        S_BODY
    ))
    story.append(Spacer(1, 5*mm))
    
    # Key findings table
    key_findings = [
        ['Metric', 'Value'],
        ['Total Cases Flagged', f'{total_cases:,} cases'],
        ['Financial Exposure', format_currency(total_amount)],
        ['Patterns Analyzed', '6 critical fraud patterns'],
        ['Patterns with Data', f'{patterns_detected} patterns'],
        ['Critical Severity', f'{len([p for p in patterns if p["severity"]=="CRITICAL"])} patterns'],
        ['High Severity', f'{len([p for p in patterns if p["severity"]=="HIGH"])} patterns'],
        ['Analysis Period', '2021-2026 (5 years)'],
        ['Data Completeness', '100% - Full descriptive information'],
    ]
    
    kf_rows = []
    for i, row in enumerate(key_findings):
        if i == 0:  # Header row
            kf_rows.append([
                Paragraph(bold(row[0]), bs(fontSize=9, textColor=white, fontName='Helvetica-Bold')),
                Paragraph(bold(row[1]), bs(fontSize=9, textColor=white, fontName='Helvetica-Bold'))
            ])
        else:  # Data rows
            # Apply color coding for specific rows
            value_text = row[1]
            if i in [1, 2]:  # Cases and exposure - critical
                value_para = Paragraph(f'<font color="#cc2222"><b>{value_text}</b></font>', bs(fontSize=9))
            elif i == 8:  # Data completeness - ok
                value_para = Paragraph(f'<font color="#1a6e1a"><b>{value_text}</b></font>', bs(fontSize=9))
            else:
                value_para = Paragraph(value_text, bs(fontSize=9))
            
            kf_rows.append([
                Paragraph(row[0], bs(fontSize=9, fontName='Helvetica-Bold', textColor=NAVY)),
                value_para
            ])
    
    t = Table(kf_rows, colWidths=[70*mm, 105*mm])
    t.setStyle(tbl_style(font_size=9))
    story.append(t)
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(
        f'The analysis identified <font color="#cc2222"><b>{total_cases:,} cases</b></font> requiring immediate investigation '
        f'with an estimated financial exposure of <font color="#cc2222"><b>{format_currency(total_amount)}</b></font>. '
        f'All flagged cases include complete descriptive information (hospital names, beneficiary details, '
        f'patient demographics, claim amounts) enabling immediate action without additional database queries.',
        S_BODY
    ))"""

exec_new = """    # ANALYSIS OF PATTERNS (Replacing redundant Executive Summary)
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
        
        ['P01: Duplicate Card IDs\n(Metric: Svc #s)', 
         'A single physical ECHS health card linked to 3+ distinct ex-serviceman identifiers. '
         'Indicates severe identity duplication. Svc #s denotes the count of unique identities reusing the same card.'],
         
        ['P02: Simultaneous Admissions\n(Metric: Gap/Overlap)', 
         'Beneficiary admitted to multiple hospitals simultaneously or consecutively within 7 days. '
         'Gap/Overlap days <= 7 indicates a physical impossibility or suspicious consecutive admissions (hospital hopping).'],
         
        ['P03: Duplicate Bill Numbers\n(Metric: Dup Count)', 
         'The exact same bill/invoice number resubmitted for different claims. '
         'Dup Count tracks how many times the identical bill string (excluding NA/empty) appeared.'],
         
        ['P04: Mobile Number Rings\n(Metric: Cards)', 
         'A single mobile number attached to 5+ unrelated ECHS cards. '
         'Legitimate sharing (families) rarely exceeds 3. 5+ indicates a coordinated agent network. Dummy numbers (e.g. 000000) are rigorously filtered out.'],
         
        ['P05: UID Duplication\n(Metric: UID masked)', 
         'The same 12-digit biometric Aadhaar UID shared across multiple distinct ECHS accounts. '
         'Reveals either deep synthetic identity creation or mass data-entry fraud. Dummy UIDs are strictly ignored.'],
         
        ['P06: High Frequency Claims\n(Metric: # Claims)', 
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
    story.append(Spacer(1, 5*mm))"""

if exec_old in content:
    content = content.replace(exec_old, exec_new)
    print("OK: Exec Summary replaced.")
else:
    print("WARNING: Exec Summary not found!")
    
with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report cover and executive summary updated.")
