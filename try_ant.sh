#!/bin/sh
(
echo gardener
echo mathemantica
echo rm $1
echo /bin/umodem $1 STOP
cat $1
echo STOP
if [ "$2" == "-i" ]; then
	echo antomaton -i $1
	cat
else
	echo antomaton $1
fi
) | ./umix
