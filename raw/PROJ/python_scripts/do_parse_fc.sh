
python fc_parse.py
mv a.*csv      ../fc/parsefi/
echo "wrote to ../fc/parsefi/"
cd ../fc/parsefi/
echo 'running concat.sh'
./concat.sh



echo 'cleaning names!'
perl -pi -e "s/Bryce Dejean-Jones/Bryce Jones/g" ./fc.composite.csv 
perl -pi -e "s/Cristiano Da Silva Felicio/Cristiano Felicio/g" ./fc.composite.csv 
perl -pi -e "s/Dante Exum/Danté Exum/g" ./fc.composite.csv 
perl -pi -e "s/DeAndre Bembry/DeAndre' Bembry/g" ./fc.composite.csv 
perl -pi -e "s/James McAdoo/James Michael McAdoo/g" ./fc.composite.csv 
perl -pi -e "s/Juan Hernangomez/Juancho Hernangomez/g" ./fc.composite.csv 
perl -pi -e "s/Luc Mbah a Moute/Luc Richard Mbah a Moute/g" ./fc.composite.csv 
perl -pi -e "s/Maurice N'dour/Maurice Ndour/g" ./fc.composite.csv 
perl -pi -e "s/Nicolas Laprovittola/Nicolás Laprovittola/g" ./fc.composite.csv 
perl -pi -e "s/Phil Pressey/Phil (Flip) Pressey/g" ./fc.composite.csv 
perl -pi -e "s/Raulzinho Neto/Raul Neto/g" ./fc.composite.csv 
perl -pi -e "s/Wade Baldwin/Wade Baldwin IV/g" ./fc.composite.csv 
perl -pi -e "s/Louis Williams/Lou Williams/g" ./fc.composite.csv


perl -pi -e "s/Jose Juan Barea/J.J. Barea/g" ./fc.composite.csv
perl -pi -e "s/Kelly Oubre Jr.,/Kelly Oubre,/g"   ./fc.composite.csv 


#perl -pi -e "s/Sergio Rodriguez/Sergio Rodríguez/g" ./fc.composite.csv 
#perl -pi -e "s/Jose Calderon/José Calderón/g" ./fc.composite.csv


echo 'done. cding back!'
cd ../../python_scripts/


