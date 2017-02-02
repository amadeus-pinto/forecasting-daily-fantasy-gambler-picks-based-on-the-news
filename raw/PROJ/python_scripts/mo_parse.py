import pandas as pd
import glob
import numpy as np
import sys,os


'''
DK 
SCORING RULES
Players will accumulate points as follows:
Point = +1 PT
Made 3pt. shot = +0.5 PTs
Rebound = +1.25 PTs
Assist = +1.5 PTs
Steal = +2 PTs
Block = +2 PTs
Turnover = -0.5 PTs
Double-Double = +1.5PTs (MAX 1 PER PLAYER: Points, Rebounds, Assists, Blocks, Steals)
Triple-Double = +3PTs (MAX 1 PER PLAYER: Points, Rebounds, Assists, Blocks, Steals)

'''

def computeFDproj(odf):
        icols=['id', 'last_name', 'first_name','team', 'opponent', 'minutes','points',
                'rebounds', 'assists', 'steals', 'blocks', 'turnovers']
        idf=odf[icols]
        idf['name']=idf['first_name']+' '+idf['last_name']
        idf['proj_mo']=idf['points']+1.2*idf['rebounds']+1.5*idf['assists']+2.0*idf['steals']+2.0*idf['blocks']-1.0*idf['turnovers']
        idf['opponent']=idf['opponent'].str.replace('@','')
        idf['opponent']=idf['opponent'].str.replace(' ','')
        idf['team']=idf['team'].str.replace(' ','')
        idf= idf[['name','team','opponent','proj_mo']]#,'Position']]
        return idf


def writedf(path):
	outpath=path.split('/')[-1]
	odf=pd.read_csv(path)
	dp=outpath.split('.csv')[0].split('_')[1:]
	date=''
	for p in dp: date=date+p+'-'
	date=date.strip('-')
	df=computeFDproj(odf)
	df['date']=pd.to_datetime(date)
	outpath='a.'+date+'.csv'
	df.to_csv(outpath,index=False)
	print "writing to: ",outpath

if __name__ == '__main__':
	
	pl=[]
	for files in glob.glob("../mo/prepfi/*"):
		print "doing ", files
		pl.append(files)
	for path in pl:
		print "doing path=",path
		writedf(path)
