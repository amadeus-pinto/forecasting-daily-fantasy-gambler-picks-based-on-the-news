import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import sys




def remove_one_offs(namel=[],A_pf=None,S=None,modeltype=None):
	if modeltype!='Lasso':
		namel = [X+'.'+modeltype for X in namel]
		S['name'] = S['name']+'.'+modeltype
	for name in namel:
		A_pf = A_pf.loc[A_pf.index!=name]
		S =       S.loc[S.name    !=name]
	
	return A_pf,S


def get_mats(mod_dict=None,modeltype=None):
	path = '../DECOMPOSE/DATA/Afp.'+modeltype+'.csv'
	spath ='../../MYMODELS/SUMMARIES/'+mod_dict[modeltype]+'.csv' 
	A = pd.read_csv(path)
	S = pd.read_csv(spath)	
	S=S[['name','mean','std','cv_score']]
	S['rmse:sig'] = S['cv_score']/S['std']
	A_pf = A.transpose()
	A_pf.columns = A.features.values.tolist()
	A_pf = A_pf[1:]
	A_pf.index = [x.replace('_',' ').strip('c.') for x in  A_pf.index]

	namel=['Brandon Ingram','Jameer Nelson','Arron Afflalo']
	A_pf,S = remove_one_offs(namel=namel,A_pf=A_pf,S=S,modeltype=modeltype)

	return A_pf,S


if __name__ == '__main__':

	mod_dict = {'RandomForestRegressor':'rfr','Lasso':'Lasso','Ridge':'ridge','GradientBoostingRegressor':'gbr'}
        try:	
		modeltype = sys.argv[1]
        except Exception:
		modeltype = 'Lasso'
	A_pf,S = get_mats(mod_dict=mod_dict,modeltype=modeltype)

	n_clusters = 5 

	est = KMeans(n_clusters=n_clusters)
	X = A_pf.values
	est.fit(X)
	labels = est.labels_

	fdf = pd.DataFrame(A_pf.index.values.tolist(),columns=['name'])
	fdf['cluster'] = labels
	fdf['name'] = [x.replace('_',' ').strip('c.') for x in  fdf.name.values.tolist()] 
	for cluster in np.unique(fdf.cluster):
		df = fdf.loc[fdf.cluster==cluster]
		print "cluster:{},len:{}".format(cluster,len(df))
		print df


	
	M = pd.merge(S,fdf)
	#M['std'] = M['std']**2
	x = M['std'].values.tolist()
	y = M['mean'].values.tolist()
	r = M['rmse:sig'].values.tolist()
	plt.scatter(x,y,c = M['cluster'].values.tolist())
	plt.xlabel('sigma/own ')
	plt.ylabel('mu/own ')
	plt.savefig('kmeans.mu.sig.'+modeltype+'.png')

	plt.clf()
	plt.scatter(x,r,c = M['cluster'].values.tolist())
	plt.xlabel('sigma/own ')
	plt.ylabel('rmse:sig ')
	plt.savefig('kmeans.sig.ratio.'+modeltype+'.png')

	plt.clf()
	plt.scatter(y,r,c = M['cluster'].values.tolist())
	plt.xlabel('mu/own ')
	plt.ylabel('rmse:sig ')
	plt.savefig('kmeans.mu.ratio.'+modeltype+'.png')

	fig = plt.figure(1, figsize=(4, 3))
	plt.clf()
	ax = Axes3D(fig)
	ax.scatter(x,y,r,c = M['cluster'].values.tolist())
	ax.set_xlabel('sig/own')
	ax.set_ylabel('mu/own')
	ax.set_zlabel('model rmse:sig')
	plt.savefig('3d.kmeans'+modeltype+'.png')


