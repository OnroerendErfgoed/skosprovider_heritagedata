#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the HeritagedataProvider to expand a concept
'''

from skosprovider_heritagedata.providers import HeritagedataProvider

periodprovider = HeritagedataProvider(
    {'id': 'Heritagedata'},
    scheme_uri='http://purl.org/heritagedata/schemes/eh_period'
)

results = periodprovider.expand('PM')

print('Results')
print('------')
for result in results:
    print(result)
