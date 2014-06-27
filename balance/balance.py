'''balance.py

implement the balance VM
also, provide some assembly and disassembly helper functions
'''

from __future__ import print_function

import sys

MATH=0b001
LOGIC=0b010
SCIENCE=0b000
PHYSICS=0b011

def do_math():
    ''' MATH    001
                 MATH  performs addition  and  its dual,  subtraction.
                 These act on different  registers so that the math is
                 not undone.  All operations are  modular with respect
                 to the number of  relevant bits. Source registers are
                 represented  with  two bits,  so  if  S1  is 3,  then
                 sR[S1+1]  is  sR[0].  Similarly,  dR[1+1]  is  dR[0].
                 Quantities in memory are eight bits, so 250 + 20 is
                 14.

                 M[ dR[D+1] ] <- M[ sR[S1+1] ]  -  M[ sR[S2+1] ]
                 M[ dR[D]   ] <- M[ sR[S1]   ]  +  M[ sR[S2]   ]'''
    print('in operation MATH',file=sys.stderr)
    pass

def do_logic():
    '''' LOGIC   010
                 LOGIC performs bitwise 'and' as well as its perfect
                 dual, bitwise 'exclusive or.'

                 M[ dR[D+1] ] <- M[ sR[S1+1] ]  XOR  M[ sR[S2+1] ]
                 M[ dR[D]   ] <- M[ sR[S1]   ]  AND  M[ sR[S2]   ]'''
    print('in operation LOGIC',file=sys.stderr)
    pass

def do_science():
    ''' SCIENCE 000
                 SCIENCE tests  a hypothesis and  determines the speed
                 at  which the program  progresses. When  executed, it
                 sets the instruction speed IS to immediate value IMM,
                 as long  as the memory  cell indicated by  sR[0] does
                 not  contain  0.  Because  this  instruction  behaves
                 specially when  the memory  cell contains 0,  it also
                 behaves specially  if IS is set to  zero: the machine
                 then  halts. The  value IMM  is treated  as  a signed
                 five-bit number  in two's complement form,  so it can
                 take on values from -16 to +15.

                 if M[ sR[0] ] = 0 then (nothing)
                 otherwise IS <- IMM

                 if IS = 0 then HALT
                 else (nothing)'''
    print('in operation SCIENCE',file=sys.stderr)
    pass

def do_physics():
    ''' PHYSICS 011
                 PHYSICS changes what the registers reference, in both
                 a linear  and angular  way. The immediate  value IMM,
                 treated as a signed  five-bit number, is added to the
                 register sR[0]  so that it may  reference a different
                 memory cell. The  instruction also rotates the values
                 between some subset of the registers, according  to a 
                 bitmask  derived from IMM.  The source register sR[0]
                 is always  part of  the rotated  set, so  the bitmask
                 used is a 6 bit  number where  the lowest 5  bits are
                 the same as IMM and the sixth bit is always 1.
                 
                 sR[0] <- sR[0] + (IMM as signed 5-bit number)
                 
                 let L=L0,...,L4 be the registers
                     dR[1], dR[0], sR[3], sR[2], sR[1]
                 then let C be the list of n elements Li
                     such that bit i is set in IMM
                     (bit 0 is the least significant,
                      bit 4 is the most significant)
                 then let Cs be the list (sR[0], C0, ..., C(n-1))
                 and  let Cd be the list (C0, ..., C(n-1), sR[0])
                 then, simultaneously
                      Cd0 <- Cs0
                      ...
                      Cdn <- Csn'''
    print('in operation PHYSICS',file=sys.stderr)
    pass

def show_machine_state():
    print('CODE:',CODE,file=sys.stderr)
    print('IP:',IP,file=sys.stderr)
    print('IS:',IS,file=sys.stderr)
    print('sR:',sR,file=sys.stderr)
    print('dR:',dR,file=sys.stderr)
    for x in xrange(16):
        for y in xrange(16):
            print(format(M[x+16*y],'02x'),end=' ',file=sys.stderr)
        print('',file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv[1]) % 2:
        print ('usage:',sys.argv[0],'CODE\nwhere CODE is a hex-encoded byte string',file=sys.stderr)
        exit()

    CODE=[]
    for n in xrange(len(sys.argv[1])):
        if n % 2 == 0:
            CODE.append(eval('0x'+sys.argv[1][n:n+2]))
    IP=0
    IS=1
    M=[0]*256
    sR=[0,0,0,0]
    dR=[0,0]
    
    counter=0
    #run the code
    while True:
        if counter > 100:
            print ('too long',file=sys.stderr)
            exit()
        else:
            counter+=1
        show_machine_state()
        inst=CODE[IP]
        opcode=inst >> 5
        if opcode==MATH:
            do_math()
        elif opcode==LOGIC:
            do_logic()
        elif opcode==SCIENCE:
            do_science()
        elif opcode==PHYSICS:
            do_physics()
        else:
            print('received instruction BAIL (code:',hex(CODE[IP]),CODE[IP],') at IP',IP,file=sys.stderr)
            exit()
        IP=((IS + IP) % 2** 32)    % len(CODE)
