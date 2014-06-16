#!/bin/sh
(
echo bbarker
echo plinko
echo run_bb 
cat $1
echo
) | ../umix 2> /dev/null | egrep 'BK|^([[:digit:]])|\*'|grep -v '/'|grep -v ^*
