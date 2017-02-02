import os,sys
import pandas as pd
import numpy as np
import math 
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor 
from sklearn.cross_validation import KFold, cross_val_score,cross_val_predict
from sklearn.grid_search import GridSearchCV


def dict_of_grids():
	d={}
	d['rfr'] = { 
		'p' : {
			'max_features':[0.5,1.0],
			'max_depth':[10,None]
		},
		'e' : RandomForestRegressor(n_estimators=500,bootstrap=True,n_jobs=2,warm_start=False,verbose=1)
		}

	d['gbr'] ={
		'p' : {
		    'n_estimators': [25,50,75,100],
		    'learning_rate': [0.1,0.3,0.5,1.0],
		    'max_depth': [2,3,4],
		    'max_features': [0.25,0.5,0.75,'auto']
		},
		'e' : GradientBoostingRegressor(verbose=0) 
		}


	d['ridge'] ={
		'p' : {
			'alpha':np.logspace(-2,5,40),   
			#[0.25,0.5,1.0],
			'normalize':[True,False]

		},
		'e' : linear_model.Ridge(copy_X=True,max_iter=None) 

		}

	d['lasso'] ={
		'p' : {
			'alpha':np.logspace(-2,5,40),   
			'normalize':[True,False]

		},
		'e' : linear_model.Lasso(copy_X=True,max_iter=10000) 
		}

	return d
	
