#!/usr/bin/python2.7

import scraperwiki
import urllib2
import xlrd
import zipfile
from cStringIO import StringIO

url = "http://www.posta.sk/subory/322/psc-obci-a-ulic.zip"

archive_file = StringIO(urllib2.urlopen(url).read())
archive = zipfile.ZipFile(archive_file)

# Post codes for cities
wb = xlrd.open_workbook(file_contents=archive.read('OBCE.XLS'))
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
wb = xlrd.open_workbook(file_contents=archive.read('ULICE.XLS'))
sheet = wb.sheets()[0]
for row in range(1, sheet.nrows):
    data = {
        'ulica': sheet.cell(row, 1).value,
        'psc': sheet.cell(row, 2).value,
        'obec': sheet.cell(row, 6).value,
    }
    scraperwiki.sqlite.save(unique_keys=['ulica'], data=data, table_name="streets")

# Take up additional 4KB so we get to a total of 666KB
open('satan.dat', 'wb').write('6' * 4 * 1024)
