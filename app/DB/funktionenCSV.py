from django.apps import apps
import datetime
import os, csv


def getCsvFile(file):
	csvRows = []
	with open(file, encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			csvRows.append(row)
	return csvRows

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

def csvDataConverter(csvData,csvImportData):
	if not 'colUse' in csvData:
		csvData['colUse'] = []
	for key, val in csvImportData['cols'].items():
		csvData['csvCountImport'][key] = 0
		csvData['colUse'].append(key)
	for csvRow in csvData['rows']:
		# Werte umwandeln
		for key, val in csvImportData['cols'].items():
			if key in csvData['colDef']:
				if 'convert' in val:
					for aconvert in val['convert']:
						if not aconvert['type'] == None:
							if aconvert['type'] == 'fxfunction':			# Eigene Funktion für umwandlung
								csvRow['cols'][key].update(aconvert['fxfunction'](csvRow['cols'][key]['value']))
							elif aconvert['type'] == 'int':				# In Ganzzahl umwandeln
								csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
								try:
									csvRow['cols'][key]['value'] = int(csvRow['cols'][key]['value'])
								except:
									csvRow['cols'][key]['value'] = 0
									csvRow['cols'][key]['convertError'] = True
							elif aconvert['type'] == 'trim':				# Trim String
								csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
								try:
									csvRow['cols'][key]['value'] = trim(csvRow['cols'][key]['value'])
								except:
									csvRow['cols'][key]['convertError'] = True
							elif aconvert['type'] == 'datetime':		# Datum Uhrzeit? (03/30/17 12:22:22)
								csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
								try:
									csvRow['cols'][key]['value'] = datetime.datetime.strptime(csvRow['cols'][key]['value'], '%m/%d/%y %H:%M:%S')
								except:
									csvRow['cols'][key]['value'] = datetime.datetime(1970, 1, 1, 0, 0, 0)
									csvRow['cols'][key]['convertError'] = True
							elif aconvert['type'] == 'duration':		# In Dauer (duration) umwandeln
								csvRow['cols'][key]['orgValue'] = csvRow['cols'][key]['value']
								try:
									csvRow['cols'][key]['value'] = datetime.timedelta(seconds=int(csvRow['cols'][key]['value'])/1000)
								except:
									csvRow['cols'][key]['value'] = datetime.timedelta(seconds=0)
									csvRow['cols'][key]['convertError'] = True
							else:
								csvRow['cols'][key].update({'error':'"convert" -> "type" = "'+aconvert['type']+'" nicht bekannt!','errorID':'converttype_unknowen'})
	return csvData

def csvDataErrorCheck(csvData,csvImportData):
	rowHasError = 0 ; colAlwaysSame = {}
	for csvRow in csvData['rows']:
		for key, val in csvImportData['cols'].items():
			if key in csvData['colDef']:
				if 'errorCheck' in val:
					for aErrorCheck in val['errorCheck']:
						if not aErrorCheck['type'] == None:
							if not 'error' in csvRow['cols'][key]:
								csvRow['cols'][key].update({'error':None,'errorID':None})
							if aErrorCheck['type'] == 'fxfunction':		# Eigene Funktion für ErrorCheck
								csvRow['cols'][key].update(aErrorCheck['fxfunction'](csvRow['cols'][key]['value']))
							elif aErrorCheck['type'] == 'pkInTable':		# Ist der Eintrag in der Tabelle vorhanden?
								try:
									aTblGet = apps.get_model(aErrorCheck['app'], aErrorCheck['table']).objects.get(pk=int(csvRow['cols'][key]['value']))
									csvRow['cols'][key]['conTable'] = aTblGet
								except:
									csvRow['cols'][key]['errorID'] = 'tbl_not_exist'
									csvRow['cols'][key]['error'] = 'Eintrag ist in der Datenbank nicht vorhanden!'
							elif aErrorCheck['type'] == 'datetime':		# Datum Uhrzeit? (03/30/17 12:22:22)
								if 'convertError' in csvRow['cols'][key] and csvRow['cols'][key]['convertError'] == True:
									csvRow['cols'][key]['errorID'] = 'date_error'
									csvRow['cols'][key]['error'] = 'Das Datum konnte nicht umgewandelt werden! (%m/%d/%y %H:%M:%S)'
							elif aErrorCheck['type'] == 'convert':
								if 'convertError' in csvRow['cols'][key] and csvRow['cols'][key]['convertError'] == True:
									csvRow['cols'][key]['errorID'] = 'convert_error'
									csvRow['cols'][key]['error'] = 'Das Feld konnte nicht umgewandelt werden!'
							elif aErrorCheck['type'] == 'colAlwaysSame':
								if not key in colAlwaysSame:
									colAlwaysSame[key] = csvRow['cols'][key]['value']
								else:
									if not csvRow['cols'][key]['value'] == colAlwaysSame[key]:
										csvRow['cols'][key]['errorID'] = 'colAlwaysSame_error'
										csvRow['cols'][key]['error'] = 'Die Spalte "'+key+'" enthält unterschiedliche Werte!'
							else:
								csvRow['cols'][key].update({'error':'"errorCheck" -> "type" = "'+aErrorCheck['type']+'" nicht bekannt!','errorID':'errortype_unknowen'})
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
			if not 'error' in csvData:
				csvData['error'] = ''
			if csvData['csvCountImport'][key] == 0:
				csvData['error']+= 'Spalte "<b>'+key+'</b>" fehlt!<br>'
			else:
				csvData['error']+= 'Spalte "<b>'+key+'</b>" unvollständig! ('+str(csvData['csvCountImport'][key])+'/'+str(csvData['rowCount'])+')<br>'
	return csvData
