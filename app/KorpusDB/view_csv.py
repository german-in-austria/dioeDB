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
	for aFile in scanFiles(csvSelDirABS,mDir,request):
		if aFile['type'] == 'csv':
			files.append({'title':aFile['name'],'value':aFile['name']})
	csvSelFile = None
	csvSelFileData = collections.OrderedDict()
	csvRows = []
	csvData = {}
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
		with open(csvSelFileABS, encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
			aLine = 0
			for row in reader:
				aLine+=1
				csvRows.append(row)
		csvSelFileData['Zeilen'] = aLine-1
		# CSV analysieren
		aRow = 0
		rowErrors = 0
		csvData = {'colDef':[],'colUse':['ID_Aufgabe'],'rows':[],'dispRows':[],'colError':{}}
		csvCountImport = {'ID_Aufgabe':0}
		from .models import tbl_aufgaben
		for csvRow in csvRows:
			aRow+=1
			if aRow == 1:
				for csvCell in csvRow:
					csvData['colDef'].append(csvCell)
			else:
				aCell = 0
				aRowData = {}
				for csvCell in csvRow:
					rowHasError = 0
					aRowData[csvData['colDef'][aCell]] = {'value': csvCell}
					# Feld auf Fehler überprüfen!
					if csvData['colDef'][aCell] == 'ID_Aufgabe':
						try:
							aTblGet = tbl_aufgaben.objects.get(pk=int(csvCell))
							aRowData[csvData['colDef'][aCell]]['conTable'] = aTblGet
							csvCountImport['ID_Aufgabe']+=1
						except:
							if not csvData['colDef'][aCell] in csvData['colError']:
								csvData['colError'][csvData['colDef'][aCell]] = {}
							aRowData[csvData['colDef'][aCell]]['error'] = 'Aufgabe ist in der Datenbank nicht vorhanden!'
							csvData['colError'][csvData['colDef'][aCell]]['tbl_aufgaben_nx'] = aRowData[csvData['colDef'][aCell]]['error']
							rowHasError = 1
					aCell+=1
				csvData['rows'].append(aRowData)
				if aRow < 12:
					csvData['dispRows'].append(aRowData)
				elif rowHasError == 1:
					rowErrors+=1
					if rowErrors < 12:
						csvData['dispRows'].append(aRowData)
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
