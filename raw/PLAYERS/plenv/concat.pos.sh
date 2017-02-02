rm Z.pos.composite.csv
a=`ls -l Z.pos*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat Z.pos*.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > Z.pos.composite.csv;

ad=`ls -l Z.pos*.csv | wc -l` 
echo "wrote Z.pos.composite.csv"; 
ls -l Z.pos*.csv
echo "nfiles=" $ad

rm header
rm temp
