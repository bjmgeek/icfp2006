#!/bin/sh
if [ "$#" -ne 2 ]; then
	echo usage: $0 filename puzzle
	exit 1
fi
(echo 'yang
U+262F
/bin/umodem code stop'
cat $1
echo stop
echo certify $2 code
)|../umix
