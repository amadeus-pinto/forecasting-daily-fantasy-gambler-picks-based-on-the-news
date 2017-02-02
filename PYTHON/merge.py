import os,sys
import pandas as pd
import numpy as np
import pickle

def compute_score(idf):
        idf['score']=idf['points']+1.2*idf['rebounds']+1.5*idf['assists']+2.0*idf['steals']+2.0*idf['blocks']-1.0*idf['turnovers']
        return idf

def get_fict():
	pathroot = '../DATA/mergeable/'
	df = pd.read_csv(pathroot+'fict.composite.csv')
	df['date']=pd.to_datetime(df['date'])
	df = df.drop_duplicates()
	return df




def get_ssdf():
	pathroot = '../DATA/mergeable/'
	renamedict = {'Name':'name','Team':'team','Opp':'opponent'}
	keepl = ['team','opponent','line','total','date']
	mdf = pd.read_csv(pathroot+'seas.composite.csv')
	mdf['date']=pd.to_datetime(mdf['date'],format='%Y%m%d')
	mdf.rename(columns=renamedict,inplace=True)
	mdf = mdf[keepl]
	mdf  = mdf.drop_duplicates()
	return mdf[keepl]

def get_spdf():
	pathroot = '../DATA/mergeable/'
	renamedict = {'Name':'name','Team':'team','Opp':'opponent'}
	keepl = ['name','team','date','score']
	mdf = pd.read_csv(pathroot+'player.composite.csv')
	mdf['date']=pd.to_datetime(mdf['date'],format='%Y%m%d')
	mdf = compute_score(mdf)	####################
	mdf.rename(columns=renamedict,inplace=True)
	mdf  = mdf.drop_duplicates()
	return mdf[keepl]
	
def get_proj():
	pathroot = '../DATA/mergeable/'
	filel = ['fc.composite.csv','mo.composite.csv']
	#pcols = ['name','proj_fc','proj_mo','status','team','opponent','date']
	pcols = ['name','proj_fc','proj_mo','status','date']
	mdf = pd.DataFrame()

	for fi in filel:
		if mdf.empty:
			mdf = pd.read_csv(pathroot+fi)
		else:
			df = pd.read_csv(pathroot+fi)
			intersec,comple=getIandC(mdf.columns,df.columns)
			mdf=pd.merge(mdf,df,on=intersec,how='outer')

	mdf['date']=pd.to_datetime(mdf['date'])
	print mdf.describe()
	return mdf[pcols]

def get_fdf():
	mdf = pd.DataFrame()
	pathroot = '../DATA/mergeable/'
	filel=['NBA_GPP.event.csv','gpp.composite.csv']
	fcols = ['contest_ID','date','name','position','slate_size','percent_own','salary','max_entries_per_user','total_entries']
	for fi in filel:
		if mdf.empty:
			mdf = pd.read_csv(pathroot+fi)
		else:
			df = pd.read_csv(pathroot+fi)
			intersec,comple=getIandC(mdf.columns,df.columns)
			mdf=pd.merge(mdf,df,on=intersec)
	mdf['date']=pd.to_datetime(mdf['date'])
	
	return mdf[fcols]

def get_pos_envplr():
	pathroot = '../DATA/mergeable/Z.pos.composite.csv'
	df =  pd.read_csv(pathroot)
	#df.drop('z.rm.01.val_exceeds.06',1,inplace=True)
	print 'WARNING FIX VARu!!!!!'
	df = df.drop_duplicates()
	return df

def get_envteam():
	pathroot = '../DATA/mergeable/Z.team.csv'
	df =  pd.read_csv(pathroot)
	df['date']=pd.to_datetime(df['date'])
	print df.info()
	df = df.drop_duplicates()
	print df.columns.values.tolist()
	print [X for X in df.columns.values.tolist() if 'rm' in X]
	return df

def get_sal_envplr():
	pathroot = '../DATA/mergeable/Z.sbin.composite.csv'
	df =  pd.read_csv(pathroot)
	#df.drop('z.sbin.rm.01.val_exceeds.06',1,inplace=True)
	print df.info()
	print 'WARNING FIX VARu!!!!!'
	df = df.drop_duplicates()
	return df

def get_plr():
	pathroot = '../DATA/mergeable/player.roll.composite.csv'
	df =  pd.read_csv(pathroot)
	df['date']=pd.to_datetime(df['date'])
	df = df.drop_duplicates()
	dl=['salary',  'score', 'position']
	df.drop(dl,1,inplace=True)
	return df

def get_tea():
	pathroot = '../DATA/mergeable/team.roll.composite.csv'
	df =  pd.read_csv(pathroot)
	df['date']=pd.to_datetime(df['date'])
	#keepcols = ['team','opponent','date']+[X for X in df.columns.values.tolist() if 'rm.' in X]
	keepcols = ['team','date']+[X for X in df.columns.values.tolist() if 'rm.' in X]
	df = df.drop_duplicates()
	
	####
	return df[keepcols]

def merge_with_big(big=None,small=None,oncols = []):
	
	intersection,complement = getIandC(big.columns.values.tolist(),small.columns.values.tolist())
	print '******merging on=',intersection
	print 'complement = ',complement
	if oncols:
		big = pd.merge(big,small,on=oncols,how='left')
	else:
		big = pd.merge(big,small,on=intersection,how='left')

	print '====================================='
	print big.info(verbose=True,null_counts=True)
	print '====================================='
	return big

def getIandC(alist,blist):
		intersec=list(set(alist) & set(blist))
		comple=list(set(alist) - set(blist))
		return intersec,comple

def add_projvalue(df=None,projcol=None):
	pvaluestr='v_'+projcol.split('_')[1]
	df[pvaluestr] = df[projcol]/(df['salary'])
	df[pvaluestr].fillna(0,inplace=True)
	return df




def add_log_transform(df=None,colname=None):
	df['log.'+colname] = np.log(df[colname]+1)
	return df

def get_baseline_df():
	ssdf = get_ssdf()
	spdf = get_spdf()
	pdf =  get_proj()
	fdf =  get_fdf()

	df = fdf

	df = merge_with_big(big=df,small=spdf)
	df = merge_with_big(big=df,small=spdf)
	df = merge_with_big(big=df,small=pdf)
	df = merge_with_big(big=df,small=ssdf)


	df=add_log_transform(df=df,colname='slate_size')

	####move these to functions
	df['v_fc']=df['proj_fc']/df['salary']
	df['v_mo']=df['proj_mo']/df['salary']
	df['v_fc'].fillna(0,inplace=True)
	df['v_mo'].fillna(0,inplace=True)

	df['max_user_frac'] = df['slate_size']/df['max_entries_per_user']
	###########################


	wrpath = '../DATA/merged/proto_merged.csv'
	print 'writing to ',wrpath
	print df.info(verbose=True,null_counts=True)
	df = df.drop_duplicates()
	df.to_csv(wrpath,index=False)

	return df

def add_feats(df):
	vpdf = get_plr()
	vtdf = get_tea()
	epdf = get_pos_envplr()
	esdf = get_sal_envplr()

	etdf = get_envteam()
	fbdf = get_fict()
	
	df = merge_with_big (big=df,small=vpdf)
	df = merge_with_big (big=df,small=vtdf)

	df =  merge_with_big(big=df,small=epdf )
	df =  merge_with_big(big=df,small=esdf )


	df = merge_with_big(df,etdf )

	df = merge_with_big(df,fbdf)
	df = df.drop_duplicates()

	return df



if __name__ == '__main__':

	writepath='../DATA/merged/merged.csv'

	df = get_baseline_df()
	df = add_feats(df)

	print 'writing to-',writepath
	df.to_csv(writepath,index=False)
	print df.info(verbose=True,null_counts=True)
	print df.describe()

	print '====================='
	print '====================='
	print '====================='
	print 'LeBron'
	le= df.loc[df.name=='LeBron James']
	print le.info()
	print '====================='
	print '====================='
	print '====================='

