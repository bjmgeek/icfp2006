'''
Random solver for black knots

reads spec on standard input and outputs black knot code, using a random
algorithm'''


from __future__ import print_function

import sys,signal,pdb,os
from random import *
import knot_util,solve_knot
from knot_util import *
from solve_knot import *

def handle_pdb(sig,frame):
    pdb.Pdb().set_trace(frame)

def improved(old,new,goal):
    '''Given two grids, old and new, and a goal, determine if the new is
    strictly better, based on number of correct output pipes, or on distance to
    correct pipes.  If the new grid has too many plinks, it is rejected, since
    it's not always possible to remove plinks.'''
    pipe_improvement=0
    pipe_regression=0
    old=get_results(old)
    new=get_results(new)
    for n in xrange(len(goal)):
        if new[n][1] > goal[n][1]:
            #too many plinks
            return False
        if abs(new[n][0] - goal[n][0]) < abs(old[n][0] - goal[n][0]):
            #we are closer to the correct output
            pipe_improvement += 1
        elif abs(new[n][0] - goal[n][0]) > abs(old[n][0] - goal[n][0]):
            #we are furthur from the correct output
            pipe_regression += 1
    return pipe_improvement - pipe_regression >= 0

def improved_plinks(old,new,goal):
    '''Given two grids, old and new, and a goal, determine if the new is
    strictly better, based on number of correct plinks, or on distance to
    correct plinks.  If the new grid has too many plinks, it is rejected, since
    it's not always possible to remove plinks. If the new grid output pipes
    don't match, it is rejected.'''
    plink_improvement=0
    plink_regression=0
    old=get_results(old)
    new=get_results(new)
    for n in xrange(len(goal)):
        if new[n][1] > goal[n][1]:
            #too many plinks
            return False
        if [x[0] for x in new] != [x[0] for x in goal]:
            #incorrect outputs
            return False
        if abs(new[n][1] - goal[n][1]) < abs(old[n][1] - goal[n][1]):
            #we are closer to the correct output
            plink_improvement += 1
        elif abs(new[n][1] - goal[n][1]) > abs(old[n][1] - goal[n][1]):
            #we are furthur from the correct output
            plink_regression += 1
    return plink_improvement - plink_regression > 0

def random_line(w):
    '''returns a random black knot line of width w'''
    line=''
    n=randrange(w-1)
    line += '|' * n
    line += '><'
    line += '|' * (w-n-2)
    return line

def add_some_plinks(grid):
    old=list(grid)
    new=list(grid)
    unimproved=0
    improved=False
    while unimproved < 16*len(grid)*width:
        for n in xrange(randint(0,width)):
            new.insert(randint(0,len(new)),random_line(width))
        if improved_plinks(old,new,goal):
            old=list(new)
            improved=True
        else:
            unimproved+=1
            new=list(old)
    if(improved):
        print ('added some plinks',file=sys.stderr)
        return new
    else:
        print ('tried',unimproved,'times without adding any plinks',file=sys.stderr)
        return grid


def go():
    '''attempts to bring grid closer to having correct outputs'''
    global grid
    added=False
    for x in xrange (width*width):
        new_grid=list(grid)
        if random() < 0.008 and len(grid) > 1:
            del new_grid[randrange(len(new_grid))]
        else:
            new_grid.insert(randint(0,len(new_grid)),random_line(width))
        if improved(grid,new_grid,goal):
            grid=list(new_grid)
            added=True
            print('.',end='',sep='',file=sys.stderr)
        if get_results(grid) == goal:
            #solved it!
            print('Grid is',len(grid),'lines long.',file=sys.stderr)
            output_grid(grid)
            solved=True
            break
    if added: print(file=sys.stderr)

def go2():
    global grid
    try:
        grid=add_targeted_plink(grid)
    except SolveGridException:
        print('caught SolveGridException',file=sys.stderr)
    finally:
        summarize(grid,goal)

def add_targeted_plink(grid,target=None):
    '''adds a valid pair of plinks to the grid.  Returns the new grid or the
    existing grid if the new one is known to not be solvable

    if target is specified, it needs to be a tuple of two input columns.  If the
    columns ever touch, plinks are added at that spot.'''
    if not solvable(grid,goal):
        raise SolveGridException('trying to add targeted plink to an unsolvable grid')
    targets=[x for x in xrange(len(goal))if goal[x][1] - get_results(grid)[x][1] !=0]
    if target==None:
        target1=choice(targets)
        while True:
            target2=find_touching(grid,target1).pop()
            if target2 in targets:
                break
    else:
        target1,target2=target
    try:
        r,c=find_touching_detail(grid,target1,target2).pop()
    except KeyError:
        print('target columns',target1,'and',target2,'never meet.',file=sys.stderr)
        raise SolveGridException('target columns never meet')
    g=insert_plinks(grid,r,c,c+2,1)
    if solvable(g,goal):
        return list(g)
    else:
        raise SolveGridException('grid not solvable')

def remove_random_plink_pair(grid):
    found=False
    g=list(grid)
    while not found:
        y=randrange(len(g) -1)
        x=randrange(width)
        if g[y][x]=='<' and g[y+1][x]=='<':
            found=True
            l1=list(g[y])
            l2=list(g[y+1])
            l1[x]=l1[x-1]=l2[x]=l2[x-1]='|'
        elif g[y][x]=='>' and g[y+1][x]=='>':
            found=True
            l1=list(g[y])
            l2=list(g[y+1])
            l1[x]=l1[x+1]=l2[x]=l2[x+1]='|'
    g[y]=''.join(l1)
    g[y+1]=''.join(l2)
    return g



if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, handle_pdb)

    goal=[]
    with open(sys.argv[1],'r') as f:
        for line in f:
            line=line.split()
            goal.append(eval(line[2]))
    width=len(goal)
    solve_knot.width=knot_util.width=width
    solve_knot.add_targeted_plink=add_targeted_plink

    solved=False
    while not solved:
        print ('starting new grid',file=sys.stderr)
        grid=['|'*width]
        while [x[0] for x in get_results(grid)] != [x[0] for x in goal]:
            old=list(grid)
            go()
            go()
            grid=remove_plinks(grid)
            go()
            if grid==old:
                print('unable to get correct outputs',file=sys.stderr)
                break
        else:
            print('correct outputs found, trying to add plinks',file=sys.stderr)
        old=None
        while grid!=old:
            old=list(grid)
            grid=remove_plinks(grid)
            otherold=False
            grid=linear_solve(grid,goal)
            if get_results(grid)==goal:
                print('solved it!',file=sys.stderr)
                solved=True
                break
            while grid!=otherold:
                otherold=list(grid)
                grid=add_some_plinks(grid)
                if not solvable(grid,goal):
                    print('oops, now the grid is not solvable',file=sys.stderr)
                    break
            if get_results(grid)==goal:
                print('solved it!',file=sys.stderr)
                solved=True
                break
            for i in xrange(10):
                grid=remove_targeted_plink_pair(grid)
            for n in xrange(10*width):
                go2()
            if get_results(grid)==goal:
                print('solved it!',file=sys.stderr)
                solved=True
                break

    print('Grid is',len(compress(grid)),'lines long.',file=sys.stderr)
    output_grid(compress(grid))
