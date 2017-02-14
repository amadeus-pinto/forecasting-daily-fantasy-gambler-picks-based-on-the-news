#Forecasting Daily Fantasy Gamblers' Picks Based on the News

## Introduction

In October of 2015, an employee of the daily fantasy (DF) gambling site DraftKings leveraged his site's user data to win $350,000 on a rival DF site, FanDuel, resulting in a huge scandal and allegations of insider trading. In a zero-sum game, knowledge of opponents' positions (the field's picks) ahead of market represents a serious advantage (or serious abuse if this information is applied by the same people setting the market). The expected value of a pick I, V(pick_I), is a product of the probability P of pick I's success and its associated payout A:
	V(pick_I) = sum_J P(S_JI)*A(S_J;w_I).

P is the probability of pick I's score J, S_JI, and is independent of gamblers' perceptions, and payout A depends on pick I's score and gamblers' collective valuation of I, where w_I represents the "market share" (also "weight" or "ownership") in pick_I. {w} is the quantity of interest here, and models projecting field ownerships ahead of the market are the goal of this project. 

Apart from the intrinsic neatness of explaining/predicting the decisions a collection of people make given incomplete information and perceived utility, knowledge of athlete market shares can potentially help one accurately project outcomes of entire fantasy contests themselves... Specifically, if one has a "good" estimate of the covariance matrix of athlete fantasy output, one can collect statistics from an ensemble of Monte-Carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted market. A basic application of such a simulation would be ranking the tickets by probability of profitability, etc.

##The Long and Short of DF Mechanics

"Fantasy owners" (the gamblers) submit one or multiple ticket(s) of athletes' names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site (a.k.a. the bookie - FanDuel, DraftKings, etc.) which takes a rake and pays out a subset of tickets as a function of ticket score, determined as a linear combination of ticket athletes' accumulated game stats after bets are locked. Broadly, there are two (very different) contest types: a "tournament" game pays out the top ~20%, with payout odds growing ~exponentially from 1:1 at the ~20th percentile line (a typical first place ticket's return is ~1000:1); a "cash" game pays out the top ~50% fixed 1:1 odds. Naturally, these payouts force fantasy owners to favor higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. This causes lower-mean/higher-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter. See [this](https://www.fanduel.com/nba-guide?t=rules) FanDuel tutorial for more (or less).

##Specifics

What causes gamblers to make the choices they make with the news they have, and how accurately can I predict the field of wagers in a given contest? 

I set out to answer these questions using scraped contest records of field ownerships in past FanDuel NBA contests (thanks to [@brainydfs](http://brainydfs.com/)), historic athlete performance data from <http://sportsdatabase.com/>, the news leading up to the particular contest (e.g., "industry" fantasy output projections from <http://basketballmonster.com>, <http://fantasycrunchers.com>, and others, themselves the output of decidedly mediocre regression models, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions. (These and others are detailed below.) I trained and validated ~400 player-centered models (estimators include Ridge, Lasso, Random Forest, and gradient-boosted regressors) on over 700 "tournament" contests from the 2016 season and the first two months of the 2017 season, holding out January 2017 slates for model testing.

## Results
a. training/validation models
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/mu.sig.Lasso.gpp.png )
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/sig.ratio.Lasso.gpp.png )
  
|name|mean|std|cv_score|train_score|test_score|
|---|---|---|---|---|---|---|
|Russell Westbrook|49.5|20.15|9.04|8.14|7.56|
|James Harden|45.22|23.94|10.57|11.11|9.11|
|Kevin Durant|42.23|23.19|10.9|9.88|8.41|
|LeBron James|41.97|23.53|11.83|10.66|9.21|
|Kawhi Leonard|41.37|25.48|10.83|11.74|7.72|
|Stephen Curry|40.24|22.59|10.43|9.53|7.8|
|Anthony Davis|37.68|22.3|11.15|11.15|9.43|
|Blake Griffin|37.61|25.23|10.31|11.52|8.41|
|Damian Lillard|37.33|24.86|9.48|7.89|7.99|
|Jimmy Butler|36.19|22.47|9.17|15.65|7.45|
|Giannis Antetokounmpo|35.35|22.95|10.12|13.83|8.19|
|Draymond Green|34.39|22.28|10.8|10.42|9.09|
|DeMar DeRozan|34.19|24.89|11.36|11.81|9.46|
|C.J. McCollum|33.88|23.32|9.92|10.01|8.72|
|Chris Paul|33.79|24.77|11.76|10.56|7.99|
|DeMarcus Cousins|33.33|21.54|10.17|10.21|7.02|
|Kristaps Porzingis|32.98|20.91|12.11|9.17|7.38|
|Gordon Hayward|32.92|24.52|9.13|9.06|6.92|
|Klay Thompson|32.69|18.24|9.69|9.45|7.78|
|Kyle Lowry|31.99|23.55|8.04|9.62|6.59|
|Carmelo Anthony|31.7|25.05|13.58|9.96|7.58|
|Paul George|31.32|22.45|13.68|9.1|11.63|
|John Wall|29.64|20.28|8.53|7.89|6.02|
|Julius Randle|29.01|23.68|11.71|8.55|9.74|
|Paul Millsap|28.97|23.04|10.42|10.44|7.31|
|Rajon Rondo|28.3|19.58|11.75|10.05|9.63|
|Harrison Barnes|28.01|18.66|8.36|7.49|6.76|
|Eric Bledsoe|27.92|21.65|9.66|9.02|7.34|
|Andrew Wiggins|27.76|20.35|9.14|8.47|7.1|
|Kyrie Irving|27.45|18.39|9.53|9.27|7.9|
|Kevin Love|27.11|17.16|9.31|8.24|7.17|
|Isaiah Thomas|27.01|21.75|8.21|10.5|6.0|
|Danilo Gallinari|26.92|21.31|9.51|12.39|7.48|
|Rudy Gay|26.89|21.91|10.83|11.96|7.71|
|Chris Bosh|26.79|21.79|8.05|8.56|4.74|
|LaMarcus Aldridge|26.64|22.28|11.15|10.22|9.05|
|Devin Booker|25.45|19.65|9.69|7.32|7.13|
|Thaddeus Young|24.78|18.89|9.81|11.6|7.59|
|Victor Oladipo|24.75|18.88|9.19|8.74|7.19|
|Khris Middleton|24.73|16.92|9.74|7.29|7.48|
|Kemba Walker|24.52|19.64|7.39|10.02|5.55|
|Will Barton|24.17|19.54|10.75|8.07|8.91|
|Nicolas Batum|24.17|16.75|11.08|7.77|6.5|
|Dwyane Wade|23.81|17.76|10.57|11.29|8.34|
|Derrick Favors|23.72|21.14|10.69|11.44|9.23|
|Tim Frazier|22.58|18.73|12.11|9.87|8.76|
|Serge Ibaka|22.37|16.21|8.53|8.03|6.99|
|Otto Porter|22.21|18.36|9.88|11.26|7.63|
|Al-Farouq Aminu|22.11|20.29|9.59|9.29|8.04|
|Jabari Parker|22.0|19.15|9.65|9.0|7.85|
|Joel Embiid|21.78|18.35|13.86|9.91|7.13|
|Avery Bradley|21.67|19.92|7.97|8.55|6.51|
|Wilson Chandler|21.64|20.28|9.57|19.6|5.0|
|Jae Crowder|21.57|17.99|11.12|13.26|8.35|
|Brandon Knight|21.41|18.4|8.9|11.47|7.59|
|Tobias Harris|21.17|17.2|7.82|8.67|3.81|
|Chandler Parsons|21.05|23.22|13.11|13.89|8.33|
|Bradley Beal|20.9|14.94|9.25|6.35|7.35|
|Hassan Whiteside|20.81|16.11|9.1|10.34|4.8|
|Dirk Nowitzki|20.69|18.67|11.33|10.86|8.57|
|Reggie Jackson|20.66|18.18|9.44|6.92|7.04|
|Rodney Hood|20.56|17.25|10.25|9.05|8.41|
|Karl-Anthony Towns|20.4|15.84|8.75|7.26|6.8|
|Jared Sullinger|20.31|17.33|5.99|10.18|2.63|
|Zach LaVine|20.27|16.72|8.07|7.92|6.16|
|Lou Williams|20.18|17.05|8.44|9.95|6.71|
|Goran Dragic|20.16|16.54|8.8|9.8|6.64|
|Andre Drummond|20.04|15.53|8.0|8.45|4.78|
|Kentavious Caldwell-Pope|19.98|17.09|8.1|6.76|6.74|
|T.J. Warren|19.93|21.48|9.89|9.53|5.1|
|Kenneth Faried|19.6|19.09|10.14|9.61|8.31|
|Evan Fournier|19.58|18.15|11.87|11.59|9.73|
|Robert Covington|19.36|16.61|9.33|8.71|6.87|
|Omri Casspi|19.32|16.43|9.28|10.34|7.18|
|Nerlens Noel|19.22|19.32|10.56|8.55|8.42|
|J.J. Redick|18.92|15.54|7.78|9.13|6.75|
|Mike Conley|18.92|17.24|9.17|10.37|7.14|
|Tyreke Evans|18.78|17.5|11.75|13.88|6.25|
|Pau Gasol|18.74|16.41|8.87|10.56|7.03|
|DeAndre Jordan|18.68|16.16|9.16|7.28|7.69|
|Trevor Ariza|18.59|15.06|7.06|7.24|6.09|
|Michael Carter-Williams|18.53|15.43|8.4|6.9|6.22|
|Marcus Morris|18.5|16.49|7.52|8.52|6.01|
|Jeff Teague|18.48|16.2|9.07|9.98|7.86|
|Derrick Rose|18.14|15.85|8.2|8.33|6.35|
|Kent Bazemore|17.82|16.6|8.96|7.04|6.59|
|Monta Ellis|17.77|15.12|8.76|8.12|7.14|
|Ricky Rubio|17.77|15.92|7.94|7.09|6.79|
|Ryan Anderson|17.68|14.97|8.81|10.55|5.77|
|Emmanuel Mudiay|17.48|16.29|7.25|8.28|6.25|
|Markieff Morris|17.44|14.68|8.15|12.02|6.48|
|Gorgui Dieng|17.22|16.42|9.03|8.15|7.59|
|Zach Randolph|17.04|15.67|8.36|7.55|6.7|
|Sergio Rodriguez|16.72|12.69|4.5|8.12|0.24|
|Taj Gibson|16.6|14.29|8.47|7.66|5.74|
|Shelvin Mack|16.49|16.64|8.84|8.85|7.01|
|Wesley Matthews|16.15|14.93|7.57|5.89|6.4|
|Sean Kilpatrick|16.06|18.16|7.43|17.78|3.08|
|Eric Gordon|15.99|13.21|6.3|4.89|5.12|
|Nikola Mirotic|15.95|15.03|6.92|12.18|5.58|
|Myles Turner|15.72|14.95|10.55|13.19|8.37|
|Jamal Crawford|15.64|15.25|8.85|5.2|7.1|
|Jordan Clarkson|15.38|14.98|8.51|7.11|6.7|
|Nikola Jokic|15.35|16.74|9.24|7.21|6.96|
|Rudy Gobert|15.16|16.48|7.89|9.07|5.96|
|Michael Kidd-Gilchrist|15.15|15.58|8.9|8.87|3.26|
|Jrue Holiday|15.09|13.46|6.17|8.18|4.27|
|Aaron Gordon|14.83|15.17|8.01|4.7|6.33|
|Luol Deng|14.82|15.32|9.15|6.46|6.99|
|Marc Gasol|14.6|13.37|9.12|12.23|7.3|
|Tristan Thompson|14.46|10.95|6.04|5.94|4.84|
|Jarrett Jack|14.34|11.72|9.0|10.31|2.51|
|Deron Williams|14.16|14.28|9.88|8.37|8.56|
|Enes Kanter|14.08|12.35|7.4|6.05|6.16|
|Andre Iguodala|14.03|15.37|8.19|7.34|7.16|
|J.R. Smith|14.02|11.92|6.15|10.39|4.49|
|Darren Collison|13.98|15.38|8.49|7.35|7.24|
|Marvin Williams|13.9|14.53|8.61|9.38|7.0|
|D'Angelo Russell|13.81|16.42|8.84|5.8|7.38|
|Matt Barnes|13.7|13.81|8.6|6.19|7.17|
|Alec Burks|13.36|11.57|5.18|5.99|2.95|
|Patrick Beverley|13.35|11.72|6.55|6.25|5.36|
|Marcin Gortat|13.26|12.64|8.59|5.21|6.47|
|Trevor Booker|13.22|15.66|6.47|11.43|4.36|
|Brook Lopez|13.19|14.36|7.41|9.19|5.69|
|Jeff Green|12.84|12.96|8.54|9.11|6.98|
|Archie Goodwin|12.83|14.57|10.04|7.05|6.3|
|Elfrid Payton|12.69|12.61|7.08|7.74|5.05|
|Kobe Bryant|12.64|12.56|8.47|4.18|6.57|
|George Hill|12.52|14.42|7.22|9.14|5.78|
|Willie Cauley-Stein|12.52|15.34|8.16|7.53|5.77|
|Al Horford|12.28|10.96|5.69|5.06|3.43|
|Dwight Howard|12.27|10.95|6.37|5.48|4.88|
|Evan Turner|12.19|14.86|7.85|7.0|6.55|
|Lance Stephenson|12.15|14.17|8.14|6.53|4.05|
|Jahlil Okafor|12.11|11.01|6.6|11.22|3.98|
|Jon Leuer|11.92|11.44|6.42|5.61|5.34|
|Ersan Ilyasova|11.89|11.6|7.47|6.05|5.48|
|Dennis Schroder|11.8|13.0|7.24|7.0|5.11|
|Thomas Robinson|11.76|15.66|8.76|5.77|5.27|
|Mason Plumlee|11.72|11.81|6.4|6.94|5.07|
|P.J. Tucker|11.7|14.71|6.82|11.65|5.23|
|Clint Capela|11.66|11.1|6.43|7.54|5.63|
|Michael Beasley|11.65|13.74|7.89|3.99|6.23|
|Ed Davis|11.6|13.21|7.37|6.71|6.0|
|Jonas Valanciunas|11.58|10.69|6.52|4.47|5.35|
|Tyler Johnson|11.57|11.14|9.1|8.96|8.27|
|Josh Richardson|11.53|11.17|8.97|7.74|4.26|
|Mo Williams|11.39|11.84|6.36|4.85|3.78|
|Arron Afflalo|11.37|11.32|5.4|156.47|3.65|
|Montrezl Harrell|11.24|12.13|6.11|24.69|3.86|
|O.J. Mayo|11.18|11.36|8.39|3.58|6.37|
|Nikola Vucevic|11.18|10.51|5.72|8.2|3.51|
|Seth Curry|11.17|13.15|7.83|6.46|3.93|
|Bojan Bogdanovic|11.14|12.89|7.27|11.14|5.24|
|Tony Parker|10.82|10.26|6.01|5.61|4.86|
|Alex Len|10.78|11.79|6.56|5.26|4.37|
|Justise Winslow|10.77|12.72|8.17|6.57|6.35|
|DeMarre Carroll|10.65|12.37|9.36|5.81|7.0|
|Greg Monroe|10.56|9.0|5.35|3.54|4.33|
|Jerryd Bayless|10.47|12.68|5.84|6.61|4.25|
|J.J. Hickson|10.37|12.42|7.28|10.67|1.9|
|Toney Douglas|10.36|10.38|8.64|10.18|2.48|
|Jordan Hamilton|10.25|8.03|5.18|96.71|0.01|
|Jeremy Lin|10.19|11.39|5.57|7.66|4.11|

  
b. models in hold-out
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/FIGS/jan.RandomForestRegressor.gpp.png)
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/FIGS/jan.mean.gpp.png)

c. models of tournament means
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/FIGS/field.Lasso.gpp.png)

  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/FIGS/field.mean.gpp.png)
  Substituting training set mean ownerships in the tournament mean equation, predicted means are wildly unrealistic.  

d. potential for stacking
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/RESIDUALS/gpp.val.corrmat.png )
##Model factors
  Follow the links below to view pair distributions of dependent and independent variables of LeBron James observations. Please bear in mind that different variables are important for different athletes.  (**: interesting!) 


1. ["industry" valuation](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/value.png)
  * proj_fc: fantasycrunchers fantasy score projection
  * proj_mo: basketballmonster fantasy score projection
  * v_fc: fantasycrunchers value  (projection /salary)                      
  * v_mo: basketballmonster value (projection /salary)                      

2. [vegas quantities](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/vegas.png )
  * 	line: sportsdatabase matchup line                       
  * 	total: sportsdatabase matchup total 

3. [momentum](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/momentum.png) (rolling mean - abbreviated below as "rm" - of previous Y=1-,5-,10-game windows; computed with sportsdatabase queries) - 
  * 	rm.Y.score: recent score        
  * 	rm.Y.salary: recent salary        
  * 	rm.Y.value : recent value
  * 	rm.Y.val_exceeds.X: recent value has exceeded X=4,5,6
  * 	rm.Y.opp_total_score: recent opponent total score
  * 	rm.Y.opp_off_score: recent opponent offensive score
  * 	rm.Y.opp_def_score: recent opponent defensive score
  * 	rm.Y.team_total_score: recent team total score   
  * 	rm.Y.team_def_score: recent team defensive score   
  * 	rm.Y.team_off_score: recent team offensive score   

4. [value over replacement](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/environ.png) (standard score within X=salary,position class) - 
  * 	z.X.proj_fc: z-score of fantasycruncher projections within class X
  * 	z.X.proj_mo: z-score of basketballmonster projections within class X          
  * 	z.X.v_fc: z-score of fantasycruncher value within class X 
  * 	z.X.v_mo: z-score of basketballmonster value within class X       

5. [game mechanics](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/mechs.png) - 
  * 	max_user_frac: maximum tickets per user / total contest tickets
  * 	slate_size: number of NBA games in slate 
  * 	log.slate_size: log( number of NBA games in slate)

6. [**fictituous gambler portfolios](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/PLAYER/fict.png) ( X=worldview,Y=max overlap w/previous solution,Z=number of tickets  ) -
   This type of feature is arguably the most interesting, and without a doubt among the most predictive. It is constructed as follows:
   For each contest, initialize a set of fictitious gamblers, each with a specified "worldview", risk-reward tolerance, and number of bets. For each fictitious gambler, solve the integer programming problem of constructing a number of unique bets (tickets), each maximizing projected fantasy points (enumerated by worldview) subject to feasibility constraints (FanDuel's salary cap, position requirements, etc.) and risk-reward tolerance constraints (maximum number of athelete overlaps with previous integer programming solution in fictitous gambler's portfolio). For each athlete in the slate, construct a vector of fictitious holdings, each entry the proportions of each fictitious portfolio in that athlete. 
  * 	gpp.fict.proj_X.Y.Z: X=(fantasycrunchers,basketballmonster,their average),Y=(2,4,6); Z=25 

