#!/bin/bash

seasonin=$1
echo "season arg= $seasonin "
todaydate=`date +%Y%m%d`
echo $todaydate 
curl "http://sportsdatabase.com/nba/query?output=default&sdql=date+%40+season%3D$seasonin+and+date%3C+$todaydate&submit=++S+D+Q+L+%21++" > rawdates
grep -A1 'valign=top bgcolor=ffffff' rawdates  | sed '/--/d' | sed '/val/d' | sort -u > dates
rm rawdates

while IFS='' read -r line || [[ -n "$line" ]]; do
qdate=$line
y=`echo $line | cut -c 1-4`
m=`echo $line | cut -c 5-6`
d=`echo $line | cut -c 7-8`
date=`echo "$y-$m-$d"`

echo "doing date,qdate=           " $date , $line
curl "http://sportsdatabase.com/nba/player_query?output=default&sdql=name+as+Name%2Cteam+as+Team%2C+o%3Ateam+as+Opp%2Cdate%2Cgame+number%2Cseason%2Cminutes%2Cassists%2C+blocks%2C+defensive+rebounds%2C+field+goals+attempted%2C+field+goals+made%2C+fouls%2C+free+throws+attempted%2C+free+throws+made%2C+offensive+rebounds%2C+plus+minus%2C+points%2C+position%2C+rebounds%2C+steals%2C+three+pointers+attempted%2C+three+pointers+made%2C+turnovers+%40+date%3D$qdate&submit=++S+D+Q+L+%21++"  | perl -pi -e 's/<\/tr\>/ENDOFLINE/g' | sed -E 's/<[^>]*>//g' | perl -pi -e 's/\n/,/g' | perl -pi -e 's/ENDOFLINE,,,/\n/g' | perl -pi -e 's/,,,/,/g' | sed '/Game/d' | sed '/,e-mail/d'  | grep -A 1000 'Name,Team,Opp,date,game number,season,minutes,assists, blocks, defensive rebounds, field goals attempted, field goals made, fouls, free throws attempted, free throws made, offensive rebounds, plus minus, points, position, rebounds, steals, three pointers attempted, three pointers made, turnovers' | perl -pi -e 's/,,$//g' |  perl -pi -e 's/,$//g' | perl -pi -e 's/^,//g' > sdb.$date.csv

echo wrote sdb.$date.csv!
perl -pi -e 's/Bucks/MIL/g'                  ./sdb.$date.csv        
perl -pi -e 's/Bulls/CHI/g'                  ./sdb.$date.csv 
perl -pi -e 's/Cavaliers/CLE/g'              ./sdb.$date.csv      
perl -pi -e 's/Celtics/BOS/g'                ./sdb.$date.csv    
perl -pi -e 's/Clippers/LAC/g'               ./sdb.$date.csv     
perl -pi -e 's/Grizzlies/MEM/g'              ./sdb.$date.csv      
perl -pi -e 's/Hawks/ATL/g'                  ./sdb.$date.csv  
perl -pi -e 's/Heat/MIA/g'                   ./sdb.$date.csv 
perl -pi -e 's/Hornets/CHA/g'                ./sdb.$date.csv    
perl -pi -e 's/Jazz/UTA/g'                   ./sdb.$date.csv 
perl -pi -e 's/Kings/SAC/g'                  ./sdb.$date.csv  
perl -pi -e 's/Knicks/NYK/g'                 ./sdb.$date.csv   
perl -pi -e 's/Lakers/LAL/g'                 ./sdb.$date.csv   
perl -pi -e 's/Magic/ORL/g'                  ./sdb.$date.csv  
perl -pi -e 's/Mavericks/DAL/g'              ./sdb.$date.csv      
perl -pi -e 's/Nets/BKN/g'                   ./sdb.$date.csv 
perl -pi -e 's/Nuggets/DEN/g'                ./sdb.$date.csv    
perl -pi -e 's/Pacers/IND/g'                 ./sdb.$date.csv   
perl -pi -e 's/Pelicans/NOR/g'               ./sdb.$date.csv     
perl -pi -e 's/Pistons/DET/g'                ./sdb.$date.csv    
perl -pi -e 's/Raptors/TOR/g'                ./sdb.$date.csv    
perl -pi -e 's/Rockets/HOU/g'                ./sdb.$date.csv    
perl -pi -e 's/Seventysixers/PHI/g'          ./sdb.$date.csv          
perl -pi -e 's/Spurs/SAS/g'                  ./sdb.$date.csv  
perl -pi -e 's/Suns/PHO/g'                   ./sdb.$date.csv 
perl -pi -e 's/Thunder/OKC/g'                ./sdb.$date.csv    
perl -pi -e 's/Timberwolves/MIN/g'           ./sdb.$date.csv         
perl -pi -e 's/Trailblazers/POR/g'           ./sdb.$date.csv         
perl -pi -e 's/Warriors/GSW/g'               ./sdb.$date.csv     
perl -pi -e 's/Wizards/WAS/g'                ./sdb.$date.csv    

perl -pi -e "s/Amare Stoudemire/Amar'e Stoudemire/g"   ./sdb.$date.csv  
perl -pi -e "s/Al Farouq Aminu/Al-Farouq Aminu/g"   ./sdb.$date.csv  
perl -pi -e "s/CJ McCollum/C.J. McCollum/g"   ./sdb.$date.csv  
perl -pi -e "s/CJ Miles/C.J. Miles/g"   ./sdb.$date.csv  
perl -pi -e "s/CJ Watson/C.J. Watson/g"   ./sdb.$date.csv  
perl -pi -e "s/DJ Augustin/D.J. Augustin/g"   ./sdb.$date.csv  
perl -pi -e "s/Dangelo Russell/D'Angelo Russell/g"   ./sdb.$date.csv  
perl -pi -e "s/Deandre Jordan/DeAndre Jordan/g"   ./sdb.$date.csv  
perl -pi -e "s/Deandre Liggins/DeAndre Liggins/g"   ./sdb.$date.csv  
perl -pi -e "s/Demar Derozan/DeMar DeRozan/g"   ./sdb.$date.csv  
perl -pi -e "s/Demarcus Cousins/DeMarcus Cousins/g"   ./sdb.$date.csv  
perl -pi -e "s/Demarre Carroll/DeMarre Carroll/g"   ./sdb.$date.csv  
perl -pi -e "s/Glenn Rice Jr/Glen Rice Jr./g"   ./sdb.$date.csv  
perl -pi -e "s/Glenn Robinson Iii/Glenn Robinson III/g"   ./sdb.$date.csv  
perl -pi -e "s/JJ Hickson/J.J. Hickson/g"   ./sdb.$date.csv  
perl -pi -e "s/JJ Redick/J.J. Redick/g"   ./sdb.$date.csv  
perl -pi -e "s/JR Smith/J.R. Smith/g"   ./sdb.$date.csv  
perl -pi -e "s/Jakarr Sampson/JaKarr Sampson/g"   ./sdb.$date.csv  
perl -pi -e "s/Jamychal Green/JaMychal Green/g"   ./sdb.$date.csv  
perl -pi -e "s/Javale McGee/JaVale McGee/g"   ./sdb.$date.csv  
perl -pi -e "s/Johnny Obryant/Johnny O'Bryant/g"   ./sdb.$date.csv  
perl -pi -e "s/Jose Juan Barea,/J.J. Barea,/g"   ./sdb.$date.csv  
perl -pi -e "s/Jose Barea,/J.J. Barea,/g"   ./sdb.$date.csv  
perl -pi -e "s/Karl Anthony Towns/Karl-Anthony Towns/g"   ./sdb.$date.csv  
perl -pi -e "s/Kj McDaniels/K.J. McDaniels/g"   ./sdb.$date.csv  
perl -pi -e "s/Kelly Oubre Jr,/Kelly Oubre,/g"   ./sdb.$date.csv  
perl -pi -e "s/Kelly Oubre Jr. Jr,/Kelly Oubre,/g"   ./sdb.$date.csv  
perl -pi -e "s/Kelly Oubre,/Kelly Oubre,/g"   ./sdb.$date.csv  
perl -pi -e "s/Kentavious Caldwell Pope/Kentavious Caldwell-Pope/g"   ./sdb.$date.csv  
perl -pi -e "s/Larry Nance,/Larry Nance Jr.,/g"   ./sdb.$date.csv  
perl -pi -e "s/Lebron James/LeBron James/g"   ./sdb.$date.csv  
perl -pi -e "s/Marcus T Thornton/Marcus Thornton/g"   ./sdb.$date.csv  
perl -pi -e "s/Michael Carter Williams/Michael Carter-Williams/g"   ./sdb.$date.csv  
perl -pi -e "s/Michael Kidd Gilchrist/Michael Kidd-Gilchrist/g"   ./sdb.$date.csv  
perl -pi -e "s/Maurice Williams/Mo Williams/g"   ./sdb.$date.csv  
perl -pi -e "s/Nene/Nene Hilario/g"   ./sdb.$date.csv  
perl -pi -e "s/OJ Mayo/O.J. Mayo/g"   ./sdb.$date.csv  
perl -pi -e "s/PJ Hairston/P.J. Hairston/g"   ./sdb.$date.csv  
perl -pi -e "s/PJ Tucker/P.J. Tucker/g"   ./sdb.$date.csv  
perl -pi -e "s/Perry Jones/Perry Jones III/g"   ./sdb.$date.csv  
perl -pi -e "s/RJ Hunter/R.J. Hunter/g"   ./sdb.$date.csv  
perl -pi -e "s/Rondae Hollis Jefferson/Rondae Hollis-Jefferson/g"   ./sdb.$date.csv  
perl -pi -e "s/Ryan J Anderson/Ryan Anderson/g"   ./sdb.$date.csv  
perl -pi -e "s/TJ McConnell/T.J. McConnell/g"   ./sdb.$date.csv  
perl -pi -e "s/TJ Warren/T.J. Warren/g"   ./sdb.$date.csv  
perl -pi -e "s/Timothy Hardaway/Tim Hardaway Jr./g"   ./sdb.$date.csv  
perl -pi -e "s/Tristan T Thompson/Tristan Thompson/g"   ./sdb.$date.csv  
perl -pi -e "s/Willie Cauley Stein/Willie Cauley-Stein/g"   ./sdb.$date.csv  
perl -pi -e 's/Lamarcus Aldridge/LaMarcus Aldridge/g' ./sdb.$date.csv
perl -pi -e 's/Luc Mbah A Moute/Luc Richard Mbah a Moute/g' ./sdb.$date.csv
perl -pi -e "s/Kyle Oquinn/Kyle O'Quinn/g" ./sdb.$date.csv
perl -pi -e 's/AJ Price/A.J. Price/g' ./sdb.$date.csv
perl -pi -e 's/Rj Hunter/R.J. Hunter/g' ./sdb.$date.csv
perl -pi -e 's/S Hawes/Spencer Hawes/g' ./sdb.$date.csv
perl -pi -e "s/Etwaun Moore/E'Twaun Moore/g" ./sdb.$date.csv
perl -pi -e "s/Louis Williams/Lou Williams/g" ./sdb.$date.csv
perl -pi -e 's/Zach Lavine/Zach LaVine/g' ./sdb.$date.csv

####
####
####
perl -pi -e "s/AJ Hammons/A.J. Hammons/g" ./sdb.$date.csv 
perl -pi -e "s/A Bradley/Avery Bradley/g" ./sdb.$date.csv 
perl -pi -e "s/A Gordon/Aaron Gordon/g" ./sdb.$date.csv 
perl -pi -e "s/Bryce Dejean Jones/Bryce Jones/g" ./sdb.$date.csv 
perl -pi -e "s/CJ Wilcox/C.J. Wilcox/g" ./sdb.$date.csv 
perl -pi -e "s/Caris Levert/Caris LeVert/g" ./sdb.$date.csv 
perl -pi -e "s/Dante Exum/Danté Exum/g" ./sdb.$date.csv 
perl -pi -e "s/Fred Vanvleet/Fred VanVleet/g" ./sdb.$date.csv 
perl -pi -e "s/J Ayres/Jeff Ayres/g" ./sdb.$date.csv 
perl -pi -e "s/James Ennis Iii/James Ennis/g" ./sdb.$date.csv 
perl -pi -e "s/John Lucas Iii/John Lucas III/g" ./sdb.$date.csv 
perl -pi -e "s/Nicolas Laprovittola/Nicolás Laprovittola/g" ./sdb.$date.csv 
perl -pi -e "s/Phil Pressey/Phil (Flip) Pressey/g" ./sdb.$date.csv 
perl -pi -e "s/Stephen Zimmerman/Stephen Zimmerman Jr./g" ./sdb.$date.csv 
perl -pi -e "s/Wade Baldwin/Wade Baldwin IV/g" ./sdb.$date.csv 
perl -pi -e "s/Jose Juan Barea,/J.J. Barea,/g" ./sdb.$date.csv
perl -pi -e "s/Juan Juan Jose Barea,/J.J. Barea,/g" ./sdb.$date.csv
perl -pi -e "s/Tim Hardaway Jr,/Tim Hardaway Jr.,/g" ./sdb.$date.csv
perl -pi -e "s/Deandre Bembry/DeAndre' Bembry/g" ./sdb.$date.csv
perl -pi -e "s/Juan Hernangomez/Juancho Hernangomez/g" ./sdb.$date.csv
perl -pi -e "s/O Johnson/Orlando Johnson/g" ./sdb.$date.csv 
perl -pi -e "s/Raulzinho Neto/Raul Neto/g" ./sdb.$date.csv 


####
####
###




perl -pi -e 's/, /,/g' ./sdb.$date.csv
perl -pi -e 's/ ,/,/g' ./sdb.$date.csv
perl -pi -e 's/,-,/,,/g' ./sdb.$date.csv
perl -pi -e 's/,-,/,,/g' ./sdb.$date.csv
mv ./sdb.$date.csv ./player/
done < dates


