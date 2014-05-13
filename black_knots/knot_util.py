def compress(grid):
    if len(grid) == 0: return []

    for y in xrange (1,len(grid)):
        l0 = list(grid[y-1])
        l1 = list(grid[y])
        for x in xrange(len(l0)-1):
            if l0[x] == '|' and l0[x+1] == '|' and l1[x] == '>' and l1[x+1] == '<':
                l0[x] = '>'
                l0[x+1] = '<'
                l1[x] = '|'
                l1[x+1] = '|'
        
    grid[y-1]=''.join(l0)
    grid[y]=''.join(l1)
    
    null_line = '|' * len(grid[0])
    if null_line in grid:
        for i in xrange(grid.count(null_line)):
            grid.remove(null_line)
    return grid

def string_to_grid(s):
    s=s.strip()
    s=s.split()
    return s

def file_to_grid(f):
    '''f is a file name'''
    grid=[]
    f=open(f,'r')
    for line in f:
        grid.append(line.strip())
    f.close()
    return grid

def input_grid():
    '''reads grid from standard input'''
    import sys
    grid=[]
    for line in sys.stdin:
        grid.append(line.strip())
    return grid

def output_grid(g):
    for line in g:
        print line

if __name__=='__main__':
    output_grid(compress(input_grid()))
