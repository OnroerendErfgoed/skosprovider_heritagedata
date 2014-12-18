#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the HeritagedataProvider to get the concept of
'POST MEDIEVAL'.
'''

from skosprovider_heritagedata.providers import HeritagedataProvider

periodprovider = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period')

pm = periodprovider.get_by_id('PM')

print('Labels')
print('------')
for l in pm.labels:
   print(l.language + ': ' + l.label + ' [' + l.type + ']')

print('Notes')
print('-----')
for n in pm.notes:
    print(n.language + ': ' + n.note + ' [' + n.type + ']')
