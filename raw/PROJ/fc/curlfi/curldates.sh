#!/bin/bash

todaydate=`date +%Y%m%d`
echo $todaydate 
curl "http://sportsdatabase.com/nba/query?output=default&sdql=date+%40+season%3E2013+and+date+%3C+$todaydate&submit=++S+D+Q+L+%21++" > rawdates
grep -A1 'valign=top bgcolor=ffffff' rawdates  | sed '/--/d' | sed '/val/d' | sort -u > dates
rm rawdates
rm curl_fc.sh

while IFS='' read -r line || [[ -n "$line" ]]; do
	y=`echo $line | cut -c 1-4`
	m=`echo $line | cut -c 5-6`
	d=`echo $line | cut -c 7-8`
	dstr=`echo "$y-$m-$d"`
	cmd='curl "https://www.fantasycruncher.com/lineup-rewind/fanduel/NBA/'
	out=" | grep 'var playerlist =' > raw.$dstr"
	echo "command is" $cmd$dstr'"'$out
	echo $cmd$dstr'"'$out >> curl_fc.sh
done < dates

chmod a+rwx curl_fc.sh

echo "********wrote script curl_fc.sh len="
cat curl_fc.sh | wc -l 

