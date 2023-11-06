'''
A script to create a JSON file with all heritagedata.org conceptschemes
'''

import csv
import json
import requests

res = requests.get('http://www.heritagedata.org/live/services/getSchemes?alias')

schemes = res.json()

print(json.dumps(schemes, indent=4))
