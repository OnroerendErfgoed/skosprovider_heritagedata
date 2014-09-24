#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the HeritagedataProvider to expand a concept
'''

from skosprovider_heritagedata.providers import HeritagedataProvider

results = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').expand('PM')

print('Results')
print('------')
for result in results:
    print(result)