"""Anzeigen für KorpusDB."""
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.template import loader
from DB.funktionenDB import formularView
from DB.funktionenDB import findDicValInList
from DB.funktionenDB import httpOutput
from DB.funktionenAuswertung import auswertungView
from django.http import HttpResponseServerError
import KorpusDB.models as KorpusDB


def aufgabensets(request):
	"""Anzeige für Aufgabensets."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_aufgabensets'
	permName = 'aufgabensets'
	primaerId = 'aufgabenset'
	aktueberschrift = 'Aufgabensets'
	asurl = '/korpusdb/aufgabensets/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Aufgabenset', 'app': 'KorpusDB', 'tabelle': 'tbl_aufgabensets', 'id': 'aufgabenset', 'optionen': ['einzeln'],
		'felder':['+id', 'Kuerzel', 'Name_Aset', 'Fokus', 'Art_ASet', 'Kommentar', 'zu_Phaenomen', '|zusammengestellt_als=aufgabenzusammenstellung:id'],
		'sub':[
			{
				'titel': 'Aufgaben', 'app': 'KorpusDB', 'tabelle': 'tbl_aufgaben', 'id': 'aufgabe', 'optionen': ['liste'],
				'felder': ['+id', 'Variante', 'stimulus_dialekt', 'evokziel_dialekt', 'Beschreibung_Aufgabe', '|von_ASet=parent:id'],
				'sub': [
					{
						'titel': 'Antwortmoeglichkeiten', 'app': 'KorpusDB', 'tabelle': 'tbl_antwortmoeglichkeiten', 'id': 'antwortmoeglichkeit', 'optionen': ['liste'],
						'felder': ['+id', 'Kuerzel', 'frei', '|Reihung=auto:reihung', '|zu_Aufgabe=parent:id']
					}, {
						'titel': 'Aufgabenfiles', 'app': 'KorpusDB', 'tabelle': 'tbl_aufgabenfiles', 'id': 'aufgabenfiles', 'optionen': ['liste'],
						'felder':['+id', 'id_Mediatyp', 'ist_Anweisung', 'File_Link', 'Kommentar', '|Reihung=auto:reihung', '|id_Aufgabe=parent:id']
					}
				]
			},
			{
				'titel': 'Aufgabenzusammenstellung', 'app': 'KorpusDB', 'tabelle': 'tbl_aufgabenzusammenstellungen', 'id': 'aufgabenzusammenstellung', 'optionen': ['einzeln'],
				'felder':['+id=parent:zusammengestellt_als', 'Bezeichnung_AZus', 'Kommentar', 'AZusCol'],
				'sub':[
					{
						'titel': 'Beinhaltete Medientypen', 'app': 'KorpusDB', 'tabelle': 'tbl_azusbeinhaltetmedien', 'id': 'azusbeinhaltetmedien', 'optionen': ['liste'],
						'felder':['+id', 'id_Mediatyp', '|Reihung=auto:reihung', '|id_AZus=parent:id']
					}
				]
			}
		]
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def tagsedit(request):
	"""Anzeige Tageditor."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_tags'
	permName = 'tags'
	primaerId = 'tags'
	aktueberschrift = 'Tags'
	asurl = '/korpusdb/tagsedit/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Tag', 'titel_plural': 'Tags', 'app': 'KorpusDB', 'tabelle': 'tbl_tags', 'id': 'tags', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'Tag', 'Tag_lang', 'zu_Phaenomen', 'Kommentar', 'Generation', 'AReihung'],
		'sub':[
			{
				'titel': 'Tag Familie - Parent', 'titel_plural': 'Tag Familie - Parents', 'app': 'KorpusDB', 'tabelle': 'tbl_tagfamilie', 'id': 'tagfamilieparents', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_ChildTag=parent:id', 'id_ParentTag'],
				'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ParentTag">{% getFeldVal aData.felder \'id_ParentTag\' %}</span>',
			},
			{
				'titel': 'Tag Familie - Child', 'titel_plural': 'Tag Familie - Childs', 'app': 'KorpusDB', 'tabelle': 'tbl_tagfamilie', 'id': 'tagfamiliechilds', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_ParentTag=parent:id', 'id_ChildTag'],
				# 'feldoptionen':{'id_ChildTag': {'foreignkey_select': {'data': {'generation': 'Generation'}, 'select_data': {'tagedit': '+1', 'taggentar': '#fid_Generation_1_1'}}, }},
				'elementtitel': '{% load dioeTags %} - <span data-formtitel="id_ChildTag">{% getFeldVal aData.felder \'id_ChildTag\' %}</span>',
			},
			{
				'titel': 'Tag Ebene zu Tag', 'titel_plural': 'Tag Ebenen zu Tag', 'app': 'KorpusDB', 'tabelle': 'tbl_tagebenezutag', 'id': 'tagebenezutag', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_Tag=parent:id', 'id_TagEbene'],
				'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
		],
		'suboption':['tab'],
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def presettagsedit(request):
	"""Ansicht für Preset Tags Editor."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'sys_presettags'
	permName = 'presettags'
	primaerId = 'presettags'
	aktueberschrift = 'Tags'
	asurl = '/korpusdb/presettagsedit/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Preset Tags', 'titel_plural': 'Presets Tags', 'app': 'KorpusDB', 'tabelle': 'sys_presettags', 'id': 'presettags', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'Bezeichnung', 'Kommentar', 'Reihung'],
		'sub':[
			{
				'titel': 'Tag zu Preset Tags', 'titel_plural': 'Tags zu Preset Tags', 'app': 'KorpusDB', 'tabelle': 'sys_tagszupresettags', 'id': 'tagszupresettags', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_PresetTags=parent:id', 'id_Tag', '|Reihung=auto:reihung'],
				'elementtitel': '{% load dioeTags %} - <span data-formtitel="id_Tag">{% getFeldVal aData.felder \'id_Tag\' %}</span>',
			},
			{
				'titel': 'Tag Ebene zu Preset Tags', 'titel_plural': 'Tag Ebenen zu Preset Tags', 'app': 'KorpusDB', 'tabelle': 'sys_tagebenezupresettags', 'id': 'tagebenezupresettags', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_PresetTags=parent:id', 'id_TagEbene'],
				'elementtitel': '{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
			{
				'titel': 'Preset Tags zu Aufgabe', 'titel_plural': 'Presets Tags zu Aufgabe', 'app': 'KorpusDB', 'tabelle': 'sys_presettagszuaufgabe', 'id': 'presettagszuaufgabe', 'optionen': ['liste', 'elementeclosed'],
				'felder': ['+id', '|id_PresetTags=parent:id', 'id_Aufgabe'],
				'elementtitel': '{% load dioeTags %} - <span data-formtitel="id_Aufgabe">{% getFeldVal aData.felder \'id_Aufgabe\' %}</span>',
			},
		],
		'suboption':['tab']
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def inferhebungupdateaudioduration(request):
	import os
	from django.conf import settings
	from DB.funktionenDateien import getPermission, removeLeftSlash
	from DB.tinytag import TinyTag
	import datetime
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	updated = ''
	for aInf in KorpusDB.tbl_inferhebung.objects.all():
		updated += str(aInf.pk)
		if not aInf.Audioduration:
			if aInf.Dateipfad and aInf.Audiofile:
				aFileABS = os.path.normpath(os.path.join(mDir, removeLeftSlash(aInf.Dateipfad), removeLeftSlash(aInf.Audiofile)))
				err = False
				if not os.path.isfile(aFileABS):
					updated += ' - ignoriert - Datei?'
					err = True
				if not getPermission(removeLeftSlash(aInf.Dateipfad), mDir, request) > 0:
					updated += ' - ignoriert - Rechte?'
					err = True
				if not err:
					fileInfo = TinyTag.get(aFileABS)
					if fileInfo and fileInfo.duration:
						aInf.Audioduration = datetime.timedelta(microseconds=int(float(fileInfo.duration) * 1000000))
						aInf.save()
						updated += ' - gesetzt - ' + str(fileInfo.duration)
					else:
						updated += ' - ignoriert - TinyTag?'
			else:
				updated += ' - ignoriert - Pfad?'
		else:
			updated += ' - ignoriert - ' + str(aInf.Audioduration)
		updated += ' - ' + str(aInf) + '\n'
	return httpOutput(updated)


def inferhebung(request):
	"""Anzeige für InfErhebungen."""
	from DB.tinytag import TinyTag
	from DB.funktionenDateien import getPermission, scanFiles, scanDir, removeLeftSlash, tree2select
	from django.conf import settings
	import os
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_inferhebung'
	permName = 'aufgabensets'
	primaerId = 'inferhebung'
	aktueberschrift = 'InfErhebungen'
	asurl = '/korpusdb/inferhebung/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	# erhInfAufgabe für Fragebögen erstellen:
	if 'erhinfaufgabefxfunction' in request.POST and int(request.POST.get('erhinfaufgabefxfunction')) == 1:
		from django.apps import apps
		import datetime
		info += '<b>ErhInfAufgabe aktuallisieren:</b><br>'
		aElement = apps.get_model(app_name, tabelle_name).objects.get(pk=int(request.POST.get('gettableview')))
		for aErhMitAufg in aElement.ID_Erh.tbl_erhebung_mit_aufgaben_set.all():
			info += str(aErhMitAufg) + ' - '
			if KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=aErhMitAufg.id_Aufgabe.pk, id_InfErh=aElement.pk).count() > 0:
				info += '<i>bereits vorhanden.</i>'
			else:
				asErhinfaufgaben = KorpusDB.tbl_erhinfaufgaben()
				asErhinfaufgaben.id_Aufgabe = aErhMitAufg.id_Aufgabe
				asErhinfaufgaben.id_InfErh = aElement
				asErhinfaufgaben.start_Aufgabe = datetime.timedelta(microseconds=0)
				asErhinfaufgaben.stop_Aufgabe = datetime.timedelta(microseconds=0)
				asErhinfaufgaben.save()
				info += '<b>erstellt.</b>'
			info += '<br>'
	if 'antwortenmitsaetzenfxfunction' in request.POST and int(request.POST.get('antwortenmitsaetzenfxfunction')) == 1:
		from django.apps import apps
		import datetime
		aElement = apps.get_model(app_name, tabelle_name).objects.get(pk=int(request.POST.get('gettableview')))
		if aElement.tbl_inf_zu_erhebung_set.count() == 1:
			info += '<b>Antworten mit Sätzen aktuallisieren:</b><br>'
			for aErhInfAufgaben in aElement.tbl_erhinfaufgaben_set.all():
				info += 'Antwort zu Aufgabe "' + str(aErhInfAufgaben.id_Aufgabe) + '" - '
				if aErhInfAufgaben.id_Aufgabe.tbl_antworten_set.filter(von_Inf_id=aElement.tbl_inf_zu_erhebung_set.first().ID_Inf_id):
					info += '<i>bereits vorhanden.</i>'
				else:
					asSatz = KorpusDB.tbl_saetze()
					asSatz.Standardorth = aErhInfAufgaben.id_Aufgabe.Aufgabenstellung
					asSatz.save()
					asAntwort = KorpusDB.tbl_antworten()
					asAntwort.von_Inf_id = aElement.tbl_inf_zu_erhebung_set.first().ID_Inf_id
					asAntwort.zu_Aufgabe = aErhInfAufgaben.id_Aufgabe
					asAntwort.Reihung = 0
					asAntwort.ist_Satz = asSatz
					asAntwort.start_Antwort = datetime.timedelta(microseconds=0)
					asAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
					asAntwort.save()
					info += '<b>erstellt.</b>'
				info += '<br>'
		else:
			error += 'Der Erhebung darf nur <b>ein</b> Informant zugewiesen sein!<br>'

	if 'stxsmfxfunction' in request.POST and int(request.POST.get('stxsmfxfunction')) == 1:
		from django.apps import apps
		# import datetime
		aElement = apps.get_model(app_name, tabelle_name).objects.get(pk=int(request.POST.get('gettableview')))
		aDir = ''
		aFile = ''
		aFileABS = None
		aStxsmFile = None
		# Audio Datei ermitteln:
		aDir = removeLeftSlash(aElement.Dateipfad)
		aFile = removeLeftSlash(aElement.Audiofile)
		if aDir and aFile:
			aFileABS = os.path.normpath(os.path.join(mDir, aDir, aFile))
		# stxsm Datei ermitteln:
		if aFileABS and os.path.isfile(aFileABS):
			if os.path.isfile(aFileABS + '.stxsm'):
				aStxsmFile = aFileABS + '.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.wav.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.wav.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.ogg.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.ogg.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.mp3.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.mp3.stxsm'
		if aStxsmFile:
			import re
			import datetime
			# Datei auswerten
			with open(aStxsmFile, 'r', encoding="utf-8") as file:
				aStxsmData = file.read()
			aHerz = int(re.findall('<AFile[^>]+SR="(\d+)"[^>]+>', aStxsmData)[0])
			aASegs = []
			for aASeg in re.findall('<ASeg[^>]+ID=".+"[^>]+>', aStxsmData):
				iType = re.findall('Type="uncl"', aASeg)
				aIdS = re.findall('ID="([^"]+)"', aASeg)[0].split('.')[0]
				if (not iType or len(iType) == 0) and not aIdS == 'Signal':
					aASegs.append(aASeg)
			aAIdList = {}
			aIdListFile = 'pp02_stxsm0.csv'
			if aElement and aElement.ID_Erh and aElement.ID_Erh.id >= 38 and aElement.ID_Erh.id <= 44:
				aIdListFile = 'pp02_p2_stxsm0.csv'
			with open(os.path.join(getattr(settings, 'BASE_DIR', None), 'KorpusDB', 'fx', aIdListFile), 'r', encoding="utf-8") as file:
				dg = 0
				for aLine in file:
					if dg > 0:
						[tId, tFx] = aLine.strip().split(';')
						aAIdList[tFx] = int(tId)
					dg += 1
			aTagList = {}
			with open(os.path.join(getattr(settings, 'BASE_DIR', None), 'KorpusDB', 'fx', 'pp02_translation_tags_2.csv'), 'r', encoding="utf-8") as file:
				dg = 0
				for aLine in file:
					if dg > 0:
						[tName, tId, tDbName] = aLine.strip().split(';')
						aTagList[tName] = [int(tId), tDbName]
					dg += 1
			for aASeg in aASegs:
				aId = re.findall('ID="([^"]+)"', aASeg)[0]
				aId = re.findall('ID="([^"]+)"', aASeg)[0]
				if aId.split('.')[-1] == 'ATL':
					aFx = '.'.join(aId.split('.')[-3:-1])
				else:
					aFx = '.'.join(aId.split('.')[-2:])
				if aFx in aAIdList:
					aAid = aAIdList[aFx]
				else:
					aAid = None
					error += '"' + aFx + '" konnte keiner Aufgaben ID zugewiesen werden! (e1)<br>'
				aStart = datetime.timedelta(microseconds=int(int(re.findall('P="([^"]+)"', aASeg)[0]) / aHerz * 1000000))
				aStop = aStart + datetime.timedelta(microseconds=int(int(re.findall('L="([^"]+)"', aASeg)[0]) / aHerz * 1000000))
				aTagsFind = re.findall('TR6="([^"]+)"', aASeg)
				aTags = [at.split(';') for at in aTagsFind[0].split('|')] if aTagsFind else None
				# Vorhandene Daten
				if aAid:
					if KorpusDB.tbl_aufgaben.objects.filter(id=aAid).count() < 1:
						error += 'Aufgabe mit der ID "' + str(aAid) + '" nicht vorhanden!'
					else:
						# erhinfaufgaben erstellen
						if KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=aAid, id_InfErh=aElement.pk).count() == 0:
							aErhinfaufgaben = KorpusDB.tbl_erhinfaufgaben()
							aErhinfaufgaben.id_Aufgabe_id = aAid
							aErhinfaufgaben.id_InfErh_id = aElement.pk
							aErhinfaufgaben.start_Aufgabe = aStart
							aErhinfaufgaben.stop_Aufgabe = aStop
							aErhinfaufgaben.save()
							info += '<b>tbl_erhinfaufgaben erstellt (Id: ' + str(aErhinfaufgaben.pk) + '):</b> ' + str(aErhinfaufgaben) + '<br>'
						else:
							aErhinfaufgaben = KorpusDB.tbl_erhinfaufgaben.objects.get(id_Aufgabe=aAid, id_InfErh=aElement.pk)
							info += '<b>tbl_erhinfaufgaben vorhanden (Id: ' + str(aErhinfaufgaben.pk) + '):</b> ' + str(aErhinfaufgaben) + '<br>'
						# Antworten erstellen
						for aInfZuErh in KorpusDB.tbl_inf_zu_erhebung.objects.filter(id_inferhebung=aElement):
							aAntwort = None
							if KorpusDB.tbl_antworten.objects.filter(von_Inf=aInfZuErh.ID_Inf, zu_Aufgabe=aAid, start_Antwort=aStart, stop_Antwort=aStop).count() == 0:
								aAntwort = KorpusDB.tbl_antworten()
								aAntwort.von_Inf = aInfZuErh.ID_Inf
								aAntwort.zu_Aufgabe_id = aAid
								aAntwort.ist_audio_only = True
								aAntwort.start_Antwort = aStart
								aAntwort.stop_Antwort = aStop
								aAntwort.save()
								info += '<b style="margin-left:25px;">Antwort erstellt (Id: ' + str(aAntwort.pk) + '):</b> ' + str(aAntwort) + '<br>'
							else:
								info += '<b style="margin-left:25px;">Antwort bereits vorhanden!</b><br>'
								aAntwort = KorpusDB.tbl_antworten.objects.filter(von_Inf=aInfZuErh.ID_Inf, zu_Aufgabe=aAid, start_Antwort=aStart, stop_Antwort=aStop).first()
							if aAntwort:
								if aTags:
									dg = 0
									for aTagE in aTags:
										for aTag in aTagE:
											if aTag in aTagList:
												if KorpusDB.tbl_tags.objects.filter(pk=aTagList[aTag][0]).count() > 0:
													if KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=aAntwort, id_Tag_id=aTagList[aTag][0]).count() > 0:
														info += '<b style="margin-left:50px;">Antworten Tag zu Tag ID ' + str(aTagList[aTag][0]) + ' vorhanden. (e1)</b><br>'
													else:
														aTagzuordnung = KorpusDB.tbl_antwortentags()
														aTagzuordnung.id_Antwort = aAntwort
														aTagzuordnung.id_Tag_id = aTagList[aTag][0]
														aTagzuordnung.id_TagEbene_id = 50
														aTagzuordnung.Reihung = dg
														aTagzuordnung.save()
														info += '<b style="margin-left:50px;">Antworten Tag zu Tag ID ' + str(aTagList[aTag][0]) + ' erstellt. (Id: ' + str(aTagzuordnung.pk) + ')</b><br>'
														dg += 1
												else:
													info += '<b style="margin-left:50x;">Tag mit ID "' + str(aTagList[aTag][0]) + '" nicht gefunden! (e1)</b><br>'
											else:
												info += '<b style="margin-left:50px;">Tag mit dem Namen "' + str(aTag) + '" nicht in Translationsliste für Tags gefunden! (e1)<br>'

	# Einstellungen:
	InlineAudioPlayer = loader.render_to_string(
		'korpusdbmaske/fxaudioplayer.html',
		RequestContext(request, {'audioDir': 'select[name="Dateipfad"]', 'audioFile': 'select[name="Audiofile"]', 'audioPbMarker': ['input[name="time_beep"]', 'input[name="sync_time"]']}),)

	def dateipfadFxfunction(aval, siblings, aElement):
		adir = removeLeftSlash(aval['value'])
		adirABS = os.path.normpath(os.path.join(mDir, adir))
		if not os.path.isdir(adirABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Verzeichnis existiert nicht!'
		if not getPermission(adir, mDir, request) > 0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = tree2select(scanDir(mDir, None, request))
			isInList = False
			aval['value'] = os.path.normpath(removeLeftSlash(aval['value']))
			for aselectitm in aselect:
				if aval['value'] == aselectitm['value']:
					isInList = True
					aval['value'] = aval['value']
					break
			if not isInList:
				aselect = [{'title': os.path.normpath(aval['value']), 'value': os.path.normpath(aval['value'])}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['showValue'] = True
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval

	def audiofileFxfunction(aval, siblings, aElement):
		aFile = removeLeftSlash(aval['value'])
		aDir = ''
		for aFeld in siblings:
			if aFeld['name'] == 'Dateipfad':
				aDir = removeLeftSlash(aFeld['value'])
				break
		aFileABS = os.path.normpath(os.path.join(mDir, aDir, aFile))
		if not os.path.isfile(aFileABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Datei existiert nicht!'
		if not getPermission(aDir, mDir, request) > 0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = []
			isInList = False
			if os.path.isdir(os.path.normpath(os.path.join(mDir, aDir))):
				for aFile in scanFiles(aDir, mDir, request):
					if aFile['name'][-4:] == '.mp3' or aFile['name'][-4:] == '.ogg' or aFile['name'][-4:] == '.wav':
						aselect.append({'title': aFile['name'], 'value': aFile['name']})
						if aFile['name'] == aval['value']:
							isInList = True
			if not isInList:
				aselect = [{'title': aval['value'], 'value': aval['value']}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval

	def audiodurationFxfunction(aval, siblings, aElement):
		aDir = ''
		aFile = ''
		for aFeld in siblings:
			if aFeld['name'] == 'Dateipfad':
				aDir = removeLeftSlash(aFeld['value'])
			if aFeld['name'] == 'Audiofile':
				aFile = removeLeftSlash(aFeld['value'])
			if aDir and aFile:
				break
		aFileABS = os.path.normpath(os.path.join(mDir, aDir, aFile))
		err = False
		if not os.path.isfile(aFileABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Datei existiert nicht!'
			err = True
		if not getPermission(aDir, mDir, request) > 0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
			err = True
		if not err:
			fileInfo = TinyTag.get(aFileABS)
			aDuration = 0
			if aval['value']:
				aDuration = aval['value'].total_seconds()
			if abs(fileInfo.duration - aDuration) > 0.001:
				aval['feldoptionen']['fxtype']['warning'] = 'Zeit stimmt nicht überein!'
				aval['feldoptionen']['fxtype']['setvalue'] = str(fileInfo.duration)
		return aval

	def erhInfAufgabeFxfunction(aval, siblings, aElement):
		"""Html Ausgabe erhInfAufgabe für Fragebögen."""
		aView_html = '<div></div>'
		useArtErhebung = [6, 7]
		aErh = findDicValInList(siblings, 'name', 'ID_Erh')
		if 'value' in aErh and aErh['value'] and aErh['value'].Art_Erhebung.pk in useArtErhebung:
			# ErhInfAufgaben
			aView_html = loader.render_to_string(
				'inferhebung/erhinfaufgabefxfunction0.html',
				RequestContext(request, {'erhinfaufgabenCount': aElement.tbl_erhinfaufgaben_set.count(), 'erhebungMitAufgabenCount': aErh['value'].tbl_erhebung_mit_aufgaben_set.count()}),)
		aval['feldoptionen'] = {
			'view_html': aView_html,
			'edit_html': '<div></div>'}
		return aval

	def antwortenMitSaetzenFxfunction(aval, siblings, aElement):
		"""Html Ausgabe Antworten für LeseWortliste."""
		aView_html = '<div></div>'
		aErh = findDicValInList(siblings, 'name', 'ID_Erh')
		if 'value' in aErh and aErh['value'] and aErh['value'].pk == 7:
			antwortenMitSaetzenCount = 0
			for aErhInfAufgaben in aElement.tbl_erhinfaufgaben_set.all():
				if aErhInfAufgaben.id_Aufgabe.tbl_antworten_set.all():
					antwortenMitSaetzenCount += 1
			aView_html = loader.render_to_string(
				'inferhebung/antwortenmitsaetzenfxfunction0.html',
				RequestContext(request, {'antwortenMitSaetzenCount': antwortenMitSaetzenCount, 'erhinfaufgabenCount': aElement.tbl_erhinfaufgaben_set.count()}),)
		aval['feldoptionen'] = {
			'view_html': aView_html,
			'edit_html': '<div></div>'}
		return aval

	def stxsmFxfunction(aval, siblings, aElement):
		"""Html Ausgabe stxsm Datei."""
		aView_html = '<div></div>'
		aDir = ''
		aFile = ''
		aFileABS = None
		aStxsmFile = None
		# Audio Datei ermitteln:
		for aFeld in siblings:
			if aFeld['name'] == 'Dateipfad':
				aDir = removeLeftSlash(aFeld['value'])
			if aFeld['name'] == 'Audiofile':
				aFile = removeLeftSlash(aFeld['value'])
			if aDir and aFile:
				break
		if aDir and aFile:
			aFileABS = os.path.normpath(os.path.join(mDir, aDir, aFile))
		# stxsm Datei ermitteln:
		if aFileABS and os.path.isfile(aFileABS):
			if os.path.isfile(aFileABS + '.stxsm'):
				aStxsmFile = aFileABS + '.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.wav.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.wav.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.ogg.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.ogg.stxsm'
			elif os.path.isfile(aFileABS[:-4] + '.mp3.stxsm'):
				aStxsmFile = aFileABS[:-4] + '.mp3.stxsm'
		if aStxsmFile:
			import re
			from html import escape
			import datetime
			errText = []
			warningText = []
			# Datei auswerten
			with open(aStxsmFile, 'r', encoding="utf-8") as file:
				aStxsmData = file.read()
			aHerz = int(re.findall('<AFile[^>]+SR="(\d+)"[^>]+>', aStxsmData)[0])
			aTest = ''
			aTest += 'Herz: <b>' + str(aHerz) + '</b><br>'
			aASegs = []
			for aASeg in re.findall('<ASeg[^>]+ID=".+"[^>]+>', aStxsmData):
				iType = re.findall('Type="uncl"', aASeg)
				aIdS = re.findall('ID="([^"]+)"', aASeg)[0].split('.')[0]
				if (not iType or len(iType) == 0) and not aIdS == 'Signal':
					aASegs.append(aASeg)
			aAIdList = {}
			aIdListFile = 'pp02_stxsm0.csv'
			if aElement and aElement.ID_Erh and aElement.ID_Erh.id >= 38 and aElement.ID_Erh.id <= 44:
				aIdListFile = 'pp02_p2_stxsm0.csv'
			aTest += 'Benutze ID-Datei <b>"' + aIdListFile + '"</b> für Erhebungs Id: <b>' + str(aElement.ID_Erh.id if aElement else None) + '</b><br><br>'
			with open(os.path.join(getattr(settings, 'BASE_DIR', None), 'KorpusDB', 'fx', aIdListFile), 'r', encoding="utf-8") as file:
				dg = 0
				for aLine in file:
					if dg > 0:
						[tId, tFx] = aLine.strip().split(';')
						aAIdList[tFx] = int(tId)
					dg += 1
			aTagList = {}
			with open(os.path.join(getattr(settings, 'BASE_DIR', None), 'KorpusDB', 'fx', 'pp02_translation_tags_2.csv'), 'r', encoding="utf-8") as file:
				dg = 0
				for aLine in file:
					if dg > 0:
						[tName, tId, tDbName] = aLine.strip().split(';')
						aTagList[tName] = [int(tId), tDbName]
					dg += 1
			aDbCount = 0
			aTagCount = 0
			aTagDoneCount = 0
			aMissingAntworten = 0
			for aASeg in aASegs:
				aId = re.findall('ID="([^"]+)"', aASeg)[0]
				if aId.split('.')[-1] == 'ATL':
					aFx = '.'.join(aId.split('.')[-3:-1])
				else:
					aFx = '.'.join(aId.split('.')[-2:])
				if aFx in aAIdList:
					aAid = aAIdList[aFx]
				else:
					aAid = None
					if aFx[0:3].lower() == 'ex.' or aFx[0:3].lower() == 'pd.':
						warningText.append('"' + aFx + '" konnte keiner Aufgaben ID zugewiesen werden! (e2)')
					else:
						warningText.append('"' + aFx + '" konnte keiner Aufgaben ID zugewiesen werden! (e3)')
				aStart = datetime.timedelta(microseconds=int(int(re.findall('P="([^"]+)"', aASeg)[0]) / aHerz * 1000000))
				aStop = aStart + datetime.timedelta(microseconds=int(int(re.findall('L="([^"]+)"', aASeg)[0]) / aHerz * 1000000))
				aTagsFind = re.findall('TR6="([^"]+)"', aASeg)
				aTags = [at.split(';') for at in aTagsFind[0].split('|')] if aTagsFind else None
				aTest += '<code>' + escape(aASeg) + '</code><br>'
				aTest += 'id: ' + aId + '<br>'
				aTest += 'fx: ' + aFx + ' - Aufgaben Id: ' + (str(aAid) if aAid else '<b><u>None</u></b>') + '<br>'
				aTest += 'start: ' + str(aStart) + '<br>'
				aTest += 'stop: ' + str(aStop) + '<br>'
				aTest += 'tags: ' + str([[{'name': a, 'db': aTagList[a] if a in aTagList else '<b><u>None</u></b>'} for a in b] for b in aTags] if aTags else None) + '<br>'
				# Vorhandene Daten
				aAntwort = None
				if aAid:
					if KorpusDB.tbl_aufgaben.objects.filter(id=aAid).count() < 1:
						errText.append('Aufgabe mit der ID "' + str(aAid) + '" nicht vorhanden! (e3)')
					else:
						if KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=aAid, id_InfErh=aElement.pk).count() > 0:
							aTest += 'In "tbl_erhinfaufgaben" vorhanden! id_Aufgabe: ' + str(aAid) + ' id_InfErh: ' + str(aElement.pk) + '<br>'
							for aInfZuErh in KorpusDB.tbl_inf_zu_erhebung.objects.filter(id_inferhebung=aElement):
								if KorpusDB.tbl_antworten.objects.filter(von_Inf=aInfZuErh.ID_Inf, zu_Aufgabe=aAid, start_Antwort=aStart, stop_Antwort=aStop).count() > 0:
									aAntwort = KorpusDB.tbl_antworten.objects.filter(von_Inf=aInfZuErh.ID_Inf, zu_Aufgabe=aAid, start_Antwort=aStart, stop_Antwort=aStop).first()
									aTest += 'Antwort mit ID ' + str(aAntwort.pk) + ' vorhanden!<br>'
								else:
									aTest += '<b>Antwort nicht vorhanden!</b><br>'
									aMissingAntworten += 1
							aDbCount += 1
						else:
							aTest += 'Nicht in "tbl_erhinfaufgaben" vorhanden! id_Aufgabe: ' + str(aAid) + ' id_InfErh: ' + str(aElement.pk) + '<br>'
				if aTags:
					for aTagE in aTags:
						for aTag in aTagE:
							aTagCount += 1
							if aTag in aTagList:
								if KorpusDB.tbl_tags.objects.filter(pk=aTagList[aTag][0]).count() > 0:
									if aAntwort:
										if KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=aAntwort, id_Tag_id=aTagList[aTag][0]).count() > 0:
											aTest += 'Antworten Tag zu Tag ID ' + str(aTagList[aTag][0]) + ' vorhanden. (e3)<br>'
											aTagDoneCount += 1
										else:
											aTest += '<b>Antworten Tag zu Tag ID ' + str(aTagList[aTag][0]) + ' nicht vorhanden. (e3)</b><br>'
									else:
										aTest += '<b>Antworten Tag zu Tag ID ' + str(aTagList[aTag][0]) + ' nicht vorhanden. (e3)</b><br>'
								else:
									errText.append('Tag mit ID "' + str(aTagList[aTag][0]) + '" nicht gefunden! (e3)')
							else:
								errText.append('Tag mit dem Namen "' + str(aTag) + '" nicht in Translationsliste für Tags gefunden! (e3)')
				aTest += '<br>'
			aView_html = loader.render_to_string(
				'inferhebung/stxsmfxfunction0.html',
				RequestContext(request, {'dataCount': len(aASegs), 'dbCount': aDbCount, 'missingAntworten': aMissingAntworten, 'tagDoneCount': aTagDoneCount, 'tagCount': aTagCount, 'createIt': aDbCount == 0 or aMissingAntworten > 0 or aTagDoneCount < aTagCount, 'errText': errText, 'warningText': warningText, 'aTest': aTest}),)
			# aView_html = '<div>' + str(aStxsmFile) + '<br>Herz: ' + str(aHerz) + '<hr>' + aTest + '</div>'
		aval['feldoptionen'] = {
			'view_html': aView_html,
			'edit_html': '<div></div>'}
		return aval

	def AufgabenIDausListe(csvData, csvImportData, options=None):
		"""Zusatzfunktion für CSVImport Erhebungs Art 4 (Übersetzungen)."""
		for csvRow in csvData['rows']:
			aErh = 0
			aFile = None
			if options:
				if 'typ' in options and options['typ'] == 'erh7':
					aErh = 7
					aFile = 'LesenWortliste_import_Aufgabenids.csv'
					aVal = 'ID'
			elif csvRow['cols']['title']['value'] == 'Uebersetzung 1 D-S':
				aErh = 12
				aFile = 'Wenkersatze_import_Aufgabenids.csv'
				aVal = 'WS_ID'
			elif csvRow['cols']['title']['value'] == 'Uebersetzung 2 S-D':
				aErh = 11
				aFile = 'Wenkersatze_import_Aufgabenids.csv'
				aVal = 'WS_ID'
			if aErh > 0 and aFile:
				aErhAnpassung = False
				import csv
				mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
				if not mDir:
					return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
				aCsvFile = os.path.join(mDir, 'csv', 'fx', aFile)
				with open(aCsvFile, encoding='utf-8') as csvfile:
					reader = csv.reader(csvfile)
					adg = 0
					for row in reader:
						if adg > 0:
							if int(row[1]) == csvRow['cols'][aVal]['value'] and int(row[2]) == aErh:
								aErhAnpassung = True
								csvRow['cols'][aVal]['value'] = int(row[0])
								break
						adg += 1
				if not aErhAnpassung:
					csvRow['cols'][aVal]['errorID'] = 'AufgabenIDausListeAnpassung_error'
					csvRow['cols'][aVal]['error'] = 'AufgabenID konnte nicht angepasst werden!'
			# else:
			# 	csvRow['cols'][csvRow['cols'].keys()[0]]['errorID'] = 'AufgabenIDausListe_error'
			# 	csvRow['cols'][csvRow['cols'].keys()[0]]['error'] = 'Konnte keiner Erhebung zugeordnet werden!'
		return csvData
	dateipfadFxType = {'fxtype': {'fxfunction': dateipfadFxfunction}, 'nl': True}
	audiofileFxType = {'fxtype': {'fxfunction': audiofileFxfunction}, 'nl': True}
	audiodurationFxType = {'fxtype': {'fxfunction': audiodurationFxfunction}, 'nl': True}
	erhInfAufgabeFxType = {'fxtype': {'fxfunction': erhInfAufgabeFxfunction}, 'nl': True, 'view_html': '<div></div>', 'edit_html': '<div></div>'}
	antwortenMitSaetzeFxType = {'fxtype': {'fxfunction': antwortenMitSaetzenFxfunction}, 'nl': True, 'view_html': '<div></div>', 'edit_html': '<div></div>'}
	stxsmFxType = {'fxtype': {'fxfunction': stxsmFxfunction}, 'nl': True, 'view_html': '<div></div>', 'edit_html': '<div></div>'}
	aufgabenform = [{
		'titel': 'InfErhebung', 'titel_plural': 'InfErhebungen', 'app': 'KorpusDB', 'tabelle': 'tbl_inferhebung', 'id': 'inferhebung', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'ID_Erh', 'id_Transcript', 'Datum', 'Explorator', 'Kommentar', 'Dateipfad', 'Audiofile', 'Audioduration', 'time_beep', 'sync_time', 'Logfile', 'Ort', 'Besonderheiten', '!Audioplayer', '!ErhInfAufgabe', '!AntwortenMitSaetzeFx', '!stxsmFx'],
		'feldoptionen':{
			'Audioplayer': {'view_html': '<div></div>', 'edit_html': InlineAudioPlayer},
			'Dateipfad': dateipfadFxType,
			'Audiofile': audiofileFxType,
			'Audioduration': audiodurationFxType,
			'ErhInfAufgabe': erhInfAufgabeFxType,
			'AntwortenMitSaetzeFx': antwortenMitSaetzeFxType,
			'stxsmFx': stxsmFxType
		},
		'sub': [
			{
				'titel': 'Informant', 'titel_plural': 'Informanten', 'app': 'KorpusDB', 'tabelle': 'tbl_inf_zu_erhebung', 'id': 'infzuerhebung', 'optionen': ['liste', 'elementeclosed'],
				'felder':['+id', '|id_inferhebung=parent:id', 'ID_Inf'],
				'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ParentTag">{% getFeldVal aData.felder \'ID_Inf\' %}</span>',
			},
			{
				'titel': 'Fragebogen', 'titel_plural': 'Fragebögen', 'app': 'KorpusDB', 'tabelle': 'tbl_fragebogen', 'id': 'fragebogen', 'optionen': ['einzeln', 'elementFrameless'],
				'felder':['+id', '|id_inferhebung=parent:id', 'Int_Sk1', 'Int_Sk2', 'Int_Sk3', 'Int_Sk4', 'Int_Sk5', 'Int_Sk6', 'Int_Sk7', 'Int_Sk8', 'Int_Sk9', 'Int_Sk10', 'Int_Sk_11_1', 'Int_Sk_11_2', 'Int_Sk_11_3', 'Int_Sk_11_4', 'Int_Sk_11_5', 'Int_Sk_11_6', 'Spt_Sk1', 'Spt_Sk2', 'Spt_Sk3', 'Spt_Sk4', 'Spt_Sk5', 'Spt_Sk6', 'All_Sk', 'All_Q1', 'All_Q2', 'All_Q3', 'All_Q4', 'Com_Inf', 'Com_Exp', 'Erhfb_Exp_1', 'Erhfb_Exp_2', 'Erhfb_Exp_3', 'Erhfb_Exp_4', 'Erhfb_Exp_5', 'Erhfb_Exp_6', 'Erhfb_Exp_7', 'Erhfb_Exp_8', 'Erhfb_Exp_9', 'Erhfb_Exp_10', 'Erhfb_Exp_11', 'Erhfb_Exp_12', 'Erhfb_Exp_13', 'Erhfb_Exp_14', 'Erhfb_Exp_15', 'Erhfb_Exp_16', 'Erhfb_Exp_17', 'Erhfb_Exp_18', 'Erhfb_Exp_19', 'Erhfb_Exp_20', 'Erhfb_Exp_21', 'Erhfb_Exp_22', 'Erhfb_Exp_23', 'FG_SK_1', 'FG_SK_2', 'FG_SK_3', 'FG_SK_4', 'FG_SK_5', 'FG_SK_6', 'FG_SK_7', 'FG_SK_8', 'FG_SK_9', 'FG_SK_10', 'FG_List', 'FG_Q_1', 'FG_Q_2', 'Comm_FB', 'id_Inf'],
				'feldoptionen': {
				}
			}
		],
		'addCSS': [{'static': 'korpusdbfx/css/fxaudioplayer.css'}],
		'addJS': [{'static': 'korpusdbfx/js/fxaudioplayer.js'}, {'static': 'korpusdbfx/js/fxerhinfaufgabe.js'}],
		'import': {
			'enabled': True,
			'csvImportData': [
				{
					'selectby': 'tableField',
					'selectField': 'ID_Erh__pk',
					'select': {
						37: {
							'name': 'SPT-S_2_PP03" (ID: 37)',
							'cols': {
								'ID_Aufgabe': {				# Aufgaben ID
									'errorCheck': [{'type': 'pkInTable', 'app': 'KorpusDB', 'table': 'tbl_aufgaben'}]
								},
								'count_BlackKon_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1_1_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1_1_1_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1_1_1_1_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1_1_1_1_1_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'datetime': {				# Zeitpunkt der Erhebung
									'convert': [{'type': 'datetime'}],
									'errorCheck': [{'type': 'datetime'}, {'type': 'colAlwaysSame'}]
								},
								'logfile': {				# Eigener Filename; sollte hinweis geben, zu welchem Ort die Erhebung ist, und zu welcher Person (letzte drei Ziffern = Inf_Sigle)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'subject_nr': {				# Inf_sigle (sollte Inf_sigle von Inf_erh entsprechen)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'time_Blackscreen_1': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_Blackscreen_1_1': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1_1_1': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1_1_1_1': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1_1_1_1_1': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1_1_1_1_1_1': {		# das ist nur für das erste SET die Zeiten
									'convert': [{'type': 'duration'}]
								},
								'time_Logg_all': {			# Ich denke, auch das könnte als Endzeitpunkt für eine Einzelaufgabe genommen werden; ist vielleicht sogar exakter; müssen wir ausprobieren, sieht aber relativ gut aus
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_Logg_all_1': {
									'convert': [{'type': 'duration'}]
								},
								'time_Logg_all_1_1': {
									'convert': [{'type': 'duration'}]
								},
								'time_Logg_all_1_1_1': {
									'convert': [{'type': 'duration'}]
								},
								'time_Logg_all_1_1_1_1': {
									'convert': [{'type': 'duration'}]
								},
								'time_Logg_all_1_1_1_1_1': {
									'convert': [{'type': 'duration'}]
								},
								'time_beep': {				# TIME_BEEP! Das so in tbl_inferhebung übernehmen; die Synctime müssen die Leute selbst eingeben
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}, {'type': 'colAlwaysSame'}]
								}
							},
							'import': {
								'once': [{
									'type': 'update',
									'table': '!this',
									'errorCheck': [{'type': 'issame', 'is': '!this__tbl_inf_zu_erhebung__!first__ID_Inf__inf_sigle=subject_nr|rjust:4,0', 'warning': True}],
									'fields': {
										'Datum': 'datetime',
										'time_beep': 'time_beep',
										'Logfile': 'logfile',
									}
								}],
								'perrow': [{
									'type': 'new',
									'table': 'KorpusDB>tbl_erhinfaufgaben',
									'errorCheck': [{'type': 'notInDB', 'fields': {'id_InfErh_id', 'id_Aufgabe_id'}, 'warning': True}],
									'fields': {
										'id_InfErh_id': '!this__pk',
										'id_Aufgabe_id': 'ID_Aufgabe',
										'Reihung': 'firstVal|count_BlackKon_1_1_1_1_1_1,count_BlackKon_1_1_1_1_1,count_BlackKon_1_1_1_1,count_BlackKon_1_1_1,count_BlackKon_1_1,count_BlackKon_1',
										'start_Aufgabe': 'firstVal|time_Blackscreen_1_1_1_1_1_1,time_Blackscreen_1_1_1_1_1,time_Blackscreen_1_1_1_1,time_Blackscreen_1_1_1,time_Blackscreen_1_1,time_Blackscreen_1',
										'stop_Aufgabe': 'firstVal|time_Logg_all_1_1_1_1_1,time_Logg_all_1_1_1_1,time_Logg_all_1_1_1,time_Logg_all_1_1,time_Logg_all_1,time_Logg_all',
									}
								}]
							}
						},
						36: {
							'name': 'Erhebung "SPT-D_2_PP03" (ID: 36)',
							'cols': {
								'ID_Aufgabe': {				# Aufgaben ID
									'errorCheck': [{'type': 'pkInTable', 'app': 'KorpusDB', 'table': 'tbl_aufgaben'}]
								},
								'count_BlackKon': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'count_BlackKon_1': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'datetime': {				# Zeitpunkt der Erhebung
									'convert': [{'type': 'datetime'}],
									'errorCheck': [{'type': 'datetime'}, {'type': 'colAlwaysSame'}]
								},
								'logfile': {				# Eigener Filename; sollte hinweis geben, zu welchem Ort die Erhebung ist, und zu welcher Person (letzte drei Ziffern = Inf_Sigle)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'subject_nr': {				# Inf_sigle (sollte Inf_sigle von Inf_erh entsprechen)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'time_Blackscreen': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1': {		# das ist nur für das erste SET die Zeiten
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_Logg_all': {			# Ich denke, auch das könnte als Endzeitpunkt für eine Einzelaufgabe genommen werden; ist vielleicht sogar exakter; müssen wir ausprobieren, sieht aber relativ gut aus
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_beep': {				# TIME_BEEP! Das so in tbl_inferhebung übernehmen; die Synctime müssen die Leute selbst eingeben
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}, {'type': 'colAlwaysSame'}]
								}
							},
							'import': {
								'once': [{
									'type': 'update',
									'table': '!this',
									'errorCheck': [{'type': 'issame', 'is': '!this__tbl_inf_zu_erhebung__!first__ID_Inf__inf_sigle=subject_nr|rjust:4,0', 'warning': True}],
									'fields': {
										'Datum': 'datetime',
										'time_beep': 'time_beep',
										'Logfile': 'logfile',
									}
								}],
								'perrow': [{
									'type': 'new',
									'table': 'KorpusDB>tbl_erhinfaufgaben',
									'errorCheck': [{'type': 'notInDB', 'fields': {'id_InfErh_id', 'id_Aufgabe_id'}, 'warning': True}],
									'fields': {
										'id_InfErh_id': '!this__pk',
										'id_Aufgabe_id': 'ID_Aufgabe',
										'Reihung': 'firstVal|count_BlackKon,count_BlackKon_1',
										'start_Aufgabe': 'firstVal|time_Blackscreen,time_Blackscreen_1',
										'stop_Aufgabe': 'time_Logg_all',
									}
								}]
							}
						},
						7: {
							'name': 'Erhebungsart "LesenWortliste_PP03" (7)',
							'cols': {
								'ID': {						# ÜBER DIE KONVERTIERUNGSTABELLE zu -> id_Aufgabe
									'convert': [{'type': 'int'}],
									'errorCheck': [{'type': 'pkInTable', 'app': 'KorpusDB', 'table': 'tbl_aufgaben'}]
								},
								'count_LemmaAnzeige': {		# Reihung
									'convert': [{'type': 'int'}],
								},
								'time_Vorlesen': {			# start_Aufgabe
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_beep_1': {			# time_beep
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}, {'type': 'colAlwaysSame'}]
								},
								'subject_nr': {				# sollte mit der Sigle vom Informanten übereinstimmen
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
							},
							'colFX': [
								{'type': 'removeDouble'},
								{'type': 'fxfunction', 'fxfunction': AufgabenIDausListe, 'options': {'typ': 'erh7'}},
							],
							'import': {
								'once': [{
									'type': 'update',
									'table': '!this',
									'errorCheck': [{'type': 'issame', 'is': '!this__tbl_inf_zu_erhebung__!first__ID_Inf__inf_sigle=subject_nr|rjust:4,0', 'warning': True}],
									'fields': {
										'time_beep': 'time_beep_1',
									}
								}],
								'perrow': [
									{
										'type': 'new',
										'table': 'KorpusDB>tbl_erhinfaufgaben',
										'errorCheck': [{'type': 'notInDB', 'fields': {'id_InfErh_id', 'id_Aufgabe_id'}, 'warning': True}],
										'fields': {
											'id_InfErh_id': '!this__pk',
											'id_Aufgabe_id': 'ID',
											'Reihung': 'count_LemmaAnzeige',
											'start_Aufgabe': 'time_Vorlesen',
											'stop_Aufgabe': 'nextRow|time_Vorlesen,time_Vorlesen',
										}
									},
								]
							},
						},
					}
				},
				{
					'selectby': 'tableField',
					'selectField': 'ID_Erh__Art_Erhebung__pk',
					'select': {
						3: {
							'name': 'Erhebungsart "SPT" (ID: 3)',
							'cols': {
								'ID_Aufgabe': {				# Aufgaben ID
									'errorCheck': [{'type': 'pkInTable', 'app': 'KorpusDB', 'table': 'tbl_aufgaben'}]
								},
								'count_BlackKon': {			# Reihenfolge der Aufgabe
									'convert': [{'type': 'int'}]
								},
								'datetime': {				# Zeitpunkt der Erhebung
									'convert': [{'type': 'datetime'}],
									'errorCheck': [{'type': 'datetime'}, {'type': 'colAlwaysSame'}]
								},
								'logfile': {				# Eigener Filename; sollte hinweis geben, zu welchem Ort die Erhebung ist, und zu welcher Person (letzte drei Ziffern = Inf_Sigle)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'subject_nr': {				# Inf_sigle (sollte Inf_sigle von Inf_erh entsprechen)
									'convert': [{'type': 'trim'}],
									'errorCheck': [{'type': 'colAlwaysSame'}]
								},
								'time_Blackscreen': {		# Das ist die Zeit einer Einzelaufgabe; also Startzeit der Einzelaufgabe; als Endzeit nehme ich dann immer die Zeit der nächsten Aufgabe; außer bei der letzten, da rechen ich einfach + 2 Sekunden (man könnte bis zum Aufnahmeende machen); die Startzeit stimmt nicht, wenn die Aufgabe wiederholt wurde; bzw. muss die Endzeit von der übernächsten Zeile (also wenn es eine andere Aufgabe ist) genommen werden
									'convert': [{'type': 'duration'}]
								},
								'time_Blackscreen_1': {		# das ist nur für das erste SET die Zeiten
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_Logg_all': {			# Ich denke, auch das könnte als Endzeitpunkt für eine Einzelaufgabe genommen werden; ist vielleicht sogar exakter; müssen wir ausprobieren, sieht aber relativ gut aus
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_beep': {				# TIME_BEEP! Das so in tbl_inferhebung übernehmen; die Synctime müssen die Leute selbst eingeben
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}, {'type': 'colAlwaysSame'}]
								}
							},
							'import': {
								'once': [{
									'type': 'update',
									'table': '!this',
									'errorCheck': [{'type': 'issame', 'is': '!this__tbl_inf_zu_erhebung__!first__ID_Inf__inf_sigle=subject_nr|rjust:4,0', 'warning': True}],
									'fields': {
										'Datum': 'datetime',
										'time_beep': 'time_beep',
										'Logfile': 'logfile',
									}
								}],
								'perrow': [{
									'type': 'new',
									'table': 'KorpusDB>tbl_erhinfaufgaben',
									'errorCheck': [{'type': 'notInDB', 'fields': {'id_InfErh_id', 'id_Aufgabe_id'}, 'warning': True}],
									'fields': {
										'id_InfErh_id': '!this__pk',
										'id_Aufgabe_id': 'ID_Aufgabe',
										'Reihung': 'count_BlackKon',
										'start_Aufgabe': 'firstVal|time_Blackscreen,time_Blackscreen_1',
										'stop_Aufgabe': 'time_Logg_all',
									}
								}]
							}
						},
						4: {
							'name': 'Erhebungsart "Übersetzungen" (ID: 4)',
							'cols': {
								'WS_ID': {					# aus CSV WS_ID übersetzt mit obiger Tabelle zu KorpusDB_tbl_erhinfaufgaben.id_Aufgabe_id
									'convert': [{'type': 'int'}],
									'errorCheck': [{'type': 'pkInTable', 'app': 'KorpusDB', 'table': 'tbl_aufgaben'}]
								},
								'time_Startscreen': {		# aus CSV time_Startscreen zu KorpusDB_tbl_erhinfaufgaben.start_Aufgabe
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}]
								},
								'time_beep': {				# aus CSV time_beep zu KorpusDB_tbl_inferh.time_beep
									'convert': [{'type': 'duration'}],
									'errorCheck': [{'type': 'convert'}, {'type': 'colAlwaysSame'}]
								},
								'experiment_file': {		# experiment_file aus CSV = logfile in InfErh
								},
								'title': {					# Wenn in title "Uebersetzung 1 D-S" dann darf das nur importiert werden für Erh_id = 12 (AufgabenIds von 389-437) | "Uebersetzung 2 S-D" -> Erh_id = 11 (Aufgabenids 340-389)
								},
							},
							'colFX': [
								{'type': 'removeDouble'},
								{'type': 'fxfunction', 'fxfunction': AufgabenIDausListe},
							],
							'import': {
								'once': [{
									'type': 'update',
									'table': '!this',
									'fields': {
										'time_beep': 'time_beep',
										'Logfile': 'experiment_file',
									}
								}],
								'perrow': [{
									'type': 'new',
									'table': 'KorpusDB>tbl_erhinfaufgaben',
									'errorCheck': [{'type': 'notInDB', 'fields': {'id_InfErh_id', 'id_Aufgabe_id'}, 'warning': True}],
									'fields': {
										'id_InfErh_id': '!this__pk',
										'id_Aufgabe_id': 'WS_ID',
										'Reihung': '!count',
										'start_Aufgabe': 'time_Startscreen',
										'stop_Aufgabe': 'nextRow|time_Startscreen,time_Startscreen',
									}
								}]
							},
						},
					}
				},
			]
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def maske(request, ipk=0, apk=0):
	"""Eingabemaske: EingabeSPT - ipk=tbl_informanten, apk=tbl_aufgaben."""
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not (request.user.has_perm('KorpusDB.antworten_maskView') or request.user.has_perm('KorpusDB.antworten_EingabeSPT_maskView')):
		return redirect('Startseite:start')
	from .view_maske import view_maske
	return view_maske(request, ipk, apk)


def maske2(request, ipk=0, apk=0):
	"""Eingabemaske: EingabeFB - ipk=tbl_informanten, apk=tbl_aufgaben."""
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not (request.user.has_perm('KorpusDB.antworten_maskView') or request.user.has_perm('KorpusDB.antworten_EingabeFB_maskView')):
		return redirect('Startseite:start')
	from .view_maske2 import view_maske2
	return view_maske2(request, ipk, apk)


def aufmoegtags(request, ipk=0, apk=0):
	"""Eingabemaske: Aufgabenmöglichkeiten Tags - ipk=tbl_informanten, apk=tbl_aufgaben."""
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not (request.user.has_perm('KorpusDB.antworten_maskView') or request.user.has_perm('KorpusDB.antworten_aufmoegtags_maskView')):
		return redirect('Startseite:start')
	from .view_aufmoegtags import view_aufmoegtags
	return view_aufmoegtags(request, ipk, apk)


def auswertung(request):
	"""Anzeige für Auswertung."""
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('KorpusDB.auswertung'):
		return redirect('Startseite:start')
	asurl = '/korpusdb/auswertung/'
	useOnlyErhebung = []
	for aUKDBES in request.user.user_korpusdb_erhebung_set.all():
		useOnlyErhebung.append(aUKDBES.erhebung_id)
	for aUGroup in request.user.groups.all():
		print('Group', aUGroup)
		for aUKDBES in aUGroup.group_korpusdb_erhebung_set.all():
			print(aUKDBES)
			useOnlyErhebung.append(aUKDBES.erhebung_id)
	auswertungen = []
	auswertungen.append(
		{
			'id': 'antworten', 'titel': 'Antworten', 'app_name': 'KorpusDB', 'tabelle_name': 'tbl_antworten',
			'felder': [
				'id', 'Reihung', 'ist_bfl', 'bfl_durch_S', 'ist_Satz_id', 'ist_Satz__Transkript', 'ist_Satz__Standardorth', 'ist_Satz__Kommentar', 'tbl_antwortentags_set__!TagListeF', 'tbl_antwortentags_set__!TagListeFid',
				'von_Inf_id', 'von_Inf__inf_sigle', 'von_Inf__id_person__geb_datum', 'von_Inf__id_person__weiblich', 'von_Inf__inf_gruppe__gruppe_bez', 'von_Inf__inf_ort', 'Kommentar',
				'zu_Aufgabe_id', 'zu_Aufgabe__Beschreibung_Aufgabe', 'zu_Aufgabe__von_ASet_id', 'zu_Aufgabe__von_ASet__Kuerzel', 'kontrolliert', 'zu_Aufgabe__stimulus_dialekt', 'zu_Aufgabe__evokziel_dialekt'
			],
			'filter': [
				[
					{'id': 'erhebungenSperre', 'type': 'always', 'queryValue': useOnlyErhebung, 'queryFilter': 'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk__in'},
				],
				[
					{'id': 'erhebungen', 'field': '>KorpusDB|tbl_erhebungen', 'type': 'select', 'selectFilter': {'Art_Erhebung__gt': 2, 'pk__in': useOnlyErhebung}, 'queryFilter': 'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk', 'verbose_name': 'Erhebung'},
					{'id': 'aufgabenset', 'field': 'zu_Aufgabe__von_ASet', 'type': 'select', 'selectFilter': {'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk': '!erhebungen'}, 'queryFilter': 'zu_Aufgabe__von_ASet__pk', 'verbose_name': 'Aufgabenset'},
					# {'field':'zu_Aufgabe','type':'select','selectFilter':{'zu_Aufgabe__von_ASet':'!aufgabenset'},'queryFilter':'zu_Aufgabe__pk','verbose_name':'Aufgabe'}
				],
			],
			# 'orderby':{'id': ['Reihung']},
		}
	)
	auswertungen.append(
		{
			'id': 'antwortenTagEbenen', 'titel': 'Antworten (Tag Ebenen)', 'app_name': 'KorpusDB', 'tabelle_name': 'tbl_antworten',
			'felder': [
				'id', 'Reihung', 'ist_bfl', 'bfl_durch_S', 'ist_Satz_id', 'ist_Satz__Transkript', 'ist_Satz__Standardorth', 'ist_Satz__ipa', 'ist_Satz__Kommentar', 'von_Inf_id', 'von_Inf__inf_sigle', 'von_Inf__id_person__geb_datum', 'von_Inf__id_person__weiblich', 'von_Inf__inf_gruppe__gruppe_bez', 'von_Inf__inf_ort',
				'tbl_antwortentags_set__!TagEbenenF', 'tbl_antwortentags_set__!TagEbenenFid', 'Kommentar', 'zu_Aufgabe_id', 'zu_Aufgabe__Beschreibung_Aufgabe', 'zu_Aufgabe__von_ASet_id', 'zu_Aufgabe__von_ASet__Kuerzel', 'kontrolliert', 'zu_Aufgabe__stimulus_dialekt', 'zu_Aufgabe__evokziel_dialekt'
			],
			'filter': [
				[
					{'id': 'erhebungenSperre', 'type': 'always', 'queryValue': useOnlyErhebung, 'queryFilter': 'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk__in'},
				],
				[
					{'id': 'erhebungen', 'field': '>KorpusDB|tbl_erhebungen', 'type': 'select', 'selectFilter': {'Art_Erhebung__gt': 2, 'pk__in': useOnlyErhebung}, 'queryFilter': 'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk', 'verbose_name': 'Erhebung'},
					{'id': 'aufgabenset', 'field': 'zu_Aufgabe__von_ASet', 'type': 'select', 'selectFilter': {'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk': '!erhebungen'}, 'queryFilter': 'zu_Aufgabe__von_ASet__pk', 'verbose_name': 'Aufgabenset'},
				],
			],
		}
	)
	auswertungen.append(
		{
			'id': 'erhebungen_inf', 'titel': 'Übersicht Informant je Erhebung', 'app_name': 'KorpusDB', 'tabelle_name': 'tbl_inf_zu_erhebung',
			'felder': [
				'id', 'id_inferhebung', 'id_inferhebung__ID_Erh__Bezeichnung_Erhebung', 'id_inferhebung__ID_Erh__Art_Erhebung', 'id_inferhebung__id_Transcript', 'id_inferhebung__Datum',
				'id_inferhebung__Explorator__id_person__nachname', 'id_inferhebung__Kommentar', 'id_inferhebung__Dateipfad', 'id_inferhebung__Audiofile', 'id_inferhebung__Audioduration', 'id_inferhebung__Ort__ort_namekurz',
				'id_inferhebung__Ort__ort_namelang', 'id_inferhebung__Ort__lat', 'id_inferhebung__Ort__lon', 'id_inferhebung__Ort__osm_id', 'ID_Inf', 'ID_Inf__id_person', 'ID_Inf__inf_sigle', 'ID_Inf__id_person__geb_datum',
				'ID_Inf__id_person__weiblich', 'ID_Inf__inf_ort__ort_namekurz', 'ID_Inf__inf_ort__ort_namelang', 'ID_Inf__geburtsort__ort_namekurz', 'ID_Inf__geburtsort__ort_namelang', 'ID_Inf__inf_gruppe__gruppe_bez',
				'ID_Inf__inf_gruppe__gruppe_team__team_bez', 'ID_Inf__migrationsklasse', 'ID_Inf__kommentar', 'ID_Inf__eignung'
			],
			'filter': [
				[
					{'id': 'erhebungenSperre', 'type': 'always', 'queryValue': useOnlyErhebung, 'queryFilter': 'id_inferhebung__ID_Erh__pk__in'},
				],
				[
					{'id': 'erhebungen', 'field': '>KorpusDB|tbl_erhebungen', 'type': 'select', 'selectFilter': {'pk__in': useOnlyErhebung}, 'queryFilter': 'id_inferhebung__ID_Erh__pk', 'verbose_name': 'Erhebung'}
				],
			],
		}
	)
	auswertungen.append(
		{
			'id': 'inf_ue', 'titel': 'Übersicht Informanten', 'app_name': 'PersonenDB', 'tabelle_name': 'tbl_informanten',
			'felder': [
				'id', 'inf_sigle', 'inf_gruppe__gruppe_bez', 'inf_gruppe__gruppe_team__team_bez', 'inf_ort__ort_namekurz', 'inf_ort__ort_namelang', 'inf_ort__lon', 'inf_ort__lat', 'inf_ort__osm_id', 'geburtsort__ort_namekurz', 'geburtsort__ort_namelang',
				'id_person__geb_datum', 'ID_Inf__id_person__weiblich', 'ID_Inf__id_person__akt_wohnort__ort_namelang', 'eignung', 'kompetenz_d', 'haeufigkeit_d', 'kompetenz_s', 'haeufigkeit_s', 'ausserhalbwohnort', 'ausbildung_max', 'ausbildung_spez',
				'familienstand', 'migrationsklasse', 'kommentar', 'pretest', 'akquiriert_am', 'kontakt_durch__id', 'kontakt_durch__nachname'
			],
			'filter': [
				[
					{'id': 'team', 'field': '>PersonenDB|tbl_teams', 'type': 'select', 'queryFilter': 'inf_gruppe__gruppe_team__pk', 'verbose_name': 'Projektteam'}
				],
			],
		}
	)
	# auswertungen.append(
	# 	{
	# 		'id': 'informantenErhoben', 'titel': 'Informanten (Erhoben)', 'app_name': 'PersonenDB', 'tabelle_name': 'tbl_informanten',
	# 		'felder': ['id', 'inf_sigle'],
	# 		'sub':[
	# 			{
	# 				'app_name': 'KorpusDB', 'tabelle_name': 'tbl_aufgaben', 'where': ['tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=parent:id'],
	# 				'felder':['id', 'Beschreibung_Aufgabe'],
	# 			},
	# 		]
	# 	},
	# )
	return auswertungView(auswertungen, asurl, request, info, error)


def erhobeneInformanten(request, xls='0'):
	"""Anzeige für erhobeneInformanten."""
	import PersonenDB.models as PersonenDB
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')

	xls = int(xls)
	lines = [['Inf. Id', 'Inf. Sigle', 'Aufg. ID', 'Aufgaben Beschreibung', 'Antworten']]
	adg = 0
	for aInf in PersonenDB.tbl_informanten.objects.all():
		aLine = [aInf.id, aInf.inf_sigle]
		for aAufgabe in KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__tbl_inf_zu_erhebung__ID_Inf=aInf.id).order_by('Beschreibung_Aufgabe'):
			aAntwortenCount = KorpusDB.tbl_antworten.objects.filter(zu_Aufgabe=aAufgabe.id, von_Inf=aInf.id).count()
			lines.append(aLine + [aAufgabe.id, aAufgabe.Beschreibung_Aufgabe, aAntwortenCount])
			adg += 1
			if adg > 29 and xls == 0:
				break
		if adg > 29 and xls == 0:
			break
	if xls == 1:
		from django.http import HttpResponse
		import xlwt
		response = HttpResponse(content_type='text/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="erhobene_informanten.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Erhobene Informanten')
		row_num = 0
		font_style = xlwt.XFStyle()
		for obj in lines:
			row_num += 1
			row = obj
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		wb.save(response)
		return response
	# Ausgabe der Seite
	return render_to_response(
		'korpusdbmaske/erhobene_informanten.html',
		RequestContext(request, {'lines': lines, 'error': error, 'info': info}),)


def transcripts(request):
	"""Anzeige Transkripte."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'AnnotationsDB'
	tabelle_name = 'transcript'
	permName = 'transcript'
	primaerId = 'transcript'
	aktueberschrift = 'Transkripte'
	asurl = '/korpusdb/transcripts/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Transkript', 'titel_plural': 'Transkripte', 'app': 'AnnotationsDB', 'tabelle': 'transcript', 'id': 'transcript', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'name', 'default_tier', '!Hinweis'],
		'feldoptionen':{
			'Hinweis': {'view_html': '<div style="text-align:center;">Transkript in <a href="/korpusdb/inferhebung">InfErhebungen</a> zuordnen.</div>', 'edit_html': '<div></div>'}
		}
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
