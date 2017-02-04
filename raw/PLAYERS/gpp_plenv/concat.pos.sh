rm Z.gpp.pos.composite.csv
a=`ls -l Z.gpp.pos*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat Z.gpp.pos*.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > Z.gpp.pos.composite.csv;

ad=`ls -l Z.gpp.pos*.csv | wc -l` 
echo "wrote Z.gpp.pos.composite.csv"; 
ls -l Z.gpp.pos*.csv
echo "nfiles=" $ad

rm header
rm temp
