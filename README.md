#
stay tuned!
 the long and short of the game is: fantasy players (gamblers) submit one or multiple ticket(s) of athlete names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site that takes a rake and pays out a subset of tickets as a function of ticket score, which depends on the athletes' performance as the slate evolves. broadly there are two (very different) contest types: a "tournament" game pays out the top ~20%, with the odds growing ~exponentially from 1:1 at the ~20th percentile line (typically first place gets a  ~1000:1 return); a "cash" game pays out the top ~50% fixed 1:1 odds. naturally, these payouts force a preference for higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. this causes lower-mean/high-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter. using scraped contest records of % ownership of players in labeled historic contests, athletes' historic fantasy points data, the news leading up to the particular contest (e.g., fantasy point projections, espn buzz, etc.)  i want to train a model projecting player ownership percentages. this is interesting i) because it's easier than predicting actual players' performances from past data, ii) it's effectively a model of bulk human behavior/perceived utility of choices given the news, iii) knowledge of %ownerships let one project the distributions of scores in fantasy contests themselves! specifically,  if one has a "good" estimate of the covariance matrix of player fantasy points, one can collect statistics from an ensemble of monte-carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted %ownerships. a basic application of the simulation would be ranking the tickets by probability of cashing, etc.


what am i doing?
for a given slate of games and tournament type comprising an instance of the burgeoning pasttime of daily fantasy sports gambling, predict the composition of the field of bets. 
more specifically, for each player, predict his % ownership given the news and relevant conditions of the (fantasy) game.

why is this interesting?
-from a game-theory perspective, knowledge of other bettors' bets can represent an 'edge' in a contest with a fixed prize pool. there are a lot of companies out there offering paid 
 services for daily fantasy players, e.g.lineup optimizers, projected player outputs, etc. these companies would no doubt be interested in providing their subscribers with expected player ownerships.
-explaining/predicting decisions a collection of people make with the (incomplete) information they have on hand and in the face of risk is neat. 

how will i do this?
build individual player models trained on historic ownerships (i have ~3 seasons' worth of fanduel tournament data) and features possibly including and/but not limited to:

easy features-
- perceived value of a player (defined as a ratio of expected fantasy points to fantasy salary. this number can depend on (commercial) projections derived from regression models. 
i have 2 independent, complete sets in the range of the dependent variable for fanduel scoring. an additional possibility for consideration is valuations by other fantasy sites, e.g., draftkings, yahoo,
since fantasy points are correlated. )

- perceived relative value (e.g., z-score,rank,etc.) of a player measured against other members in his cluster. cluster label can be assigned by,e.g., a one-dimensional k-means calculation on, for instance, salary or position. fantasy bettors' bets are highly constrained (required 9 players total, membership in 5 positions, total salary under cap.) 

- notions of momentum- fantasy players are possibly sensitive to recently high- or low-performing athletes. rolling true-value averages over a set of intervals might be good predictors

- prior probability of obtaining value at or exceeding some average value required to 'cash'. e.g., some measure of average mis-pricing error by the game for the player.

- vegas total, line projections- higher vegas totals project the notion of higher concentrations of fantasy points. lower totals project the opposite. high-magnitude lines might emphasize inflated bench/deflated starter valuation by fantasy owners. low-magnitude lines might emphasize inflated starter/deflated bench valuation. 

- scraped recommended plays from 'fantasy experts' at a number of sites, including, espn, fanduel, rotogrinders, fantasypros


wishlist features-
-use integer programming solutions (parametrized on the predicted ownerships) to constrained problems as new training inputs. models become parametrized on model's own predictions.
e.g., for each player's ownership prediction, create a new variable reflecting that player's optimal ownership in a fictitous bet composed of a set of best individual solutions to:
	 maximizing value (projected points[ predicted ownerships ]  ) satisfying salary and position constraints. 

