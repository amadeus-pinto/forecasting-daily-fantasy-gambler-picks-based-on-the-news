The long and short of the game is: "fantasy players" (gamblers) submit one or multiple ticket(s) of athletes' names together satisfying a set of constraints (e.g., on the total fantasy salary of the athletes, fantasy positions, etc.) to an online site that takes a rake and pays out a subset of tickets as a function of ticket score, which depends on the athletes' performance as the slate evolves.

Broadly, there are two (very different) contest types: a "tournament" game pays out the top ~20%, with the odds growing ~exponentially from 1:1 at the ~20th percentile line (typically first place gets a  ~1000:1 return); a "cash" game pays out the top ~50% fixed 1:1 odds.

Naturally, these payouts force fantasy owners to favor higher-variance players (riskier positions) in "tournaments" and lower-variance players (safer positions) in "cash" games. This causes lower-mean/higher-variance distributions of ticket scores in the former and higher-mean/lower-variance distributions in the latter.

Using scraped contest records of % ownership of athletes in past contests, past points data, the news leading up to the particular contest (e.g., fantasy point projections, available injury/roster reporting, etc.), and elements of the fantasy game mechanics presumed to impact fantasy gamblers' decisions, I developed and benchmarked models projecting the market share of each athlete.

Apart from the intrinsic neatness of explaining/predicting the decisions a collection of people make given incomplete information and perceived utility, knowledge of % ownerships help one accurately project the distributions of scores in fantasy contests themselves! Specifically,  if one has a "good" estimate of the covariance matrix of player fantasy points, one can collect statistics from an ensemble of monte-carlo-sampled contests, each one represented in a set of tickets giving rise to the predicted % ownerships. A basic application of such a  simulation would be ranking the tickets by probability of cashing, etc.






contest_ID                     168 non-null int64
date                           168 non-null object
name                           168 non-null object
position                       168 non-null object
slate_size                     168 non-null int64
percent_own                    168 non-null float64
salary                         168 non-null float64
max_entries_per_user           168 non-null int64
total_entries                  168 non-null int64
proj_fc                        168 non-null float64
proj_mo                        168 non-null float64
status                         168 non-null float64
team                           168 non-null object
score                          168 non-null float64
opponent                       168 non-null object
line                           168 non-null float64
total                          168 non-null float64
log.slate_size                 168 non-null float64
v_fc                           168 non-null float64
v_mo                           168 non-null float64
max_user_frac                  168 non-null float64
value                          168 non-null float64
season                         168 non-null float64
val_exceeds.04                 168 non-null float64
val_exceeds.05                 168 non-null float64
val_exceeds.06                 168 non-null float64
rm.01.score                    168 non-null float64
rm.05.score                    168 non-null float64
rm.10.score                    168 non-null float64
rm.01.salary                   168 non-null float64
rm.05.salary                   168 non-null float64
rm.10.salary                   168 non-null float64
rm.01.value                    168 non-null float64
rm.05.value                    168 non-null float64
rm.10.value                    168 non-null float64
rm.01.val_exceeds.04           168 non-null float64
rm.05.val_exceeds.04           168 non-null float64
rm.10.val_exceeds.04           168 non-null float64
rm.01.val_exceeds.05           168 non-null float64
rm.05.val_exceeds.05           168 non-null float64
rm.10.val_exceeds.05           168 non-null float64
rm.01.val_exceeds.06           168 non-null float64
rm.05.val_exceeds.06           168 non-null float64
rm.10.val_exceeds.06           168 non-null float64
rm.01.opp_total_score          168 non-null float64
rm.02.opp_total_score          168 non-null float64
rm.05.opp_total_score          168 non-null float64
rm.01.opp_def_score            168 non-null float64
rm.02.opp_def_score            168 non-null float64
rm.05.opp_def_score            168 non-null float64
rm.01.opp_off_score            168 non-null float64
rm.02.opp_off_score            168 non-null float64
rm.05.opp_off_score            168 non-null float64
rm.01.team_total_score         168 non-null float64
rm.02.team_total_score         168 non-null float64
rm.05.team_total_score         168 non-null float64
rm.01.team_def_score           168 non-null float64
rm.02.team_def_score           168 non-null float64
rm.05.team_def_score           168 non-null float64
rm.01.team_off_score           168 non-null float64
rm.02.team_off_score           168 non-null float64
rm.05.team_off_score           168 non-null float64
z.salary                       168 non-null float64
z.proj_fc                      168 non-null float64
z.proj_mo                      168 non-null float64
z.v_fc                         168 non-null float64
z.v_mo                         168 non-null float64
sbin                           168 non-null object
z.sbin.proj_fc                 168 non-null float64
z.sbin.proj_mo                 168 non-null float64
z.sbin.v_fc                    168 non-null float64
z.sbin.v_mo                    168 non-null float64
counts.sbin                    168 non-null int64
z.rm.01.opp_total_score        168 non-null float64
z.rm.02.opp_total_score        168 non-null float64
z.rm.05.opp_total_score        168 non-null float64
z.rm.01.opp_def_score          168 non-null float64
z.rm.02.opp_def_score          168 non-null float64
z.rm.05.opp_def_score          168 non-null float64
z.rm.01.opp_off_score          168 non-null float64
z.rm.02.opp_off_score          168 non-null float64
z.rm.05.opp_off_score          168 non-null float64
z.rm.01.team_total_score       168 non-null float64
z.rm.02.team_total_score       168 non-null float64
z.rm.05.team_total_score       168 non-null float64
z.rm.01.team_def_score         168 non-null float64
z.rm.02.team_def_score         168 non-null float64
z.rm.05.team_def_score         168 non-null float64
z.rm.01.team_off_score         168 non-null float64
z.rm.02.team_off_score         168 non-null float64
z.rm.05.team_off_score         168 non-null float64
gpp.fict.proj_fc.04.025.006    168 non-null float64
gpp.fict.proj_fc.06.025.006    168 non-null float64
gpp.fict.proj_fc.08.025.006    168 non-null float64
gpp.fict.proj_mo.04.025.006    168 non-null float64
gpp.fict.proj_mo.06.025.006    168 non-null float64
gpp.fict.proj_mo.08.025.006    168 non-null float64
gpp.fict.proj_mu.04.025.006    168 non-null float64
gpp.fict.proj_mu.06.025.006    168 non-null float64
gpp.fict.proj_mu.08.025.006    168 non-null float64

