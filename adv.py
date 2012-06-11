#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

def list_items(tree):
    items=[]
    for i in tree.iter('item'):
        for j in i.getchildren():
            t=j.text.strip()
            print (j.tag,":",t,file=stderr)
            if j.tag == 'name':
                items.append(t)
    return items 

def get_deps(x):
    if x in deps: return deps[x]
    else: return []

def build(thing):
    print('attempting build of ' + thing,file=sys.stderr)
    if complete(thing):
        for x in items_above(thing):
            incinerate(x)
    else:
        for x in get_deps(thing):
            if complete(x): #thing depends on a complete object
                build(x)
            else:
                build_partial(x)

def build_partial(thing,missing):
    print('attempting build of ' + thing + ' missing ', missing,file=sys.stderr)


# put the goggles in xml mode
print ('sw xml')

deps={}
deps['uploader']=['MOSFET','status LED','RS232 adapter','EPROM burner','battery']
deps['downloader']=['USB cable','display','jumper shunt','progress bar','power cord']

in_xml=False
for line in file('junkroom.xml'):
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
        items=list_items(tree)
        for i in items:
            deps[i]=get_deps(i)
            if i in deps['uploader'] or i in deps['downloader']:
                build(i)
