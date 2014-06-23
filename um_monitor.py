#!/usr/bin/env python
'''um_monitor
allow multiple processes to interact with a single running UM instance.

usage: um_monitor um_file [session]

where um_file is a UM binary. 
If a UM session is not running, one will will be started.  Otherwise, input and
output from the existing one will de duplicated. 
If session is specified, all invocations of the um_monitor script with the same
session name share a single UM instance.
'''

import os,sys,multiprocessing,shutil
from __future__ import print_function

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage:',sys.argv[0],'um_file [session]',file=sys.stderr)
        exit()
    elif len(sys.argv) == 2:
        session=''
        lock_dir=os.path.join(sys.path[0],'lock')
    else len(sys.argv)==3:
        session=sys.argv[2]
        lock_dir=os.path.join(sys.path[0],'lock'+session)

    #try to get the lock
    try:
        os.mkdir(lock_dir)
        master=True
    except OSError:
        master=False
    
    if master:
        setup_dir(lock_dir)
        print('starting UM session',session,file=sys.stderr)
        run_UM(sys.argv[1],lock_dir)
        print('done with UM session',session,file=sys.stderr)
        shutil.rmdir(lock_dir)
    else:
        print('connecting to UM session',session,file=sys.stderr)
        interact_UM(lock_dir)
        print('done with UM session',session,file=sys.stderr)
