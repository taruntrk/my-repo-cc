with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

bad_start = '<h1 style="margin-top:20px; margin-bottom:14px;">Executive Policy Interventions</h1>'
if bad_start in code:
    code = code.replace(bad_start, 'H.append(f"""\n' + bad_start)

bad_end = 'Generated on {today_str} | Confidential &amp; Restricted Distribution</p>\n</div>\n</div>\n""")'
if bad_end in code:
    pass # Wait, my string replacement had """\) at the end of the regex, which means it deleted the closing bracket!

