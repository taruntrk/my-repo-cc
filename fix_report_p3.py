with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

# 1. Update pattern 3 wildcard
content = content.replace("'file': '03_Duplicate_Bill_Numbers.csv',", "'file': '03_Duplicate_Bill_Numbers*.csv',")

# 2. Replace Pattern 3 table section
p3_old = """        p03_data = [['Bill Number', 'Bill Date', 'Duplicate Count', 'Total Amount', 'Hospitals', 'Claims']]
        for row in patterns[2]['data'][:15]:
            bill_no = str(row.get('bill_number', ''))
            if len(bill_no) > 22:
                bill_no = bill_no[:19] + '...'
            p03_data.append([
                Paragraph(bill_no, bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('bill_date', ''))[:10], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('duplicate_count', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(format_currency(row.get('total_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('hospitals', ''))[:35], bs(fontSize=6.5, leading=9)),
                Paragraph(str(str(row.get('claim_ids', '')).count('|') + 1 if row.get('claim_ids') else 0), bs(fontSize=7, leading=10)),
            ])
        
        p03_tbl = Table(p03_data, colWidths=[30*mm, 20*mm, 20*mm, 26*mm, 50*mm, 18*mm])"""

p3_new = """        p03_data = [['Bill Number', 'Bill Date', 'Dup Count', 'Beneficiaries', 'Hospitals', 'Total Exposure']]
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
        
        p03_tbl = Table(p03_data, colWidths=[28*mm, 18*mm, 16*mm, 35*mm, 40*mm, 25*mm])"""

if p3_old in content:
    content = content.replace(p3_old, p3_new)
    print("OK: Pattern 3 table replaced.")
else:
    print("WARNING: Pattern 3 old block not found!")

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report generator updated for P3.")
