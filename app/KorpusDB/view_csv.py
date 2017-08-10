from django.shortcuts import render_to_response
from django.template import RequestContext
from DB.funktionenDB import httpOutput
from .view_dateien import getPermission, scanFiles, scanDir, removeLeftSlash, tree2select
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
		csvData['colUse'] = ['ID_Aufgabe']

		# CSV analysieren
		from .models import tbl_aufgaben
		csvCountImport = {'ID_Aufgabe':0}
		for csvRow in csvData['rows']:
			rowHasError = 0
			# Fehler Prüfung für 'ID_Aufgabe'
			if 'ID_Aufgabe' in csvData['colDef']:
				try:
					aTblGet = tbl_aufgaben.objects.get(pk=int(csvRow['cols']['ID_Aufgabe']['value']))
					csvRow['cols']['ID_Aufgabe']['conTable'] = aTblGet
					csvCountImport['ID_Aufgabe']+=1
				except:
					if not 'ID_Aufgabe' in csvData['colError']:
						csvData['colError']['ID_Aufgabe'] = {}
					csvRow['cols']['ID_Aufgabe']['error'] = 'Aufgabe ist in der Datenbank nicht vorhanden!'
					csvData['colError']['ID_Aufgabe']['tbl_aufgaben_nx'] = csvRow['cols']['ID_Aufgabe']['error']
					rowHasError = 1
			# Vorschau Daten
			if len(csvData['dispRows']) < 10 or (rowHasError == 1 and len(csvData['dispRows']) < 20):
				csvData['dispRows'].append(csvRow)
		if csvCountImport['ID_Aufgabe']<csvSelFileData['Zeilen']:
			if csvCountImport['ID_Aufgabe'] == 0:
				error+= 'Spalte "<b>ID_Aufgabe</b>" fehlt!<br>'
			else:
				error+= 'Spalte "<b>ID_Aufgabe</b>" unvollständig! ('+str(csvCountImport['ID_Aufgabe'])+'/'+str(csvSelFileData['Zeilen'])+')<br>'
	if 'csvSelDirCol' in request.POST:
		return render_to_response('korpusdb/csv_selectcol.html',
			RequestContext(request, {'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData}),)

	return render_to_response('korpusdb/csv_start.html',
		RequestContext(request, {'csvData':csvData,'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData,'info':info,'error':error}),)

def getCsvData(rows):
	csvData = {'colDef':[],'rows':[],'dispRows':[],'colError':{},'rowCount':0,'colCount':0}
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
	return csvData

def getCsvFile(file):
	csvRows = []
	with open(file, encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			csvRows.append(row)
	return csvRows
