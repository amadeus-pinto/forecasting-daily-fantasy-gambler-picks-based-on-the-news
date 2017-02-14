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

I set out to answer these questions using scraped contest records of field ownerships in past FanDuel NBA contests (thanks to [@brainydfs](http://brainydfs.com/)), historic athlete performance data from <http://sportsdatabase.com/>, the news leading up to the particular contest (e.g., "industry" fantasy output projections from <http://basketballmonster.com>, <http://fantasycrunchers.com>, and others, themselves the output of decidedly mediocre regression models, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions. (These and others are detailed below.) I trained and validated 400+ player-centered models (estimators include Ridge, Lasso, Random Forest, and gradient-boosted regressors) on over 700 "tournament" contests from the 2016 season and the first two months of the 2017 season, holding out January 2017 slates for model testing.

## Results
a. training/validation models
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/mu.sig.Lasso.gpp.png )
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/KMEANS/FIGS/sig.ratio.Lasso.gpp.png )
  
  
|name|mean|std|cv_score|train_score|test_score|
|---|---|---|---|---|---|
|Anthony Davis|37.6802197802|22.2974310834|11.1536821421|11.1542144774|9.42783571919|
|Stephen Curry|40.2421641791|22.5911944232|10.4332356052|9.53188243093|7.79943795076|
|LeBron James|41.9718562874|23.5288837306|11.8259324967|10.6638153162|9.21278685356|
|Harrison Barnes|28.0086956522|18.662648422|8.35956976911|7.48857983708|6.76184234785|
|Nikola Mirotic|15.9467032967|15.0348520061|6.91842655275|12.1848916035|5.57747380116|
|Eric Gordon|15.987037037|13.2128077543|6.29605062982|4.89242680954|5.12273751067|
|Jimmy Butler|36.1865|22.4739041501|9.16687639786|15.6473987755|7.44529681081|
|Klay Thompson|32.6866666667|18.2376687919|9.69068231134|9.44735772254|7.77871644008|
|Mo Williams|11.3941176471|11.8432393516|6.35622170022|4.85414752292|3.77792585742|

  
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

