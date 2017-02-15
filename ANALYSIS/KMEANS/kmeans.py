import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import sys




def remove_one_offs(namel=[],A_pf=None,S=None,modeltype=None):
	#if modeltype!='Lasso':
	#	namel = [X+'.'+modeltype for X in namel]
	#	S['name'] = S['name']+'.'+modeltype
	for name in namel:
		A_pf = A_pf.loc[A_pf.index!=name]
		S =       S.loc[S.name    !=name]
	
	return A_pf,S


def get_mats(mod_dict=None,modeltype=None,ttype ='gpp'):
	path = '../DECOMPOSE/DATA/Aplayers.'+ttype+'.'+modeltype+'.csv'
	spath ='../../'+ttype+'_MYMODELS/SUMMARIES/'+mod_dict[modeltype]+'.csv' 
	A = pd.read_csv(path)
	S = pd.read_csv(spath)	
	S=S[['name','mean','std','cv_score']]
	S['fraction unexplained variance'] = (S['cv_score']/S['std'])**2
	A_pf = A.transpose()
	A_pf.columns = A.features.values.tolist()
	A_pf = A_pf[1:]

	#namel=['Brandon Ingram','Jameer Nelson','Arron Afflalo']
	#A_pf,S = remove_one_offs(namel=namel,A_pf=A_pf,S=S,modeltype=modeltype)
	#print A_pf
	#print S
	#sys.exit()

	return A_pf,S


if __name__ == '__main__':

	mod_dict = {'RandomForestRegressor':'rfr','Lasso':'Lasso','Ridge':'ridge','GradientBoostingRegressor':'gbr'}
        try:	
		modeltype = sys.argv[1]
		ttype = sys.argv[2]
        except Exception:
		modeltype = 'Lasso'
		ttype = 'gpp'

	A_pf,S = get_mats(mod_dict=mod_dict,modeltype=modeltype,ttype=ttype)

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
	x = M['std'].values.tolist()
	y = M['mean'].values.tolist()
	r = M['fraction unexplained variance'].values.tolist()
	plt.scatter(x,y,c = M['cluster'].values.tolist(),alpha=0.5)
	plt.xlabel('stddev ownership',size=15)
	plt.ylabel('avg ownership',size=15)
	plt.xlim([0,27.5])
	plt.ylim([0,50])
	#plt.title(ttype+' avg. ownership v natural spread')
	plt.savefig('mu.sig.'+modeltype+'.'+ttype+'.png')

	plt.clf()
	plt.scatter(x,r,c = M['cluster'].values.tolist(),alpha=0.5)
	plt.xlabel('stddev ownership',size=15)
	plt.ylabel('fraction unexplained variance',size=15)
	plt.xlim([0,27.5])
	#plt.title(ttype+' ownership model error : natural error v natural spread')
	plt.savefig('sig.ratio.'+modeltype+'.'+ttype+'.png')

	plt.clf()
	plt.scatter(y,r,c = M['cluster'].values.tolist(),alpha=0.5)
	plt.xlabel('avg ownership',size=15)
	plt.ylabel('fraction unexplained variance',size=15)
	plt.xlim([0,50])
	#plt.title(ttype+' ownership model error : natural spread v avg. ownership')
	plt.savefig('mu.ratio.'+modeltype+'.'+ttype+'.png')

	#fig = plt.figure(1, figsize=(4, 3))
	#plt.clf()
	#ax = Axes3D(fig)
	#ax.scatter(x,y,r,c = M['cluster'].values.tolist())
	#ax.set_xlabel('sig/own')
	#ax.set_ylabel('mu/own')
	#ax.set_zlabel('model rmse:sig')
	#plt.savefig('3d.kmeans'+modeltype+'.'+ttype+'.png')


