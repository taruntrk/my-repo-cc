with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

# 1. Update pattern 2 wildcard
content = content.replace("'file': '02_Simultaneous_Admissions.csv',", "'file': '02_Simultaneous_Admissions*.csv',")

# 2. Replace Pattern 2 table section
p2_old = """        # Check if amounts are available
        has_amounts = False
        for row in patterns[1]['data'][:15]:
            amt1 = float(row.get('amount_1', 0) or 0)
            amt2 = float(row.get('amount_2', 0) or 0)
            if amt1 > 0 or amt2 > 0:
                has_amounts = True
                break
        
        if has_amounts:
            # Show with amounts
            p02_data = [['Service Number', 'Beneficiary', 'Hospital 1', 'Hospital 2', 'Overlap Days', 'Amount 1', 'Amount 2']]
            for row in patterns[1]['data'][:15]:
                p02_data.append([
                    Paragraph(str(row.get('service_number', ''))[:14], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('beneficiary_name', ''))[:22], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('hospital_name_1', ''))[:28], bs(fontSize=6.5, leading=9)),
                    Paragraph(str(row.get('hospital_name_2', ''))[:28], bs(fontSize=6.5, leading=9)),
                    Paragraph(str(row.get('overlap_days', '0')), bs(fontSize=7, leading=10)),
                    Paragraph(format_currency(row.get('amount_1', 0)), bs(fontSize=7, leading=10)),
                    Paragraph(format_currency(row.get('amount_2', 0)), bs(fontSize=7, leading=10)),
                ])
            p02_tbl = Table(p02_data, colWidths=[22*mm, 28*mm, 32*mm, 32*mm, 18*mm, 24*mm, 24*mm])
        else:
            # Show without amounts - wider columns for hospitals
            p02_data = [['Service Number', 'Beneficiary', 'Hospital 1', 'Hospital 2', 'Overlap Days']]
            for row in patterns[1]['data'][:15]:
                p02_data.append([
                    Paragraph(str(row.get('service_number', ''))[:14], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('beneficiary_name', ''))[:25], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('hospital_name_1', ''))[:35], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('hospital_name_2', ''))[:35], bs(fontSize=7, leading=10)),
                    Paragraph(str(row.get('overlap_days', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                ])
            p02_tbl = Table(p02_data, colWidths=[24*mm, 32*mm, 45*mm, 45*mm, 24*mm])"""

p2_new = """        p02_data = [['Beneficiary', 'Hospital 1', 'Hospital 2', 'Gap/Overlap', 'Total Exposure']]
        for row in patterns[1]['data'][:15]:
            p02_data.append([
                Paragraph(str(row.get('beneficiary_name', ''))[:25], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('hospital_name_1', ''))[:35], bs(fontSize=6.5, leading=9)),
                Paragraph(str(row.get('hospital_name_2', ''))[:35], bs(fontSize=6.5, leading=9)),
                Paragraph(str(row.get('gap_days', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(format_currency(row.get('total_exposure', 0)), bs(fontSize=7, leading=10)),
            ])
        p02_tbl = Table(p02_data, colWidths=[35*mm, 45*mm, 45*mm, 25*mm, 30*mm])"""

if p2_old in content:
    content = content.replace(p2_old, p2_new)
else:
    print("WARNING: p2_old not found")
    
cap_old = "story.append(cap('Overlap Days = Days when patient was simultaneously admitted at both hospitals. Physical impossibility indicates fraud.'))"
cap_new = "story.append(cap('Gap/Overlap = Gap between admissions. Gap <= 7 days indicates fraud. Physical impossibility (overlap) or quick hop.'))"

if cap_old in content:
    content = content.replace(cap_old, cap_new)

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report generator updated for P2.")
