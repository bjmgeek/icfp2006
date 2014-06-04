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
        for n in xrange(randint(0,5)):
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


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, handle_pdb)

    goal=[]
    for line in sys.stdin:
        line=line.split()
        goal.append(eval(line[2]))
    width=len(goal)
    solve_knot.width=knot_util.width=width

    solved=False
    while not solved:
        #start with a grid consisting of only one line
        grid=['|'*width]

        for x in xrange (200*width):
            new_grid=list(grid)
            if random() < 0.01 and len(grid) > 1:
                del new_grid[randrange(len(new_grid))]
            else:
                new_grid.insert(randint(0,len(new_grid)),random_line(width))
            if improved(grid,new_grid,goal):
                print('.',end='',sep='',file=sys.stderr)
                grid=list(new_grid)
            if get_results(grid) == goal:
                #solved it!
                output_grid(grid)
                solved=True
                break
        else:
            print ('trying again...',file=sys.stderr)
