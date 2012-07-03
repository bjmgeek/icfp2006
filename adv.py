#!/usr/bin/env python 
from __future__ import print_function
from xml.etree.ElementTree import ElementTree,XML
import sys
from collections import OrderedDict

debug=True
if debug: 
    stderr=sys.stderr
else: 
    stderr=file('/dev/null')

global tree
global items

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
        i_dict['missing']=[]
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
    missing=[]
    for x in element.findall('condition/broken/missing/kind'):
        if x.find('condition/pristine') is not None:
            missing.append(x.find('name').text.strip())
        else:
            missing.append((element_to_name(x),get_missing(x)))
    print (element_to_name(element)," missing: ",missing,file=stderr)
    return missing

def list_items():
    return [x for x in items]

def find_deps(x):
    print ('deps for:',x,file=stderr,end=' ')
    print (items[x]['missing'],file=stderr)
    return items[x]['missing']

def find_all_deps(x):
    print('find_all_deps: ',x,file=stderr)
    d=find_deps(x)
    if len(d)==0:
        return []
    if type(x)==tuple:
        print (tuple)
        return [x[0]]
    else:
        result=d
        for i in d:
            result+=find_all_deps(i)
        return result



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


def pre_interact():
    # this will put us to the corner of 54th St and Ridgewood Ct.
    #print('starting pre_interact...',file=sys.stderr)
    for line in file('junkroom.steps'):
        print(line.strip())
    # put commands to navigate to target room here 
    # 
    # I would love to be able to have this program interacting
    # with umix, but still have stdin from the user's terminal
    # also going to umix, but I haven't figured out how to do
    # that.  In the mean time, we can work a room at a time
    # but then you might as well just use the preexisting xml.
    
    #print('e')

    # end of navigation commands.  Switch the goggles to XML mode
    print('sw xml')
    sys.stdout.flush()
    #sys.stdin.flush()
    #print('done with pre_interact...',file=sys.stderr)

items=OrderedDict()
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
        if l in ['<error>','<success>']:
            in_xml=True
            buf='' #start a new buffer
        if in_xml:
            buf+=line
        if in_xml and l in ['</error>','</success>']:
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
