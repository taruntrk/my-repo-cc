with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

# 1. Update pattern 5 wildcard
content = content.replace("'file': '05_UID_Duplication.csv',", "'file': '05_UID_Duplication*.csv',")

# 2. Update pattern 6 wildcard
content = content.replace("'file': '08_High_Frequency_Claims.csv',", "'file': '08_High_Frequency_Claims*.csv',")

# 3. Pattern 5 Replace
p5_old = """        p05_data = [['UID (masked)', 'Service #s', 'Cards', 'Claims', 'Hospitals', 'Total Claimed', 'Total Approved']]
        for row in patterns[4]['data'][:15]:
            uid = str(row.get('uid_number', ''))
            masked_uid = uid[:4] + '****' + uid[-4:] if len(uid) == 12 else uid
            p05_data.append([
                Paragraph(masked_uid, bs(fontSize=7, leading=10, fontName='Courier')),
                Paragraph(str(row.get('unique_service_numbers', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(str(row.get('unique_cards', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_hospitals', '0')), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_claimed_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_approved_amount', 0)), bs(fontSize=7, leading=10)),
            ])
        
        p05_tbl = Table(p05_data, colWidths=[24*mm, 18*mm, 16*mm, 16*mm, 18*mm, 28*mm, 28*mm])"""

p5_new = """        p05_data = [['UID (masked)', 'Service #s', 'Claims', 'Hospitals', 'Total Exposure']]
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
        
        p05_tbl = Table(p05_data, colWidths=[28*mm, 20*mm, 18*mm, 52*mm, 30*mm])"""

if p5_old in content:
    content = content.replace(p5_old, p5_new)
    print("OK: Pattern 5 replaced.")

# 4. Pattern 6 Replace
p6_old = """        story.append(Paragraph(
            f'Beneficiaries with 10+ claims in 5 years (indicates potential over-utilization or fraud). '
            f'<font color="#d46a00"><b>{patterns[5]["count"]} cases detected</b></font>. Top 15 by claim count shown.',
            S_BODY
        ))
        story.append(Spacer(1, 4*mm))
        
        p08_data = [['Service #', 'Beneficiary', '# Claims', '# Hosps', 'Years Active', 'Total Claimed', 'Avg/Claim', 'Span (days)']]
        for row in patterns[5]['data'][:15]:
            avg_amt = float(row.get('total_claimed_amount', 0)) / max(int(row.get('total_claims', 1)), 1)
            p08_data.append([
                Paragraph(str(row.get('service_number', ''))[:12], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('beneficiary_name', ''))[:18], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(str(row.get('unique_hospitals', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('years_with_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_claimed_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(avg_amt), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('fraud_span_days', '0')), bs(fontSize=7, leading=10)),
            ])
        
        p08_tbl = Table(p08_data, colWidths=[20*mm, 25*mm, 14*mm, 14*mm, 16*mm, 22*mm, 20*mm, 17*mm])
        p08_tbl.setStyle(tbl_style(font_size=7))
        story.append(p08_tbl)"""

p6_new = """        import glob
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
        story.append(p08_tbl)"""

if p6_old in content:
    content = content.replace(p6_old, p6_new)
    print("OK: Pattern 6 replaced.")
else:
    print("WARNING: Pattern 6 old block not found!")

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report generator updated for P5 and P6.")
