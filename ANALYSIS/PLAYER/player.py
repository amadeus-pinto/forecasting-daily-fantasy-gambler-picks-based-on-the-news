import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import seaborn as sns
from scipy import stats

def player(df=None,name=None,do_loadXy=False):
	print 'localizing on {},len={}'.format(name,len(df.loc[df.name==name]))
	if do_loadXy==True:
		return load_Xy(df=df.loc[df.name==name].dropna())
		
	else:
		return df.loc[df.name==name].dropna()





if __name__ == '__main__':

        try:	
		ttype =   sys.argv[1]
		plname =   sys.argv[2]
        except Exception:
		ttype = 'gpp'
		plname='LeBron James'
	path = '../../DATA/merged/'+ttype+'.merged.csv'
	df = pd.read_csv(path)
	pldf  = player(df=df,name=plname)
	print pldf.info()


	ifeats = ['percent_own','total','line','slate_size']
	sns.pairplot(pldf[ifeats],hue='slate_size')
	plt.savefig(plname+'.png')
