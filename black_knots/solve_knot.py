import sys
import array

class result():
    def __init__(self,in_col):
        self.plinks=0
        self.out_col=in_col

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
for i in xrange(width): #output_cache[x] is what input gives output x
    results.append(result(i))

# find the input that is supposed to go to 0
for i in xrange(width):
    src=find_rule(target=i)
    #find the current output row of src, and move from there
    move_left(i,results[src].out_col)
