rm team.roll.composite.csv
a=`ls -l *.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat *.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > team.roll.composite.csv;

ad=`ls -l *.csv | wc -l` 
echo "wrote team.roll.composite.csv"; 
ls -l *.csv
echo "nfiles=" $ad

rm header
rm temp
