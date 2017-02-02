rm gpp.composite.csv
a=`ls -l *player*.csv | head -1 | awk -F ' ' '{print $09}'` ;  FL=`cat $a | head -1` ; echo "FIRST LINE IS $FL"
echo $FL > header ; 
echo "pre-cat"
cat *player*.csv | sed "/$FL/d" | sed '/^\s*$/d' > temp ;
echo "catted"
cat header temp > gpp.composite.csv;


echo 'cleaning names!'

perl -pi -e "s/José Calderón/Jose Calderon/g" ./gpp.composite.csv
perl -pi -e "s/Álex Abrines/Alex Abrines/g" ./gpp.composite.csv
perl -pi -e "s/Sergio Rodríguez/Sergio Rodriguez/g" ./gpp.composite.csv 
perl -pi -e "s/Sergio  Rodríguez/Sergio Rodriguez/g" ./gpp.composite.csv
perl -pi -e "s/Brad Beal/Bradley Beal/g" ./gpp.composite.csv
perl -pi -e "s/Guillermo Hernangómez/Guillermo Hernangomez/g" ./gpp.composite.csv
perl -pi -e "s/James Ennis III/James Ennis/g" ./gpp.composite.csv
perl -pi -e "s/Jose Juan Barea/J.J. Barea/g" ./gpp.composite.csv
perl -pi -e "s/Kelly Oubre Jr./Kelly Oubre/g" ./gpp.composite.csv
perl -pi -e "s/Raulzinho Neto/Raul Neto/g" ./gpp.composite.csv
perl -pi -e "s/RJ Hunter/R.J. Hunter/g" ./gpp.composite.csv
perl -pi -e "s/Louis Williams/Lou Williams/g" ./gpp.composite.csv


ad=`ls -l *player*.csv | wc -l` 
echo "wrote gpp.composite.csv"; 
ls -l *player*.csv
echo "nfiles=" $ad

rm header
rm temp
