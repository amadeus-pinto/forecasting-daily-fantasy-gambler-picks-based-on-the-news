
python mo_parse.py
mv a.*csv      ../mo/parsefi/
echo "wrote to ../mo/parsefi/"

cd ../mo/parsefi/
echo 'running concat.sh'
./concat.sh

echo 'cleaning names!'

perl -pi -e "s/AJ Hammons/A.J. Hammons/g" ./mo.composite.csv 
perl -pi -e "s/Bryce Dejean-Jones/Bryce Jones/g" ./mo.composite.csv 
perl -pi -e "s/CJ McCollum/C.J. McCollum/g" ./mo.composite.csv 
perl -pi -e "s/CJ Miles/C.J. Miles/g" ./mo.composite.csv 
perl -pi -e "s/CJ Watson/C.J. Watson/g" ./mo.composite.csv 
perl -pi -e "s/CJ Wilcox/C.J. Wilcox/g" ./mo.composite.csv 
perl -pi -e "s/DJ Augustin/D.J. Augustin/g" ./mo.composite.csv 
perl -pi -e "s/Dante Exum/Danté Exum/g" ./mo.composite.csv 
perl -pi -e "s/Fred Vanvleet/Fred VanVleet/g" ./mo.composite.csv 
perl -pi -e "s/JJ Barea/J.J. Barea/g" ./mo.composite.csv 
perl -pi -e "s/JJ Hickson/J.J. Hickson/g" ./mo.composite.csv 
perl -pi -e "s/JJ O'Brien/J.J. O'Brien/g" ./mo.composite.csv 
perl -pi -e "s/JJ Redick/J.J. Redick/g" ./mo.composite.csv 
perl -pi -e "s/JR Smith/J.R. Smith/g" ./mo.composite.csv 
perl -pi -e "s/JaKarr Sampson/Jakarr Sampson/g" ./mo.composite.csv 
perl -pi -e "s/James McAdoo/James Michael McAdoo/g" ./mo.composite.csv 
perl -pi -e "s/John Lucas/John Lucas III/g" ./mo.composite.csv 
perl -pi -e "s/Juan Hernangomez/Juancho Hernangomez/g" ./mo.composite.csv 
perl -pi -e "s/KJ McDaniels/K.J. McDaniels/g" ./mo.composite.csv 
perl -pi -e "s/Larry Nance,/Larry Nance Jr.,/g" ./mo.composite.csv 
perl -pi -e "s/Nicolas Laprovittola/Nicolás Laprovittola/g" ./mo.composite.csv 
perl -pi -e "s/OJ Mayo/O.J. Mayo/g" ./mo.composite.csv 
perl -pi -e "s/PJ Hairston/P.J. Hairston/g" ./mo.composite.csv 
perl -pi -e "s/PJ Tucker/P.J. Tucker/g" ./mo.composite.csv 
perl -pi -e "s/Petr Cornelie/Phil (Flip) Pressey/g" ./mo.composite.csv 
perl -pi -e "s/Stephen Zimmerman/Stephen Zimmerman Jr./g" ./mo.composite.csv 
perl -pi -e "s/TJ McConnell/T.J. McConnell/g" ./mo.composite.csv 
perl -pi -e "s/TJ Warren/T.J. Warren/g" ./mo.composite.csv 
perl -pi -e "s/Wade Baldwin/Wade Baldwin IV/g" ./mo.composite.csv 
perl -pi -e "s/Tim Hardaway Jr/Tim Hardaway Jr./g" ./mo.composite.csv 
perl -pi -e "s/Luc Mbah a Moute/Luc Richard Mbah a Moute/g" ./mo.composite.csv
perl -pi -e "s/Deandre Bembry/DeAndre' Bembry/g" ./mo.composite.csv

#perl -pi -e "s/Jose Calderon/José Calderón/g" ./mo.composite.csv
#perl -pi -e "s/Sergio Rodriguez/Sergio Rodríguez/g" ./mo.composite.csv 
#perl -pi -e "s/Alex Abrines/Álex Abrines/g" ./mo.composite.csv


echo 'done. cding back!'
cd ../../python_scripts/

