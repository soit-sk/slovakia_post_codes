#!/usr/bin/python

import scraperwiki
import urllib2
import xlrd
import zipfile
import re
from cStringIO import StringIO

url = "http://www.posta.sk/subory/322/psc-obci-a-ulic.zip"

archive_file = StringIO(urllib2.urlopen(url).read())
archive = zipfile.ZipFile(archive_file)
archive_namelist = archive.namelist()
r1 = re.compile('^obce.', re.IGNORECASE)
r2 = re.compile('^ulice.', re.IGNORECASE)
obce_filename = filter(r1.match, archive_namelist)[0]
ulice_filename = filter(r2.match, archive_namelist)[0]

# Post codes for cities
wb = xlrd.open_workbook(file_contents=archive.read(obce_filename))
sheet = wb.sheets()[0]
for row in range(1, sheet.nrows):
    data = {
        'obec': sheet.cell(row, 1).value,
        'okres': sheet.cell(row, 2).value,
        'psc': sheet.cell(row, 3).value,
        'kraj': sheet.cell(row, 7).value,
    }
    scraperwiki.sqlite.save(unique_keys=['obec'], data=data, table_name="towns")

# Streets
wb = xlrd.open_workbook(file_contents=archive.read(ulice_filename))
sheet = wb.sheets()[0]
for row in range(1, sheet.nrows):
    data = {
        'ulica': sheet.cell(row, 1).value,
        'psc': sheet.cell(row, 2).value,
        'obec': sheet.cell(row, 6).value,
    }
    scraperwiki.sqlite.save(unique_keys=['ulica'], data=data, table_name="streets")
