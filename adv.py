#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree
import sys

print('l')

tree=ElementTree(file=sys.stdin)
for i in tree.iter('item'):
    for j in i.getchildren():
        t=j.text.strip()
        print (j.tag,":",t,file=sys.stderr)
        if j.tag == 'name':
            print ('get ' + t)
