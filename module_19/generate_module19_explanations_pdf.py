import os
import re
from datetime import date

try:
    from weasyprint import HTML
except ImportError:
    print("ERROR: weasyprint not installed. Please run: pip install weasyprint")
    exit(1)

BASE = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

md_path = "/home/tarun/.gemini/antigravity/brain/406b7255-c353-4381-b9c0-3a06240677de/fraud_explanations.md"
PDF_OUT = os.path.join(REPORTS_DIR, "ECHS_Fraud_Explanations.pdf")

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# Parse the markdown into simple HTML
html_body = []
lines = content.split("\n")
in_list = False

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith("# "):
        if in_list:
            html_body.append("</ul>")
            in_list = False
        html_body.append(f"<h1>{line[2:]}</h1>")
    elif line.startswith("### "):
        if in_list:
            html_body.append("</ul>")
            in_list = False
        html_body.append(f"<h3>{line[4:]}</h3>")
    elif line.startswith("---"):
        if in_list:
            html_body.append("</ul>")
            in_list = False
        html_body.append("<hr/>")
    elif line.startswith("- "):
        if not in_list:
            html_body.append("<ul>")
            in_list = True
        
        # Parse bold text **word**
        item = line[2:]
        item = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", item)
        html_body.append(f"<li>{item}</li>")
    else:
        if in_list:
            html_body.append("</ul>")
            in_list = False
        # Bold text
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        html_body.append(f"<p>{text}</p>")

if in_list:
    html_body.append("</ul>")

html_content = "\n".join(html_body)

today_str = date.today().strftime("%B %d, %Y")

CSS_STR = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10pt;
    color: #111;
    line-height: 1.6;
    background: #fff;
    margin: 0;
}
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @top-left {
        content: "ECHS FRAUD ANALYTICS — EXPLANATIONS GUIDE";
        font-family: Arial; font-size: 7.5pt; font-weight: 700; color: #555;
        border-bottom: 1px solid #ddd; padding-bottom: 4px; vertical-align: bottom;
    }
    @top-right {
        content: "IIT Kanpur | Page " counter(page);
        font-family: Arial; font-size: 7.5pt; color: #555;
        border-bottom: 1px solid #ddd; padding-bottom: 4px; vertical-align: bottom;
    }
    @bottom-left {
        content: "CONFIDENTIAL — For Internal Audit Review Only.";
        font-family: Arial; font-size: 7pt; color: #666; border-top: 1px solid #ddd; padding-top: 3px;
    }
    @bottom-right {
        content: "Generated: """ + today_str + """";
        font-family: Arial; font-size: 7pt; color: #666; border-top: 1px solid #ddd; padding-top: 3px;
    }
}
h1 {
    font-size: 16pt;
    font-weight: 900;
    color: #111;
    text-transform: uppercase;
    border-bottom: 2px solid #111;
    padding-bottom: 6px;
    margin-bottom: 15px;
    margin-top: 10px;
}
p {
    font-size: 10pt;
    margin-bottom: 15px;
    color: #333;
}
h3 {
    font-size: 12pt;
    font-weight: 800;
    color: #111;
    margin-top: 25px;
    margin-bottom: 12px;
    page-break-after: avoid;
}
ul {
    margin-left: 20px;
    margin-bottom: 20px;
    list-style-type: square;
}
li {
    margin-bottom: 8px;
    font-size: 10pt;
    color: #222;
}
li strong {
    color: #111;
}
hr {
    border: 0;
    border-top: 1px dashed #ccc;
    margin: 25px 0;
    page-break-inside: avoid;
}
"""

H = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{CSS_STR}</style>
</head>
<body>
<div style="padding: 10px 0;">
{html_content}
</div>
</body>
</html>"""

HTML(string=H, base_url=BASE).write_pdf(PDF_OUT)
print(f"✅ Explanations PDF generated at: {PDF_OUT}")
