rm seas.composite.csv
a=`ls -l *.*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
cat *.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
cat header temp > seas.composite.csv;

ad=`ls -l *.*.csv | wc -l` 
echo "wrote seas.composite.csv"; 
#ls -l *.*.csv
echo "nfiles=" $ad

rm header
rm temp
