rm Z.composite.csv
a=`ls -l Z*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat Z*.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > Z.composite.csv;

ad=`ls -l Z*.csv | wc -l` 
echo "wrote Z.composite.csv"; 
ls -l Z*.csv
echo "nfiles=" $ad

rm header
rm temp
