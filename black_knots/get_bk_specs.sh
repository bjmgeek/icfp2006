#!/bin/sh
for model in 000 010 020 030 040 050 100 200 300 400 500
do 
	(echo bbarker
	echo plinko
	echo bk_specs
	echo $model)|../umix |fgrep -e '->' |grep -v '*' > $model.spec 
done
