#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

def list_items():
    items=[]
    for i in tree.iter('item'):
        for j in i.getchildren():
            t=j.text.strip()
            print (j.tag,":",t,file=stderr)
            if j.tag == 'name':
                items.append(t)
    return items 

def find_deps(x):
    if x in deps: return deps[x]
    d=[]
    return d

def broken(thing):
    # This is sort of kludgey, but it works.  The problem is that iter() 
    # searches differently than find().
    result=[x.find('condition').find('broken') for x in tree.iter('item') if x.find('name').text.strip()==thing]
    return result!=[None]


def build(thing):
    print('attempting build of ' + thing,file=sys.stderr)
    if not broken(thing):
        for x in items_above(thing):
            incinerate(x)
    else:
        for x in find_deps(thing):
            if complete(x): #thing depends on a complete object
                build(x)
            else:
                build_partial(x)

def build_partial(thing):
    missing=find_deps(thing)
    print('attempting build of ' + thing + ' missing ', missing,file=sys.stderr)


deps={}
deps['uploader']=['MOSFET','status LED','RS232 adapter','EPROM burner','battery']
deps['downloader']=['USB cable','display','jumper shunt','progress bar','power cord']

tree=ElementTree(file=sys.argv[1])
items=list_items()
for i in items:
    if i in deps['uploader'] or i in deps['downloader']:
        build(i)
