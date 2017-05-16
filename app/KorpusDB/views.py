from django.shortcuts import get_object_or_404 , render , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.db.models import Count
from DB.funktionenDB import formularView
import datetime
import json
from .models import sys_presettags
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB

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
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ChildTag">{% getFeldVal aData.felder \'id_ChildTag\' %}</span>',
		 	},
	 		{'titel':'Tag Ebene zu Tag','titel_plural':'Tag Ebenen zu Tag','app':'KorpusDB','tabelle':'tbl_tagebenezutag','id':'tagebenezutag','optionen':['liste','elementeclosed'],
 		 	 'felder':['+id','|id_Tag=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
		 	},
		 ],
		 'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

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
			ptags=KorpusDB.tbl_antwortentags.objects.filter(primaer=True,id_Antwort=val.pk).order_by('Reihung')
			stags=KorpusDB.tbl_antwortentags.objects.filter(primaer=False,id_Antwort=val.pk).order_by('Reihung')
			xtags = []
			for xval in KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
				xtags.append({'ebene':KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags':getTagFamilie(KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
			Antworten.append({'model':val, 'ptags':ptags, 'stags':stags, 'xtags':xtags})
		Antworten.append(eAntwort)
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk,id_InfErh__ID_Inf__pk=ipk)
		aPresetTags = []
		for val in sys_presettags.objects.all():
			aPresetTags.append({'model':val,'tagfamilie':getTagFamiliePT(val.id_Tags.all())})
		return render_to_response(aFormular,
			RequestContext(request, {'Informant':Informant,'Aufgabe':Aufgabe,'Antworten':Antworten, 'TagEbenen':TagEbenen ,'TagsList':TagsList,'ErhInfAufgaben':ErhInfAufgaben,'PresetTags':aPresetTags,'test':test,'error':error}),)
	InformantenCount=PersonenDB.tbl_informanten.objects.all().count()
	aAufgabenset = 0	; Aufgabensets = [{'model':val,'Acount':KorpusDB.tbl_aufgaben.objects.filter(von_ASet = val.pk).count()} for val in KorpusDB.tbl_aufgabensets.objects.all()]
	aAufgabe = 0		; Aufgaben = None
	Informanten = None
	if 'aaufgabenset' in request.POST:
		aAufgabenset = int(request.POST.get('aaufgabenset'))
		if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
			aAufgabe = int(request.POST.get('aaufgabe'))
			aResponse = HttpResponse(str({str(val.pk):str(KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count()) for val in PersonenDB.tbl_informanten.objects.all()}).replace("'",'"'))
			aResponse['Content-Type'] = 'text/text'
			return aResponse
		if aAufgabenset == int(request.POST.get('laufgabenset')):
			aAufgabe = int(request.POST.get('aaufgabe'))
			Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count} for val in PersonenDB.tbl_informanten.objects.all()]
		Aufgaben = []
		for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aAufgabenset):
			try:
				aproz = (100/InformantenCount*KorpusDB.tbl_antworten.objects.filter(zu_Aufgabe=val.pk).values('zu_Aufgabe').annotate(total=Count('von_Inf'))[0]['total'])
			except:
				aproz = 0
			Aufgaben.append({'model':val, 'aProz': aproz})
	# Ausgabe der Seite
	return render_to_response('korpusdbmaske/start.html',
		RequestContext(request, {'aAufgabenset':aAufgabenset,'Aufgabensets':Aufgabensets,'aAufgabe':aAufgabe,'Aufgaben':Aufgaben,'Informanten':Informanten,'test':test}),)



### Funktionen: ###

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
