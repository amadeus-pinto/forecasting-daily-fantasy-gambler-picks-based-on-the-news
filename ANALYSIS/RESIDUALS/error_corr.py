import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
from collections import defaultdict
import seaborn as sns



def merge_preds(modell=['RandomForestRegressor','GradientBoostingRegressor','Ridge','Lasso'],path=None,writepath=None,predtype=None):
	d=defaultdict(list)

	for modeltype in modell:
		print 'modeltype=',modeltype
		for X in  glob.glob(path+'/*'+modeltype+'.csv'):
			print 'doing path=',X
			print X
			df = pd.read_csv(X)
			name = X.split('/')[-1].split('.'+modeltype+'.csv')[0]
			df['name']  = name
			if 'test_pred' in df.columns:
				df.rename(columns={'test_pred':'test.'+modeltype},inplace=True)
			d[name].append(df)

	for key in d.keys():
		mydf = pd.DataFrame()
		for el in d[key]:
			if mydf.empty: mydf = el
			else: 
				mydf = pd.concat([mydf,el.drop(['true','name'],1)],axis=1)
		fi = writepath+key+'.csv'
		print '************ writing {} to {}'.format(key,fi)
		mydf.to_csv(fi,index=False)

def concat_merge(path=None):
	print 'WRITING CONCATENATED FILE!'
	pll =   glob.glob(path+'/*.csv')
	c_df =pd.DataFrame()
	dfs = []
	for X in pll:
		this = pd.read_csv(X)
		dfs.append(this)
		#if c_df.empty:
		#	c_df =this
		#else:
		#	c_df = pd.concat([c_df,this],axis=0)
		#print 'at {},len={}'.format(X,len(c_df))
		#print c_df.columns.values.tolist()
	c_df = pd.concat(dfs)
	c_df.to_csv(path+'composite.csv',index=False)
	return c_df
	
	


def get_residual(df=None,modell=['RandomForestRegressor','GradientBoostingRegressor','Ridge','Lasso'],predtype=None):

	mod_dict = {'RandomForestRegressor':'rfr','Lasso':'Lasso','Ridge':'ridge','GradientBoostingRegressor':'gbr'}
	if predtype=='val': impstr = 'cv.'
	else: impstr = 'test.'
	print df
	pcols = [X for X in df.columns.values.tolist() if impstr in X]
	idcols = [X for X in df.columns.values.tolist() if 'contest_ID' in X]
	df.drop(idcols,1,inplace=True)
	rescols = []

	for X in pcols:
		Y = mod_dict[X.replace(impstr,'')]
		resstr = 'res.'+Y.lower()
		rescols.append(resstr)
		df[resstr] = df[X]-df['true']
	df.drop(pcols,1,inplace=True)
	keepcols = rescols#+['name']
	df = df[keepcols]
	df.columns = [X.split('.')[-1] for X in df.columns.values.tolist()]
	scols = sorted(df.columns.values.tolist())
	df.dropna(inplace=True)
	return df[scols]


if __name__ == '__main__':
	redo_merge_preds= False


	ptype_dict = {'val':'cv_PREDS','test':'test_PREDS'}
        try:	
		predtype = sys.argv[1]
		ttype = sys.argv[2]
		if predtype not in ptype_dict.keys():
			print '*** predtype {}. choose from {}'.format(predtype, ptype_dict.keys())
			sys.exit()
        except Exception: predtype = 'test' ; ttype='gpp'

	readpath_piece = '../../'+ttype+'_MYMODELS/'
	path = readpath_piece+ptype_dict[predtype]+'/'
	writepath = './DATA/'+predtype+'/'
	composite_path = writepath+'composite.csv'

	if redo_merge_preds:
		merge_preds(path = path,writepath=writepath,predtype=predtype)
		df = concat_merge(path=writepath)

	else:
		df = pd.read_csv(composite_path)
	cdf = get_residual(df=df,predtype=predtype)
	print cdf.info(verbose=True,null_counts=True)
	corrmat = cdf.corr()
	print corrmat
	sns.heatmap(corrmat,center=0.5,annot=True,linewidths=0.5,robust=True)
	plt.xticks(rotation=0,fontsize=15)
	plt.yticks(rotation=0,fontsize=15)
	#plt.title(predtype+' residual correlations',fontsize=20)
	plt.savefig(ttype+'.'+predtype+'.corrmat.png')
