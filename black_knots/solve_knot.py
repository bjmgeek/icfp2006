#! /usr/bin/env python

import sys
import array
from collections import namedtuple

from knot_util import *

def swap(x,y):
    '''
    swap(x,y)
    prints black knot code to swap two input columns.

    Generates plinks according to the following formula (assuming x < y):
        y-x = 1: 1 plink to input x; 0 plinks to input y
        y-x > 1: y-x plinks to input x; 1 plink to intervening inputs; 0 plinks to
                 input y

    If x > y, the parameters are swapped first.
    '''
    (x,y)=sorted((x,y))
    path=[]
    for z in xrange(x,y):
         path.append ('|' * (z) + '><' + '|' * (width-z-2))
    if abs(x-y) > 1: 
        path.extend(reversed(path[:-1]))
    for row in path: 
        print row 

def add_plinks(start,stop,plinks):
    '''
    add_plinks(start,stop,plinks)
    prints black knot code to add plinks to the specified range of columns

    start is the first input column to start adding plinks to, and stop is the
    first input column to not add plinks.  The range must be contiguous, and
    greater than one column.

    If the number of columns to add plinks to is even, plinks can be any number,
    but if it's odd, plinks must be an even number.
    '''
    (start,stop)=sorted((start,stop))
    #sanity checks:
    if (stop - start) <= 1:
        print "not enough columns to add plinks to"
        raise ValueError
    if (stop - start) % 2 != 0 and  plinks % 2 != 0:
        print "Either number of columns or plinks (or both) must be even"
        raise ValueError

    if (stop-start) % 2 == 0: #even number of columns
        for n in xrange(plinks):
            print '|' * start + '><' * ((stop-start)/2) + '|' * (width-stop)
            print '|' * start + '><' * ((stop-start)/2) + '|' * (width-stop)
    else:
        for n in xrange(plinks/2):
            print '|' * start + '><|' + '|' * (width - 3 - start)
            print '|' * start + '|><' + '|' * (width - 3 - start)
            print '|' * start + '><|' + '|' * (width - 3 - start)
            print '|' * start + '|><' + '|' * (width - 3 - start)
            print '|' * start + '><|' + '|' * (width - 3 - start)
            print '|' * start + '|><' + '|' * (width - 3 - start)
        if (stop-start) > 3:
            add_plinks(start+3,stop,plinks)

def find_adjacencies(steps):
    '''
    find_adjacencies(steps)
    given a list of black knot code strings, return dict
    to list when any two input columns are next to each other.

    the 
    '''
    a={}
    i=range(width)
    step=0
    for line in steps:
        n=0
        while n < width:
            if line[n]=='|':
                n+=1
            else:
                i[n],i[n+1]=i[n+1],i[n]
                n+=2
        for n in xrange(width-1):
            try:
                a[frozenset((i[n],i[n+1]))].append(step)
            except KeyError:
                a[frozenset((i[n],i[n+1]))]=[step]
        step+=1
    return a

# generate code to move left from y to x
def move_left(x,y):
    x,y=tuple(sorted((x,y)))
    for z in xrange(y,x,-1):
         print '|' * (z-1) + '><' + '|' * (width-z-1)



# main
if __name__=='__main__':
    if len(sys.argv) == 1:
        print 'usage:',sys.argv[0], '<spec file>'
        exit()

    rules={}
    inputs={} #gets turned into a list later
    Column=namedtuple('Column','source current goal distance plinks_current plinks_goal')

    for line in open(sys.argv[1]):
        l=line.split()
        rules[int(l[0])]=eval(l[2]) #eval because it's already a tuple


    width=len(rules)

    #add distance
    for x in rules:
        inputs[x]=Column(source=x,current=x,goal=rules[x][0],plinks_current=0,
                        plinks_goal=rules[x][1],distance=abs(x-rules[x][0]))

    inputs=sorted(inputs.values(),key=lambda x: x.distance)
