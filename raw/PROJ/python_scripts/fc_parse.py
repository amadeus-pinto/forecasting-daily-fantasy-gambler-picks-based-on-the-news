import pandas as pd
import glob
import numpy as np
import sys,os

def trans_inj_stat(df):
	mapping = {'': 0, 'U':-1,'O': -1,'P':0,'S':1}
	df['Injury_status']=df['Injury_status'].str.replace('null','').replace('OUT','O').replace('Unk','U')
	for k,v in mapping.iteritems():
		df['Injury_status'] = df['Injury_status'].replace(to_replace=k,value=v)
	return df


def writedf(path):
	outpath='a.'+path+'.csv'
	outpath='a.'+path.split('/')[-1]
	outpath=outpath+'.csv'
	f = open(path,'r')
	gl=[]
        for line in f:
		br=list(line.split(','))
		d={}
		for x in br:
			piece= x.split('":"')
			piece=[Y.replace('"','').replace('\n','') for Y in piece]
			if len(piece)!=2: pass #print "SMALL!",piece
			else: 
				d[piece[0]]=piece[1]
		gl.append(d)
	df=pd.DataFrame(gl)
	datel=df['DateTime'].str.split(' ').values.tolist()
	datel=[row[0] for row in datel]
	df['date']=pd.to_datetime(datel)


	df = trans_inj_stat(df)

	wantl = ['PlayerName','Injury_status','date','Proj_Score']#, 'Salary','Last_Sal']
	rename_dict = {'PlayerName':'name','Proj_Score':'proj_fc','Injury_status':'status_fc','Injury_status':'status'}
	df= df[wantl]
	df.rename(columns=rename_dict,inplace=True)
	df.to_csv(outpath,index=False)
	print "writing to: ",outpath

if __name__ == '__main__':
	
	pl=[]
	for files in glob.glob("../fc/prepfi/*"):
		print "doing ", files
		fsize=os.path.getsize(files)
		print "fsize=",fsize
		if fsize>4:
			pl.append(files)
		else:
			print "**************************fi-",files,"empty.... "

	print pl
	for path in pl:
		writedf(path)
