from django.shortcuts import get_object_or_404 , render , render_to_response , redirect
from django.template import RequestContext, loader
from DB.funktionenDB import formularView, auswertungView
from .models import sys_presettags
import KorpusDB.models as KorpusDB

def aufgabensets(request):
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
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Aufgabenset','app':'KorpusDB','tabelle':'tbl_aufgabensets','id':'aufgabenset','optionen':['einzeln'],
		 'felder':['+id','Kuerzel','Name_Aset','Fokus','Art_ASet','Kommentar','zu_Phaenomen','|zusammengestellt_als=aufgabenzusammenstellung:id'],
		 'sub':[
			{'titel':'Aufgaben','app':'KorpusDB','tabelle':'tbl_aufgaben','id':'aufgabe','optionen':['liste'],
			 'felder':['+id','Variante','ist_dialekt','Beschreibung_Aufgabe','|von_ASet=parent:id'],
			 'sub':[
				{'titel':'Antwortmoeglichkeiten','app':'KorpusDB','tabelle':'tbl_antwortmoeglichkeiten','id':'antwortmoeglichkeit','optionen':['liste'],
				 'felder':['+id','Kuerzel','frei','|Reihung=auto:reihung','|zu_Aufgabe=parent:id']},
				{'titel':'Aufgabenfiles','app':'KorpusDB','tabelle':'tbl_aufgabenfiles','id':'aufgabenfiles','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','ist_Anweisung','File_Link','Kommentar','|Reihung=auto:reihung','|id_Aufgabe=parent:id']}
			 ]
			},
			{'titel':'Aufgabenzusammenstellung','app':'KorpusDB','tabelle':'tbl_aufgabenzusammenstellungen','id':'aufgabenzusammenstellung','optionen':['einzeln'],
			 'felder':['+id=parent:zusammengestellt_als','Bezeichnung_AZus','Kommentar','AZusCol'],
			 'sub':[
				{'titel':'Beinhaltete Medientypen','app':'KorpusDB','tabelle':'tbl_azusbeinhaltetmedien','id':'azusbeinhaltetmedien','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','|Reihung=auto:reihung','|id_AZus=parent:id']}
			 ]
			}
		 ]
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def tagsedit(request):
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
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Tag','titel_plural':'Tags','app':'KorpusDB','tabelle':'tbl_tags','id':'tags','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','Tag','Tag_lang','zu_Phaenomen','Kommentar','Generation','AReihung'],
		 'sub':[
			{'titel':'Tag Familie - Parent','titel_plural':'Tag Familie - Parents','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamilieparents','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_ChildTag=parent:id','id_ParentTag'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ParentTag">{% getFeldVal aData.felder \'id_ParentTag\' %}</span>',
			},
			{'titel':'Tag Familie - Child','titel_plural':'Tag Familie - Childs','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamiliechilds','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_ParentTag=parent:id','id_ChildTag'],
#			 'feldoptionen':{'id_ChildTag':{'foreignkey_select':{'data':{'generation':'Generation'},'select_data':{'tagedit':'+1','taggentar':'#fid_Generation_1_1'}},}},
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ChildTag">{% getFeldVal aData.felder \'id_ChildTag\' %}</span>',
			},
			{'titel':'Tag Ebene zu Tag','titel_plural':'Tag Ebenen zu Tag','app':'KorpusDB','tabelle':'tbl_tagebenezutag','id':'tagebenezutag','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_Tag=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
		 ],
		 'suboption':['tab'],
#		 'addJS':[{'static':'korpusdbmaske/js/tagedit.js'},],
		},
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def presettagsedit(request):
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
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Preset Tags','titel_plural':'Presets Tags','app':'KorpusDB','tabelle':'sys_presettags','id':'presettags','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','Bezeichnung','Kommentar','Reihung'],
		 'sub':[
			{'titel':'Tag zu Preset Tags','titel_plural':'Tags zu Preset Tags','app':'KorpusDB','tabelle':'sys_tagszupresettags','id':'tagszupresettags','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_Tag','|Reihung=auto:reihung'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_Tag">{% getFeldVal aData.felder \'id_Tag\' %}</span>',
			},
			{'titel':'Tag Ebene zu Preset Tags','titel_plural':'Tag Ebenen zu Preset Tags','app':'KorpusDB','tabelle':'sys_tagebenezupresettags','id':'tagebenezupresettags','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
			},
			{'titel':'Preset Tags zu Aufgabe','titel_plural':'Presets Tags zu Aufgabe','app':'KorpusDB','tabelle':'sys_presettagszuaufgabe','id':'presettagszuaufgabe','optionen':['liste','elementeclosed'],
			 'felder':['+id','|id_PresetTags=parent:id','id_Aufgabe'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_Aufgabe">{% getFeldVal aData.felder \'id_Aufgabe\' %}</span>',
			},
		 ],
		 'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def inferhebung(request):
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
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	InlineAudioPlayer = loader.render_to_string('korpusdbmaske/fxaudioplayer.html',
		RequestContext(request, {'audioDir':'input[name="Dateipfad"]','audioFile':'input[name="Audiofile"]', 'audioPbMarker':['input[name="time_beep"]','input[name="sync_time"]']}),)
	from .view_dateien import getPermission, scanFiles, scanDir, removeLeftSlash, tree2select
	from django.conf import settings
	import os
	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
	def dateipfadFxfunction(aval,siblings):
		adir = removeLeftSlash(aval['value'])
		adirABS = os.path.normpath(os.path.join(mDir,adir))
		if not os.path.isdir(adirABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Verzeichniss existiert nicht!'
		if not getPermission(adir,mDir,request)>0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = tree2select(scanDir(mDir,None,request))
			isInList = False
			aval['value'] = os.path.normpath(removeLeftSlash(aval['value']))
			for aselectitm in aselect:
				if aval['value'] == aselectitm['value']:
					isInList = True
					aval['value'] = aval['value']
					break
			if not isInList:
				aselect = [{'title':os.path.normpath(aval['value']),'value':os.path.normpath(aval['value'])}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['showValue'] = True
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval
	def audiofileFxfunction(aval,siblings):
		aFile = removeLeftSlash(aval['value'])
		aDir = ''
		for aFeld in siblings:
			if aFeld['name']=='Dateipfad':
				aDir = removeLeftSlash(aFeld['value'])
				break
		aFileABS = os.path.normpath(os.path.join(mDir,aDir,aFile))
		if not os.path.isfile(aFileABS):
			aval['feldoptionen']['fxtype']['danger'] = 'Verzeichniss existiert nicht!'
		if not getPermission(aDir,mDir,request)>0:
			aval['feldoptionen']['fxtype']['type'] = 'blocked'
		else:
			aselect = []
			isInList = False
			if os.path.isdir(os.path.normpath(os.path.join(mDir,aDir))):
				for aFile in scanFiles(aDir,mDir,request):
					aselect.append({'title':aFile['name'],'value':aFile['name']})
					if aFile['name'] == aval['value']:
						isInList = True
			if not isInList:
				aselect = [{'title':aval['value'],'value':aval['value']}] + aselect
			aval['feldoptionen']['fxtype']['type'] = 'select'
			aval['feldoptionen']['fxtype']['select'] = aselect
		return aval
	dateipfadFxType = {'fxtype':{'fxfunction':dateipfadFxfunction},'nl':True}
	audiofileFxType = {'fxtype':{'fxfunction':audiofileFxfunction},'nl':True}
	aufgabenform = [
		{'titel':'InfErhebung','titel_plural':'InfErhebungen','app':'KorpusDB','tabelle':'tbl_inferhebung','id':'inferhebung','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','ID_Erh','ID_Inf','Datum','Explorator','Kommentar','Dateipfad','Audiofile','time_beep','sync_time','Logfile','Ort','Besonderheiten','!Audioplayer'],
		 'feldoptionen':{'Audioplayer':{'view_html':'<div></div>','edit_html':InlineAudioPlayer},'Dateipfad':dateipfadFxType,'Audiofile':audiofileFxType},
		 'addCSS':[{'static':'korpusdbmaske/css/fxaudioplayer.css'},],
		 'addJS':[{'static':'korpusdbmaske/js/fxaudioplayer.js'},],
		 'import':{
		 	'enabled':True,

		 },
		},
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

# Eingabemaske - ipk=tbl_informanten, apk=tbl_aufgaben
def maske(request,ipk=0,apk=0):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('KorpusDB.antworten_maskEdit'):
		return redirect('Startseite:start')
	from .view_maske import view_maske
	return view_maske(request,ipk,apk)

# Auswertung
def auswertung(request):
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('KorpusDB.auswertung'):
		return redirect('Startseite:start')
	asurl = '/korpusdb/auswertung/'
	auswertungen = [{'id':'antworten','titel':'Antworten','app_name':'KorpusDB','tabelle_name':'tbl_antworten',
					 'felder':['id','ist_bfl','bfl_durch_S','ist_Satz_id','ist_Satz__Transkript','ist_Satz__Standardorth','ist_Satz__Kommentar','tbl_antwortentags_set__!TagListeF','tbl_antwortentags_set__!TagListeFid','von_Inf_id','von_Inf__inf_sigle','von_Inf__id_person__geb_datum','von_Inf__id_person__weiblich','von_Inf__inf_gruppe__gruppe_bez','von_Inf__inf_ort','Kommentar','zu_Aufgabe_id','zu_Aufgabe__Beschreibung_Aufgabe','zu_Aufgabe__von_ASet_id','zu_Aufgabe__von_ASet__Kuerzel'],
					 'filter':[[{'id':'erhebungen','field':'>KorpusDB|tbl_erhebungen','type':'select','selectFilter':{'Art_Erhebung__gt':2},'queryFilter':'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk','verbose_name':'Erhebung'},
								{'id':'aufgabenset','field':'zu_Aufgabe__von_ASet','type':'select','selectFilter':{'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk':'!erhebungen'},'queryFilter':'zu_Aufgabe__von_ASet__pk','verbose_name':'Aufgabenset'},
								#{'field':'zu_Aufgabe','type':'select','selectFilter':{'zu_Aufgabe__von_ASet':'!aufgabenset'},'queryFilter':'zu_Aufgabe__pk','verbose_name':'Aufgabe'}
							  ]],
					 #'orderby':{'id':['id']},
					},
					{'id':'antwortenTagEbenen','titel':'Antworten (Tag Ebenen)','app_name':'KorpusDB','tabelle_name':'tbl_antworten',
					 'felder':['id','ist_bfl','bfl_durch_S','ist_Satz_id','ist_Satz__Transkript','ist_Satz__Standardorth','ist_Satz__Kommentar','tbl_antwortentags_set__!TagEbenenF','tbl_antwortentags_set__!TagEbenenFid','von_Inf_id','von_Inf__inf_sigle','von_Inf__id_person__geb_datum','von_Inf__id_person__weiblich','von_Inf__inf_gruppe__gruppe_bez','von_Inf__inf_ort','Kommentar','zu_Aufgabe_id','zu_Aufgabe__Beschreibung_Aufgabe','zu_Aufgabe__von_ASet_id','zu_Aufgabe__von_ASet__Kuerzel'],
					 'filter':[[{'id':'erhebungen','field':'>KorpusDB|tbl_erhebungen','type':'select','selectFilter':{'Art_Erhebung__gt':2},'queryFilter':'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk','verbose_name':'Erhebung'},
								{'id':'aufgabenset','field':'zu_Aufgabe__von_ASet','type':'select','selectFilter':{'tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk':'!erhebungen'},'queryFilter':'zu_Aufgabe__von_ASet__pk','verbose_name':'Aufgabenset'},
							  ]],
				   }]
	return auswertungView(auswertungen,asurl,request,info,error)

# CSV Import
def csv(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	# Rechte!
	if not request.user.is_superuser:
		return redirect('dissdb_login')

	from .view_csv import view_csv
	return view_csv(request)


### Funktionen: ###
