import sys
import array

inputs={}
output=[]

for line in open(sys.argv[1]):
    l=line.split()
    inputs[int(l[0])]=eval(l[2])

width=1+max(inputs)

movements_remaining={}
plinks_remaining={}
for i in inputs:
    movements_remaining[i]=inputs[i][0]-i #positive to the right, negative to the left
    plinks_remaining[i]=inputs[i][1]
