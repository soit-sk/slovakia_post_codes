#!/usr/bin/python2.7

import scraperwiki
#import csv
import urllib2
import xlrd
import zipfile
from cStringIO import StringIO

url = "http://www.posta.sk/subory/322/psc-obci-a-ulic.zip"

archive_file = StringIO(urllib2.urlopen(url).read())
archive = zipfile.ZipFile(archive_file)

wb = xlrd.open_workbook(file_contents=archive.read('OBCE.XLS'))
sheet = wb.sheets()[0]
with open('psc.csv', 'wb') as f:
    #writer = csv.writer(f)
    for row in range(1, sheet.nrows):
        #writer.writerow([sheet.cell(row, i).value.encode('utf8') for i in cell_idxs])
        data = {
            'obec': sheet.cell(row, 1).value,
            'okres': sheet.cell(row, 2).value,
            'psc': sheet.cell(row, 3).value,
            'kraj': sheet.cell(row, 7).value,
        }
        scraperwiki.sqlite.save(unique_keys=['obec'], data=data)
