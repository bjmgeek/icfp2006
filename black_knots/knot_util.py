'''some utility functions for black knots

command line arguments:
    compress     compress stdin to stdout
    results      print results from stdin to stdout'''

import sys

def _compress(grid):
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

def compress(grid):
    '''
    compress(grid)

    takes a list of strings of black knot code, and compresses them
    vertically by "sliding" >< combinators up when there are two |
    combinators above, then eliminating rows of only | combinators

    returns a list of strings of black knot code
    '''
    g=[]
    for x in xrange(len(grid)/100 + 1):
        g.append(_compress(grid[100*x:100*x+100]))
    return _compress(sum(g,[]))

def find_touching(grid,i):
    '''given a grid and an input column i, return a set of all input columns that
    are ever adjacent to it'''
    results=set()
    paths=[path_drop(grid,col) for col in xrange(width)]
    for x in xrange(width):
        for step in xrange(1+len(grid)):
            if abs(paths[x][step] - paths[i][step]) == 1:
                results.add(x)
    return results-{i}

def find_touching_detail(grid,i,j):
    '''Given a grid and two input columns, i and j, return a set of tuples of
    the form (x,y) where:
    x is the row in the grid where the inputs are adjacent, and
    y is the first column where the inputs are adjacent.'''
    path_i=path_drop(grid,i)
    path_j=path_drop(grid,j)
    results=set()
    for n in xrange(1+len(grid)):
        if abs(path_i[n] - path_j[n]) == 1:
            results.add((n,min((path_i[n],path_j[n]))))
    return results

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

def grid_to_file(grid,f):
    '''write a grid to a file named f'''
    f=open(f,'w')
    for line in grid:
        f.write(line)
        f.write('\n')
    f.close()

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
    path=[pipe]
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
