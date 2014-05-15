'''
Random solver for black knots

reads spec on standard input and outputs black knot code, using a random
algorithm'''


import sys
from random import *
from knot_util import *

def improved(old,new,goal):
    '''Given two grids, old and new, and a goal, determine if the new is
    strictly better, based on number of correct output pipes, and number of
    correct plinks.'''
    pipe_improvement=0
    plink_improvement=0
    pipe_regression=0
    plink_regression=0
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
        if abs(new[n][1] - goal[n][1]) < abs(old[n][1] - goal[n][1]):
            #we added useful plinks
            plink_improvement += 1
        elif abs(new[n][1] - goal[n][1]) > abs(old[n][1] - goal[n][1]):
            #we lost useful plinks
            plink_regression += 1
    return  plink_improvement-plink_regression >= 0 and pipe_improvement - pipe_regression >= 0

def random_line(w):
    '''returns a random black knot line of width w'''
    line=''
    while len(line) < w:
        if len(line) == w-1:
            line+='|'
            return line
        elif choice((True,False)):
            line+='><'
        else:
            line+='|'
    return line

goal=[]
for line in sys.stdin:
    line=line.split()
    goal.append(eval(line[2]))
width=len(goal)
#start with a grid consisting of only one line
grid=['|'*width]

for x in xrange (100000):
    new_grid=list(grid)
    new_grid.insert(randint(0,len(new_grid)),random_line(width))
    if improved(grid,new_grid,goal):
        grid=list(new_grid)
        print '.',
    if get_results(grid) == goal:
        #solved it!
        print ''
        break

output_grid(grid)
