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
<meta  http-equiv="Content-Type" content="text/html" charset="utf-8" />
<title>Sano Agrar Institut</title>
<style type="text/css">
.master_topBar {{ background: url("http://sano.agrarinstitut.pl/themes/MasterImages/topBar.png") repeat-x scroll center 0 transparent;float: left;width: 100%;clear: both;height: 11px;}}
.content {{ margin: 0 auto; display: block; padding-bottom: 20px;}}
.space {{ height: 10px}}
.wrapper {{width: 450px; margin-left: auto; margin-right: auto; position: relative; min-height: 100%}}
.footer {{position:fixed; bottom:0px;height:20px;width:100%;left:auto;background:#fff; font-size: 80%}}
h1 {{text-align: center}}
img {{float: right; }}
body {{background-color: #fff;color: #333333;font-family: Tahoma,Sans-Serif;font-size: 13px;line-height: 18px;margin: 0;overflow-y: scroll;padding: 0; height: 100%}}
p {{margin: 0px auto;}}
p#contact {{margin-left: auto; margin-right: auto; position: relative;}}
a:link {{color: #666;}}
a:visited {{color: #666;}}
table.reporttable {{ background: url("http://sano.agrarinstitut.pl/themes/MasterImages/mainBg.jpg") repeat scroll center 0 transparent; border: 2px solid black; border-radius: 10px;margin: auto; text-align: center; border-collapse: collapse;}}
table.reporttable tr.odd {{ }}
table.reporttable tr.even {{ }}
table.reporttable th {{ color: black; border: 2px solid black; }}
table.reporttable td {{ color: black; border: 1px solid black; font-family: monospace; text-align: right;}}
table.reporttable td.cell_bold {{ font-weight: bold; border: 2px solid black;}}
table.reporttable td.cell_money {{ text-align: right; font-family: monospace; }}
</style>
</head>
<body>
<div class="master_topBar"></div>
<div class="space"></div>
<div class="wrapper">
<div class="content">
<img src="logo.png" alt="Logo Sano Agrar Institut" />
<h1>Täglicher Gülle Stand</h1>
<p><strong>Monat: {0}</strong>
<br>Messzeit täglich immer 8:00 Uhr</p>
</div>
""".format(month_name[current_month])

htmlfooter = """\
<div class="footer">
<p id="contact">Developed by <a href="mailto:simone@neosb.net?subject=Sano">Szymon Błaszczyński</a> for <a href="http://www.sano.pl">Sano</a></p>
</div>
</div>
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

tableclass = HTMLTable
extension = 'html'
backup('report-{0}-{1}.{2}'.format(current_year, current_month, extension))
outfile = open('report-{0}-{1}.{2}'.format(current_year, current_month, extension), 'wb')
if tableclass is HTMLTable:
    outfile.write(htmlheader)
outfile.write(tableclass(headers=[mainrs, subrow1, subrow2]).render(rows))
if tableclass is HTMLTable:
    outfile.write(htmlfooter)
outfile.close()
