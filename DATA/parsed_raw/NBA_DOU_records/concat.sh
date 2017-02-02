rm dou.composite.csv
a=`ls -l *player*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat *player*.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > dou.composite.csv;

ad=`ls -l *player*.csv | wc -l` 
echo "wrote dou.composite.csv"; 
ls -l *player*.csv
echo "nfiles=" $ad

rm header
rm temp
