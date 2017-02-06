import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import ast



def write_A(modeltype=None,ttype=None,n_cutoff=0,writepath=None):
	path =  '../../'+ttype+'_MYMODELS/COEFFS/'
	opath = '../../'+ttype+'_MYMODELS/cv_PREDS/'
	paths =glob.glob(path+'/*'+modeltype+'.csv')
	opaths =glob.glob(opath+'/*'+modeltype+'.csv')
	A = pd.DataFrame()
	for path,opath in zip(paths,opaths):
		name = awkward_name_parse(path = path)

		my_df = pd.read_csv(path)
		odf = pd.read_csv(opath)
		
		if len(odf)<n_cutoff:
			print 'TOO FEW PTS for {}!!!'.format(name)
			continue
		try:
			my_df.columns = ['features',name]
		except Exception:
			print 'Exception?'
			print Exception
			print my_df.columns.values.tolist()
			continue
			
		if A.empty:
			A = my_df
		else:
			A = pd.merge(A,my_df,on='features',how='inner')
		print 'name={},paths={}\n{}'.format(name,path,opath)
	A.to_csv(writepath,index=False)


def awkward_name_parse(path=None):
	name = path.split('/')[-1]
	name = name.replace(' ','_').replace('.Lasso','')
	name = name.split('.csv')[0]
	name = name.replace('_',' ')
	return name




def plot_varexpl(S=None,modeltype=None,ttype=None):
	var_expl = 1 - S**2 / np.cumsum(S**2)[-1]
	fig = plt.figure(figsize=(8,5))
	nvec = np.arange(1,len(var_expl)+1)
	plt.plot(nvec,var_expl, 'ro-', linewidth=2)
	plt.title('model= '+modeltype+'; type= '+ttype)
	plt.xlabel('n_sing_vecs')
	plt.ylabel('recovery')
	plt.savefig('svd.'+modeltype+'.'+ttype+'.png')
	plt.clf()

def do_svd(A=None,modeltype=None):
	U,S,V = np.linalg.svd(A)
	return U,S,V

def get_transformed(A=None,basis_str=None):
	A_fP = pd.DataFrame(A.dot(V))
	A_Fp = pd.DataFrame(U.transpose().dot(A))
	A_Fp.columns=A.columns.values.tolist()
	A_Fp = A_Fp.transpose()
	if basis_str=='Fp': return A_Fp
	elif basis_str=='fP': return A_fP
	else: print 'invalid basis str', basis_str ;sys.exit()

def add_str(basis_str=None):
	if basis_str == 'Fp' : return 'players'
	elif basis_str == 'fP' : return 'features'

def do_plots(Aaa=None,S=None,nconsider=4,ntop=10,modeltype=None,ttype=None,basis_str=None):
	nrows = int(np.sqrt(nconsider))
	ncols = int(nrows)
	axesg=[]
	for r in range(0,nrows):
		for c in range(ncols):
			axesg.append([r,c])

	fig, axes = plt.subplots(nrows=nrows, ncols=ncols)

	for svect in range(0,nconsider):
		subdf = pd.DataFrame(np.abs(Aaa[svect])/np.sum(np.abs(Aaa[svect]))).sort( svect,ascending=False) [0:ntop]
		print subdf
		subdf.plot(kind='barh',fontsize=8,rot=0,mark_right=False,ax=axes[axesg[svect][0],axesg[svect][1]],label='sv'+str(svect) )
	plt.legend()
	plt.title('type = '+ttype+'; original-basis '+add_str(basis_str=basis_str)+' contributions in reduced space vecs'  ,size = 7)
	sstr = 'svd.i.'+add_str(basis_str=basis_str)+'.'+ttype+'.'+modeltype
	print 'saving to', sstr
	plt.savefig(sstr+'.png')
	plt.clf()

	plot_varexpl(S=S,ttype=ttype,modeltype=modeltype)

	#X = Aaa.values
	#fig = plt.figure(1, figsize=(4, 3))
	#plt.clf()
	#ax = Axes3D(fig)
	#ax.scatter(X[:, 0], X[:, 1], X[:, 2])
	#axstr = 'svd.'+ttype+'.ax.'+basis_str+'.'+modeltype
	#plt.title(sstr)
	#plt.savefig(axstr+'.png')
	#print 'saving to', axstr
	#plt.show()
def set_default():
	modeltype = 'Lasso'
	basis_str = 'fP'	#fP or Fp
	ttype     = 'gpp'
	return modeltype,basis_str,ttype



if __name__ == '__main__':


	re_write_A=False
	basis_strl = ['fP','Fp']

	try:	
		modeltype = str(sys.argv[1])
		basis_str = str(sys.argv[2])
		ttype =     str(sys.argv[3])
		if basis_str not in basis_strl:
			print 'BAD BASIS_STR " {} ". choose from {}'.format(basis_str,basis_strl) ; sys.exit()
        except Exception:
		print 'got here!'
		modeltype,basis_str,ttype = set_default()

	path = './DATA/A'+add_str(basis_str=basis_str)+'.'+ttype+'.'+modeltype+'.csv'
	if re_write_A:
		write_A(modeltype=modeltype,n_cutoff=50,ttype=ttype,writepath=path)
	
	A = pd.read_csv(path)
	A.set_index('features',inplace=True)
	U,S,V = do_svd(A=A,modeltype=modeltype)
	
	Aaa = get_transformed(A=A,basis_str=basis_str)
	do_plots(Aaa=Aaa,S=S,nconsider=4,ntop=10,modeltype=modeltype,ttype=ttype,basis_str=basis_str)



