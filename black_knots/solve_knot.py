import sys
import array

rules={}
movements_remaining={}
plinks_remaining={}

for line in open(sys.argv[1]):
    l=line.split()
    i=int(l[0])
    rules[i]=(eval(l[2]))

width=max(rules)

for i in rules:
    movements_remaining[i]=rules[i][0]-i #positive to the right, negative to the left
    plinks_remaining[i]=rules[i][1]

def swap(x,y):
    path=[]
    for z in xrange(x,y):
         path.append ('|' * (z) + '><' + '|' * (width-z-1))
    if abs(x-y) > 1: 
        path.extend(reversed(path[:-1]))
    for row in path: 
        print row 
