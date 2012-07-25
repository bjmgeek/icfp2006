#!/bin/sh
(
echo bbarker
echo plinko
echo run_bb 
cat $1
echo
) | ../umix 2> /dev/null | egrep '^([[:digit:]])|\*' | grep -v ':'
