import os,sys
import pandas as pd
import numpy as np
import math 
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import KFold, cross_val_score,cross_val_predict
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
import cPickle as pickle
import gzip
from estgrids import dict_of_grids


def split_data(X=None,y=None,test_size=0.20):
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,random_state=42)
	return X_train, X_test, y_train, y_test

def save_model(model=None,path='this_model',do_zip=True,ttype=None):
	rootpath = './../'+ttype+'_MYMODELS/PICKLES/'
	path = rootpath+path+'.pkl'
	if do_zip:
		zp = path+'.gz'
		with gzip.GzipFile(zp, 'wb') as f: pickle.dump(model, f)
	else:
		with open(path, 'w') as f:
			print 'writing PICKLED model to path=',path
			pickle.dump(model, f)

def save_preds(preds=None,path='this_model',rootpiece ='',ttype=None):
	rootpath = './../'+ttype+'_MYMODELS/'+rootpiece+'_PREDS/'
	path = rootpath+path+'.csv'
	print 'writing specs to ',path
	preds.to_csv(path,index=False)

def save_specs(specs=None,path='this_model',ttype=None):
	rootpath = './../'+ttype+'_MYMODELS/COEFFS/'
	path = rootpath+path+'.csv'
	print 'writing specs to ',path
	specs.to_csv(path,index=False)

def get_mypreds(estimator=None,X=None,y=None):
	thisname = estimator.__init__.im_class.__name__
	train_preds=estimator.predict(X)
	cv_preds   = cross_val_predict(estimator,X, y)
	mypreds = pd.DataFrame()
	mypreds['true'] = y.values
	mypreds['cv.'+thisname] = cv_preds
	mypreds['train.'+thisname] = train_preds
	return mypreds


def get_cv_model(estimator=None,param_grid=None,X=None,y=None,num_folds=0,processors=1,scoring='neg_mean_squared_error'):
	if (int(len(X)-0.20*len(X)))<=num_folds:
		return 0,0,0,0,0
	thisname = estimator.__init__.im_class.__name__
	print '**** doing estimator = ',thisname
	X_train, X_test, y_train, y_test= split_data(X=X,y=y,test_size=0.20)
	kfold = KFold(n=len(X_train), n_folds=num_folds,shuffle=True)
	grid = GridSearchCV(
	cv = kfold, 
	estimator=estimator,
	param_grid = param_grid,
	scoring = scoring, 
	n_jobs = processors
	)

	grid.fit(X_train,y_train)
	print '************best params-', grid.best_params_
	estimator.set_params(**grid.best_params_)
	estimator.fit(X_train,y_train)
	preds=estimator.predict(X)
	test_preds = estimator.predict(X_test)
	train_preds = estimator.predict(X_train)
	tdf  = pd.DataFrame(test_preds,columns=['test_pred'])
	tdf['true']=list(y_test)
	if hasattr(estimator, 'coef_'):coeffs = estimator.coef_
	elif hasattr(estimator,'feature_importances_'):coeffs = estimator.feature_importances_
	else:print 'no coeffs!'; return 0,0
	headers = X.columns.values.tolist()
	lmfdf,errorst=summarize_grid_search_model(headers,y,y_test,y_train,coeffs,test_preds,train_preds,grid)
	cvpreds =         get_mypreds(estimator=estimator,X=X,y=y)

	print lmfdf
	return estimator,lmfdf,errorst,cvpreds,tdf

def player(df=None,name=None):
	print 'localizing on {},len={}'.format(name,len(df.loc[df.name==name]))
	return df.loc[df.name==name].dropna()

def summarize_grid_search_model(headers,y,y_test,y_train,coeffs,test_preds,train_preds,grid):
	print headers
	dfl=[]
	for x in range(0,len(headers)):
		dfl.append([headers[x],coeffs[x]])
	lmfdf=pd.DataFrame(dfl,columns=['features','coeffs'])
	lmfdf.sort('coeffs',ascending=False,inplace=True)
	errorst=[]
	errorst = [np.mean(y),np.std(y),np.sqrt(np.abs(grid.best_score_)),
			np.sqrt( np.mean(np.abs( y_test-test_preds )**2)),np.sqrt( np.mean(np.abs( y_train-train_preds )**2)) ,grid.best_params_]

	print "%%%%%%%%%%%%%%% error dist %%%%%%%%%%%%%%%%%%%"
	print "               n={}".format(len(y))
	print "              MU={}".format(np.mean(y))
	print "              SD={}".format( np.std(y))
	print "         CV_RMSE={}".format(np.sqrt(np.abs(grid.best_score_)))
	print "       test_RMSE={}".format(np.sqrt( np.mean(np.abs( y_test-test_preds )**2)))
	print "      train_RMSE={}".format(np.sqrt( np.mean(np.abs( y_train-train_preds )**2)))
	print 'best grid params={}'.format(grid.best_params_)
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	return lmfdf,errorst



if __name__ == '__main__':
	print 'here'

	
	proj_cols = ['proj_fc','proj_mo',
			'v_fc','v_mo',
			'status']
	vegas_cols = ['line','total']
	game_cols = ['slate_size','max_user_frac','total_entries','log.slate_size']
	
	momentum_cols = ['rm.01.score', 'rm.05.score',  'rm.01.salary', 'rm.05.salary',  'rm.01.value', 'rm.05.value', 'rm.01.val_exceeds.04', 'rm.05.val_exceeds.04',  'rm.01.val_exceeds.05', 'rm.05.val_exceeds.05', 'rm.01.val_exceeds.06', 'rm.05.val_exceeds.06'] 

	posenv_cols = ['z.salary', 'z.proj_fc', 'z.proj_mo', 'z.v_fc', 'z.v_mo']#, 'z.line', 'z.total']

	salenv_cols = ['z.sbin.proj_fc', 'z.sbin.proj_mo', 'z.sbin.v_fc', 'z.sbin.v_mo']#, 'z.sbin.line', 'z.sbin.total', 'counts.sbin']

	team_cols  =['rm.01.opp_total_score', 'rm.05.opp_total_score', 'rm.01.opp_def_score', 'rm.05.opp_def_score', 'rm.01.opp_off_score', 'rm.05.opp_off_score', 'rm.01.team_total_score', 'rm.05.team_total_score', 'rm.01.team_def_score',  'rm.05.team_def_score', 'rm.01.team_off_score', 'rm.05.team_off_score']

	team_env_cols = ['z.rm.01.opp_total_score', 'z.rm.02.opp_total_score', 'z.rm.05.opp_total_score', 'z.rm.01.opp_def_score', 'z.rm.02.opp_def_score', 'z.rm.05.opp_def_score', 'z.rm.01.opp_off_score', 'z.rm.02.opp_off_score', 'z.rm.05.opp_off_score', 
			'z.rm.01.team_total_score', 'z.rm.02.team_total_score', 'z.rm.05.team_total_score', 'z.rm.01.team_def_score', 'z.rm.02.team_def_score', 'z.rm.05.team_def_score', 'z.rm.01.team_off_score', 'z.rm.02.team_off_score', 'z.rm.05.team_off_score'] 
	ystr = 'percent_own'

	fict_bettor_cols = [
		'fict.proj_fc.03.025.006', 'fict.proj_fc.04.025.006', 'fict.proj_fc.05.025.006', 'fict.proj_fc.06.025.006', 'fict.proj_fc.07.025.006', 
		'fict.proj_fc.08.001.006', 'fict.proj_fc.08.025.006', 'fict.proj_mo.03.025.006', 'fict.proj_mo.04.025.006', 'fict.proj_mo.05.025.006', 'fict.proj_mo.06.025.006', 
		'fict.proj_mo.07.025.006', 'fict.proj_mo.07.050.006', 'fict.proj_mo.08.001.006', 'fict.proj_mo.08.025.006', 'fict.proj_mu.03.025.006', 
		'fict.proj_mu.04.025.006', 'fict.proj_mu.05.025.006', 'fict.proj_mu.06.025.006', 'fict.proj_mu.07.025.006', 'fict.proj_mu.08.001.006', 'fict.proj_mu.08.025.006'
		]


	d = dict_of_grids()
	ttypel = ['gpp','dou']

        try:	
		modeltype = sys.argv[1]
		ttype = sys.argv[2]
		if ttype not in ttypel:
			print 'unknown tournament type!',ttype
			sys.exit()
        except Exception:
		print "specify modeltype, tournament type!"
		sys.exit()

	ep = d[modeltype]
	estimator= ep['e']
	param_grid=ep['p']

	path = '../DATA/merged/'+ttype+'.merged.csv'
	df = pd.read_csv(path)

	fict_bettor_cols =  [ X for X in df.columns.values.tolist() if 'fict' in X]

	Xcols = proj_cols+vegas_cols+game_cols+momentum_cols+posenv_cols+salenv_cols+team_cols+fict_bettor_cols


	myplayers = df.name.unique()
	rl=[]

	for I,plname in enumerate(myplayers):
		pldf = player(df=df,name=plname)



		if len(pldf)<5:
			print 'SMALL DF for PLAYER=',plname
			continue
		X = pldf[Xcols]
		y = pldf[ystr]
		cids = pldf.ix[X.index.values.tolist()].contest_ID.values.tolist()

		print '============doing {}; {}% done =============='.format(plname, 100.0*I/len(myplayers)    )
		print X.info(verbose=True,null_counts=True)
		print '=================================='

		mymodel,myspecs,errstats,mypreds,testpreds = get_cv_model(estimator=ep['e'],param_grid=ep['p'],X=X,y=y,num_folds=5)

	
		if type(mymodel)!=int:

			mypreds['contest_ID']  = cids
			sname = mymodel.__init__.im_class.__name__
			save_model(model=mymodel,path=plname+'.'+  sname   ,do_zip=True    ,ttype=ttype)
			save_specs(specs=myspecs,path=plname+'.'+  sname                   ,ttype=ttype)
			save_preds(preds=mypreds,path=plname+'.'  +sname,rootpiece ='cv'  ,ttype=ttype)
			save_preds(preds=testpreds,path=plname+'.'+sname,rootpiece= 'test',ttype=ttype)
			v = [plname]+errstats+[modeltype]
			rl.append(v)
		else:	
			print "EXITING!"
			continue


	spath = './../'+ttype+'_MYMODELS/SUMMARIES/'+modeltype+'.csv'
	adf =  pd.DataFrame(rl,columns=['name','mean','std','cv_score','train_score','test_score','params','modeltype'])
	print 'writing to ',spath
	adf.to_csv(spath,index=False)
	print adf
	print adf.info()
	print adf.describe()
	print 'OUT!'

