import markdown
from weasyprint import HTML
import os

md_path = "/home/tarun/.gemini/antigravity/brain/d10b068d-ca5d-405f-86ea-1a0fc7d0a07b/fraud_explanations.md"
pdf_path = "/home/tarun/Downloads/CC/echs_analysis/module_19/reports/ECHS_Fraud_Explanations.pdf"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

html_content = markdown.markdown(text)

styled_html = f"""
<html>
<head>
<style>
    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 11pt; color: #333; line-height: 1.6; padding: 20px; }}
    h1 {{ color: #2c3e50; border-bottom: 2px solid #e74c3c; padding-bottom: 5px; font-size: 18pt; }}
    h3 {{ color: #2980b9; margin-top: 25px; font-size: 13pt; }}
    ul {{ margin-bottom: 20px; }}
    li {{ margin-bottom: 8px; }}
    strong {{ color: #c0392b; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""

HTML(string=styled_html).write_pdf(pdf_path)
print("PDF created successfully at:", pdf_path)
