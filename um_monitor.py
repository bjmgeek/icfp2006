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

from __future__ import print_function
import os,sys,subprocess,shutil,select,fcntl


def increment_counter(path,filename):
    with open(os.path.join(path,filename),'r+') as counter_file:
        try:
            fcntl.lockf(counter_file,fcntl.LOCK_SH)
            n=int(counter_file.readline().strip())
        except ValueError:
            n=0
        fcntl.lockf(counter_file,fcntl.LOCK_EX)
        counter_file.truncate(0)
        counter_file.seek(0)
        print(n+1,file=counter_file)
        fcntl.lockf(counter_file,fcntl.LOCK_UN)

def decrement_counter(path,filename):
    with open(os.path.join(path,filename),'r+') as counter_file:
        try:
            fcntl.lockf(counter_file,fcntl.LOCK_SH)
            n=int(counter_file.readline().strip())
        except ValueError:
            n=0
        fcntl.lockf(counter_file,fcntl.LOCK_EX)
        counter_file.truncate(0)
        counter_file.seek(0)
        print(n-1,file=counter_file)
        fcntl.lockf(counter_file,fcntl.LOCK_UN)

def set_counter(path,filename,n):
    with open(os.path.join(path,filename),'a') as counter_file:
        fcntl.lockf(counter_file,fcntl.LOCK_EX)
        counter_file.truncate(0)
        counter_file.seek(0)
        print(n,file=counter_file)
        fcntl.lockf(counter_file,fcntl.LOCK_UN)

def get_counter(path,filename):
    with open(os.path.join(path,filename),'r') as counter_file:
        try:
            fcntl.lockf(counter_file,fcntl.LOCK_SH)
            n=int(counter_file.readline().strip())
            fcntl.lockf(counter_file,fcntl.LOCK_UN)
        except ValueError:
            n=0
            fcntl.lockf(counter_file,fcntl.LOCK_UN)
    return n

def get_input_bytes(data_dir):
    '''to be called by the server'''
    with open(os.path.join(data_dir,'input'),'r+') as input_file:
        fcntl.lockf(input_file,fcntl.LOCK_SH)
        buf=input_file.read()
        fcntl.lockf(input_file,fcntl.LOCK_EX)
        input_file.truncate(0)
        input_file.seek(0)
        fcntl.lockf(input_file,fcntl.LOCK_UN)
    return buf

def send_output_bytes(data,data_dir):
    '''to be called by the server'''
    print ('server received',len(data),'bytes of output',file=sys.stderr)
    with open(os.path.join(data_dir,'output'),'r+') as output_file:
        fcntl.lockf(output_file,fcntl.LOCK_EX)
        output_file.truncate(0)
        output_file.seek(0)
        output_file.write(data)
        print ('should have written',len(data),'bytes of output',file=sys.stderr)
        output_file.flush()
        print(os.fstat(output_file.fileno()).st_size,
              'bytes actually written',file=sys.stderr)
        fcntl.lockf(output_file,fcntl.LOCK_UN)
    set_counter(data_dir,'readers',get_counter(data_dir,'clients'))

def get_output_bytes(data_dir):
    '''to be called by the clients'''
    filename=os.path.join(data_dir,'output')
    with open(filename,'r') as f:
        fcntl.lockf(f,fcntl.LOCK_SH)
        size=os.fstat(f.fileno()).st_size
        if size > 0:
            print('read',size,'bytes of output',file=sys.stderr)
            buf=f.read()
        fcntl.lockf(f,fcntl.LOCK_UN)
    decrement_counter(data_dir,'readers')
    if get_counter(data_dir,'readers') == 0:
        print('last client is done reading, truncating file',file=sys.stderr)
        with open(filename,'r+'):
            fcntl.lockf(fcntl.LOCK_EX)
            f.truncate(0)
            f.seek(0)
            fcntl.lockf(fcntl.LOCK_UN)
    return buf

def send_input_bytes(data,data_dir):
    '''to be called by the clients'''
    fiename=os.path.join(data_dir,'input')
    with open(filename,'a') as f:
        fcntl.lockf(f,fcntl.LOCK_EX)
        f.write(data)
        fcntl.lockf(f,fcntl.LOCK_UN)

def run_UM(um,target,temp_dir,session):
    p=subprocess.Popen([um,target],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    print('UM process',p.pid,'started',file=sys.stderr)
    #set stdout to non-blocking, so read() will not wait for EOF
    fl = fcntl.fcntl(p.stdout, fcntl.F_GETFL) #get current file flags
    fcntl.fcntl(p.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK) #set flags
    output_waiting=select.poll()
    output_waiting.register(p.stdout)
    #check if the process is still running
    while p.returncode is None:
        p.poll()
        print('UM process',p.pid,'running',file=sys.stderr)
        #check if there are input bytes available
        in_bytes=get_input_bytes(temp_dir)
        p.stdin.write(in_bytes)
        if output_waiting.poll(1000):
            print('output waiting',file=sys.stderr)
            send_output_bytes(p.stdout.read(),temp_dir)
    print ('UM process ended with status',p.returncode,file=sys.stderr)

def register_client(path):
    increment_counter(path,'clients')

def unregister_client(path):
    decrement_counter(path,'clients')

def interact_UM(path):
    for line in sys.stdin:
        print(get_output_bytes(path))
        send_input_bytes(line,path)

def setup_dir(path):
    with open(os.path.join(path,'pidfile'),'w') as pidfile:
        print(os.getpid(),file=pidfile)
    open(os.path.join(path,'input'),'w').close()
    open(os.path.join(path,'output'),'w').close()
    with open(os.path.join(path,'clients'),'w') as f: print(0,file=f)
    with open(os.path.join(path,'readers'),'w') as f: print(0,file=f)


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage:',sys.argv[0],'um_file [session]',file=sys.stderr)
        exit()
    elif len(sys.argv) == 2:
        session=''
        lock_dir=os.path.join(sys.path[0],'lock')
    else:
        session=sys.argv[2]
        lock_dir=os.path.join(sys.path[0],'lock'+session)

    #try to get the lock
    try:
        os.mkdir(lock_dir)
        master=True
    except OSError:
        master=False
    
    if master:
        #we are the server
        setup_dir(lock_dir)
        print('starting UM session',session,file=sys.stderr)
        um=os.path.join(sys.path[0],'um')
        run_UM(um,sys.argv[1],lock_dir,session)
        print('done with UM session',session,file=sys.stderr)
        #shutil.rmtree(lock_dir)
    else:
        #we are the client
        print('connecting to UM session',session,file=sys.stderr)
        register_client(lock_dir)
        interact_UM(lock_dir)
        print('done with UM session',session,file=sys.stderr)
        unregister_client(lock_dir)
