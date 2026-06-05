import re
import os

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('# '):
        new_lines.append(line[2:])
    elif line.startswith('#\n'):
        new_lines.append('\n')
    else:
        new_lines.append(line)

content = "".join(new_lines)

# Now apply Pattern 1 modifications
pattern1_old = """        p01_data = [['Card Number', 'Svc #s', 'Names', 'Claims', 'Hospitals', 'Total Claimed', 'Total Approved', 'Span (days)']]
        for row in patterns[0]['data'][:15]:
            p01_data.append([
                Paragraph(row.get('card_number', '')[:14], bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_service_numbers', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_names', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('total_claims', '0')), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('unique_hospitals', '0')), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_claimed_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(format_currency(row.get('total_approved_amount', 0)), bs(fontSize=7, leading=10)),
                Paragraph(str(row.get('fraud_span_days', '0')), bs(fontSize=7, leading=10)),
            ])
        
        p01_tbl = Table(p01_data, colWidths=[24*mm, 15*mm, 15*mm, 15*mm, 18*mm, 26*mm, 26*mm, 20*mm])"""

pattern1_new = """        p01_data = [['Card Number', 'Svc #s', 'Names', 'Claims', 'Hospitals', 'Total Exposure']]
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
        
        p01_tbl = Table(p01_data, colWidths=[24*mm, 15*mm, 35*mm, 15*mm, 40*mm, 25*mm])"""

content = content.replace(pattern1_old, pattern1_new)

# Update output report name to use timestamp
old_output = "output_file = os.path.join(reports_folder, \n                               'ECHS_Module11_Identity_Fraud_Report.pdf')"
new_output = """import time\n    ts = time.strftime("%Y%m%d_%H%M%S")\n    output_file = os.path.join(reports_folder, f'ECHS_Module11_Identity_Fraud_Report_{ts}.pdf')"""
content = content.replace(old_output, new_output)
# Single line version too in case formatting is different
old_output_2 = "output_file = os.path.join(reports_folder, 'ECHS_Module11_Identity_Fraud_Report.pdf')"
content = content.replace(old_output_2, new_output)

# Update get_pattern_summary to look for timestamped file for pattern 1
find_csv_code = """
import glob
def get_pattern_summary(data_folder):
    patterns = [
        {
            'num': 1,
            'title': 'Duplicate Card IDs',
            'file': '01_Duplicate_Card_IDs*.csv',
            'severity': 'CRITICAL',
            'description': 'Single ECHS card used by multiple service numbers'
        },"""

content = content.replace("def get_pattern_summary(data_folder):\n    \"\"\"Get summary statistics for all patterns - EXCLUDING Pattern 6 & 7\"\"\"\n    patterns = [\n        {\n            'num': 1,\n            'title': 'Duplicate Card IDs',\n            'file': '01_Duplicate_Card_IDs.csv',\n            'severity': 'CRITICAL',\n            'description': 'Single ECHS card used by multiple service numbers'\n        },", find_csv_code)

load_csv_loop = """    for pattern in patterns:
        if '*' in pattern['file']:
            files = glob.glob(os.path.join(data_folder, pattern['file']))
            if files:
                # Get latest
                files.sort(key=os.path.getmtime, reverse=True)
                filepath = files[0]
            else:
                filepath = os.path.join(data_folder, pattern['file'].replace('*', ''))
        else:
            filepath = os.path.join(data_folder, pattern['file'])"""

content = content.replace("    for pattern in patterns:\n        filepath = os.path.join(data_folder, pattern['file'])", load_csv_loop)

# Remove span description from pattern 1 text
content = content.replace("Svc #s = Unique Service Numbers using same card. Span = Days between first and last claim. Full data in CSV file.", "Svc #s = Unique Service Numbers using same card. Full data in CSV file.")

with open('/home/aman/Desktop/echs_analysis/module_11/generate_module11_report.py', 'w') as f:
    f.write(content)

print("Report generator updated.")
