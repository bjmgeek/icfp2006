#!/bin/sh
( echo guest
echo cd code
echo rm hack.bas
echo /bin/umodem hack.bas STOP
cat hack.bas
echo STOP
echo /bin/qbasic hack.bas
echo hack.exe $1
if [ "$2" == "-i" ] ; then
cat
fi  ) | ./um codex.um 
