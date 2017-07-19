from django.shortcuts import get_object_or_404 , render , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.db.models import Count, Q
from DB.funktionenDB import formularView, auswertungView
import datetime
import json
from .models import sys_presettags
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from django.conf import settings
import os

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
	aufgabenform = [
		{'titel':'InfErhebung','titel_plural':'InfErhebungen','app':'KorpusDB','tabelle':'tbl_inferhebung','id':'inferhebung','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','ID_Erh','ID_Inf','Datum','Explorator','Kommentar','Dateipfad','Audiofile','time_beep','sync_time','Logfile','Ort','Besonderheiten','!Audioplayer'],
		 'feldoptionen':{'Audioplayer':{'view_html':'<div></div>','edit_html':InlineAudioPlayer},},
	 	 'addCSS':[{'static':'korpusdbmaske/css/fxaudioplayer.css'},],
	 	 'addJS':[{'static':'korpusdbmaske/js/fxaudioplayer.js'},],
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
	aFormular = 'korpusdbmaske/start_formular.html'
	test = ''
	error = ''
	apk=int(apk)
	ipk=int(ipk)
	if apk>0 and ipk>0:
		if 'save' in request.POST:
			if request.POST.get('save') == 'ErhInfAufgaben':
				saveErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.get(pk=int(request.POST.get('pk')))
				saveErhInfAufgaben.start_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('start_Aufgabe') if request.POST.get('start_Aufgabe') else 0)*1000000))
				saveErhInfAufgaben.stop_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('stop_Aufgabe') if request.POST.get('stop_Aufgabe') else 0)*1000000))
				saveErhInfAufgaben.save()
				aFormular = 'korpusdbmaske/audio_formular.html'
			elif request.POST.get('save') == 'Aufgaben':
				for aAntwort in json.loads(request.POST.get('aufgaben')):
					if 'delit' in aAntwort:		# Löschen
						aDelAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
						test+=str(aDelAntwort)+' Löschen!<br>'
						if aDelAntwort.ist_Satz:
							aDelAntwort.ist_Satz.delete()
							test+='Satz gelöscht<br>'
						aDelAntwort.delete()
						test+='<hr>'
					else:						# Speichern/Erstellen
						if aAntwort['Kommentar'] or aAntwort['ist_Satz_Standardorth'] or aAntwort['ist_bfl'] or aAntwort['bfl_durch_S'] or aAntwort['ist_Satz_Transkript'] or aAntwort['start_Antwort'] or aAntwort['stop_Antwort'] or aAntwort['tags']:
							if int(aAntwort['id_Antwort']) > 0:		# Speichern
								aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
								sTyp = ' gespeichert!<br>'
							else:									# Erstellen
								aSaveAntwort = KorpusDB.tbl_antworten()
								sTyp = ' erstellt!<br>'
							aSaveAntwort.ist_gewaehlt = False
							aSaveAntwort.ist_nat = False
							aSaveAntwort.von_Inf = PersonenDB.tbl_informanten.objects.get(pk=int(aAntwort['von_Inf']))
							aSaveAntwort.zu_Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=int(aAntwort['zu_Aufgabe']))
							aSaveAntwort.Reihung = int(aAntwort['reihung'])
							aSaveAntwort.ist_bfl = aAntwort['ist_bfl']
							aSaveAntwort.bfl_durch_S = aAntwort['bfl_durch_S']
							aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['start_Antwort'] if aAntwort['start_Antwort'] else 0)*1000000))
							aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['stop_Antwort'] if aAntwort['stop_Antwort'] else 0)*1000000))
							aSaveAntwort.Kommentar = aAntwort['Kommentar']
							if int(aAntwort['ist_Satz_pk']) > 0:	# Satz bearbeiten
								asSatz = KorpusDB.tbl_saetze.objects.get(pk=aAntwort['ist_Satz_pk'])
								ssTyp = ' gespeichert!<br>'
							else:									# Satz erstellen
								asSatz = KorpusDB.tbl_saetze()
								ssTyp = ' erstellt!<br>'
							asSatz.Transkript = aAntwort['ist_Satz_Transkript']
							asSatz.Standardorth = aAntwort['ist_Satz_Standardorth']
							asSatz.save()
							aSaveAntwort.ist_Satz = asSatz
							test+= 'Satz "'+str(aSaveAntwort.ist_Satz)+'" (PK: '+str(aSaveAntwort.ist_Satz.pk)+')'+ssTyp
							aSaveAntwort.save()
							for asTag in aAntwort['tags']:
								if int(asTag['id_tag'])==0 or int(asTag['id_TagEbene'])==0:
									if int(asTag['pk']) > 0:
										aDelAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										test+= 'AntwortenTag "'+str(aDelAntwortenTag)+'" (PK: '+str(aDelAntwortenTag.pk)+') gelöscht!<br>'
										aDelAntwortenTag.delete()
								else:
									if int(asTag['pk']) > 0:		# Tag bearbeiten
										asAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										stTyp = ' gespeichert!<br>'
									else:							# Tag erstellen
										asAntwortenTag = KorpusDB.tbl_antwortentags()
										stTyp = ' erstellt!<br>'
									asAntwortenTag.id_Antwort = aSaveAntwort
									asAntwortenTag.id_Tag =  KorpusDB.tbl_tags.objects.get(pk=int(asTag['id_tag']))
									asAntwortenTag.id_TagEbene =  KorpusDB.tbl_tagebene.objects.get(pk=int(asTag['id_TagEbene']))
									asAntwortenTag.Reihung =  int(asTag['reihung'])
									asAntwortenTag.save()
									test+= 'AntwortenTag "'+str(asAntwortenTag)+'" (PK: '+str(asAntwortenTag.pk)+')'+stTyp
							test+= 'Antwort "'+str(aSaveAntwort)+'" (PK: '+str(aSaveAntwort.pk)+')'+sTyp+'<hr>'
				aFormular = 'korpusdbmaske/antworten_formular.html'
		Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		eAntwort = KorpusDB.tbl_antworten()
		eAntwort.von_Inf = Informant
		eAntwort.zu_Aufgabe = Aufgabe
		TagEbenen = KorpusDB.tbl_tagebene.objects.all()
		TagsList = getTagList(KorpusDB.tbl_tags,None)
		Antworten = []
		for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk,zu_Aufgabe=apk).order_by('Reihung'):
			xtags = []
			for xval in KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
				xtags.append({'ebene':KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags':getTagFamilie(KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
			Antworten.append({'model':val, 'xtags':xtags})
		Antworten.append(eAntwort)
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk,id_InfErh__ID_Inf__pk=ipk)
		aPresetTags = []
		for val in sys_presettags.objects.filter(Q(sys_presettagszuaufgabe__id_Aufgabe = Aufgabe) | Q(sys_presettagszuaufgabe__id_Aufgabe = None)).distinct():
			aPresetTags.append({'model':val,'tagfamilie':getTagFamiliePT([tzpval.id_Tag for tzpval in val.sys_tagszupresettags_set.all()])})
		return render_to_response(aFormular,
			RequestContext(request, {'Informant':Informant,'Aufgabe':Aufgabe,'Antworten':Antworten, 'TagEbenen':TagEbenen ,'TagsList':TagsList,'ErhInfAufgaben':ErhInfAufgaben,'PresetTags':aPresetTags,'test':test,'error':error}),)
	# aErhebung = 0		; Erhebungen = [{'model':val,'Acount':KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhinfaufgaben__id_InfErh__ID_Erh__pk = val.pk).values('pk').annotate(Count('pk')).count()} for val in KorpusDB.tbl_erhebungen.objects.all()]
	aErhebung = 0		; Erhebungen = [{'model':val,'Acount':KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = val.pk).values('pk').annotate(Count('pk')).count()} for val in KorpusDB.tbl_erhebungen.objects.filter(Art_Erhebung__gt = 2)]
	aAufgabenset = 0	; Aufgabensets = None
	aAufgabe = 0		; Aufgaben = None
	Informanten = None
	aErhebung = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
	if aErhebung:
		InformantenCount=PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).count()
		Aufgabensets = []
		for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).distinct():
			Aufgabensets.append({'model':val,'Acount':KorpusDB.tbl_aufgaben.objects.filter(von_ASet = val.pk,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).count()})
		aAufgabenset = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
		if KorpusDB.tbl_aufgabensets.objects.filter(pk=aAufgabenset,tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).count() == 0:
			aAufgabenset = 0
		if aAufgabenset:
			aAufgabe = int(request.POST.get('aaufgabe')) if 'aaufgabenset' in request.POST else 0
			if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
				# aResponse = HttpResponse(str({str(val.pk):str(KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count()) for val in PersonenDB.tbl_informanten.objects.all()}).replace("'",'"'))
				# aResponse['Content-Type'] = 'text/text'
				# return aResponse
				Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
				return render_to_response('korpusdbmaske/lmfa-l_informanten.html',
					RequestContext(request, {'aErhebung':aErhebung,'aAufgabenset':aAufgabenset,'aAufgabe':aAufgabe,'Informanten':Informanten}),)
			if aAufgabenset == int(request.POST.get('laufgabenset')):
				Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
			Aufgaben = []
			for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aAufgabenset,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung):
				(aproz,atags,aqtags) = val.status()
				aproz = 100/InformantenCount*aproz
				Aufgaben.append({'model':val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
	# Ausgabe der Seite
	return render_to_response('korpusdbmaske/start.html',
		RequestContext(request, {'aErhebung':aErhebung,'Erhebungen':Erhebungen,'aAufgabenset':aAufgabenset,'Aufgabensets':Aufgabensets,'aAufgabe':aAufgabe,'Aufgaben':Aufgaben,'Informanten':Informanten,'test':test}),)

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

# Dateien
def dateien(request):
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	# Testmodus ... nur für Admins!
	# Permissions noch einbauen!
	if not request.user.is_superuser:
		return redirect('dissdb_login')

	mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
	if not mDir:
		return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')

	# Dateienliste:
	if 'getDirContent' in request.POST:
		dateien = scanFiles(request.POST.get('getDirContent'),mDir)
		return render_to_response('korpusdb/dateien.html',
			RequestContext(request, {'dateien':dateien,'verzeichniss':request.POST.get('getDirContent'),'info':info,'error':error}),)

	# Startseite mit "Baum":
	tree = scanDir(mDir)
	return render_to_response('korpusdb/dateien_start.html',
		RequestContext(request, {'tree':tree,'info':info,'error':error}),)

### Funktionen: ###

def scanFiles(sDir,bDir):
	imgTypes = ['jpg','jpeg','png']
	import datetime
	_FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
	def FiletimeToDateTime(ft):
		timestamp = ft.dwHighDateTime
		timestamp <<= 32
		timestamp |= ft.dwLowDateTime
		return _FILETIME_null_date + datetime.timedelta(microseconds=timestamp/10)
	psUrl = getattr(settings, 'AUDIO_URL', None)
	if psUrl[-1] == '/':
		psUrl = psUrl[:-1]
	if sDir[0] == '\\' or sDir[0] == '/':
		sDir = sDir[1:]
	rFiles = []
	aDir = os.path.join(bDir,sDir)
	objectList = os.listdir(aDir)
	objectList.sort()
	# Permissions noch einbauen!
	for aObject in objectList:
		aObjectAbs = os.path.join(aDir,aObject)
		if os.path.isfile(aObjectAbs):
			aObjectDir = aObjectAbs[len(bDir):]
			if aObjectDir[0] == '\\' or aObjectDir[0] == '/':
				aObjectDir = aObjectDir[1:]
			if os.stat_float_times():
				lmod = datetime.datetime.utcfromtimestamp(os.path.getmtime(aObjectAbs))
			else:
				lmod = os.path.getmtime(aObjectAbs)
			alink = os.path.normpath(aObjectDir).replace('\\','/')
			if alink[0] == '/':
				alink = alink[1:]
			alink = psUrl+'/'+alink
			aObjectData = {'name':aObject,'fullpath':aObjectDir,'link':alink,'size':os.path.getsize(aObjectAbs),'lmod':lmod}
			if '.' in aObjectDir:
				aObjectData['type'] = aObjectDir.rsplit('.', 1)[1].lower()
				if aObjectDir.rsplit('.', 1)[1].lower() in imgTypes and not '_temp' in aObjectDir:
					prevFile = os.path.join(bDir,'_temp',aObjectDir)
					if not os.path.isdir(os.path.dirname(prevFile)):
						print(os.makedirs(os.path.dirname(prevFile)))
					if not os.path.exists(prevFile) or os.path.getmtime(prevFile)<os.path.getmtime(aObjectAbs):
						from PIL import Image
						im = Image.open(aObjectAbs)
						im.thumbnail((300,200))
						im.save(prevFile, im.format)
					aObjectData['prvImg'] =  os.path.normpath(prevFile[len(bDir):]).replace('\\','/')
					if aObjectData['prvImg'][0] == '/':
						aObjectData['prvImg'] = aObjectData['prvImg'][1:]
					aObjectData['prvImg'] = psUrl+'/'+aObjectData['prvImg']
			rFiles.append(aObjectData)
	return rFiles

def scanDir(sDir,bDir=None):
	if not bDir:
		bDir = sDir
	rDirs = []
	objectList = os.listdir(sDir)
	objectList.sort()
	# Permissions noch einbauen!
	for aObject in objectList:
		if not '_temp' in aObject:
			aObjectAbs = os.path.join(sDir,aObject)
			if os.path.isdir(aObjectAbs):
				aObjectData = {'name':aObject,'fullpath':aObjectAbs[len(bDir):],'subdir':scanDir(aObjectAbs,bDir)}
				# Permissions noch einbauen! -> aObjectData['subdir']
				rDirs.append(aObjectData)
	return rDirs

def getTagList(Tags,TagPK):
	TagData = []
	if TagPK == None:
		for value in Tags.objects.filter(id_ChildTag=None):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	else:
		for value in Tags.objects.filter(id_ChildTag__id_ParentTag=TagPK):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	return TagData

# getTagFamilie für AntwortenTags
def getTagFamilie(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.id_Tag.Tag)+' ('+str(value.id_Tag.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_Tag.id_ParentTag.all().count()})
		afam.append(value.id_Tag)
		aGen+=1
	return oTags

# getTagFamilie für PresetTags
def getTagFamiliePT(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.Tag)+' ('+str(value.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_ParentTag.all().count()})
		afam.append(value)
		aGen+=1
	return oTags
