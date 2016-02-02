#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys
from collections import OrderedDict
import json
import sqlite3
import os

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

global tree
global items
global umix_process


def get_unique_name(element):
    name=element_to_name(element)
    print('name:',name,file=stderr)
    adjectives=element.find('adjectives/adjective')
    print ('adjectives:',adjectives,file=stderr)
    if adjectives is None:
        return name
    else:
        adjectives=adjectives.text.strip()
        return adjectives+' '+name

def build_items_database():
    for i in tree.iter('item'):
        i_dict={}
        i_dict['Element']=i
        for field in ['name','description']:
            i_dict[field]=i.find(field).text.strip()
        unique_name=get_unique_name(i)
        if i.find('condition/pristine') is not None:
            i_dict['condition']='pristine'
        else:
            i_dict['condition']='broken'
            i_dict['missing']=get_missing(i)
        if i.find('piled_on/item') is not None:
            i_dict['piled_on']=get_unique_name(i.find('piled_on/item'))
        else:
            i_dict['piled_on']=''

        items[unique_name]=i_dict

def get_missing(element):
    missing=set()
    for x in element.findall('condition/broken/missing/kind'):
        if x.find('condition/pristine') is not None:
            missing.add(x.find('name').text.strip())
        else:
            missing.add((element_to_name(x),frozenset(get_missing(x))))
    print (element_to_name(element)," missing: ",missing,file=stderr)
    return missing

def list_items():
    return [x for x in items]

def find_deps(x,missing=None):
    print ('deps for ',x,': ',sep='',file=stderr,end=' ')
    if missing:
        #FIXME
        print ('missing:',missing,file=stderr)
        return set()
    else:
        if 'missing' in items[x]:
            print (items[x]['missing'],file=stderr)
            return items[x]['missing']
        else:
            print(None)
            return set()

def find_all_deps(x):
    print('find_all_deps: ',x,file=stderr)
    if type(x)==tuple:
        print (x,'is a tuple',file=stderr)
        d=find_deps(*x)
    else:
        d=find_deps(x)
    if len(d)==0:
        return set()
    if type(x)==tuple:
        print (tuple)
        return [x[0]]
    else:
        result=set(d)
        for i in d:
            result|=find_all_deps(i)
        return result

def build(thing):
    print('attempting build of ' + thing,file=sys.stderr)
    if not broken(thing):
        for x in items_above(thing):
            print ('get ',x)
            if x not in find_all_deps(thing) and x not in deps['uploader'] and x not in deps['downloader']:
                print ('incinerate ',x)
    else:
        print('fixme: build()',file=stderr)

def broken(thing):
    return items[thing]['condition']=='broken'

def items_above(thing):
    l=list_items()
    return l[:l.index(thing)]

def name_to_element(t):
    return  [x for x in tree.iter('item') if
             x.find('name').text.strip()==t][0]

def element_to_name(e):
    return e.find('name').text.strip()


def pre_interact(proc):
    # this will put us to the corner of 54th St and Ridgewood Ct.
    for line in file('junkroom.steps'):
        proc.stdin.write(line)

    # end of navigation commands.  Switch the goggles to XML mode
    proc.stdin.write('sw xml\n')
    return proc.stdout.readlines()


def getxml(command):
    in_xml=False 
    for line in umix_process.communicate(command):
        l=line.strip()
        if l in ['<error>','<success>']:
            in_xml=True
            buf='' #start a new buffer
        if in_xml:
            buf+=line
        if in_xml and l in ['</error>','</success>']:
            in_xml=False
            tree=ElementTree(XML(buf))

items=OrderedDict()
deps={}
deps['uploader']=['MOSFET','status LED','RS232 adapter','EPROM burner','battery']
deps['downloader']=['USB cable','display','jumper shunt','progress bar','power cord']
tree=ElementTree(XML('<items />'))

if len(sys.argv) == 1:
    interactive=True;

    print ('spawning umix process...',file=stderr)
    umix_process=subprocess.Popen('../umix',bufsize=1,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    print(pre_interact(umix_process))

else:
    tree=ElementTree(file=sys.argv[1])
    build_items_database()
    interactive=False
    if len(sys.argv) > 2:
        build(sys.argv[2])
    else:
        for i in list_items():
            if i in deps['uploader'] or i in deps['downloader']:
                build(i)
