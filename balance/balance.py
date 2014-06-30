'''balance.py

implement the balance VM
also, provide some assembly and disassembly helper functions
'''

from __future__ import print_function

import sys
import array

MATH=0b001
LOGIC=0b010
SCIENCE=0b000
PHYSICS=0b011

def do_math(D,S1,S2):
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
    global M,IP,IS,sR,dR
    D_1=(D+1)%2
    S1_1=(S1+1)%4
    S2_1=(S2+1)%4
    M[ dR[D_1] ] = (M[ sR[S1_1] ]  -  M[ sR[S2_1] ]) & 0xFF
    M[ dR[D]   ] = (M[ sR[S1]   ]  +  M[ sR[S2]   ]) & 0xFF

def do_logic(D,S1,S2):
    '''' LOGIC   010
                 LOGIC performs bitwise 'and' as well as its perfect
                 dual, bitwise 'exclusive or.'

                 M[ dR[D+1] ] <- M[ sR[S1+1] ]  XOR  M[ sR[S2+1] ]
                 M[ dR[D]   ] <- M[ sR[S1]   ]  AND  M[ sR[S2]   ]'''
    print('in operation LOGIC',file=sys.stderr)
    global M,IP,IS,sR,dR
    D_1=(D+1)%2
    S1_1=(S1+1)%4
    S2_1=(S2+1)%4
    M[ dR[D_1] ] <- M[ sR[S1_1] ]  ^  M[ sR[S2_1] ]
    M[ dR[D]   ] <- M[ sR[S1]   ]  &  M[ sR[S2]   ]

def do_science(IMM):
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
    global M,IP,IS,sR,dR
    if M[ sR[0] ] == 0:
        pass
    else: IS = IMM
    if IS == 0:
        print('halted',file=sys.stderr)
        exit()

def rotate(bitmask,items):
    '''helper function for PHYSICS'''
    moving=[None]*6
    not_moving=[None]*6
    results=[]
    for n in xrange(6):
        if (bitmask >> n) & 1:
            moving[n] = items[n]
        else:
            not_moving[n] = items[n]
    moving.append(moving.pop(0))
    while moving.count(None) > 0:
        moving.remove(None)
    for n in xrange(6):
        if not_moving[n]:
            results.append(not_moving[n])
        else:
            results.append(moving.pop(0))
    return tuple(results)

def do_physics(IMM):
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
    global M,IP,IS,sR,dR
    sR[0] += twos_complement(IMM,5)
    sR[0] &= 0xFF
    bitmask = IMM | 0b100000
    regs=(sR[0],sR[1],sR[2],sR[3],dR[0],dR[1])
    sR[0],sR[1],sR[2],sR[3],dR[0],dR[1] = rotate(bitmask,regs)

def show_machine_state():
    global M,IP,IS,sR,dR
    print('CODE:',CODE,file=sys.stderr)
    print('IP:',IP,file=sys.stderr)
    print('IS:',IS,file=sys.stderr)
    print('sR:',sR,file=sys.stderr)
    print('dR:',dR,file=sys.stderr)
    for x in xrange(16):
        for y in xrange(16):
            print(format(M[x+16*y],'02x'),end=' ',file=sys.stderr)
        print('',file=sys.stderr)

def twos_complement(n,bits):
    '''given an unsigned number n, and a number of bits, return the int
   equivalent using 2's complement for negatives'''
    if n < 2 ** (bits - 1):
        return n
    else:
        return  -(( 1 + ~ n) & ((2 ** bits) - 1))

if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv[1]) % 2:
        print ('usage:',sys.argv[0],'CODE\nwhere CODE is a hex-encoded byte string',file=sys.stderr)
        exit()

    CODE=array.array('B')
    for n in xrange(len(sys.argv[1])):
        if n % 2 == 0:
            CODE.append(eval('0x'+sys.argv[1][n:n+2]))
    IP=0
    IS=1
    M=array.array('B',[0]*256)
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
            do_math(inst >> 4 & 0b1, inst >> 2 & 0b11, inst & 0b11)
        elif opcode==LOGIC:
            do_logic(inst >> 4 & 0b1, inst >> 2 & 0b11, inst & 0b11)
        elif opcode==SCIENCE:
            do_science(inst & 0b11111)
        elif opcode==PHYSICS:
            do_physics(inst & 0b11111)
        else:
            print('received instruction BAIL (code:',hex(CODE[IP]),CODE[IP],') at IP',IP,file=sys.stderr)
            exit()
        IP=((IS + IP) % 2** 32)    % len(CODE)
