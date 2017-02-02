#!/bin/bash
season=$1
echo season=$season

todaydate=`date +%Y%m%d`
echo $todaydate 



curl "http://sportsdatabase.com/nba/query?output=default&sdql=season%2C+date%2C+day%2C+site%2C+time+of+game%2C+time+zone%2C+game+number%2C+line%2C+total%2Cmatchup+losses%2C+matchup+wins%2Cteam+as+Team%2C+o%3Ateam+as+Opp%2C+assists%2Co%3Aassists+as+o_assists%2C+blocks%2Co%3Ablocks+as+o_blocks%2C+defensive+rebounds%2C+o%3Adefensive+rebounds+as+o_defensive+rebounds%2C+offensive+rebounds%2C+o%3Aoffensive+rebounds+as+o_offensive+rebounds%2C+rebounds%2Co%3Arebounds+as+o_rebounds%2C+steals%2Co%3Asteals+as+o_steals%2C+points%2C+o%3Apoints+as+o_points%2C+three+pointers+made%2Co%3Athree+pointers+made+as+o_three+pointers+made%2C+turnovers%2Co%3Aturnovers+as+o_turnovers+%2C+%28field+goals+attempted%2B0.4*free+throws+attempted-1.07*%28offensive+rebounds%2F%28offensive+rebounds%2Bo%3Adefensive+rebounds%29%29*%28field+goals+attempted-field+goals+made%29+%2Bturnovers+%29+as+poss+%2C+%28o%3Afield+goals+attempted%2B0.4*o%3Afree+throws+attempted-1.07*%28o%3Aoffensive+rebounds%2F%28o%3Aoffensive+rebounds%2Bdefensive+rebounds%29%29*%28o%3Afield+goals+attempted-o%3Afield+goals+made%29+%2Bo%3Aturnovers+%29+as+o_poss+%2C+%28%28o%3Afield+goals+attempted%2B0.4*o%3Afree+throws+attempted-1.07*%28o%3Aoffensive+rebounds%2F%28o%3Aoffensive+rebounds%2Bdefensive+rebounds%29%29*%28o%3Afield+goals+attempted-o%3Afield+goals+made%29+%2Bo%3Aturnovers+%29%2B+%28field+goals+attempted%2B0.4*free+throws+attempted-1.07*%28offensive+rebounds%2F%28offensive+rebounds%2Bo%3Adefensive+rebounds%29%29*%28field+goals+attempted-field+goals+made%29+%2Bturnovers+%29++%29%2F%282*minutes%29+as+mu_poss%2Cminutes+as+team_minutes+%40+season+%3D+$season+and+date+<+$todaydate&submit=++S+D+Q+L+%21++" | sed -E 's/<[^>]*>//g' | perl -pi -e 's/\n/,/g' | perl -pi -e 's/,,,,,/\n/g' | perl -pi -e 's/,,,/,/g' | sed '/Game/d' | sed '/,e-mail/d'  | grep -A 10000 ',,season, date, day, site, time of game, time zone, game number, line, total,matchup losses, matchup wins,Team,Opp, assists,o_assists, blocks,o_blocks, defensive rebounds,o_defensive rebounds, offensive rebounds,o_offensive rebounds, rebounds,o_rebounds, steals,o_steals, points,o_points, three pointers made,o_three pointers made, turnovers,o_turnovers ,poss ,o_poss ,mu_poss,team_minutes' | perl -pi -e 's/,,/\n/g' | sed '/^$/d' |  perl -pi -e 's/\[/"\[/g' | perl -pi -e 's/\]/\]"/g' > games.$season.csv



echo wrote games.$season.csv!
perl -pi -e 's/Bucks/MIL/g'                  ./games.$season.csv        
perl -pi -e 's/Bulls/CHI/g'                  ./games.$season.csv 
perl -pi -e 's/Cavaliers/CLE/g'              ./games.$season.csv      
perl -pi -e 's/Celtics/BOS/g'                ./games.$season.csv    
perl -pi -e 's/Clippers/LAC/g'               ./games.$season.csv     
perl -pi -e 's/Grizzlies/MEM/g'              ./games.$season.csv      
perl -pi -e 's/Hawks/ATL/g'                  ./games.$season.csv  
perl -pi -e 's/Heat/MIA/g'                   ./games.$season.csv 
perl -pi -e 's/Hornets/CHA/g'                ./games.$season.csv    
perl -pi -e 's/Jazz/UTA/g'                   ./games.$season.csv 
perl -pi -e 's/Kings/SAC/g'                  ./games.$season.csv  
perl -pi -e 's/Knicks/NYK/g'                 ./games.$season.csv   
perl -pi -e 's/Lakers/LAL/g'                 ./games.$season.csv   
perl -pi -e 's/Magic/ORL/g'                  ./games.$season.csv  
perl -pi -e 's/Mavericks/DAL/g'              ./games.$season.csv      
perl -pi -e 's/Nets/BKN/g'                   ./games.$season.csv 
perl -pi -e 's/Nuggets/DEN/g'                ./games.$season.csv    
perl -pi -e 's/Pacers/IND/g'                 ./games.$season.csv   
perl -pi -e 's/Pelicans/NOR/g'               ./games.$season.csv     
perl -pi -e 's/Pistons/DET/g'                ./games.$season.csv    
perl -pi -e 's/Raptors/TOR/g'                ./games.$season.csv    
perl -pi -e 's/Rockets/HOU/g'                ./games.$season.csv    
perl -pi -e 's/Seventysixers/PHI/g'          ./games.$season.csv          
perl -pi -e 's/Spurs/SAS/g'                  ./games.$season.csv  
perl -pi -e 's/Suns/PHO/g'                   ./games.$season.csv 
perl -pi -e 's/Thunder/OKC/g'                ./games.$season.csv    
perl -pi -e 's/Timberwolves/MIN/g'           ./games.$season.csv         
perl -pi -e 's/Trailblazers/POR/g'           ./games.$season.csv         
perl -pi -e 's/Warriors/GSW/g'               ./games.$season.csv     
perl -pi -e 's/Wizards/WAS/g'                ./games.$season.csv    

perl -pi -e 's/, /,/g' ./games.$season.csv
perl -pi -e 's/ ,/,/g' ./games.$season.csv
perl -pi -e 's/,-,/,,/g' ./games.$season.csv
perl -pi -e 's/,-,/,,/g' ./games.$season.csv
perl -pi -e 's/,-$/,/g' ./games.$season.csv
echo "wrote games.$season.csv. putting in ./season/"
mv ./games.$season.csv ./season/
