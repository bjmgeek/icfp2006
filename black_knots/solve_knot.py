import sys
import array

inputs={}
for line in open(sys.argv[1]):
    l=line.split()
    inputs[int(l[0])]=eval(l[2])

movements={}
plinks={}
for i in inputs:
    movements[i]=inputs[i][0]-i #positive to the right, negative to the left
    plinks[i]=inputs[i][1]

