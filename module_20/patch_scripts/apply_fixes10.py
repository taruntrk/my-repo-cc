import re

with open("generate_module20_report_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace column header
code = code.replace('<th style="width:15%">Data Status</th>', '<th style="width:18%">Impact Summary</th>')

# Replace the rows one by one.
# Row 1
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>2</td>\n    <td><b>Macro',
    '<td><b>{fmt(total_claims_top)} Claims Evaluated</b></td>\n  </tr>\n  <tr>\n    <td>2</td>\n    <td><b>Macro'
)

# Row 2
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n\n  <tr>\n    <td>3</td>\n    <td><b>Itemized',
    '<td><b>{cr(kpi_deducted_cr)} System-Wide Leakage</b></td>\n  </tr>\n\n  <tr>\n    <td>3</td>\n    <td><b>Itemized'
)

# Row 3
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>4</td>\n    <td><b>Extended',
    '<td><b>1.46M Item Deductions</b></td>\n  </tr>\n  <tr>\n    <td>4</td>\n    <td><b>Extended'
)

# Row 4
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>5</td>\n    <td><b>Ping-Pong',
    '<td><b>838 Extended Stay Cases</b></td>\n  </tr>\n  <tr>\n    <td>5</td>\n    <td><b>Ping-Pong'
)

# Row 5
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>6</td>\n    <td><b>Weekend',
    '<td><b>500 Readmission Events</b></td>\n  </tr>\n  <tr>\n    <td>6</td>\n    <td><b>Weekend'
)

# Row 6
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>7</td>\n    <td><b>Doctor',
    '<td><b>1.32M Weekend Admissions</b></td>\n  </tr>\n  <tr>\n    <td>7</td>\n    <td><b>Doctor'
)

# Row 7
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n  <tr>\n    <td>8</td>\n    <td><b>Threshold',
    '<td><b>17.3K Provider Outliers</b></td>\n  </tr>\n  <tr>\n    <td>8</td>\n    <td><b>Threshold'
)

# Row 8 (Threshold Avoiding)
code = code.replace(
    '<td><b>Extracted</b></td>\n  </tr>\n\n</tbody>',
    '<td><b>2.8K Threshold Events</b></td>\n  </tr>\n\n</tbody>'
)

# Also fix the text in the Methodology column to match our earlier softening adjustments
code = code.replace("Keeping patients admitted > 10 days unnecessarily", "Clinically unusual extended hospital stays (> 10 days)")
code = code.replace("The Friday Hustle: Exploiting lack of physical verification on weekends", "Statistical anomalies in admission rates on non-working days")

with open("generate_module20_report_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS")
