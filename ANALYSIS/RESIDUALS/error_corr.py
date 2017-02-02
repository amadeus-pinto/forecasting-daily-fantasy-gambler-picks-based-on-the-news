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
			df = pd.read_csv(X)
			name = X.split('/')[-1].split('.'+modeltype+'.csv')[0].replace(' ','_')
			df['name']  = name
			if predtype=='test':
				df.rename(columns={'test_pred':'test.'+modeltype},inplace=True)	
				#hack fix because test/val pred cols inconsistently labeled
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


def get_residual(df=None,modell=['RandomForestRegressor','GradientBoostingRegressor','Ridge','Lasso'],predtype=None):
	if predtype=='val': impstr = 'cv'
	else: impstr = 'test.'
	pcols = [X for X in df.columns.values.tolist() if impstr in X]
	rescols = []

	for X in pcols:
		resstr = 'res.'+X
		rescols.append(resstr)
		df[resstr] = df[X]-df['true']
	df.drop(pcols,1,inplace=True)
	keepcols = rescols#+['name']
	df = df[keepcols]
	df.columns = [X.split('.')[-1] for X in df.columns.values.tolist()]
	scols = sorted(df.columns.values.tolist())

	return df[scols]


if __name__ == '__main__':
	redo_merge_preds=True
	redo_merge_preds= False


	ptypes = ['val','test']
	ptype_dict = {'val':'PREDS','test':'test_PREDS'}
	readpath_piece = '../../MYMODELS/'
        try:	
		predtype = sys.argv[1]
		if predtype not in ptypes:
			print '*** predtype {}. choose from {}'.format(predtype, ptypes)
			sys.exit()
        except Exception: predtype = 'val'

	path = readpath_piece+ptype_dict[predtype]+'/'
	writepath = './DATA/'+predtype+'/'
	mpath =writepath+'/*.csv'


	if redo_merge_preds:
		pldict = merge_preds(path = path,writepath=writepath,predtype=predtype)
	
	composite_path = writepath+'composite.csv'
	df = pd.read_csv(composite_path)
	cdf = get_residual(df=df,predtype=predtype)
	print cdf.info()
	sns.heatmap(cdf.corr(),center=0,annot=True)
	plt.xticks(rotation=45,fontsize=7)
	plt.yticks(rotation=45,fontsize=7)
	plt.xticks(rotation=45,fontsize=7)
	plt.savefig(predtype+'.heat.png')
