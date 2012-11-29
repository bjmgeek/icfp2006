import sys
import array

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


# main
rules=[]

for line in open(sys.argv[1]):
    l=line.split()
    rules.append(eval(l[2]))

width=len(rules)

