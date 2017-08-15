from django.shortcuts import render_to_response
from django.template import RequestContext
from DB.funktionenDB import httpOutput
from DB.funktionenDateien import getPermission, scanFiles, scanDir, removeLeftSlash, tree2select
from django.conf import settings
import datetime
import collections
import os, csv

def view_csv(request):
	info = ''
	error = ''
	# Test ...
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	adirABS = os.path.normpath(os.path.join(mDir,'csv'))
	if not os.path.isdir(adirABS):
		return httpOutput('Fehler: "csv" Verzeichniss existiert nicht!')
	tree = tree2select(scanDir(adirABS,adirABS,request))
	if not tree:
		return httpOutput('Fehler: Keine Zugriffsrechte für Verzeichniss!')
	csvSelDir = tree[0]['value']
	if 'csvSelDir' in request.POST:
		csvSelDir = request.POST.get('csvSelDir')
	csvSelDirABS = os.path.normpath(os.path.join(adirABS,removeLeftSlash(csvSelDir)))
	if not os.path.isdir(csvSelDirABS):
		return httpOutput('Fehler: Ausgewähltes Verzeichniss existiert nicht!')
	files = []
	for aFile in scanFiles(csvSelDirABS[len(mDir):],mDir,request):
		if aFile['type'] == 'csv':
			files.append({'title':aFile['name'],'value':aFile['name']})
	csvSelFile = None
	csvSelFileData = collections.OrderedDict()
	csvData = {}
	# Datei auswerten
	if 'csvSelFile' in request.POST:
		csvSelFile = request.POST.get('csvSelFile')
		csvSelFileABS = os.path.normpath(os.path.join(csvSelDirABS,removeLeftSlash(csvSelFile)))
		if not os.path.isfile(csvSelFileABS):
			return httpOutput('Fehler: Ausgewähltes Datei existiert nicht!')
		csvSelFileData['Name'] = csvSelFile
		if os.stat_float_times():
			lmod = datetime.datetime.utcfromtimestamp(os.path.getmtime(csvSelFileABS))
		else:
			lmod = os.path.getmtime(csvSelFileABS)
		csvSelFileData['Datum'] = lmod.strftime("%d.%m.%Y - %H:%M")+" Uhr"
		csvSelFileData['Größe'] = os.path.getsize(csvSelFileABS)
		csvData = getCsvData(getCsvFile(csvSelFileABS))
		csvSelFileData['Zeilen'] = csvData['rowCount']
		csvSelFileData['Spalten'] = csvData['colCount']

		# Testdaten
		# def errorCheckIDAufgabe(val):
		# 	from .models import tbl_aufgaben
		# 	aOutput = {'error':None,'errorID':None}
		# 	try:
		# 		aTblGet = tbl_aufgaben.objects.get(pk=int(val))
		# 		aOutput['conTable'] = aTblGet
		# 	except:
		# 		aOutput['errorID'] = 'tbl_aufgaben_not_exist'
		# 		aOutput['error'] = 'Aufgabe ist in der Datenbank nicht vorhanden!'
		# 	return aOutput
		from .models import tbl_aufgaben
		from PersonenDB.models import tbl_informanten
		csvImportData = {
			'cols':{
				'ID_Aufgabe':{				# Aufgaben ID
					#'errorCheck': {'type':'fxfunction','fxfunction':errorCheckIDAufgabe}
					'errorCheck': {'type':'pkInTable','table':tbl_aufgaben}
				},
				'count_BlackKon':{			# Reihenfolge der Aufgabe
					'convert': {'type':'int'}
				},
				'datetime': {				# Zeitpunkt der Erhebung
					'convert': {'type':'datetime'},
					'errorCheck': {'type':'datetime'}
				},
				'logfile': {				# Eigener Filename; sollte hinweis geben, zu welchem Ort die Erhebung ist, und zu welcher Person (letzte drei Ziffern = Inf_Sigle)
				},
				'subject_nr': {				# Inf_sigle (sollte Inf_sigle von Inf_erh entsprechen)
					'convert': {'type':'trim'}
				},
				'time_Blackscreen': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
					'convert': {'type':'int'}
				},
				'time_Blackscreen_1': {		# das ist nur für das erste SET die Zeiten
					'convert': {'type':'int'},
					'errorCheck': {'type':'convert'}
				},
				'time_Logg_all': {			# Ich denke, auch das könnte als Endzeitpunkt für eine Einzelaufgabe genommen werden; ist vielleicht sogar exakter; müssen wir ausprobieren, sieht aber relativ gut aus
					'convert': {'type':'int'},
					'errorCheck': {'type':'convert'}
				},
				'time_beep': {				# TIME_BEEP! Das so in tbl_inferhebung übernehmen; die Synctime müssen die Leute selbst eingeben
					'convert': {'type':'int'},
					'errorCheck': {'type':'convert'}
				}
			}
		}

		# CSV analysieren
		csvData['colUse'] = []
		for key, val in csvImportData['cols'].items():
			csvData['csvCountImport'][key] = 0
			csvData['colUse'].append(key)
		for csvRow in csvData['rows']:
			rowHasError = 0
			# Werte umwandeln
			for key, val in csvImportData['cols'].items():
				if key in csvData['colDef']:
					if 'convert' in val and not val['convert']['type'] == None:
						if val['convert']['type'] == 'fxfunction':			# Eigene Funktion für umwandlung
							csvRow['cols'][key].update(val['convert']['fxfunction'](csvRow['cols'][key]['value']))
						elif val['convert']['type'] == 'int':				# In Ganzzahl umwandeln
							csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
							try:
								csvRow['cols'][key]['value'] = int(csvRow['cols'][key]['value'])
							except:
								csvRow['cols'][key]['value'] = 0
								csvRow['cols'][key]['convertError'] = True
						elif val['convert']['type'] == 'trim':				# Trim String
							csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
							try:
								csvRow['cols'][key]['value'] = trim(csvRow['cols'][key]['value'])
							except:
								csvRow['cols'][key]['convertError'] = True
						elif val['convert']['type'] == 'datetime':		# Datum Uhrzeit? (03/30/17 12:22:22)
							csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
							try:
								csvRow['cols'][key]['value'] = datetime.datetime.strptime(csvRow['cols'][key]['value'], '%m/%d/%y %H:%M:%S')
							except:
								csvRow['cols'][key]['value'] = datetime.datetime(1970, 1, 1, 0, 0, 0)
								csvRow['cols'][key]['convertError'] = True
						else:
							csvRow['cols'][key].update({'error':'"convert" -> "type" = "'+val['convert']['type']+'" nicht bekannt!','errorID':'converttype_unknowen'})
			# Fehler Prüfung
			for key, val in csvImportData['cols'].items():
				if key in csvData['colDef']:
					if 'errorCheck' in val and not val['errorCheck']['type'] == None:
						if val['errorCheck']['type'] == 'fxfunction':		# Eigene Funktion für ErrorCheck
							csvRow['cols'][key].update(val['errorCheck']['fxfunction'](csvRow['cols'][key]['value']))
						elif val['errorCheck']['type'] == 'pkInTable':		# Ist der Eintrag in der Tabelle vorhanden?
							csvRow['cols'][key].update({'error':None,'errorID':None})
							try:
								aTblGet = val['errorCheck']['table'].objects.get(pk=int(csvRow['cols'][key]['value']))
								csvRow['cols'][key]['conTable'] = aTblGet
							except:
								csvRow['cols'][key]['errorID'] = 'tbl_not_exist'
								csvRow['cols'][key]['error'] = 'Eintrag ist in der Datenbank nicht vorhanden!'
						elif val['errorCheck']['type'] == 'datetime':		# Datum Uhrzeit? (03/30/17 12:22:22)
							csvRow['cols'][key].update({'error':None,'errorID':None})
							if 'convertError' in csvRow['cols'][key] and csvRow['cols'][key]['convertError'] == True:
								csvRow['cols'][key]['errorID'] = 'date_error'
								csvRow['cols'][key]['error'] = 'Das Datum konnte nicht umgewandelt werden! (%m/%d/%y %H:%M:%S)'
						elif val['errorCheck']['type'] == 'convert':
							csvRow['cols'][key].update({'error':None,'errorID':None})
							if 'convertError' in csvRow['cols'][key] and csvRow['cols'][key]['convertError'] == True:
								csvRow['cols'][key]['errorID'] = 'convert_error'
								csvRow['cols'][key]['error'] = 'Das Feld konnte nicht umgewandelt werden!'
						else:
							csvRow['cols'][key].update({'error':'"errorCheck" -> "type" = "'+val['errorCheck']['type']+'" nicht bekannt!','errorID':'errortype_unknowen'})
					else:
						csvRow['cols'][key].update({'error':None,'errorID':None})
					if csvRow['cols'][key]['error'] == None:
						csvData['csvCountImport'][key]+=1
					else:
						if not key in csvData['colError']:
							csvData['colError'][key] = {}
						csvData['colError'][key][csvRow['cols'][key]['errorID']] = csvRow['cols'][key]['error']
						rowHasError = 1
			# Vorschau Daten
			if len(csvData['dispRows']) < 10 or (rowHasError == 1 and len(csvData['dispRows']) < 20):
				csvData['dispRows'].append(csvRow)
		for key, val in csvImportData['cols'].items():
			if csvData['csvCountImport'][key]<csvData['rowCount']:
				if csvData['csvCountImport'][key] == 0:
					error+= 'Spalte "<b>'+key+'</b>" fehlt!<br>'
				else:
					error+= 'Spalte "<b>'+key+'</b>" unvollständig! ('+str(csvData['csvCountImport'][key])+'/'+str(csvSelFileData['Zeilen'])+')<br>'
	if 'csvSelDirCol' in request.POST:
		return render_to_response('korpusdb/csv_selectcol.html',
			RequestContext(request, {'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData}),)

	return render_to_response('korpusdb/csv_start.html',
		RequestContext(request, {'csvData':csvData,'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData,'info':info,'error':error}),)

def getCsvData(rows):
	csvData = {'colDef':[],'rows':[],'dispRows':[],'colError':{},'rowCount':0,'colCount':0,'csvCountImport':{}}
	for csvRow in rows:
		if csvData['rowCount'] == 0:
			for csvCell in csvRow:
				csvData['colCount']+=1
				csvData['colDef'].append(csvCell)
		else:
			aCell = 0
			aRowData = {}
			for csvCell in csvRow:
				aRowData[csvData['colDef'][aCell]] = {'value': csvCell}
				aCell+=1
			csvData['rows'].append({'nr': csvData['rowCount'],'cols':aRowData})
		csvData['rowCount']+=1
	csvData['rowCount']-=1
	return csvData

def getCsvFile(file):
	csvRows = []
	with open(file, encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			csvRows.append(row)
	return csvRows
