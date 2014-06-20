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
	get_item_names $f| while read item; do
		echo item \"$item\"
		adjectives=$(xpath -q -e '//item/name/text()' $f | egrep -v '^[[:space:]]*$'|sed 's/^[[:space:]]*//g')
		if [ -z "$adjectives" ]; then
			echo no adjectives
			query="insert into items(name,location) values ('$item','$room');"
			echo $query >> $queryfile
		else
			for adj in $adjectives; do
				echo adjective \"$adj\"
				query="insert into items(name,adjectives,location) values('$item','$adj','$room');"
				echo $query >> $queryfile
			done
		fi
	done
done
echo 'commit;' >> $queryfile
sqlite3 adventure.sqlite3 < $queryfile
