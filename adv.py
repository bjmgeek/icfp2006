#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

global tree;

def list_items():
    items=[]
    for i in tree.iter('item'):
        for j in i.getchildren():
            t=j.text.strip()
            j.text=t
            if j.tag == 'name':
                items.append(t)
    return items 

def build_items_database():
    for i in tree.iter('item'):
        i_dict={}
        i_dict['deps']=[]
        for field in ['name','description']:
            i_dict[field] = i.find(field).text.strip()
            try:
                i_dict['adjectives']=i.find('adjectives/adjective').text.strip()
            except:
                i_dict['adjectives']=''
        if i.find('condition/pristine') is not None:
            i_dict['condition']='pristine'
        else:
            i_dict['condition']='broken'
            for x in i.findall('condition/broken/missing/kind'):
                if x.find('condition/pristine') is not None:
                    i_dict['deps'].append(x.find('name').text.strip())
                else:
                    missing={}
                    missing['name']=x.find('name').text.strip()
                    missing['deps']=[z.find('name').text.strip() for z in x.findall('condition/broken/missing/kind')]
                    i_dict['deps'].append(missing)
        items[i_dict['name']]=i_dict


def find_deps(x):
    if x in deps: return deps[x]
    d=[]
    for missing in name_to_element(x).findall('condition/broken/missing/kind'):
        if missing.find('condition/pristine') is not None:
            d.append(missing.find('name').text.strip())
        else:
            print('fixme: find_deps(',x,')')
    return d

def find_all_deps(x):
    d=find_deps(x)
    if len(d)==0:
        return []
    else:
        result=d
        for i in d:
            result+=find_all_deps(i)
        return result



def broken(thing):
    # This is sort of kludgey, but it works.  The problem is that iter() 
    # searches differently than find().
    result=[x.find('condition').find('broken') for x in tree.iter('item') if x.find('name').text.strip()==thing]
    return result!=[None]

def items_above(thing):
    l=list_items()
    return l[:l.index(thing)]

def name_to_element(t):
    return  [x for x in tree.iter('item') if
             x.find('name').text.strip()==t][0]

def build(thing):
    print('attempting build of ' + thing,file=sys.stderr)
    if not broken(thing):
        for x in items_above(thing):
            print ('get ',x)
            if x not in find_all_deps(thing) and x not in deps['uploader'] and x not in deps['downloader']:
                print ('incinerate ',x)
    else:
        for x in find_deps(thing):
            if not broken(x): #thing depends on a complete object
                build(x)
                print('get ' + x)
            else:
                build_partial(x)
            print('combine ' + thing + ' ' + x)

def build_partial(thing):
    missing=find_deps(thing)
    print('attempting build of ' + thing + ' missing ', missing,file=sys.stderr)
    print('fixme (build_partial)')


def pre_interact():
    # this will put us to the corner of 54th St and Ridgewood Ct.
    #print('starting pre_interact...',file=sys.stderr)
    for line in file('junkroom.steps'):
        print(line.strip())
    print('sw xml')
    print ('l')
    sys.stdout.flush()
    #print('done with pre_interact...',file=sys.stderr)

items={}
deps={}
deps['uploader']=['MOSFET','status LED','RS232 adapter','EPROM burner','battery']
deps['downloader']=['USB cable','display','jumper shunt','progress bar','power cord']
tree=ElementTree(XML('<items />'))

if len(sys.argv) == 1:
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
    build_items_database()
    interactive=False

for i in list_items():
    if i in deps['uploader'] or i in deps['downloader'] or i=='keypad':
        build(i)
