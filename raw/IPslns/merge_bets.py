import pandas as pd
import glob



def getIandC(alist,blist):
		intersec=list(set(alist) & set(blist))
		comple=list(set(alist) - set(blist))
		return intersec,comple

if __name__ == '__main__':


	writepath = './IPviews/'
	fname = writepath+'fict.composite.csv'


	#fict_paths =glob.glob(writepath+'*.csv')
	fict_paths =glob.glob(writepath+'*_*.csv')
	#fict_paths = [X for X in fict_paths if '050' in X or '001' in X or '.03' in X or '.04' in X or '.05' in X]
	mdf = pd.DataFrame()
	for X in fict_paths:
		print 'doing ', X
		df = pd.read_csv(X)
		if mdf.empty:
			mdf=df
		else:	
			intersec,comple=getIandC(mdf.columns,df.columns)
			mdf=pd.merge(mdf,df,on=intersec,how='outer')
		mdf = mdf.drop_duplicates()
	
	print mdf
	print 'writing df of len={} to {}'.format(len(mdf),fname)
	mdf.to_csv(fname,index=False)






