import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import seaborn as sns


def contest(df=None,name=None):
	print 'localizing on {},len={}'.format(name,len(df.loc[df.contest_ID==name]))
	return df.loc[df.contest_ID==name].dropna()

def get_se(df=None,modell=['RandomForestRegressor','GradientBoostingRegressor','Ridge','Lasso','mean'],predtype=None):
	for model in modell:
		df['se_'+model]  = (df[model]-df['true'])**2
	return df[[X for X in df.columns if 'se_' in X]+['position']]

def get_rm(x):
	return np.sqrt(np.mean(x))
 

def norm_pos(df=None,modell=['RandomForestRegressor','GradientBoostingRegressor','Ridge','Lasso','mean']):
	rdf = pd.DataFrame()
	posl = ['PG','SG','C','PF','SF']

	cols =modell+['true']
	norm_df= df.groupby('position').sum()[cols] 
	adj =  norm_df[modell].apply(lambda x: x/norm_df['true'] )

	for pos in posl: 
		posdf = df.loc[df.position==pos]
		posdf[modell]= posdf[modell]*1/adj.ix[pos]
		if rdf.empty: rdf=posdf
		else: rdf=pd.concat([rdf,posdf])
	return rdf 
	
def eval_contest(df=None,do_norm=False):
	if do_norm: 
		df = norm_pos(df=df)
	se_df = get_se(df=df)
	se_df =  se_df.groupby('position').apply(get_rm)
	se_df['position'] = se_df.index
	se_df.reset_index(inplace=True,drop=True)
	return se_df

def get_basal(ttype=None):
	path='../../'+ttype+'_MYMODELS/SUMMARIES/lasso.csv'
	kcols = ['name','mean','std']
	df = pd.read_csv(path)
	return df[kcols]

def do_contest_rmsd_by_pos(df=None,do_norm=None):
	writedf = pd.DataFrame()
	for cid in df.contest_ID.unique():
		print 'doing CID=',cid
		errs = eval_contest(contest(df=df,name=cid),do_norm=do_norm)
		errs['cid'] = cid
		if writedf.empty:writedf = errs
		else:writedf=pd.concat([writedf,errs])
	writedf.reset_index(inplace=True,drop=True)
	writedf.sort('position',ascending=True,inplace=True)
	print writedf.to_string()

	writestr = './DATA/pos_rmsd.normed_'+str(int(do_norm))+'.csv'
	print 'writing to',writestr
	writedf.to_csv(writestr,index=False)


def plot_model(df=None,model=None,ttype=None):
	posl = ['PG','SG','C','PF','SF']
	cmap = plt.cm.Accent
	for i,X in enumerate(posl): 
		plt.scatter(df.loc[df.position==X].true.values.tolist(),
				df.loc[df.position==X][model].values.tolist(),color=cmap(i / float(len(posl))    ),label=posl[i] ,alpha=0.75)
	plt.legend()
	plt.ylabel('%ownership/model='+model)
	plt.xlabel('%ownership/true')
	plt.savefig('jan.'+model+'.'+ttype+'.png')


def plot_slate_pos_error(posdf=None,model_err=None,do_norm=None,ttype=None):
	posl = ['PG','SG','C','PF','SF']
	for pos in posl: plt.hist(posdf.loc[posdf.position==pos]['se_'+model_err],bins=25,label=pos,alpha=0.75)
	plt.legend()
	plt.xlabel('rmse ownership%/model='+model_err)
	plt.savefig('rmse.jan.'+model_err+'.n.'+str(int(do_norm))+'.'+ttype+'.png')
	plt.clf()


def plot_slate_pos_error_ratio(posdf=None,model_err=None,do_norm=None,ttype=None):
	posdf.dropna(inplace=True)
	posl = ['PG','SG','C','PF','SF']
	posdf['se_ratio'] = posdf['se_'+model_err]/posdf['se_mean']
	for pos in posl: plt.hist(posdf.loc[posdf.position==pos]['se_ratio'],bins=25,label=pos,alpha=0.75,normed=True)
	plt.legend()
	plt.xlabel('rmse:std ownership%/model='+model_err)
	plt.savefig('ratio.jan.'+model_err+'.n.'+str(int(do_norm))+'.'+ttype+'.png')

def load_contest_rmsd_by_pos(do_norm=None):
	mypath = './DATA/pos_rmsd.normed_'+str(int(do_norm))+'.csv'
	return pd.read_csv(mypath)
if __name__ == '__main__':

        try:	
		ttype =   sys.argv[1]
		do_norm = bool(int(sys.argv[2]))
        except Exception:
		ttype = 'gpp'
		do_norm=False
	redo_rmsd_by_pos=False


	readpath = '../../'+ttype+'_MYMODELS/test_SLATE_PREDS/composite.csv'
	df = pd.read_csv(readpath)
	bdf = get_basal(ttype=ttype) 
	df = pd.merge(df,bdf,on='name')

	#plot_model(df=df,model='GradientBoostingRegressor',ttype=ttype)

	if redo_rmsd_by_pos:
		do_contest_rmsd_by_pos(df=df,do_norm=do_norm)
	else:
		posdf = load_contest_rmsd_by_pos(do_norm=do_norm)
	print posdf

	
	plot_slate_pos_error_ratio(posdf=posdf,model_err='GradientBoostingRegressor',do_norm=do_norm,ttype=ttype)
	#plot_slate_pos_error(posdf=posdf,model_err='GradientBoostingRegressor',do_norm=do_norm,ttype=ttype)
	#plot_slate_pos_error(posdf=posdf,model_err='mean',do_norm=do_norm,ttype=ttype)
	#plot_slate_pos_error(posdf=posdf,model_err='mean')



