#!/usr/bin/env python 
from __future__ import print_function
import sys,binascii


if len(sys.argv) !=2:
    print('usage: ' + sys.argv[0] + ' filename',file=sys.stderr)
    exit()

dump=open(sys.argv[1]).read().split('%')[1]
dump=''.join(dump.split())
dump=binascii.unhexlify(dump)

out=open(sys.argv[1].replace('.dump',''),'w')
out.write(dump)
