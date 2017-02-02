rm $1.composite.csv
a=`ls -l *$1.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat *$1.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > $1.composite.csv;



echo 'done nlines='
cat $1.composite.csv | wc -l 
rm header
rm temp
