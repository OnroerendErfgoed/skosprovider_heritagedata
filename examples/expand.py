#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the HeritagedataProvider to expand a concept
'''

from skosprovider_heritagedata.providers import HeritagedataProvider

results = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').expand('PM')

print('Results')
print('------')
for result in results:
    print(result)