import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import ast



def write_A(modeltype='Ridge',n_cutoff=0):
	path = '../../MYMODELS/COEFFS/'
	opath = '../../MYMODELS/PREDS/'
	paths =glob.glob(path+'/*'+modeltype+'.csv')
	opaths =glob.glob(opath+'/*'+modeltype+'.csv')
	A = pd.DataFrame()
	for path,opath in zip(paths,opaths):
		name = path.split('/')[-1]
		name = name.replace(' ','_').replace('.Lasso','')
		name = name.split('.csv')[0]

		df = pd.read_csv(path)
		odf = pd.read_csv(opath)
		if len(odf)<n_cutoff:
			print 'TOO FEW PTS for {}!!!'.format(name)
			continue
		df.columns = ['features','c.'+name]
		if A.empty:
			A = df
		else:
			A = pd.merge(A,df,on='features')
		print 'name={},path={}'.format(name,path)
	A.to_csv('./DATA/Afp.'+modeltype+'.csv',index=False)


def do_svd(A=None,modeltype=None):
	U,S,V = np.linalg.svd(A)
	var_expl = 1 - S**2 / np.cumsum(S**2)[-1]
	fig = plt.figure(figsize=(8,5))
	nvec = np.arange(1,len(var_expl)+1)
	plt.plot(nvec,var_expl, 'ro-', linewidth=2)
	plt.title('var recovered')
	plt.xlabel('n_sing_vecs')
	plt.ylabel('recovery')
	plt.savefig('svd.'+modeltype+'.png')
	plt.clf()

	return U,S,V



def write_transformed(Aaa=None,basis_str=None,modeltype=None,ntop=5,nconsider=6,do_norm=True):
	faal = []
	for svect in range(0,nconsider):
		if do_norm:
			dfsv = pd.DataFrame(np.abs(Aaa[svect])/np.sum(np.abs(Aaa[svect])))
			#subdf.cumsum(axis=0)
		else:
			dfsv = pd.DataFrame(Aaa[svect])	
		tophi = dfsv.sort(svect,ascending=False)[0:ntop][svect].index.tolist()
		toplo = dfsv.sort(svect,ascending=True)[0:ntop][svect].index.tolist()
		print dfsv.sort(svect,ascending=False)
		faal.append([svect,tophi,toplo])
	df_fP = pd.DataFrame(faal,columns = [modeltype+'.sing_vect','tophi','toplo'])
	for X in range(0,nconsider):
		print df_fP.ix[X].values
	
	df_fP.to_csv('./DATA/svd.'+basis_str+'.'+modeltype+'.csv')


if __name__ == '__main__':


	re_write_A=True
	nconsider = 4
	ntop  = 10

        try:	
		argl= ast.literal_eval(sys.argv[1])
		print argl
		modeltype = argl[0]
		basis_str = argl[1]
        except Exception:
		modeltype = 'Lasso'
		basis_str = 'fP'


	if re_write_A:
		write_A(modeltype=modeltype,n_cutoff=50)
	
	path = './DATA/Afp.'+modeltype+'.csv'
	A = pd.read_csv(path)
	A.set_index('features',inplace=True)
	U,S,V = do_svd(A=A,modeltype=modeltype)
	
	A_fP = pd.DataFrame(A.dot(V))
	A_Fp = pd.DataFrame(U.transpose().dot(A))
	A_Fp.columns=A.columns.values.tolist()
	A_Fp = A_Fp.transpose()

	
	if basis_str=='pF':
		Aaa=A_Fp
	elif basis_str=='fP':
		Aaa=A_fP
	else: print 'invalid basis str', basis_str ;sys.exit()

	#write_transformed(Aaa=Aaa,basis_str=basis_str,modeltype=modeltype,ntop=ntop,nconsider=nconsider)




	nrows = int(np.sqrt(nconsider))
	ncols = int(nrows)

	axesg=[]
	for r in range(0,nrows):
		for c in range(ncols):
			axesg.append([r,c])
		

	fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
	Aaa.index = [X.replace('.'+modeltype,'') for X in Aaa.index.values.tolist() ]
	Aaa.index = [X.replace('c.','') for X in Aaa.index.values.tolist() ]

	for svect in range(0,nconsider):
		subdf = pd.DataFrame(np.abs(Aaa[svect])/np.sum(np.abs(Aaa[svect]))).sort( svect,ascending=False) [0:ntop]
		print subdf
		subdf.plot(kind='barh',fontsize=8,rot=0,mark_right=False,ax=axes[axesg[svect][0],axesg[svect][1]],label='sv'+str(svect) )
	plt.legend()
	sstr = 'svd.i.'+basis_str+'.'+modeltype
	print 'saving to', sstr
	plt.savefig(sstr+'.png')
	plt.clf()




	X = Aaa.values
	fig = plt.figure(1, figsize=(4, 3))
	plt.clf()
	ax = Axes3D(fig)#, rect=[0, 0, .95, 1], elev=48, azim=134)
	ax.scatter(X[:, 0], X[:, 1], X[:, 2])
	axstr = 'svd.ax.'+sstr
	plt.title(sstr)
	plt.savefig(axstr+'.png')
	print 'saving to', axstr

	#plt.show()
