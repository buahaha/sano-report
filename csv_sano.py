#!/usr/bin/env python
# -*- coding: utf-8 -*-

from csv_sano_lib import *

import os
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
settings_path = os.path.join(SITE_ROOT, 'settings.ini')

assert os.path.isfile(settings_path)

# read settings.ini to get configuration
with open(settings_path, 'r') as f:
	files_to_read = read_line_helper(f)
	column = int(read_helper_equals(read_helper_temp_line(f))[1])  # map(int, read_line_helper(f)) || results = [int(i) for i in results]
	row = int(read_helper_equals(read_helper_temp_line(f))[1])
	file = read_helper_equals(read_helper_temp_line(f))[1]
	delim = read_helper_equals(read_helper_temp_line(f))[1]

write_to_csv(os.path.join(SITE_ROOT, file), delim, get_data(files_to_read, delim, row, column))

from TableFactory import *
from calendar import month_name
from datetime import date

current_year = date.today().year
current_month = date.today().month

htmlheader = """\
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html"; charset="utf-8">
<title>Sano</title>
<style type="text/css">

body {{margin: 100px; padding: 0; text-align: left;}}
h1 {{text-align: center}}
img {{display: relative; float: right;}}

body {{ font-family: Helvetica,Arial,FreeSans; margin: 0; padding: 0; text-align: left;width: 600px;}}
table.reporttable {{ border-style: solid; border-width: 1px; margin: 20px auto; text-align: center;}}
table.reporttable tr.tr_odd {{ background-color: white; }}
table.reporttable tr.tr_even {{ background-color: white; }}
table.reporttable th {{ background-color: white; color: black; border: 1px solid black; }}
table.reporttable td.cell_bold {{ font-weight: bold; }}
table.reporttable td.cell_money {{ text-align: right; font-family: monospace; }}
</style>
</head>
<body>
<div id="head">
<img src="logo.png">
<h1>Täglicher Gülle Stand</h1>
<p><b> Monat: {0}</b></p>
<h3>Messzeit täglich immer 8:00 Uhr</h3>
</div>
""".format(month_name[current_month])

htmlfooter = """\
</body>
</html>"""

exampletypes = ((HTMLTable, 'html'), (PDFTable, 'pdf'), (SpreadsheetTable, 'xls'))

mainrs = RowSpec(
    ColumnSpec('', '', width=1),
    ColumnSpec('bar', 'Dairy Farm', width=3, span=3),
    ColumnSpec('baz', 'Heifers Farm', width=1),
    )

subrow1 = RowSpec(
    ColumnSpec('', '', bold=True, span=1, width=1),
    ColumnSpec('dB1', 'B1', bold=True, span=1, width=1),
    ColumnSpec('dB2', 'B2', bold=True, span=1, width=1),
    ColumnSpec('dB3', 'B3', bold=True, span=1, width=1),
    ColumnSpec('hB1', 'B1', bold=True, span=1, width=1))

subrow2 = RowSpec(
    ColumnSpec('Daten', '', bold=True, span=1, width=1),
    ColumnSpec('dArea1', '5.000 m[3]', span=1, width=1),
    ColumnSpec('dArea2', '1.700 m[3]', span=1, width=1),
    ColumnSpec('dArea3', '5.000 m[3]', span=1, width=1),
    ColumnSpec('hArea1', '3.600 m[3]', span=1, width=1))



monthly_data = read_month(file, delim, current_year, current_month)

rows = []
temp = ""
for row in monthly_data:
    if (not temp == row[0]):
    	rows.append([
    		subrow2({'Daten': row[0], 'dArea1': row[1], \
    			'dArea2': row[2], 'dArea3': row[3], 'hArea1': row[4]})
    		])
    temp = row[0]

for tableclass, extension in exampletypes:
    outfile = open('report-{0}-{1}.{2}'.format(current_year, current_month, extension), 'wb')
    if tableclass is HTMLTable:
        outfile.write(htmlheader)
    outfile.write(tableclass(headers=[mainrs, subrow1, subrow2]).render(rows))
    if tableclass is HTMLTable:
        outfile.write(htmlfooter)
