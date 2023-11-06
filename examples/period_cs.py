#!/usr/bin/python
'''
This script demonstrates using the HeritagedataProvider with the
eh_period conceptscheme already loaded.
'''

from skosprovider_heritagedata.providers import HeritagedataProvider
from skosprovider_heritagedata.utils import CONCEPTSCHEMES

cs_uri = 'http://purl.org/heritagedata/schemes/eh_period'

periodprovider = HeritagedataProvider(
    {'id': 'Heritagedata'},
    scheme_uri=cs_uri,
    concept_scheme = CONCEPTSCHEMES[cs_uri]
)

cs = periodprovider.concept_scheme

print('Labels')
print('------')
for l in cs.labels:
   print(l.language + ': ' + l.label + ' [' + l.type + ']')
print()

print('Notes')
print('-----')
for n in cs.notes:
    print(n.language + ': ' + n.note + ' [' + n.type + ']')
print()

print('Sources')
print('-------')
for s in cs.sources:
    print(s.citation)
print()
