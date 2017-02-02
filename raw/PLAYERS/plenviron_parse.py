import pandas as pd
import sys
import time
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

def get_agg(zcol=None,df=None,prefix=None):
	myl =[]

	IDS = np.unique(df.index.get_level_values('contest_ID'))
	print '*****************zcol={},nIDS ={}'.format(zcol,len(IDS))
	for i,this_id in enumerate(IDS):
		print '######## doing ID={}; {} %done'.format( this_id,100.0*i/len(IDS))
		this =  df.loc[( df.index.get_level_values('contest_ID')==this_id )   ] [zcol]
		myl.append(dict(this.reset_index(level='position').values.tolist()))
	outdf = pd.DataFrame(myl,index=IDS)
	newcolnames = [prefix+'.'+str(zcol)+'.'+thiscol for thiscol in outdf.columns.values.tolist()]
	outdf.columns = newcolnames
	outdf.drop_duplicates(inplace=True)
	return outdf


def write_dist_by_position(mydf =None,zscols=None):
	rootpath='./plenv/'
	###could make this lest repetitive by specifying agg. function
	mudf = mydf.groupby(['contest_ID','position']).mean().sort('percent_own',ascending=False)[zscols]
	stddf= mydf.groupby(['contest_ID','position']).std().sort('percent_own',ascending=False) [zscols]
	for zcol in zscols:
		writepath=rootpath+'mu.sd.'+zcol+'.csv'
		mu_by_pos_df =  get_agg(zcol= zcol,df = mudf, prefix  ='mu')
		std_by_pos_df = get_agg(zcol=zcol, df = stddf,prefix ='sd')

		merged_df = mu_by_pos_df.join(std_by_pos_df)#,how='left')
		print '###'*25+'writing DF TO ',writepath
		merged_df.to_csv(writepath,index=True)
	

def get_index_joined_composite(dbp_paths=None):
	composite_df = pd.DataFrame()
	for X in dbp_paths:
		if 'Z' in X: continue
		mydf = pd.read_csv(X,index_col=0)
		if composite_df.empty:composite_df = mydf
		else:composite_df = composite_df.join(mydf)
	return composite_df


def Z_write_dist_by_position(cdf=None,rel_cols=None):
	composite_df=pd.DataFrame()
	mod_df = cdf[rel_cols].set_index('contest_ID')
	dbp_paths =glob.glob('./plenv/*.csv')
	composite_df = get_index_joined_composite(dbp_paths) 

	posl=cdf.position.unique()
	for pos in posl:
		strp ='.'+pos
		poscols= [X for X in composite_df.columns.values.tolist() if strp in X]
		Cposdf  = composite_df[poscols]
		CMposdf =mod_df.loc[mod_df.position==pos]
		tempJ = CMposdf.join(Cposdf)
		tempJ.drop_duplicates(inplace=True)
		for zcol in zscols:
			print 'doing zcol=',zcol
			tempJ['z.'+zcol] = (tempJ[zcol]-tempJ['mu.'+zcol+strp])/tempJ['sd.'+zcol+strp]
		zouts = [X for X in tempJ.columns.values.tolist() if 'z' in X]
		outDF = tempJ[['name']+zouts]
		outDF.drop_duplicates(inplace=True)
		cidl = outDF.index.values.tolist()
		outDF['contest_ID'] = cidl 
		fname = writepath+'Z.pos'+strp+'.csv'
		outDF.to_csv(fname,index=False)
		print 'pos={},len={},path={}'.format(pos,len(outDF),fname)


def get_df_subset_iseq(df,col,value):
	return df.loc[df[col]==value]

def make_cols_on_ind(df=None,colprependstr=None,colnamestr=None):
	nm = [ colprependstr+'.'+colnamestr+'.'+cols for cols in df.columns.values.tolist()]
	df.columns = nm
	df [colnamestr] = df.index
	return df.reset_index(drop=True)

def write_binsize(df=None,binname=None):
	df['counts.'+binname] = df.groupby(binname)[binname].transform('count')
	return df




def Z_write_dist_by_salary(cdf=None,rel_cols=None):
	r_df = pd.DataFrame()
	for I,cid in enumerate(cdf.contest_ID.unique()):
		cid_df = get_df_subset_iseq(cdf,'contest_ID',cid)
		sb_series = pd.cut(cid_df['salary'],bins=3,right=False,labels=['sb1','sb2','sb3'])
		cid_df['sbin']= sb_series.values

		mudf  =  cid_df.groupby('sbin').mean()[rel_cols]
		stddf  = cid_df.groupby('sbin').std() [rel_cols]
		mudf =  make_cols_on_ind(df=mudf,colprependstr= 'mu',colnamestr='sbin')
		stddf = make_cols_on_ind(df=stddf,colprependstr='sd',colnamestr='sbin')

		scid_df = pd.merge(cid_df, mudf,on='sbin')
		scid_df = pd.merge(scid_df,stddf,on='sbin')
		rcols=[]
		for col in rel_cols:
			scid_df,rcolname = get_Z_score(df=scid_df,colname=col)
			rcols.append(rcolname)

		sldf = scid_df[['contest_ID','name','sbin']+rcols].sort('sbin',ascending=False)
		sldf.drop_duplicates(inplace=True)
		sldf=write_binsize(df=sldf,binname='sbin')
		
		if r_df.empty:	r_df = sldf
		else:	r_df = r_df.append(sldf,ignore_index=True)
		print '###'*10+'growing zsbin df_len={},this_cid={}; this zsbin df_len={},***  %done={}'.format( len(r_df),
												cid ,len(sldf),100.0*I/len(cdf.contest_ID.unique()))
	fname = writepath+'Z.sbin.composite.csv'
	r_df.to_csv(fname,index=False)
	print 'wrote Z.sbin.csv; len={},path={}'.format(len(r_df),fname)


def get_Z_score(df=None,colname=None,colprependstr='sbin'):
	mup = 'mu.'+colprependstr+'.'+colname
	sdp = 'sd.'+colprependstr+'.'+colname
	rcolname='z.'+colprependstr+'.'+colname
	df[rcolname]  =  (df[colname]-df[mup])/df[sdp]
	df[rcolname].fillna(0,inplace=True)
	return df,rcolname






if __name__ == '__main__':

	rerun_write_dist_by_position   = True  
	rerun_Z_write_dist_by_position = True
	rerun_Z_write_dist_by_salary   = True

	writepath = './plenv/'
	path='../../DATA/merged/proto_merged.csv' 

	zscols=['salary','proj_fc','proj_mo', 'v_fc', 'v_mo']#,'line','total']
	
	#['rm.01.value','rm.01.score','rm.01.salary',
	#'rm.01.val_exceeds.04','rm.01.val_exceeds.05','rm.01.val_exceeds.06']

	rel_cols = ['contest_ID','name','position']+zscols
	cdf = pd.read_csv(path,parse_dates=['date'],
			date_parser= lambda x: pd.datetime.strptime(x, '%Y-%m-%d')  )

	if rerun_write_dist_by_position:
		write_dist_by_position(mydf=cdf,zscols=zscols)

	if rerun_Z_write_dist_by_position:
		Z_write_dist_by_position(cdf=cdf,rel_cols=rel_cols)

	if rerun_Z_write_dist_by_salary:
		Z_write_dist_by_salary(cdf=cdf,rel_cols=['proj_fc','proj_mo','v_fc','v_mo'])

		#,'line','total'
		#'rm.01.value','rm.01.score','rm.01.salary','rm.01.val_exceeds.04'
		#,'rm.01.val_exceeds.05','rm.01.val_exceeds.06'


