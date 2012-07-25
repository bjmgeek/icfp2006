#!/bin/sh
(
echo bbarker
echo plinko
echo verify
cat $1
echo ''
echo $USER
echo ''
) | ../umix
