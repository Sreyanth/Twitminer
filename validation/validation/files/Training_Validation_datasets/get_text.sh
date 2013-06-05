#!/bin/bash

for id in `cat $1 | cut -d' ' -f2 | uniq`
do
	max_id=`grep $id $1 | cut -d' ' -f1 | head -1`
	temp=`grep $id $1 | cut -d' ' -f1 | tail -1`
	since_id=`expr $temp - 1`
	curl --retry 5 --max-time 500 "https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&exclude_replies=false&user_id="$id"&max_id="$max_id"&since_id="$since_id"&count=200" >> output
	#python parse4.py  
done > tmp
sed ':a;N;$!ba;s/\nu/ /g' tmp > $1.data
cat $1 | sort > file1.txt
cat $1.data | sort > file2.txt

join file1.txt file2.txt > $1.txt
rm tmp $1.data file1.txt file2.txt
