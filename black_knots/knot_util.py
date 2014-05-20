'''some utility functions for black knots

command line arguments:
    compress     compress stdin to stdout
    results      print results from stdin to stdout'''

import sys

def compress(grid):
    '''
    compress(steps)

    takes a list of strings of black knot code, and compresses them
    vertically by "sliding" >< combinators up when there are two |
    combinators above, then eliminating rows of only | combinators

    returns a list of strings of black knot code
    '''
    working_grid=list(grid)
    if len(working_grid) == 0: return []
    old=list(working_grid)
    new=[]
    while old != new:
        for y in xrange (len(working_grid)-1):
            l0 = list(working_grid[y])
            l1 = list(working_grid[y+1])
            for x in xrange(len(l0)-1):
                if l0[x] == '|' and l0[x+1] == '|' and l1[x] == '>' and l1[x+1] == '<':
                    l0[x] = '>'
                    l0[x+1] = '<'
                    l1[x] = '|'
                    l1[x+1] = '|'
            working_grid[y]=''.join(l0)
            working_grid[y+1]=''.join(l1)
        old=list(new)
        new=list(working_grid)
    null_line = '|' * len(working_grid[0])
    if null_line in working_grid:
        for i in xrange(working_grid.count(null_line)):
            working_grid.remove(null_line)
    return working_grid

def find_adjacencies(grid):
    '''
    find_adjacencies(grid)

    Given a list of black knot code strings, return dict
    indexed by pair of adjacencies (as a frozenset).

    The output is a list of rows after which the inputs are adjacent.
    To find the columns at that point, path_drop() may be helpful.
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


def string_to_grid(s):
    '''read a grid from a string'''
    s=s.strip()
    s=s.split()
    return s

def file_to_grid(f):
    '''read a grid from file named f'''
    grid=[]
    f=open(f,'r')
    for line in f:
        grid.append(line.strip())
    f.close()
    return grid

def input_grid():
    '''read a grid from standard input'''
    grid=[]
    for line in sys.stdin:
        grid.append(line.strip())
    return grid

def output_grid(g):
    '''print out a grid in the format expected by the verifier'''
    for line in g:
        print line

def path_drop(grid,pipe):
    '''given a grid and a pipe, return the path taken'''
    path=[]
    for line in grid:
        if line[pipe] == '<':
            pipe -= 1
        elif line[pipe] == '>':
            pipe += 1
        path.append(pipe)
    return path

def drop(grid,pipe):
    '''given a grid and a pipe, return a tuple of pipe,plinks'''
    plinks=0
    for line in grid:
        if line[pipe] == '<':
            pipe -= 1
        elif line[pipe] == '>':
            plinks +=1
            pipe += 1
    return pipe,plinks

def print_results(grid):
    '''prints output similar to the "run_bb" program'''
    for n in xrange(len(grid[0])):
        print n,'->',drop(grid,n)

def get_results(grid):
    '''returns list of tuples of the results'''
    results=[]
    for n in xrange(len(grid[0])):
        results.append(drop(grid,n))
    return results

def equivalent(g1,g2):
    '''determine if two grids have the same results'''
    return get_results(g1) == get_results(g2)

if __name__=='__main__':
    if sys.argv[1]=='compress':
        output_grid(compress(input_grid()))
    elif sys.argv[1]=='results':
        print_results(input_grid())
