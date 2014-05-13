'''some utility functions for black knots

if called as a script, compress stdin to stdout'''
def compress(grid):
    '''given a grid, return an equivalent grid that takes up less lines'''
    if len(grid) == 0: return []
    old=list(grid)
    new=[]
    while old != new:
        for y in xrange (len(grid)-1):
            l0 = list(grid[y])
            l1 = list(grid[y+1])
            for x in xrange(len(l0)-1):
                if l0[x] == '|' and l0[x+1] == '|' and l1[x] == '>' and l1[x+1] == '<':
                    l0[x] = '>'
                    l0[x+1] = '<'
                    l1[x] = '|'
                    l1[x+1] = '|'
            grid[y]=''.join(l0)
            grid[y+1]=''.join(l1)
        old=list(new)
        new=list(grid)
    null_line = '|' * len(grid[0])
    if null_line in grid:
        for i in xrange(grid.count(null_line)):
            grid.remove(null_line)
    return grid

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
    import sys
    grid=[]
    for line in sys.stdin:
        grid.append(line.strip())
    return grid

def output_grid(g):
    '''print out a grid in the format expected by the verifier'''
    for line in g:
        print line

if __name__=='__main__':
    output_grid(compress(input_grid()))
