#Forecasting Daily Fantasy Gamblers' Picks Based on the News

## Introduction

In October of 2015, an employee of the daily fantasy gambling site DraftKings leveraged his site's user data to win $350,000 on a rival daily fantasy site, FanDuel, resulting in a huge scandal and allegations of insider trading. In a zero-sum game, knowledge of opponents' positions (the field's picks) ahead of market represents a serious advantage (or serious abuse if this information is applied by the same people setting the market). The expected value of a pick I, V(pick_I), is a product of the probability P of pick I's success and its associated payout A:
	V(pick_I) = \sum_J P(S_JI)*A(S_J;w_I).

P depends on the probability of pick I's score J, S_JI, and is independent of gamblers' perceptions, and payout A depends on pick I's score and gamblers' collective valuation of I, where w_I represents the market share (also termed "weight" or "ownership") in pick_I. {w} is the quantity of interest here, and models projecting field ownerships ahead of the market are the goal of this project. 

Apart from the intrinsic neatness of explaining/predicting the decisions a collection of people make given incomplete information and perceived utility, knowledge of athlete market shares can potentially help one accurately project outcomes of entire fantasy contests themselves... Specifically, if one has a "good" estimate of the covariance matrix of athlete fantasy output, one can collect statistics from an ensemble of Monte-Carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted ownership percentages. A basic application of such a simulation would be ranking the tickets by probability of profitability, etc.

##The Long and Short of Daily Fantasy mechanics

"Fantasy owners" (the gamblers) submit one or multiple ticket(s) of athletes' names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site (a.k.a. the bookie - FanDuel, DraftKings, etc.) which takes a rake and pays out a subset of tickets as a function of ticket score, which depends on the athletes' collection of stats as the slate evolves. Broadly, there are two (very different) contest types: a "tournament" game pays out the top ~20%, with payout odds growing ~exponentially from 1:1 at the ~20th percentile line (a typical first place ticket's return is ~1000:1); a "cash" game pays out the top ~50% fixed 1:1 odds. Naturally, these payouts force fantasy owners to favor higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. This causes lower-mean/higher-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter. See [this](https://www.fanduel.com/nba-guide?t=rules) FanDuel tutorial for more.

##Specifics

What causes gamblers to make the choices they make with the news they have, and how accurately can I predict the field of wagers in a given contest? 

I set out to answer these questions using scraped contest records of field ownerships in past FanDuel NBA contests (thanks to [@brainydfs](http://brainydfs.com/)), historic athlete performance data from <http://sportsdatabase.com/>, the news leading up to the particular contest (e.g., "industry" fantasy output projections from <http://basketballmonster.com>, <http://fantasycrunchers.com>, and others, themselves the output of -surprisingly mediocre- regression models, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions. (These and others are detailed below.) I trained and validated 400+ player-centered models (estimators include Ridge, Lasso, Random Forest, and gradient-boosted regressors) on over 700 "tournament" contests from the 2016 season and the first two months of the 2017 season, holding out January 2017 slates for model testing.

## Results & Discussion
1. models

2. models of tournament means
  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/FIGS/field.RandomForestRegressor.gpp.png)

  ![alt text](https://github.com/amadeus-pinto/forecasting-daily-fantasy-gambler-picks-based-on-the-news/blob/master/ANALYSIS/SLATES/
FIGS/field.mean.gpp.png)
  Substituting training set mean ownerships in the tournament mean equation, predicted means are wildly unrealistic.  

##Model factors

1. "industry" valuation 
  * proj_fc: fantasycrunchers fantasy score projection
  * proj_mo: basketballmonster fantasy score projection
  * v_fc: fantasycrunchers value  (proj_fc /salary)                      
  * v_mo: basketballmonster value (proj_mo/salary)                      

2. vegas quantities -
  * 	line: sportsdatabase matchup line                       
  * 	total: sportsdatabase matchup total 

3. momentum (rolling mean - abbreviated below as "rm" - of previous Y=1-,5-,10-game windows; computed with sportsdatabase queries) - 
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

4. player standard score (value-over-replacement within X=salary,position class) - 
  * 	z.X.proj_fc: z-score of fantasycruncher projections within class X
  * 	z.X.proj_mo: z-score of basketballmonster projections within class X          
  * 	z.X.v_fc: z-score of fantasycruncher value within class X 
  * 	z.X.v_mo: z-score of basketballmonster value within class X       

5. game mechanics - 
  * 	max_user_frac: maximum tickets per user / total contest tickets
  * 	slate_size: number of NBA games in slate 
  * 	log.slate_size: log( number of NBA games in slate)

6. fictituous gambler portfolios ( X=worldview,Y=max overlap w/previous solution,Z=number of tickets  ) -
   This type of feature is arguably the most interesting. It is constructed as follows:
   For each contest, initialize a set of fictitious gamblers, each with a specified "worldview", risk-reward tolerance, and number of bets. For each fictitious gambler, solve the integer programming problem of constructing a number of unique bets (tickets), each maximizing projected fantasy points (enumerated by worldview) subject to feasibility constraints (FanDuel's salary cap, position requirements, etc.) and risk-reward tolerance constraints (maximum number of athelete overlaps with previous integer programming solution in fictitous gambler's portfolio).
  * 	gpp.fict.proj_X.Y.Z: X=(fantasycrunchers,basketballmonster,their average),Y=(2,4,6); Z=25 
