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
            j.text=t
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

def items_above(thing):
    l=list_items()
    return l[:l.index(thing)]


def build(thing):
    print('attempting build of ' + thing,file=sys.stderr)
    if not broken(thing):
        for x in items_above(thing):
            print ('get ',x)
            print ('incinerate ',x)
    else:
        for x in find_deps(thing):
            if complete(x): #thing depends on a complete object
                build(x)
            else:
                build_partial(x)

def build_partial(thing):
    missing=find_deps(thing)
    print('attempting build of ' + thing + ' missing ', missing,file=sys.stderr)


def pre_interact():
    # this will put us to the corner of 54th St and Ridgewood Ct.
    #print('starting pre_interact...',file=sys.stderr)
    for line in file('junkroom.steps'):
        print(line,end='')
        #print (line,file=sys.stderr)
    print('sw xml')
    print ('l')
    #print('done with pre_interact...',file=sys.stderr)



deps={}
deps['uploader']=['MOSFET','status LED','RS232 adapter','EPROM burner','battery']
deps['downloader']=['USB cable','display','jumper shunt','progress bar','power cord']

if len(sys.argv) !=2:
    print('usage: ' + sys.argv[0] + ' filename',file=sys.stderr)
    exit()

if sys.argv[1]=='-':
    interactive=True;

    pre_interact()
    
    in_xml=False 
    for line in sys.stdin:
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
            for i in list_items():
                if i in deps['uploader'] or i in deps['downloader'] or i=='keypad':
                    build(i)


else:
    tree=ElementTree(file=sys.argv[1])
    interactive=False

for i in list_items():
    if i in deps['uploader'] or i in deps['downloader'] or i=='keypad':
        build(i)
