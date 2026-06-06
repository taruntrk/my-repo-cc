with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    content = f.read()

# 1. Update pattern 4 wildcard
content = content.replace("'file': '04_Mobile_Number_Rings.csv',", "'file': '04_Mobile_Number_Rings*.csv',")

# 2. Replace Pattern 4 table section
p4_old = """        p04_data = [['Mobile Number', 'Cards', 'Service #s', 'Claims', 'Hospitals', 'Total Claimed', 'Span (days)']]
        for row in patterns[3]['data'][:15]:
            p04_data.append([
                Paragraph(str(row.get('mobile_number', ''))[:10], bs(fontSize=7, leading=10, fontName='Courier')),
                Paragraph(str(row.get('unique_cards', '0')), bs(fontSize=7, leading=10, textColor=RED, fontName='Helvetica-Bold')),
                Paragraph(str(row.get('unique_service_numbers', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_hospitals', '0')), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_claimed_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(str(int(float(row.get('last_claim_date', '0')[:4]) - float(row.get('first_claim_date', '0')[:4])) * 365 if row.get('first_claim_date') and row.get('last_claim_date') else '0'), bs(fontSize=7, leading=10)),
            ])
        
        p04_tbl = Table(p04_data, colWidths=[22*mm, 16*mm, 18*mm, 16*mm, 18*mm, 28*mm, 22*mm])"""

p4_new = """        p04_data = [['Mobile Number', 'Cards', 'Svc Numbers', 'Claims', 'Hospitals', 'Total Exposure']]
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
        
        p04_tbl = Table(p04_data, colWidths=[22*mm, 14*mm, 16*mm, 14*mm, 48*mm, 25*mm])"""

if p4_old in content:
    content = content.replace(p4_old, p4_new)
    print("OK: Pattern 4 table replaced.")
else:
    print("WARNING: Pattern 4 old block not found!")

# 3. Update pattern 4 description text
p4_desc_old = """            f'Single mobile number linked to 5+ unrelated ECHS cards (fraud ring indicator). '
            f'<font color="#d46a00"><b>{patterns[3]["count"]} cases detected</b></font>. Top 15 by card count shown.'"""
p4_desc_new = """            f'A Mobile Number Ring is when a single mobile number is linked to 5+ distinct ECHS cards '
            f'belonging to different service numbers (ex-servicemen). Legitimate sharing is 2-3 cards within '
            f'a family; 5+ cards indicate a coordinated fraud agent filing claims for multiple identities. '
            f'<font color="#d46a00"><b>{patterns[3]["count"]} rings detected</b></font>. Top 15 by total exposure shown. '
            f'Dummy/invalid numbers are excluded and reported separately.'"""
if p4_desc_old in content:
    content = content.replace(p4_desc_old, p4_desc_new)
    print("OK: Pattern 4 desc replaced.")
else:
    print("WARNING: Pattern 4 desc not found!")

# 4. Update caption
p4_cap_old = "story.append(cap('Cards = Number of unique ECHS cards linked to same mobile number. Indicates coordinated fraud ring.'))"
p4_cap_new = "story.append(cap('Cards = Unique ECHS health cards on same mobile. Svc Numbers = Distinct ex-serviceman IDs sharing the mobile. Total Exposure = Sum of all claims. Dummy numbers excluded.'))"
if p4_cap_old in content:
    content = content.replace(p4_cap_old, p4_cap_new)
    print("OK: Pattern 4 cap replaced.")

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report generator updated for P4.")
