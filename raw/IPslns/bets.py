from pulp import *
import csv
import time
import pandas as pd
import scipy.stats as stats
from scipy.stats import norm
import numpy as np
import ast
import os,sys



def flatten(listOfLists):
    result = []
    for i in listOfLists:
        if isinstance(i, basestring):
            result.append(i)
        else:
            result.extend(flatten(i))
    return result

def lpDot(v1, v2):
    """Calculate the dot product of two lists of linear expressions"""
    if not isiterable(v1) and not isiterable(v2):
        return v1 * v2
    elif not isiterable(v1):
        return lpDot([v1]*len(v2),v2)
    elif not isiterable(v2):
        return lpDot(v1,[v2]*len(v1))
    else:
        return lpSum([lpDot(e1,e2) for e1,e2 in zip(v1,v2)])

def add_maxsameteam_constr(p_assign,options,teams,IP):
        gdl=[]
	d=options['pdictl']
	C = options['max_sameteam']
	if C>6:C=6;print "C>6 invalid... setting C=",C

        for team in teams:
                tl  =[p_assign[p['ID']] for p in d if p['team'] == team]
                gdl.append(tl)

        for dp in gdl:
		IP+= lpSum( (dp) ) <= C
        return IP

def add_feasibility_constr(p_assign,options,IP):

	d=options['pdictl']
	lbsal = options['lbsal']
	IP += lpSum([p_assign[p['ID']] for p in d ]) == 9 
	IP += sum([float(p['salary']) * p_assign[p['ID']] for p in d] ) <= 60.0
	IP += sum([float(p['salary']) * p_assign[p['ID']] for p in d] ) >= lbsal
	IP += lpSum([p_assign[p['ID']] for p in d if  p['isPG'] ==  1]) == 2
	IP += lpSum([p_assign[p['ID']] for p in d if  p['isSG'] == 1 ]) == 2
	IP += lpSum([p_assign[p['ID']] for p in d if  p['isPF'] == 1 ]) == 2
	IP += lpSum([p_assign[p['ID']] for p in d if  p['isSF'] == 1 ]) == 2
	IP += lpSum([p_assign[p['ID']] for p in d if  p['isC'] == 1 ])  == 1

	return IP



def initializeIPproblem(df=None,options=None,lbsal=55.5):
	dlist=[]
	for index, row in df.iterrows():
	    p = {k: v for k, v in row.iteritems()}
	    p['ID'] = str(index)#+'.'+p['name'] 
	    dlist.append(p)
	options['pdictl'] = dlist
	options['lbsal'] = lbsal

	p_assign = LpVariable.dicts("v", ([p['ID'] for p in dlist]), 0, 1, LpBinary)

	#objective
	IP = LpProblem("maximize ", LpMaximize)
	IP += sum([float(p[options['maximize']]) * p_assign[ p['ID']] for p in dlist ])
	return IP,p_assign



def solve_one_IP(IP=None,p_assign=None,options=None,occs=None):
	l=[]
	dlist = options['pdictl'] 
	failedstatus=False
	if occs:
		pslnv=occs[-1]
		IP+=lpDot([p_assign[p['ID']] for p in dlist ], pslnv) <= options['overlap']
	try:
		IP.solve(GLPK(msg=0))
	except Exception:failedstatus=True
	if failedstatus or LpStatus[IP.status]=='Infeasible': 
		print "**fail status: {}".format(LpStatus[IP.status])
		return [],[] 
	for p in dlist:
		if p_assign[p['ID']].value() == 1.0: l.append(p['name']) 
	slnv = [p_assign[ p['ID']].value() for p in dlist ]

	return slnv,l 

def getbet(df=None,options=None):
	
	df[options['maximize']].fillna(0,inplace=True)
	
	#{'c_ID': 206066206, 'lockl': ['lockl'], 'max_sameteam': 5, 'overlap': 4, 
	#'maximize': 'proj_fc', 'n_want': 50}
	n_have=0
	occs=[]
	namel=[]

	IP,p_assign = initializeIPproblem(df=df,options=options)
	IP=add_feasibility_constr(p_assign,options,IP)
	IP=add_maxsameteam_constr(p_assign,options,df.team.unique(),IP)#,dlist,df,IP)

        start_time=time.time()
	while n_have<options['n_want']: 
		slnv,nms = solve_one_IP(IP=IP,p_assign=p_assign,options=options,occs=occs)
		#if type(slnv)==list:
		if slnv:
			occs.append(slnv)
			namel.append(nms)
			ssal = do_eval_bet_sum(df=df,options=options,sl=nms,sumcolstr='salary')
			spts = do_eval_bet_sum(df=df,options=options,sl=nms,sumcolstr=options['maximize'])
			print '***{},S={},PP_"{}"={};  n={}'.format( nms, ssal,options['maximize'],spts,len(occs))
		else: return occs,namel 

		if n_have>0:
			pass
			#print "overlap w/prev.sln={}; n={}".format(lpDot(occs[-2],slnv),len(occs))
		n_have=n_have+1

	print "*****returning {} rosters...total {}s seconds".format(n_have,(time.time() -start_time ))
	
	return occs,namel


##############

def get_fict_b_df(rl=None,ptgname=None):
	rll=flatten([list(x) for x in rl])
	dl= dict((x,rll.count(x)) for x in set(rll)) 
	dldf=pd.DataFrame.from_dict(dl.items())
	dldf.columns=['name','fr']
	dldf[ptgname]=dldf.fr/len(rl)*100
	dldf.sort(ptgname,inplace=True,ascending=False,axis=0)
	dldf=dldf[['name',ptgname]]
	return dldf

def get_fict_b_name(options): return options['tournament_type']+'.fict.'+options['maximize']+'.'+str(options['overlap']).zfill(2)+'.'+str(options['n_want']).zfill(3)+'.'+str(options['max_sameteam']).zfill(3)
def get_pops(rl=None,options=None,df=None):
	ptgname = get_fict_b_name(options) 
	dldf = get_fict_b_df(rl=rl,ptgname = ptgname)
	dldf=pd.merge(dldf,df[['name','date','percent_own','contest_ID','position']],on='name',how='outer')
	dldf[ptgname].fillna(0,inplace=True)	
	dldf.sort(ptgname,inplace=True,ascending=False)
	print "--- len=", len(rl)
	print "--- nunique players=", len(dldf)
	print "--- pos count:    \n", dldf.position.value_counts()
	print dldf[['name','percent_own',ptgname]][0:20]
	return dldf[['name',ptgname,'contest_ID','date']]

#############
#############


def do_eval_bet_sum(df=None,options=None,sl=None,sumcolstr=None):
		return np.sum(df.loc[df['name'].isin(sl)][sumcolstr].fillna(0).values.tolist())

def add_ipos_bool(rdf,posstr):
	rdf['is'+posstr] = [int(posstr in x) for x in  rdf.position]
	return rdf
def add_pos_bool(rdf):
	for X in rdf.position.unique():
		rdf=add_ipos_bool(rdf,X)
	return rdf

def set_options():
	options={}
	maxstr='proj_mo'		#max on
	n_want=5         		#total want
	overlap=1       		#tolerated overlap with prev
	max_sameteam=6          	# N=(0-6)     max number pl from same team 
	tournament_type='gpp'
	#lockl=['mylock1','mylock2']	#require rostered 'mylockX' 
	#c_ID = None
	dict_str = ['maximize','n_want','overlap','max_sameteam','tournament_type']

        try:	
		argl= ast.literal_eval(sys.argv[1])
        except Exception:
		argl = [maxstr,n_want,overlap,max_sameteam]
        for s,a in zip(dict_str,argl): options[s]=a

	if options['overlap']>=9: 
		options['overlap']=8
		print '**overlap too large. setting to ',options['overlap']
        return options


def get_avg_proj(df=None,options=None,mul=['proj_fc','proj_mo']):
	df['proj_mu'] = df[mul].mean(axis=1)
	df['v_mu'] = df['proj_mu']/df['salary']
	df['proj_mu'].fillna(0,inplace=True)
	return df
	

def getdf(options):
	path = '../../DATA/merged/'+options['tournament_type']+'.proto_merged.csv'
	df = pd.read_csv(path)
	df['date']=pd.to_datetime(df['date'])
	df = add_pos_bool(df)
	df = get_avg_proj(df=df,options=options)
	df[options['maximize']].fillna(0,inplace=True)
	print df.info()
	return df

def df_subset(df=None,colname=None,colvalue=None):
	return df.loc[df[colname]==colvalue]


if __name__ == '__main__':
	options=set_options()
	df = getdf(options)
	writepath = './'+options['tournament_type']+'_IPviews/'
	fpiece = get_fict_b_name(options)
	fpath = writepath+fpiece+'.csv'
	df_fict = pd.DataFrame()
	
	doing_ids = df.contest_ID.unique()

	for this_id,i in zip(doing_ids,range(1,len(doing_ids)+1)):
		print 'DOING ID=',this_id
		cdf = df_subset(df=df,colname= 'contest_ID',colvalue=this_id)
		numlist_bet,namelist_bet=getbet(df=cdf,options=options)

		if numlist_bet:
			dldf=get_pops(namelist_bet,options=options,df=cdf)
			if df_fict.empty: df_fict = dldf
			else: df_fict = df_fict.append(dldf,ignore_index=True)
		else:
			print 'failed for id=',this_id
			print cdf[['name','position','salary',options['maximize']]]
			print cdf.position.value_counts()
			for P in np.unique(cdf.position):
				print cdf.loc[cdf.position==P][['name','position','salary',options['maximize']]]
			print cdf.info()
		
		print "*******fictitious portfolio of len={}; total len={} ; %done ={} ".format(len(dldf),len(df_fict),100.0*i/len(doing_ids))
	
	print 'writing fport of len={} to path={}'.format(len(df_fict),fpath)
	df_fict.to_csv(fpath,index=False)
