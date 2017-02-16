import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
from collections import Counter

def get_top_coeff(modeltype=None,ttype=None,ntop=1):
	mod_dict = {'rfr':'RandomForestRegressor','lasso':'Lasso','ridge':'Ridge','gbr':'GradientBoostingRegressor'}
	path =  '../../'+ttype+'_MYMODELS/COEFFS/'
	mstr = mod_dict[modeltype]+'.csv' 
	paths = glob.glob(path+'/*'+mstr)
	l=[]
	for piece in paths:
		name =  piece.strip(path).split('.'+mstr)[0]
		df = pd.read_csv(piece)
		df['coeffs']=np.abs(df['coeffs'])
		coeffs = df.sort('coeffs',ascending=False,inplace=False).features[0:ntop].values.tolist()
		print name,coeffs
		l.append([name,coeffs])
	ldf = pd.DataFrame(l,columns = ['name','top_coeffs'])
	return ldf


def do_counts(ldf=None):
	c  = Counter(flatten(ldf['top_coeffs'].values.tolist()))
	a = pd.DataFrame.from_dict(c, orient='index').reset_index()
	a.columns = ['feature','count']
	a.sort('count',ascending=False,inplace=True)
	return a 
	
def flatten(listOfLists):
    result = []
    for i in listOfLists:
        if isinstance(i, basestring):
            result.append(i)
        else:
            result.extend(flatten(i))
    return result

if __name__ == '__main__':

        try:	
		modeltype = sys.argv[1]
		ttype = sys.argv[2]
        except Exception:
		modeltype='rfr'
		ttype='gpp'

	ntop=5
	ldf = get_top_coeff(modeltype=modeltype,ttype=ttype,ntop=ntop)
	adf = do_counts(ldf)
	adf['%time_in_top_'+str(ntop)] =100.0*adf['count']/len(ldf)
	adf = adf[['feature','%time_in_top_'+str(ntop)]].round(1)
	adf.to_csv('./DATA/'+modeltype+'.csv',index=False)
	print adf

	


