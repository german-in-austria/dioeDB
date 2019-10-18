"""Funktionen für Dateien."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from DB.funktionenDB import httpOutput
from django.http import HttpResponseServerError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.conf import settings
import os
from .models import sys_filesystem
import json


def view_dateien(request, ojson=False):
	"""Anzeige für Dateien."""
	info = ''
	error = ''
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		if ojson:
			return httpOutput(json.dumps({'error': 'PRIVATE_STORAGE_ROOT wurde nicht gesetzt!'}), 'application/json')
		else:
			return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	# Dateien hochladen:
	if 'upload' in request.POST:
		uplDir = removeLeftSlash(request.POST.get('upload'))
		if getPermission(uplDir, mDir, request) < 2:
			if ojson:
				return httpOutput(json.dumps({'error': 'no directory permission'}), 'application/json')
			else:
				return httpOutput('Fehler! Sie haben nicht die nötigen Rechte für dieses Verzeichnis!')
		uplDir = os.path.join(mDir, uplDir)
		from django.core.files.storage import FileSystemStorage
		fs = FileSystemStorage(location=mDir)
		import unicodedata
		for afile in request.FILES.getlist('dateien'):
			asavename = os.path.join(uplDir, afile.name)
			asavename = unicodedata.normalize('NFKD', asavename).encode('ascii', 'ignore').decode("utf-8")
			filename = fs.save(asavename, afile)
			LogEntry.objects.log_action(
				user_id=request.user.pk,
				content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
				object_id=0,
				object_repr='Datei',
				action_flag=ADDITION,
				change_message='Datei hinzugefügt: ' + filename
			)
		if ojson:
			return httpOutput(json.dumps({'file': 'uploaded'}), 'application/json')
		else:
			return httpOutput('OK')

	# Datei löschen:
	if 'delFile' in request.POST:
		delFile = removeLeftSlash(request.POST.get('delFile'))
		delFile = os.path.join(mDir, delFile)
		if getPermission(delFile, mDir, request) < 2:
			if ojson:
				return httpOutput(json.dumps({'error': 'no directory permission'}), 'application/json')
			else:
				return httpOutput('Fehler! Sie haben nicht die nötigen Rechte für dieses Verzeichnis!')
		if not os.path.isfile(delFile):
			if ojson:
				return httpOutput(json.dumps({'error': 'file dosn\'t exist'}), 'application/json')
			else:
				return httpOutput('Fehler! "' + request.POST.get('delFile') + '" existiert nicht oder ist keine Datei!')
		try:
			os.remove(delFile)
			LogEntry.objects.log_action(
				user_id=request.user.pk,
				content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
				object_id=0,
				object_repr='Datei',
				action_flag=DELETION,
				change_message='Datei gelöscht: ' + delFile
			)
			if ojson:
				return httpOutput(json.dumps({'file': 'removed'}), 'application/json')
			else:
				return httpOutput('OK')
		except Exception as e:
			if ojson:
				return httpOutput(json.dumps({'error': 'can\'t delete File'}), 'application/json')
			else:
				return httpOutput('Fehler! Datei "' + delFile + '" konnte nicht gelöscht werden! ' + str(e))

	# Datei umbenennen
	if 'renameFile' in request.POST:
		renameFile = request.POST.get('renameFile')
		if '/' in renameFile or '\\' in renameFile:
			if ojson:
				return httpOutput(json.dumps({'error': 'file has spezial character'}), 'application/json')
			else:
				return httpOutput('Fehler! Dateiname darf keine Sonderzeichen enthalten!')
		filename = request.POST.get('filename')
		fullpath = removeLeftSlash(request.POST.get('fullpath'))
		fullpathABS = os.path.join(mDir, fullpath)
		newfullpath = fullpath[:-len(filename)] + renameFile
		newfullpathABS = os.path.join(mDir, newfullpath)
		if getPermission(fullpath, mDir, request) < 2:
			if ojson:
				return httpOutput(json.dumps({'error': 'no directory permission'}), 'application/json')
			else:
				return httpOutput('Fehler! Sie haben nicht die nötigen Rechte für dieses Verzeichnis!')
		if not os.path.isfile(fullpathABS):
			if ojson:
				return httpOutput(json.dumps({'error': 'file dosn\'t exists'}), 'application/json')
			else:
				return httpOutput('Fehler! Datei "' + fullpath + '" existiert nicht!')
		if os.path.isfile(newfullpathABS):
			if ojson:
				return httpOutput(json.dumps({'error': 'file already exists'}), 'application/json')
			else:
				return httpOutput('Fehler! Datei "' + newfullpath + '" existiert bereits!')
		try:
			os.rename(fullpathABS, newfullpathABS)
			LogEntry.objects.log_action(
				user_id=request.user.pk,
				content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
				object_id=0,
				object_repr='Datei',
				action_flag=CHANGE,
				change_message='Datei umbenannt: ' + fullpathABS + ' -> ' + newfullpathABS
			)
			if ojson:
				return httpOutput(json.dumps({'file': 'renamed'}), 'application/json')
			else:
				return httpOutput('OK')
		except Exception as e:
			if ojson:
				return httpOutput(json.dumps({'error': 'can\'t rename file'}), 'application/json')
			else:
				return httpOutput('Fehler! Datei "' + fullpath + '" konnte nicht umbenannt werden! ' + str(e))

	# Verzeichnis erstellen:
	if 'makeDir' in request.POST:
		makeDir = request.POST.get('makeDir')
		if '/' in makeDir or '\\' in makeDir or '.' in makeDir:
			if ojson:
				return httpOutput(json.dumps({'error': 'file has spezial character'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnisname darf keine Sonderzeichen enthalten!')
		baseDir = removeLeftSlash(request.POST.get('baseDir'))
		makeDir = os.path.join(mDir, baseDir, makeDir)
		if getPermission(makeDir, mDir, request) < 3:
			if ojson:
				return httpOutput(json.dumps({'error': 'no directory permission'}), 'application/json')
			else:
				return httpOutput('Fehler! Sie haben nicht die nötigen Rechte für dieses Verzeichnis!')
		if not makeDir[:len(mDir)] == mDir:
			return httpOutput('Fehler! "' + makeDir[:len(mDir)] + '" != "' + mDir + '"')
		if os.path.isdir(makeDir):
			if ojson:
				return httpOutput(json.dumps({'error': 'directory already exists'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnis "' + makeDir + '" existiert bereits!')
		try:
			os.makedirs(makeDir)
			LogEntry.objects.log_action(
				user_id=request.user.pk,
				content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
				object_id=0,
				object_repr='Verzeichnis',
				action_flag=ADDITION,
				change_message='Verzeichnis erstellt: ' + makeDir
			)
			if ojson:
				return httpOutput(json.dumps({'directory': 'created'}), 'application/json')
			else:
				return httpOutput('OK')
		except Exception as e:
			if ojson:
				return httpOutput(json.dumps({'error': 'can\'t create directory'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnis "' + makeDir + '" konnte nicht erstellt werden! ' + str(e))

	# Verzeichnis umbenennen/löschen
	if 'renameDir' in request.POST:
		renameDir = request.POST.get('renameDir')
		if '/' in renameDir or '\\' in renameDir or '.' in renameDir:
			if ojson:
				return httpOutput(json.dumps({'error': 'directory has spezial character'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnisname darf keine Sonderzeichen enthalten!')
		subname = request.POST.get('subname')
		fullpath = removeLeftSlash(request.POST.get('fullpath'))
		fullpathABS = os.path.join(mDir, fullpath)
		newfullpath = fullpath[:-len(subname)] + renameDir
		newfullpathABS = os.path.join(mDir, newfullpath)
		if getPermission(fullpath, mDir, request) < 3:
			if ojson:
				return httpOutput(json.dumps({'error': 'no directory permission'}), 'application/json')
			else:
				return httpOutput('Fehler! Sie haben nicht die nötigen Rechte für dieses Verzeichnis!')
		if not os.path.isdir(fullpathABS):
			if ojson:
				return httpOutput(json.dumps({'error': 'directory didn\'t exist'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnis "' + fullpath + '" existiert nicht!')
		if renameDir == 'löschen':
			try:
				if getPermission(fullpath, mDir, request) > 3:
					for root, dirs, files in os.walk(fullpathABS, topdown=False):
						for name in files:
							os.remove(os.path.join(root, name))
						for name in dirs:
							os.rmdir(os.path.join(root, name))
				os.rmdir(fullpathABS)
				LogEntry.objects.log_action(
					user_id=request.user.pk,
					content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
					object_id=0,
					object_repr='Verzeichnis',
					action_flag=DELETION,
					change_message='Verzeichnis gelöscht: ' + fullpathABS
				)
				if ojson:
					return httpOutput(json.dumps({'directory': 'deleted'}), 'application/json')
				else:
					return httpOutput('OK')
			except Exception as e:
				if ojson:
					return httpOutput(json.dumps({'error': 'can\'t delete directory'}), 'application/json')
				else:
					return httpOutput('Fehler! Verzeichnis "' + fullpath + '" konnte nicht gelöscht werden! ' + str(e))
		if os.path.isdir(newfullpathABS):
			if ojson:
				return httpOutput(json.dumps({'error': 'directory already exist'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnis "' + newfullpath + '" existiert bereits!')
		try:
			os.rename(fullpathABS, newfullpathABS)
			LogEntry.objects.log_action(
				user_id=request.user.pk,
				content_type_id=ContentType.objects.get_for_model(sys_filesystem).pk,
				object_id=0,
				object_repr='Verzeichnis',
				action_flag=CHANGE,
				change_message='Verzeichnis umbenannt: ' + fullpathABS + ' -> ' + newfullpathABS
			)
			if ojson:
				return httpOutput(json.dumps({'directory': 'renamed'}), 'application/json')
			else:
				return httpOutput('OK')
		except Exception as e:
			if ojson:
				return httpOutput(json.dumps({'error': 'can\'t rename directory'}), 'application/json')
			else:
				return httpOutput('Fehler! Verzeichnis "' + fullpath + '" konnte nicht umbenannt werden! ' + str(e))

	# Dateienliste:
	if 'getDirContent' in request.POST:
		dateien = scanFiles(request.POST.get('getDirContent'), mDir, request)
		aPath = removeLeftSlash(request.POST.get('getDirContent'))
		if ojson:
			return httpOutput(json.dumps({'files': dateien, 'directory': request.POST.get('getDirContent'), 'permission': getPermission(aPath, mDir, request)}), 'application/json')
		else:
			return render_to_response(
				'DB/dateien.html',
				RequestContext(request, {'dateien': dateien, 'verzeichnis': request.POST.get('getDirContent'), 'permission': getPermission(aPath, mDir, request), 'info': info, 'error': error}),)

	# Startseite mit "Baum":
	tree = scanDir(mDir, None, request)
	if not ojson and 'getTree' in request.POST:
		return render_to_response(
			'DB/dateien_tree.html',
			RequestContext(request, {'sdir': tree}),)
	if ojson:
		return httpOutput(json.dumps({'basetree': tree}), 'application/json')
	else:
		return render_to_response(
			'DB/dateien_start.html',
			RequestContext(request, {'tree': tree, 'info': info, 'error': error}),)


# Funktionen:


def getPermission(pDir, bDir, request):
	"""Zugriffsrechte für aktuelles Verzeichnis ermitteln."""
	aPerm = 0
	pDir = removeLeftSlash(pDir)
	if request.user.is_superuser:
		aPerm = 3
	aAbsDir = os.path.join(bDir, pDir)
	if os.path.isfile(aAbsDir):
		aAbsDir = os.path.dirname(aAbsDir)
	for aUDir in request.user.user_verzeichnis_set.all():
		aAbsUDir = os.path.normpath(os.path.join(bDir, removeRightSlash(removeLeftSlash(aUDir.Verzeichnis))))
		if aAbsUDir == aAbsDir[:len(aAbsUDir)] and (len(aAbsUDir) == len(aAbsDir) or aAbsDir[len(aAbsUDir):len(aAbsUDir) + 1] == '\\' or aAbsDir[len(aAbsUDir):len(aAbsUDir) + 1] == '/'):
			if aUDir.Rechte and aUDir.Rechte > aPerm:
				aPerm = aUDir.Rechte
	for aUGroup in request.user.groups.all():
		for aUDir in aUGroup.group_verzeichnis_set.all():
			aAbsUDir = os.path.normpath(os.path.join(bDir, removeRightSlash(removeLeftSlash(aUDir.Verzeichnis))))
			if aAbsUDir == aAbsDir[:len(aAbsUDir)] and (len(aAbsUDir) == len(aAbsDir) or aAbsDir[len(aAbsUDir):len(aAbsUDir) + 1] == '\\' or aAbsDir[len(aAbsUDir):len(aAbsUDir) + 1] == '/'):
				if aUDir.Rechte and aUDir.Rechte > aPerm:
					aPerm = aUDir.Rechte
	return aPerm


def scanFiles(sDir, bDir, request):
	"""Liste der Dateien erstellen."""
	imgTypes = ['jpg', 'jpeg', 'png']
	import datetime
	_FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)

	def FiletimeToDateTime(ft):
		timestamp = ft.dwHighDateTime
		timestamp <<= 32
		timestamp |= ft.dwLowDateTime
		return _FILETIME_null_date + datetime.timedelta(microseconds=timestamp / 10)
	psUrl = removeRightSlash(getattr(settings, 'AUDIO_URL', None))
	sDir = removeLeftSlash(sDir)
	rFiles = []
	aDir = os.path.join(bDir, sDir)
	objectList = os.listdir(aDir)
	objectList.sort()
	for aObject in objectList:
		aObjectAbs = os.path.join(aDir, aObject)
		if os.path.isfile(aObjectAbs):
			aObjectDir = removeLeftSlash(aObjectAbs[len(bDir):])
			if os.stat_float_times():
				lmod = datetime.datetime.utcfromtimestamp(os.path.getmtime(aObjectAbs))
			else:
				lmod = os.path.getmtime(aObjectAbs)
			alink = os.path.normpath(aObjectDir).replace('\\', '/')
			if alink[0] == '/':
				alink = alink[1:]
			alink = psUrl + '/' + alink
			aObjectData = {'name': aObject, 'fullpath': aObjectDir, 'link': alink, 'size': os.path.getsize(aObjectAbs), 'lmod': lmod}
			if '.' in aObjectDir:
				aObjectData['type'] = aObjectDir.rsplit('.', 1)[1].lower()
				if aObjectDir.rsplit('.', 1)[1].lower() in imgTypes and '_temp' not in aObjectDir:
					prevFile = os.path.join(bDir, '_temp', aObjectDir)
					if not os.path.isdir(os.path.dirname(prevFile)):
						print(os.makedirs(os.path.dirname(prevFile)))
					if not os.path.exists(prevFile) or os.path.getmtime(prevFile) < os.path.getmtime(aObjectAbs):
						from PIL import Image
						im = Image.open(aObjectAbs)
						im.thumbnail((300, 200))
						im.save(prevFile, im.format)
					aObjectData['prvImg'] = os.path.normpath(prevFile[len(bDir):]).replace('\\', '/')
					if aObjectData['prvImg'][0] == '/':
						aObjectData['prvImg'] = aObjectData['prvImg'][1:]
					aObjectData['prvImg'] = psUrl + '/' + aObjectData['prvImg']
			rFiles.append(aObjectData)
	return rFiles


def scanDir(sDir, bDir, request):
	"""Verzeichnisliste erstellen."""
	rDirs = []
	if not bDir:
		bDir = sDir
		abPerm = getPermission('', bDir, request)
		if abPerm > 0:
			aObjectData = {'name': '...', 'fullpath': '', 'permission': abPerm}
			rDirs.append(aObjectData)
	try:
		objectList = os.listdir(sDir)
		objectList.sort()
		for aObject in objectList:
			if '_temp' not in aObject:
				aObjectAbs = os.path.join(sDir, aObject)
				if os.path.isdir(aObjectAbs):
					aObjectData = {'name': aObject, 'fullpath': aObjectAbs[len(bDir):], 'permission': getPermission(aObjectAbs[len(bDir):], bDir, request), 'subdir': scanDir(aObjectAbs, bDir, request)}
					for asub in aObjectData['subdir']:
						if ('permission' in asub and asub['permission'] > 0) or ('subperm' in asub and asub['subperm'] is True):
							aObjectData['subperm'] = True
					rDirs.append(aObjectData)
	except:
		pass
	return rDirs


# Sonstiges


def removeLeftSlash(aStr):
	"""Schrägstriche links entfernen."""
	if aStr and (aStr[0] == '\\' or aStr[0] == '/'):
		aStr = aStr[1:]
	return aStr


def removeRightSlash(aStr):
	"""Schrägstriche rechts entfernen."""
	if aStr and (aStr[-1] == '\\' or aStr[-1] == '/'):
		aStr = aStr[:-1]
	return aStr


def tree2select(tree, deep=0):
	"""Dateibaum in select umwanden."""
	select = []
	for aDir in tree:
		if aDir['permission'] > 0 or aDir['subperm']:
			select.append({'title': ('&nbsp;' * deep * (4 if deep > 1 else 2)) + ('+' if deep > 0 else '') + aDir['name'], 'value': os.path.normpath(aDir['fullpath'])})
			if 'subdir' in aDir:
				select = select + tree2select(aDir['subdir'], deep + 1)
	return select
