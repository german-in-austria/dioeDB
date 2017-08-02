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
	if 'csvSelFile' in request.POST:
		csvSelFile = request.POST.get('csvSelFile')
		csvSelFileABS = os.path.normpath(os.path.join(csvSelDirABS,removeLeftSlash(csvSelFile)))
		if not os.path.isfile(csvSelFileABS):
			return httpOutput('Fehler: Ausgewähltes Datei existiert nicht!')
		csvSelFileData['Name:'] = csvSelFile
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


	if 'csvSelDirCol' in request.POST:
		return render_to_response('korpusdb/csv_selectcol.html',
			RequestContext(request, {'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData}),)

	return render_to_response('korpusdb/csv_start.html',
		RequestContext(request, {'csvRows':csvRows,'tree':tree,'csvSelDir':csvSelDir,'files':files,'csvSelFile':csvSelFile,'csvSelFileData':csvSelFileData,'info':info,'error':error}),)
