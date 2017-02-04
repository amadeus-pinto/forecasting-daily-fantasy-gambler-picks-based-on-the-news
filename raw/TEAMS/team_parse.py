import pandas as pd
import sys
import time
import math
import numpy as np




def getrollingmean(df=None,c=None,w=None):
	rdf=pd.DataFrame()
	df.sort('date',ascending=True,inplace=True)

	for season in df.season.unique():
		print 'DOING SEASON=',season
		sdf = df.loc[df.season==season]
		cname='rm.'+str(w).zfill(2)+'.'+c
		sdf[cname] = pd.rolling_sum(sdf[c],window=w+1,center=False,min_periods=None)-sdf[c]
		sdf[cname] = sdf[cname]*1.0/w
		sdf[cname].fillna(np.mean(sdf[c]),inplace=True)
		if rdf.empty:
			rdf = sdf
		else:
			rdf=pd.concat([rdf,sdf],axis=0)
		print 'LEN_df={},col={}'.format(len(rdf),cname)

	kl = list(set(rdf)-set(df))
	return rdf[kl]




def get_team_data():
	pathroot = '../../DATA/mergeable/'
	keepl=['season', 'date', 'team','opponent']
	renamedict = {'Team':'team','Opp':'opponent'}
	mdf = pd.read_csv(pathroot+'seas.composite.csv')
	mdf.rename(columns=renamedict,inplace=True)
	mdf['date']=pd.to_datetime(mdf['date'],format='%Y%m%d')
	mdf = compute_team_score(df=mdf,is_opp=True)
	mdf = compute_team_score(df=mdf,is_opp=False)
	teamsccols = [X for X in mdf.columns.values.tolist() if 'score' in X]
	return mdf[teamsccols+keepl]
	
def compute_team_score(df=None,is_opp=False):
	if is_opp:mystr = 'o_'; cstr = 'opp'
	else: mystr='' ; cstr = 'team'
        df[cstr+'_total_score']=df[mystr+'points']+1.2*df[mystr+'defensive rebounds']+1.2*df[mystr+'offensive rebounds'] +1.5*df[mystr+'assists']+2.0*df[mystr+'steals']+2.0*df[mystr+'blocks']-1.0*df[mystr+'turnovers']
	df[cstr+'_def_score'] = 1.2*df[mystr+'defensive rebounds']+2.0*df[mystr+'steals']+2.0*df[mystr+'blocks']+1.0*df['o_turnovers']
	df[cstr+'_off_score'] = df[mystr+'points']+1.2*df[mystr+'offensive rebounds']+1.5*df[mystr+'assists'] 
        return df

def write_rolling_team():
	rcols = ['opp_total_score', 'opp_def_score', 'opp_off_score', 'team_total_score', 'team_def_score', 'team_off_score']
	wl= [1,2,5]

	tdf = get_team_data()

	print tdf.columns.values.tolist()
	print tdf.info()

	namel = tdf.team.unique()

	for i,tname in enumerate(tdf.team.unique()):
		pldf = tdf.loc[tdf.team==tname]
		for col in rcols:
			for w in wl:
				plrmdf = getrollingmean(df = pldf,c =col, w =w)
				pldf = pldf.join(plrmdf,how='outer')
		writestr = tname.replace(' ','_')+'.csv'
		writepath = './rolling/'+writestr
		pldf.to_csv(writepath,index=False)
		print '#'*25+'   writing pl={},on len={} to {}; {} %done '.format(tname,len(pldf),writepath,100*float(i)/len(namel))

def get_agg(zcol=None,df=None,prefix=None):
	myl =[]

	IDS = np.unique(df.index.get_level_values('contest_ID'))
	print '*****************zcol={},nIDS ={}'.format(zcol,len(IDS))
	for i,this_id in enumerate(IDS):
		print '######## doing ID={}; {} %done'.format( this_id,100.0*i/len(IDS))
		this =  df.loc[( df.index.get_level_values('contest_ID')==this_id )   ] [zcol]
		myl.append(dict(this.reset_index(level='team').values.tolist()))
	outdf = pd.DataFrame(myl,index=IDS)
	newcolnames = [prefix+'.'+str(zcol)+'.'+thiscol for thiscol in outdf.columns.values.tolist()]
	outdf.columns = newcolnames
	outdf.drop_duplicates(inplace=True)
	return outdf

def write_dist_by_team(mydf =None,zscols=None,ttype=None):
	rootpath='./'+ttype+'_tenv/'
	mudf = mydf.groupby('contest_ID').mean()[zscols]
	stddf= mydf.groupby('contest_ID').std() [zscols]
	mudf.columns = ['mu.'+X for X in mudf.columns.values.tolist()]
	stddf.columns = ['sd.'+X for X in stddf.columns.values.tolist()]
	df = mudf.join(stddf)
	writepath = rootpath+'mu.sd.team.csv'
	print '###'*25+'writing DF TO ',writepath
	df.to_csv(writepath,index=True)

def write_Z_team(ttype=None):
	composite_df=pd.DataFrame()
	rootpath='./'+ttype+'_tenv/'
	path ='./'+ttype+'_tenv/mu.sd.team.csv'
	tpath = './rolling/team.roll.composite.csv'
	protopath = '../../DATA/merged/'+ttype+'.proto_merged.csv'
	cdf = pd.read_csv(path,index_col=0)
	tdf = pd.read_csv(tpath)
	pdf = pd.read_csv(protopath)
	mdf = pd.merge(pdf,tdf,how='left')
	
	zscols = [X for X in mdf.columns.values.tolist() if 'rm' in X]
	
	for I,cid in enumerate(cdf.index.values.tolist()):
		cid_df = cdf.loc[cdf.index == cid]
		newn=['contest_ID','date','team']
		for zcol in zscols:
			strz = 'z.'+zcol
			newn.append(strz)
			mu= cid_df['mu.'+zcol].values.tolist()[0]
			sd= cid_df['sd.'+zcol].values.tolist()[0]
			mdf[strz] = ( mdf[zcol]- mu )  / sd
			mdf[strz].fillna(0,inplace=True)
		a = mdf[newn].loc[mdf.contest_ID==cid]
		if composite_df.empty:
			composite_df = a
		else: 
			composite_df = composite_df.append(a,ignore_index=True)
		print '###'*10+'growing z.team_len={},***  %done={}'.format( len(composite_df),
				100.0*I/len(np.unique(cdf.index.values.tolist())   ))
	fname = rootpath+'Z.'+ttype+'.team.csv'
	composite_df.to_csv(fname,index=False)
	print 'wrote Z.team.csv; len={},path={}'.format(len(composite_df),fname)


def write_team(ttype=None):
	teampath = './rolling/team.roll.composite.csv'
	protopath = '../../DATA/merged/'+ttype+'.proto_merged.csv'
	print 'writing Zteam!'
	df  = pd.read_csv(protopath)
	tdf = pd.read_csv(teampath)
	zcols = [ X for X in tdf.columns.values.tolist() if 'team_' in X]+[ X for X in tdf.columns.values.tolist() if 'opp_' in X] 
	zcols = [X for X in zcols if 'rm' in X]
	mdf = pd.merge(df,tdf,how='left')
	mdf=mdf[tdf.columns.values.tolist()+['contest_ID']]
	write_dist_by_team(mydf= mdf,zscols=zcols,ttype=ttype)

if __name__ == '__main__':

	try:	
		ttype= sys.argv[1]
		if ttype not in ['gpp','dou']:
			print 'bad tournament type {}'.format(ttype)
			sys.exit()
	except Exception:
		print 'specify tournament type!'
		sys.exit()

	relcols = []

	rerun_write_rolling_team=True 
	rerun_write_team  =      True
	rerun_write_Z_team  =    True

	if rerun_write_rolling_team:
		write_rolling_team()
	if rerun_write_team:
		write_team(ttype=ttype)
	if rerun_write_Z_team:
		write_Z_team(ttype=ttype)
