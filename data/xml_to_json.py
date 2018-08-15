# Examples from https://stackoverflow.com/questions/191536/converting-xml-to-json-using-python

import xmltodict, json

o = xmltodict.parse('<e> <a>text</a> <a>text</a> </e>')
json.dumps(o) # '{"e": {"a": ["text", "text"]}}'

''' 
Alternatively 

import json, xmljson
from lxml.etree import fromstring, tostring
xml = fromstring('<p id="1">text</p>')
json.dumps(xmljson.badgerfish.data(xml))
# '{"p": {"@id": 1, "$": "text"}}'
xmljson.parker.etree({'ul': {'li': [1, 2]}})
# Creates [<ul><li>1</li><li>2</li></ul>]
'''
