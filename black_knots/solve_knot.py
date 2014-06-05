#! /usr/bin/env python

from __future__ import print_function

import sys,os,signal
import array
from collections import namedtuple

from knot_util import *

def swap(x,y):
    '''
    swap(x,y)
    returns black knot code to swap two input columns.

    Generates plinks according to the following formula (assuming x < y):
        y-x = 1: 1 plink to input x; 0 plinks to input y
        y-x > 1: y-x plinks to input x; 1 plink to intervening inputs; 0 plinks to
                 input y

    If x > y, the parameters are swapped first.
    '''
    result=[]
    (x,y)=sorted((x,y))
    path=[]
    for z in xrange(x,y):
         path.append ('|' * (z) + '><' + '|' * (width-z-2))
    if abs(x-y) > 1: 
        path.extend(reversed(path[:-1]))
    for row in path: 
        result.append(row)
    return result

def add_plinks(start,stop,plinks):
    '''
    add_plinks(start,stop,plinks)
    returns black knot code to add plinks to the specified range of columns

    start is the first input column to start adding plinks to, and stop is the
    first input column to not add plinks.  The range must be contiguous, and
    greater than one column.

    If the number of columns to add plinks to is even, plinks can be any number,
    but if it's odd, plinks must be an even number.
    '''
    output=[]
    (start,stop)=sorted((start,stop))
    #sanity checks:
    if (stop - start) <= 1:
        raise ValueError ("not enough columns to add plinks to")
    if (stop - start) % 2 != 0 and  plinks % 2 != 0:
        raise ValueError ("Either number of columns or plinks (or both) must be even")

    if (stop-start) % 2 == 0: #even number of columns
        for n in xrange(plinks):
            output.append( '|' * start + '><' * ((stop-start)/2) + '|' * (width-stop) )
            output.append( '|' * start + '><' * ((stop-start)/2) + '|' * (width-stop) )
    else:
        for n in xrange(plinks/2):
            output.append( '|' * start + '><|' + '|' * (width - 3 - start) )
            output.append( '|' * start + '|><' + '|' * (width - 3 - start) )
            output.append( '|' * start + '><|' + '|' * (width - 3 - start) )
            output.append( '|' * start + '|><' + '|' * (width - 3 - start) )
            output.append( '|' * start + '><|' + '|' * (width - 3 - start) )
            output.append( '|' * start + '|><' + '|' * (width - 3 - start) )
        if (stop-start) > 3:
            output.extend(add_plinks(start+3,stop,plinks))
    return output


def remove_plinks(grid):
    '''given a grid, returns an equivalent grid with all removable plinks
    removed.  Removable plinks are plinks that can be removed without changing
    the output pipes.'''
    g=compress(grid)
    found=0
    #remove simple plinks
    #eg ><|
    #   ><|
    for y in xrange(len(g)-1):
        l1=list(g[y])
        l2=list(g[y+1])
        for x in xrange(width-1):
            if g[y][x] == '>' and g[y+1][x] == '>':
                found+=2
                l1[x] = l1[x+1] = l2[x] = l2[x+1] = '|'
        g[y]=''.join(l1)
        g[y+1]=''.join(l2)
    #remove complex plinks such as added by add_plinks() with an odd number of
    #columns
    if len(g) >= 6:
        for y in xrange(len(g)-5):
            l1=list(g[y])
            l2=list(g[y+1])
            l3=list(g[y+2])
            l4=list(g[y+3])
            l5=list(g[y+4])
            l6=list(g[y+5])
            for x in xrange(width-2):
                a=all((l1[x]=='>',l1[x+1]=='<',l1[x+2]=='|',
                       l2[x]=='|',l2[x+1]=='>',l2[x+2]=='<',
                       l3[x]=='>',l3[x+1]=='<',l3[x+2]=='|',
                       l4[x]=='|',l4[x+1]=='>',l4[x+2]=='<',
                       l5[x]=='>',l5[x+1]=='<',l5[x+2]=='|',
                       l6[x]=='|',l6[x+1]=='>',l6[x+2]=='<'))
                b=all((l1[x]=='|',l1[x+1]=='>',l1[x+2]=='<',
                       l2[x]=='>',l2[x+1]=='<',l2[x+2]=='|',
                       l3[x]=='|',l3[x+1]=='>',l3[x+2]=='<',
                       l4[x]=='>',l4[x+1]=='<',l4[x+2]=='|',
                       l5[x]=='|',l5[x+1]=='>',l5[x+2]=='<',
                       l6[x]=='>',l6[x+1]=='<',l6[x+2]=='|'))
                if a or b:
                    l1[x] = l1[x+1] = l1[x+2] = '|'
                    l2[x] = l2[x+1] = l2[x+2] = '|'
                    l3[x] = l3[x+1] = l3[x+2] = '|'
                    l4[x] = l4[x+1] = l4[x+2] = '|'
                    l5[x] = l5[x+1] = l5[x+2] = '|'
                    l6[x] = l6[x+1] = l6[x+2] = '|'
                    print ('found complex plink at row:',y,'column:',x,file=sys.stderr)
                    found+=6
            g[y]=''.join(l1)
            g[y+1]=''.join(l2)
            g[y+2]=''.join(l3)
            g[y+3]=''.join(l4)
            g[y+4]=''.join(l5)
            g[y+5]=''.join(l6)
    print ('removed',found,'plinks',file=sys.stderr)
    return g

def move_left(x,y):
    '''return black knot code to move left from y to x'''
    result=[]
    x,y=tuple(sorted((x,Y)))
    for z in xrange(y,x,-1):
         result.append('|' * (z-1) + '><' + '|' * (width-z-1))
    return result

def solvable(grid,goal):
    '''checks if a grid is solvable.

    This checks for solvability by seeing if there are any inputs needing plinks
    that are never adjacent to other plinks.  If this returns True, it does not
    mean that a solution necessarily exists, but if it returns False, one
    certainly does not.'''
    targets={x for x in xrange(len(goal)) if goal[x][1] - get_results(grid)[x][1] !=0}
    for t in targets:
        if find_adjacencies(grid,t).isdisjoint(targets):
            #none of the adjacencies of t are in targets
            return False
    return True

# main
if __name__=='__main__':
    if len(sys.argv) == 1:
        print ('usage:',sys.argv[0], '<spec file>',file=sys.stderr)
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
