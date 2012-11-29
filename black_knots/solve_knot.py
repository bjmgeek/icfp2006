import sys
import array

class result():
    def __init__(self,in_col):
        self.plinks=0
        self.out_col=in_col
    def __str__(self):
        return str((self.out_col,self.plinks))
    __repr__ = __str__


# generates code to swap output columns x and y.
# The lower (leftmost) output column gets abs(x-y) plinks
# the higher numbered (rightmost) column gets 0 plinks
# all other columns between x and y get 1 plink
def swap(x,y):
    x,y=sorted((x,y))
    for z in xrange(x,y):
         print '|' * (z) + '><' + '|' * (width-z-1)
         results[z].plinks += 1
         results[z-1].out_col,results[z].out_col = results[z].out_col,results[z-1].out_col
    if abs(x-y) > 1: 
        for z in xrange(y,x,-1):
             print '|' * (z-1) + '><' + '|' * (width-z)
             results[z].plinks += 1
             results[z-1].out_col,results[z].out_col = results[z].out_col,results[z-1].out_col

# generate code to move left from y to x
def move_left(x,y):
    #print 'moving from',y,'to',x
    for z in xrange(y,x,-1):
         print '|' * (z-1) + '><' + '|' * (width-z-1)
         results[z-1].plinks += 1
         results[z-1].out_col,results[z].out_col = results[z].out_col,results[z-1].out_col
         #print "results:",results


def find_rule(target):
    for i in xrange(width):
        if rules[i][0]==target:
            return i

# main
rules=[]
results=[]

for line in open(sys.argv[1]):
    l=line.split()
    rules.append(eval(l[2]))

width=len(rules)

# start out with output_cache equal to inputs
for i in xrange(width): 
    results.append(result(i))
 
def swap(x,y):
    '''
    swap(x,y)
    prints black knot code to swap two input columns.

    Generates plinks according to the following formula (assuming x < y):
        y-x = 1: 1 plink to input x; 0 plinks to input y
        y-x > 1: 2 plinks to input x; 1 plink to intervening inputs; 0 plinks to
                 input y

    If x > y, they are swapped first.
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
    adds plinks to the specified range of columns

    start is the first input column to start adding plinks to, and stop is the
    first input column to not add plinks.  The range must be contiguous, and
    greater than one column.

    If the number of columns to add plinks to is even, plinks can be any number,
    but if it's odd, plinks must be an even number.
    '''
    l=[]
    o=''
    (start,stop)=sorted((start,stop))
    #sanity checks:
    assert (stop - start) > 1 and (stop - start) % 2 == 0 or plinks % 2 == 0

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
