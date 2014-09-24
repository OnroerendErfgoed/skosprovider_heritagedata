#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the HeritagedataProvider to find the concepts with 'iron' in their label
'''

from skosprovider_heritagedata.providers import HeritagedataProvider

results = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find({'label': 'iron', 'type': 'concept'})

print('Results')
print('------')
for result in results:
    print(result)

