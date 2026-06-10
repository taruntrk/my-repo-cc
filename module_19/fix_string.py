with open('generate_module19_report_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all bad footers
import re
bad_footer = r"""    </body>\n    </html>\n    """ + '\"\"\"' + r"""\n    \n    print\("Generating PDF..."\)\n    HTML\(string=H, base_url=BASE\)\.write_pdf\(PDF_OUT\)\n    print\(f"✅ PDF successfully generated at: \{PDF_OUT\}"\)\n\nif __name__ == "__main__":\n    generate_report\(\)"""

# Also it could be:
text = text.replace("</body>\n    </html>\n    \"\"\"\n    \n    print(\"Generating PDF...\")\n    HTML(string=H, base_url=BASE).write_pdf(PDF_OUT)\n    print(f\"✅ PDF successfully generated at: {PDF_OUT}\")\n\nif __name__ == \"__main__\":\n    generate_report()", "")

text = text.replace("    </body>\n    </html>\n    \"\"\"\n    \n    print(\"Generating PDF...\")\n    HTML(string=H, base_url=BASE).write_pdf(PDF_OUT)\n    print(f\"✅ PDF successfully generated at: {PDF_OUT}\")\n\nif __name__ == \"__main__\":\n    generate_report()\n", "")

text = re.sub(r'\s*</body>\s*</html>\s*"""\s*print\("Generating PDF..."\)\s*HTML\(string=H, base_url=BASE\)\.write_pdf\(PDF_OUT\)\s*print\(f"✅ PDF successfully generated at: \{PDF_OUT\}"\)\s*if __name__ == "__main__":\s*generate_report\(\)\s*', '', text)

# Just clean up everything after the last Pattern 10 div closing
parts = text.rsplit('Stay Extension Farming</div>\n        <div class="kf-item"><b>Artificial Discharge Delays:</b> Hospitals artificially delay patient discharge, requesting "Stay Extensions" strictly to farm daily room rent. A clear spike in requests for exactly 2 or 3 extra days across standard procedures indicates systematic manipulation of discharge protocols.</div>\n    </div>', 1)

if len(parts) == 2:
    clean_text = parts[0] + 'Stay Extension Farming</div>\n        <div class="kf-item"><b>Artificial Discharge Delays:</b> Hospitals artificially delay patient discharge, requesting "Stay Extensions" strictly to farm daily room rent. A clear spike in requests for exactly 2 or 3 extra days across standard procedures indicates systematic manipulation of discharge protocols.</div>\n    </div>\n</body>\n</html>\n"""\n\n    print("Generating PDF...")\n    HTML(string=H, base_url=BASE).write_pdf(PDF_OUT)\n    print(f"✅ PDF successfully generated at: {PDF_OUT}")\n\nif __name__ == "__main__":\n    generate_report()\n'
    with open('generate_module19_report_html.py', 'w', encoding='utf-8') as f:
        f.write(clean_text)
    print("Fixed.")
else:
    print("Could not find anchor.")
