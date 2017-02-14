#Forecasting Daily Fantasy Gamblers' Picks Based on the News

## Introduction

In October of 2015, an employee of the daily fantasy (DF) gambling site DraftKings leveraged his site's user data to win $350,000 on a rival DF site, FanDuel, resulting in [allegations of insider trading, and renewed concern for consumer protection against exploitation by an unregulated industry](https://www.nytimes.com/2015/10/06/sports/fanduel-draftkings-fantasy-employees-bet-rivals.html?_r=0). In a zero-sum game, knowledge of opponents' positions (the field's picks) ahead of market represents a serious advantage (or serious abuse when applied by the same people making the market). The expected value of a pick I, ```V(pick_I)```, is a product of the probability ```P``` of pick I's success and its associated payout ```p```:

	V(pick_I) = sum_J P(S_JI)*p(S_JI;w_I).

```P(S_JI)``` is the probability of pick I's score J,``` S_JI```, and is independent of gamblers' perceptions, whereas payout ```p``` depends on pick I's score and gamblers' collective valuation of I, where ```w_I``` represents the "market share" (also "weight" or "ownership") in pick I. ```{w_I}``` is the quantity of interest here, and models projecting field ownerships ahead of market are the goal of this project. 

Apart from the intrinsic neatness of explaining/predicting the decisions a collection of people make given incomplete information and perceived utility, knowledge of athlete market shares can potentially help one accurately project outcomes of entire fantasy contests themselves... Specifically, if one has a "good" estimate of the covariance matrix of athlete fantasy output, one can collect statistics from an ensemble of Monte-Carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted market. A basic application of such a simulation would be ranking the tickets by probability of profitability, etc.

##The Long and Short of DF Mechanics

"Fantasy owners" (the gamblers) submit one or multiple ticket(s) of athletes' names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site (a.k.a. the bookie - FanDuel, DraftKings, etc.) which takes a rake and pays out a subset of tickets as a function of ticket score, determined as a linear combination of ticket athletes' accumulated game stats after bets are locked. Broadly, there are two (very different) contest types: a "tournament" game pays out the top ~20%, with payout odds growing ~exponentially from 1:1 at the ~20th percentile line (a typical first place ticket's return is ~1000:1); a "cash" game pays out the top ~50% fixed 1:1 odds. Naturally, these payouts force fantasy owners to favor higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. This causes lower-mean/higher-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter. See [this](https://www.fanduel.com/nba-guide?t=rules) FanDuel tutorial for more (or less).

##Specifics

What causes gamblers to make the choices they make with the news they have, and how accurately can I predict the field of wagers in a given contest? 

I set out to answer these questions using scraped contest records of field ownerships in past FanDuel NBA contests (thanks to [@brainydfs](http://brainydfs.com/)), historic athlete performance data from [sportsdatabase.com](http://sportsdatabase.com/), the news leading up to the particular contest (e.g., "industry" fantasy output projections from [basketballmonster.com](http://basketballmonster.com), [fantasycrunchers.com](http://fantasycrunchers.com), and others, themselves the output of decidedly mediocre regression models, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions. (These and others are detailed below.) I trained and validated ~400 player-centered models (estimators include ridge, lasso, random forest, and gradient-boosted regressors) on over 700 "tournament" contests from the 2016 season and the first two months of the 2017 season, holding out January 2017 slates for model testing.

## Results
a. training/validation models
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/mu.sig.Lasso.gpp.png )
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/sig.ratio.Lasso.gpp.png )

|name|mean|std|rmse(train)|rmse(val)|R2|
|---|---|---|---|---|---|
|Russell Westbrook|49.5|20.15|8.14|9.04|0.8|
|James Harden|45.22|23.94|11.11|10.57|0.81|
|Kevin Durant|42.23|23.19|9.88|10.9|0.78|
|LeBron James|41.97|23.53|10.66|11.83|0.75|
|Kawhi Leonard|41.37|25.48|11.74|10.83|0.82|
|Stephen Curry|40.24|22.59|9.53|10.43|0.79|
|Anthony Davis|37.68|22.3|11.15|11.15|0.75|
|Blake Griffin|37.61|25.23|11.52|10.31|0.83|
|Damian Lillard|37.33|24.86|7.89|9.48|0.85|
|Jimmy Butler|36.19|22.47|15.65|9.17|0.83|
|Giannis Antetokounmpo|35.35|22.95|13.83|10.12|0.81|
|Draymond Green|34.39|22.28|10.42|10.8|0.77|
|DeMar DeRozan|34.19|24.89|11.81|11.36|0.79|
|C.J. McCollum|33.88|23.32|10.01|9.92|0.82|
|Chris Paul|33.79|24.77|10.56|11.76|0.77|
|DeMarcus Cousins|33.33|21.54|10.21|10.17|0.78|
|Kristaps Porzingis|32.98|20.91|9.17|12.11|0.66|
|Gordon Hayward|32.92|24.52|9.06|9.13|0.86|
|Klay Thompson|32.69|18.24|9.45|9.69|0.72|
|Kyle Lowry|31.99|23.55|9.62|8.04|0.88|
|Carmelo Anthony|31.7|25.05|9.96|13.58|0.71|
|Paul George|31.32|22.45|9.1|13.68|0.63|
|John Wall|29.64|20.28|7.89|8.53|0.82|
|Julius Randle|29.01|23.68|8.55|11.71|0.76|
|Paul Millsap|28.97|23.04|10.44|10.42|0.8|
|Rajon Rondo|28.3|19.58|10.05|11.75|0.64|
|Harrison Barnes|28.01|18.66|7.49|8.36|0.8|
|Eric Bledsoe|27.92|21.65|9.02|9.66|0.8|
|Andrew Wiggins|27.76|20.35|8.47|9.14|0.8|
|Kyrie Irving|27.45|18.39|9.27|9.53|0.73|
|Kevin Love|27.11|17.16|8.24|9.31|0.71|
|Isaiah Thomas|27.01|21.75|10.5|8.21|0.86|
|Danilo Gallinari|26.92|21.31|12.39|9.51|0.8|
|Rudy Gay|26.89|21.91|11.96|10.83|0.76|
|Chris Bosh|26.79|21.79|8.56|8.05|0.86|
|LaMarcus Aldridge|26.64|22.28|10.22|11.15|0.75|
|Devin Booker|25.45|19.65|7.32|9.69|0.76|
|Thaddeus Young|24.78|18.89|11.6|9.81|0.73|
|Victor Oladipo|24.75|18.88|8.74|9.19|0.76|
|Khris Middleton|24.73|16.92|7.29|9.74|0.67|
|Kemba Walker|24.52|19.64|10.02|7.39|0.86|
|Nicolas Batum|24.17|16.75|7.77|11.08|0.56|
|Will Barton|24.17|19.54|8.07|10.75|0.7|
|Dwyane Wade|23.81|17.76|11.29|10.57|0.65|
|Derrick Favors|23.72|21.14|11.44|10.69|0.74|
|Tim Frazier|22.58|18.73|9.87|12.11|0.58|
|Serge Ibaka|22.37|16.21|8.03|8.53|0.72|
|Otto Porter|22.21|18.36|11.26|9.88|0.71|
|Al-Farouq Aminu|22.11|20.29|9.29|9.59|0.78|
|Jabari Parker|22.0|19.15|9.0|9.65|0.75|
|Joel Embiid|21.78|18.35|9.91|13.86|0.43|
|Avery Bradley|21.67|19.92|8.55|7.97|0.84|
|Wilson Chandler|21.64|20.28|19.6|9.57|0.78|
|Jae Crowder|21.57|17.99|13.26|11.12|0.62|
|Brandon Knight|21.41|18.4|11.47|8.9|0.77|
|Tobias Harris|21.17|17.2|8.67|7.82|0.79|
|Chandler Parsons|21.05|23.22|13.89|13.11|0.68|
|Bradley Beal|20.9|14.94|6.35|9.25|0.62|
|Hassan Whiteside|20.81|16.11|10.34|9.1|0.68|
|Dirk Nowitzki|20.69|18.67|10.86|11.33|0.63|
|Reggie Jackson|20.66|18.18|6.92|9.44|0.73|
|Rodney Hood|20.56|17.25|9.05|10.25|0.65|
|Karl-Anthony Towns|20.4|15.84|7.26|8.75|0.69|
|Jared Sullinger|20.31|17.33|10.18|5.99|0.88|
|Zach LaVine|20.27|16.72|7.92|8.07|0.77|
|Lou Williams|20.18|17.05|9.95|8.44|0.75|
|Goran Dragic|20.16|16.54|9.8|8.8|0.72|
|Andre Drummond|20.04|15.53|8.45|8.0|0.73|
|Kentavious Caldwell-Pope|19.98|17.09|6.76|8.1|0.78|
|T.J. Warren|19.93|21.48|9.53|9.89|0.79|
|Kenneth Faried|19.6|19.09|9.61|10.14|0.72|
|Evan Fournier|19.58|18.15|11.59|11.87|0.57|
|Robert Covington|19.36|16.61|8.71|9.33|0.68|
|Omri Casspi|19.32|16.43|10.34|9.28|0.68|
|Nerlens Noel|19.22|19.32|8.55|10.56|0.7|
|J.J. Redick|18.92|15.54|9.13|7.78|0.75|
|Mike Conley|18.92|17.24|10.37|9.17|0.72|
|Tyreke Evans|18.78|17.5|13.88|11.75|0.55|
|Pau Gasol|18.74|16.41|10.56|8.87|0.71|
|DeAndre Jordan|18.68|16.16|7.28|9.16|0.68|
|Trevor Ariza|18.59|15.06|7.24|7.06|0.78|
|Michael Carter-Williams|18.53|15.43|6.9|8.4|0.7|
|Marcus Morris|18.5|16.49|8.52|7.52|0.79|
|Jeff Teague|18.48|16.2|9.98|9.07|0.69|
|Derrick Rose|18.14|15.85|8.33|8.2|0.73|
|Kent Bazemore|17.82|16.6|7.04|8.96|0.71|
|Ricky Rubio|17.77|15.92|7.09|7.94|0.75|
|Monta Ellis|17.77|15.12|8.12|8.76|0.66|
|Ryan Anderson|17.68|14.97|10.55|8.81|0.65|
|Emmanuel Mudiay|17.48|16.29|8.28|7.25|0.8|
|Markieff Morris|17.44|14.68|12.02|8.15|0.69|
|Gorgui Dieng|17.22|16.42|8.15|9.03|0.7|
|Zach Randolph|17.04|15.67|7.55|8.36|0.72|
|Sergio Rodriguez|16.72|12.69|8.12|4.5|0.87|
|Taj Gibson|16.6|14.29|7.66|8.47|0.65|
|Shelvin Mack|16.49|16.64|8.85|8.84|0.72|
|Wesley Matthews|16.15|14.93|5.89|7.57|0.74|
|Sean Kilpatrick|16.06|18.16|17.78|7.43|0.83|
|Eric Gordon|15.99|13.21|4.89|6.3|0.77|
|Nikola Mirotic|15.95|15.03|12.18|6.92|0.79|
|Myles Turner|15.72|14.95|13.19|10.55|0.5|
|Jamal Crawford|15.64|15.25|5.2|8.85|0.66|
|Jordan Clarkson|15.38|14.98|7.11|8.51|0.68|
|Nikola Jokic|15.35|16.74|7.21|9.24|0.7|
|Rudy Gobert|15.16|16.48|9.07|7.89|0.77|
|Michael Kidd-Gilchrist|15.15|15.58|8.87|8.9|0.67|
|Jrue Holiday|15.09|13.46|8.18|6.17|0.79|
|Aaron Gordon|14.83|15.17|4.7|8.01|0.72|
|Luol Deng|14.82|15.32|6.46|9.15|0.64|
|Marc Gasol|14.6|13.37|12.23|9.12|0.53|
|Tristan Thompson|14.46|10.95|5.94|6.04|0.7|
|Jarrett Jack|14.34|11.72|10.31|9.0|0.41|
|Deron Williams|14.16|14.28|8.37|9.88|0.52|
|Enes Kanter|14.08|12.35|6.05|7.4|0.64|
|Andre Iguodala|14.03|15.37|7.34|8.19|0.72|
|J.R. Smith|14.02|11.92|10.39|6.15|0.73|
|Darren Collison|13.98|15.38|7.35|8.49|0.7|
|Marvin Williams|13.9|14.53|9.38|8.61|0.65|
|D'Angelo Russell|13.81|16.42|5.8|8.84|0.71|
|Matt Barnes|13.7|13.81|6.19|8.6|0.61|
|Alec Burks|13.36|11.57|5.99|5.18|0.8|
|Patrick Beverley|13.35|11.72|6.25|6.55|0.69|
|Marcin Gortat|13.26|12.64|5.21|8.59|0.54|
|Trevor Booker|13.22|15.66|11.43|6.47|0.83|
|Brook Lopez|13.19|14.36|9.19|7.41|0.73|
|Jeff Green|12.84|12.96|9.11|8.54|0.57|
|Archie Goodwin|12.83|14.57|7.05|10.04|0.53|
|Elfrid Payton|12.69|12.61|7.74|7.08|0.68|
|Kobe Bryant|12.64|12.56|4.18|8.47|0.55|
|George Hill|12.52|14.42|9.14|7.22|0.75|
|Willie Cauley-Stein|12.52|15.34|7.53|8.16|0.72|
|Al Horford|12.28|10.96|5.06|5.69|0.73|
|Dwight Howard|12.27|10.95|5.48|6.37|0.66|
|Evan Turner|12.19|14.86|7.0|7.85|0.72|
|Lance Stephenson|12.15|14.17|6.53|8.14|0.67|
|Jahlil Okafor|12.11|11.01|11.22|6.6|0.64|
|Jon Leuer|11.92|11.44|5.61|6.42|0.69|
|Ersan Ilyasova|11.89|11.6|6.05|7.47|0.59|
|Dennis Schroder|11.8|13.0|7.0|7.24|0.69|
|Thomas Robinson|11.76|15.66|5.77|8.76|0.69|
|Mason Plumlee|11.72|11.81|6.94|6.4|0.71|
|P.J. Tucker|11.7|14.71|11.65|6.82|0.79|
|Clint Capela|11.66|11.1|7.54|6.43|0.66|
|Michael Beasley|11.65|13.74|3.99|7.89|0.67|
|Ed Davis|11.6|13.21|6.71|7.37|0.69|
|Jonas Valanciunas|11.58|10.69|4.47|6.52|0.63|
|Tyler Johnson|11.57|11.14|8.96|9.1|0.33|
|Josh Richardson|11.53|11.17|7.74|8.97|0.36|
|Mo Williams|11.39|11.84|4.85|6.36|0.71|
|Arron Afflalo|11.37|11.32|156.47|5.4|0.77|
|Montrezl Harrell|11.24|12.13|24.69|6.11|0.75|
|O.J. Mayo|11.18|11.36|3.58|8.39|0.45|
|Nikola Vucevic|11.18|10.51|8.2|5.72|0.7|
|Seth Curry|11.17|13.15|6.46|7.83|0.65|
|Bojan Bogdanovic|11.14|12.89|11.14|7.27|0.68|
|Tony Parker|10.82|10.26|5.61|6.01|0.66|
|Alex Len|10.78|11.79|5.26|6.56|0.69|
|Justise Winslow|10.77|12.72|6.57|8.17|0.59|
|DeMarre Carroll|10.65|12.37|5.81|9.36|0.43|
|Greg Monroe|10.56|9.0|3.54|5.35|0.65|
|Jerryd Bayless|10.47|12.68|6.61|5.84|0.79|
|J.J. Hickson|10.37|12.42|10.67|7.28|0.66|
|Toney Douglas|10.36|10.38|10.18|8.64|0.31|
|Jordan Hamilton|10.25|8.03|96.71|5.18|0.58|
|Jeremy Lin|10.19|11.39|7.66|5.57|0.76|
|David Lee|10.15|13.54|8.56|7.09|0.73|
|Andrew Harrison|10.13|11.75|6.46|6.01|0.74|
|Dion Waiters|10.08|10.5|7.95|6.78|0.58|
|Gary Harris|9.99|10.83|9.94|5.63|0.73|
|Kris Dunn|9.74|13.8|9.46|5.27|0.85|
|Dwight Powell|9.71|11.29|6.64|7.07|0.61|
|Robin Lopez|9.69|9.88|5.41|5.27|0.72|
|E'Twaun Moore|9.55|12.29|7.51|6.81|0.69|
 
  
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

