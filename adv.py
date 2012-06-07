#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

def get_items(tree):
    items=[]
    for i in tree.iter('item'):
        for j in i.getchildren():
            t=j.text.strip()
            print (j.tag,":",t,file=stderr)
            if j.tag == 'name':
                items.append(t)
    return items 



# put the goggles in xml mode
print ('sw xml')

for line in file('multi.xml'):
    l=line.strip()
    print("read line: "+l,file=stderr)
    if l=='<error>' or l=='<success>':
        in_xml=True
        buf='' #start a new buffer
    if in_xml:
        buf+=line
    if l=='</error>' or l=='</success>':
        in_xml=False
        tree=ElementTree(XML(buf))
        items=get_items(tree)


