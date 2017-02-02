# The
long and short of the game is: "fantasy players" (gamblers) submit one or multiple ticket(s) of athletes' names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site that takes a rake and pays out a subset of tickets as a function of ticket score, which depends on the athletes' performance as the slate evolves.

Broadly, there are two (very different) contest types: a "tournament" game pays out the top ~20%, with the odds growing ~exponentially from 1:1 at the ~20th percentile line (typically first place gets a  ~1000:1 return); a "cash" game pays out the top ~50% fixed 1:1 odds.

Naturally, these payouts force fantasy owners to favor higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. This causes lower-mean/higher-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter.

Using scraped contest records of % ownership of athletes in past contests, past points data, the news leading up to the particular contest (e.g., fantasy point projections, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions, I developed and benchmarked models projecting the market share of each athlete.

Apart from the intrinsic neatness of explaining/predicting the decisions a collection of people make given incomplete information and perceived utility, knowledge of % ownerships help one accurately project the distributions of scores in fantasy contests themselves! Specifically,  if one has a "good" estimate of the covariance matrix of player fantasy points, one can collect statistics from an ensemble of monte-carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted % ownerships. A basic application of such a  simulation would be ranking the tickets by probability of cashing, etc.


