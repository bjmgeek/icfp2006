#!/bin/sh

get_room_name() {
	xpath -q -e '//room/name/text()' $1| egrep -v '^[[:space:]]*$'|sed 's/^[[:space:]]*//g' 
}

get_item_names() {
	xpath -q -e '//item/name/text()' $1| egrep -v '^[[:space:]]*$'|sed 's/^[[:space:]]*//g' 
}

queryfile=`mktemp`
echo 'begin transaction;' >> $queryfile
for f in *xml; do
	room=`get_room_name $f`
	echo room \"$room\"
	query="insert into rooms(name) values('$room');"
	echo $query >> $queryfile

	query="update rooms set json=json(' $(cat `basename $f .xml`.json| sed 's/\x27/\x27\x27/g') ') where name='$room';"
	echo $query >> $queryfile


	get_item_names $f | sort | uniq | while read item; do
		echo item \"$item\"
		path="//adjective[contains(../../name,'$item')]/text()"
		adjectives=$(xpath -q -e "$path" $f| egrep -v '^[[:space:]]*$'|sed 's/^[[:space:]]*//g')
		if [ -z "$adjectives" ]; then
			echo no adjectives
			path="//condition[contains(../name,'$item')]"
			condition=$(xpath -q -e "$path" $f | head -2|tail -1|sed 's/.*<//g;s/>.*//g')
			echo condition: $condition
			query="insert into items(name,location,condition) values ('$item','$room','$condition');"
			echo $query >> $queryfile
		else
			for adj in $adjectives; do
				echo adjective \"$adj\"
				path="//condition[contains(../name,'$item') and contains(../adjectives/adjective,'$adj')]"
				condition=$(xpath -q -e "$path" $f | head -2|tail -1|sed 's/.*<//g;s/>.*//g')
				echo condition: $condition
				query="insert into items(name,adjectives,location,condition) values('$item','$adj','$room','$condition');"
				echo $query >> $queryfile
			done
		fi
	done
done
echo 'commit;' >> $queryfile
sqlite3 adventure.sqlite3 < $queryfile
