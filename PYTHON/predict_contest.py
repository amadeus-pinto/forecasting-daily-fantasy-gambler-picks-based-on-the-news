import os,sys
import glob
import pandas as pd
import numpy as np
import math 
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
import cPickle as pickle
import gzip
from collections import defaultdict
from estgrids import dict_of_grids
from model import player,save_preds,save_specs,get_mypreds,load_Xy 

def contest(df=None,name=None):
	print 'localizing on {},len={}'.format(name,len(df.loc[df.contest_ID==name]))
	return df.loc[df.contest_ID==name].dropna()

def get_norm_pos(df=None,pos=None):
	return np.sum(df.loc[df.position==pos].percent_own)

def load_model(plname='richie azar',ttype=None):
	plmodell=[]
	rootpath = './../'+ttype+'_MYMODELS/PICKLES/'
	plpath = [X for X in glob.glob(rootpath+'/*.gz') if plname in X]

	for path in plpath:
		with gzip.open(path, 'rb') as f: 
			f= f.read()
			mymodel =  pickle.loads(f)
			plmodell.append( pickle.loads(f))
	return plmodell
		
def pred_player(df=None,plname='richie azar',ttype=None):
	myd = defaultdict(list)
	plmods = load_model(plname=plname,ttype=ttype)
	mnames  = [estimator.__init__.im_class.__name__ for estimator in plmods]

	X,y = player(df=df,name=plname,do_loadXy=True)

	true = y.values.tolist()[0]

	myd = {  N : model.predict(X)[0] for N,model in zip(mnames,plmods)  }
	print '@ {}, preds:{},true: {}'.format(plname,myd.values(),true)
	myd['true']= true 
	myd['name'] = plname
	return myd

	


def get_contest_specs(df=None):
	return [ df[X].unique()[0] for X  in ['contest_ID','date','slate_size'] ]
def do_contest(df=None,ttype=None):
	contestl = []
	specs = get_contest_specs(df=df)
	print '############################# doing contest,date,len:  {}'.format(specs)
	plnames = df.name.values.tolist()
	#plnames = plnames[0:3]
	for plname in plnames:
		contestl.append( pred_player(df=df,plname = plname,ttype=ttype))
	pcdf  = pd.DataFrame(contestl)
	pcdf['contest_ID'] = specs[0]
	return pcdf

if __name__ == '__main__':





	ttypel = ['gpp','dou']
        try:	
		ttype = sys.argv[1]
		if ttype not in ttypel:
			print 'unknown tournament type!',ttypel
			sys.exit()
        except Exception:
		print "specify tournament type in ",ttypel
		sys.exit()

	readpath =  '../DATA/merged/test.'+ttype+'.merged.csv'
	writerootpath = '../'+ttype+'_MYMODELS/test_SLATE_PREDS/'
	df = pd.read_csv(readpath)

	mycontests = df.contest_ID.unique()
	#mycontests= mycontests[0:2]
	for I,cname in enumerate(mycontests): 
		preds = do_contest(df=contest(df=df,name=cname),ttype=ttype) 
		write_df = pd.merge(df[['name','contest_ID','position']],preds,on=['name','contest_ID'])
		writepath  = writerootpath +str(cname)+'.csv'
		print '###########  {} %  DONE! writing " {} "  tournament  to:  \t {} ############ '.format(100.0*I*1.0/len(mycontests),ttype,writepath)
		write_df.to_csv(writepath,index=False)

	#posl = set(df.position)
	#mydict =  { P : get_norm_pos(df=cdf,pos=P) for P in posl }
