import pandas as pd
import sys
import time
import math
import glob


#path1 = './ALL/gpps/15253-23803603.json'
#path1 = './ALL/doubleUps/14216-21172256.json'

pathl=  glob.glob("./NBA_GPP/*")
#pathl=  glob.glob("./NBA_DOU/*")
tournament_type = pathl[0].split('/')[1]
write_path = '../../DATA/parsed_raw/'+tournament_type+'_records/'
tournament_writestr = write_path+tournament_type+'.event'
player_writestr =     write_path+tournament_type+'.player' 

datel=[]
slatesizel=[]
gameIDl=[]
contestIDl=[]
contestnamel = []
maxentriesl=[]
totalentriesl=[]
playercountl=[]
prizesCountl=[]
prizestotalcashl=[]


plnamel=[]
plstatusl=[]
plsalaryl=[]
plppol=[]
plscorel=[]
plposl=[]
plstmrl=[]  
plstml =[]
plsthl =[]
plownl=[]
plteamsl=[]
pltophl=[]
#pathl=pathl[0:5]
for path in pathl:
	pdf = pd.DataFrame()
	qdf = pd.read_json(path)
	this_date = pd.to_datetime(time.strftime('%Y-%m-%d %H:%M', time.localtime(qdf['start'][0])))
	this_id = qdf['contestId'][0]
	plwr = player_writestr+'.'+str(this_id)
	#contestname = qdf['game']['name']
	#this_size = qdf['game']['size']['max']
	print '*******************', path,this_id,plwr
	for key,value in qdf['players'].iteritems():
		if isinstance(value, dict):
			plnamel.append(key)
			pdict = value['player']

			plstmrl.append( pdict['status']['missing_reason'])
			plstml.append(  pdict['status']['missing'] )
			plsthl.append(  pdict['status']['hidden']  )

			plposl.append(   pdict['position'])
			plsalaryl.append(1./1000*pdict['salary'])
			plscorel.append( pdict['score'])
			plownl.append(pdict['ppo'])
			plteamsl.append(value['teams'])

			pltophl.append( value.get('topHundred'))
		else: continue

	pdf['name'] = plnamel
	pdf['name'] = pdf['name'].apply(lambda x: x.encode('utf-8').strip())
	pdf['percent_own'] = plownl
	###
	###error with score in FD_data; going with home-computed
	#pdf['score'] = plscorel
	pdf['position']  = plposl
	pdf['salary'] = plsalaryl
	#pdf['n_teams'] = plteamsl
	pdf['top_hundred'] = pltophl
	pdf['top_hundred'].fillna(0,inplace=True)
	#pdf['st.missing'] = plstmrl
	#pdf['st.missing_reason'] =plstml
	#pdf['st.hidden'] =plsthl

	pdf['contest_ID'] = this_id
	pdf['date']= this_date
	pdf['start_time']=pdf['date'].dt.time
	pdf['date']=pdf['date'].dt.date

	#pdf['contest_name']=contestname
	#pdf['total_entries']  = this_size

	pdf = pdf.sort('percent_own',ascending=False)
	try:
		pdf.to_csv(plwr+'.csv',index=False)
	except:
		print 'Exception!'
		print pdf.name.values.tolist()

	plnamel=[]
	plstatusl=[]
	plsalaryl=[]
	plppol=[]
	plscorel=[]
	plposl=[]
	plstmrl=[]
	plstml =[]
	plsthl =[]
	plownl=[]
	
	plteamsl=[]
	pltophl=[]
	

######
######

for path in pathl:
	print 'path=',path
	qdf = pd.read_json(path)
	datel.append(pd.to_datetime(time.strftime('%Y-%m-%d %H:%M', time.localtime(qdf['start'][0]))))
	contestIDl.append(qdf['contestId'][0])
	playercountl.append(qdf['playerCount'][0])
	slatesizel.append(qdf['slateSize'][0])

	gameIDl.append(qdf['game']['id'])
	contestnamel.append(qdf['game']['name'])
	maxentriesl.append(qdf['game']['max_entries_per_user'])
	totalentriesl.append(qdf['game']['size']['max'])
	prizesCountl.append(qdf['game']['prizes']['count'])
	prizestotalcashl.append(qdf['game']['prizes']['total'])


tdf = pd.DataFrame()
tdf['contest_ID'] = contestIDl
tdf['contest_name']=contestnamel
tdf['date'] = datel 
tdf['start_time']=tdf['date'].dt.time
tdf['date']=tdf['date'].dt.date
tdf['game_ID'] = gameIDl 
tdf['slate_size'] = slatesizel 
tdf['max_entries_per_user'] = maxentriesl
tdf['total_entries'] = totalentriesl
tdf['n_prizes'] = prizesCountl
tdf['total_cash'] = prizestotalcashl
tdf.sort('date',ascending=True,inplace=True)
print tdf
print tournament_writestr+'.csv'
tdf.to_csv(tournament_writestr+'.csv',index=False)
