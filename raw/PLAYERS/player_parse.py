import pandas as pd
import sys
import time
import math
import numpy as np

def getrollingmean(df=None,c=None,w=None):
	rdf=pd.DataFrame()
	df.sort('date',ascending=True,inplace=True)

	for season in df.season.unique():
		#print 'DOING SEASON=',season
		sdf = df.loc[df.season==season]
		cname='rm.'+str(w).zfill(2)+'.'+c
		sdf[cname] = pd.rolling_sum(sdf[c],window=w+1,center=False,min_periods=None)-sdf[c]
		sdf[cname] = sdf[cname]*1.0/w
		sdf[cname].fillna(np.mean(sdf[c]),inplace=True)
		if rdf.empty:
			rdf = sdf
		else:
			rdf=pd.concat([rdf,sdf],axis=0)
		#print 'LEN_df={},col={}'.format(len(rdf),cname)

	kl = list(set(rdf)-set(df))
	return rdf[kl]


def addseason(df):
	sudf=pd.DataFrame()
	sbounds=[[20161020,20151020,2015],[20171020,20161020,2016]]
        for b in sbounds:
		lb =  pd.to_datetime(b[0] ,format='%Y%m%d').date()
		ub =  pd.to_datetime(b[1] ,format='%Y%m%d').date()
                sdf=df.loc[(df.date<lb)&(df.date>ub)]
		sdf['season']=b[2]
		sudf=pd.concat([sudf,sdf])
	return sudf


def get_spdf():
	pathroot = '../../DATA/mergeable/'
	renamedict = {'Name':'name','Team':'team','Opp':'opponent'}
	keepl = ['name','date','score']#,'points','position','rebounds','steals','assists','blocks','turnovers']
	mdf = pd.read_csv(pathroot+'player.composite.csv')
	mdf['date']=pd.to_datetime(mdf['date'],format='%Y%m%d')
	mdf = compute_score(mdf)
	mdf.rename(columns=renamedict,inplace=True)
	return mdf[keepl]
	
def compute_score(idf):
        idf['score']=idf['points']+1.2*idf['rebounds']+1.5*idf['assists']+2.0*idf['steals']+2.0*idf['blocks']-1.0*idf['turnovers']
        return idf


def addvalue(df):
	spdf = get_spdf()
	df = pd.merge(spdf,df,on=['name','date'],how='right')
	df['value'] = df['score']/(df['salary'])
	df['value'].fillna(0,inplace=True)
	return df

def add_value_exceeds(df=None,vcutoff=0):
	vecoln='val_exceeds.'+str(vcutoff).zfill(2)
	df[vecoln] = df['value'] > vcutoff
	return df,vecoln

def add_all_val_exceeds(df=None,vcl=None):
	vecl=[]
	for vc in vcl:	
		df,ve_col = add_value_exceeds(df,vcutoff=vc)
		vecl.append(ve_col)
	return df,vecl

if __name__ == '__main__':

	path='../../DATA/parsed_raw/NBA_GPP_records/gpp.composite.csv' 
	cdf = pd.read_csv(path,parse_dates=['date'],
			date_parser= lambda x: pd.datetime.strptime(x, '%Y-%m-%d')  )
	
	cdf = addvalue(cdf)
	cdf = addseason(cdf)
	cdf,vecl = add_all_val_exceeds(df=cdf,vcl=[4,5,6])
	for V in vecl:
		cdf[V]=np.rint(cdf[V])

	dropl = ['start_time','percent_own','top_hundred','contest_ID']
	rcols = ['score','salary','value']
	rcols = rcols+vecl
	
	cdf.drop(dropl,1,inplace=True)
	cdf = cdf.drop_duplicates()



	namel = cdf.name.unique()
	wl= [1,5,10]
	for i,plname in enumerate(namel):
		pldf = cdf.loc[cdf.name==plname]
		for col in rcols:
			for w in wl:
				plrmdf = getrollingmean(df = pldf,c =col, w =w)
				pldf = pldf.join(plrmdf,how='outer')
		writestr = plname.replace(' ','_')+'.csv'
		writepath = './rolling/'+writestr
		pldf.to_csv(writepath,index=False)
		print '#'*25+'   writing pl={},on len={} to {}; {} %done '.format(plname,len(pldf),writepath,100*float(i)/len(namel))
		#print pldf
