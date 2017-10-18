from django.shortcuts import render , render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db.models import Count, Q
import datetime
import json
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB

def view_maske2(request,ipk=0,apk=0):
	aFormular = 'korpusdbmaske2/start_formular.html'
	aUrl = '/korpusdb/maske2/'
	aDUrl = 'KorpusDB:maske2'
	useArtErhebung = [6,7]
	test = ''
	error = ''
	apk=int(apk)
	ipk=int(ipk)
	aAuswahl=1
	if 'aauswahl' in request.POST:
		aAuswahl=int(request.POST.get('aauswahl'))
	if apk>0 and ipk>0:
		if 'save' in request.POST:
			if request.POST.get('save') == 'Aufgaben':
				for aAntwort in json.loads(request.POST.get('aufgaben')):
					if 'delit' in aAntwort:		# Löschen
						test+='Löschen funktioniert nicht!'
	# 					aDelAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
	# 					test+=str(aDelAntwort)+' Löschen!<br>'
	# 					if aDelAntwort.ist_Satz:
	# 						aDelAntwort.ist_Satz.delete()
	# 						test+='Satz gelöscht<br>'
	# 					aDelAntwort.delete()
	# 					test+='<hr>'
					else:						# Speichern/Erstellen
						if int(aAntwort['Aufgabenart']) == 1:	# Aufgabenart: Bewertungsaufgabe (1)
							for aSub in aAntwort['sub']:
								if int(aSub['sys_antworten_pk']) > 0:
									aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=int(aSub['sys_antworten_pk']))
									sTyp = ' gespeichert!<br>'
									aSaveAntwortNew = False
								else:
									aSaveAntwort = KorpusDB.tbl_antworten()
									sTyp = ' erstellt!<br>'
									aSaveAntwortNew = True
								aSaveAntwort.von_Inf = PersonenDB.tbl_informanten.objects.get(pk=int(aAntwort['von_Inf']))
								aSaveAntwort.zu_Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=int(aAntwort['zu_Aufgabe']))
								aSaveAntwort.ist_am = KorpusDB.tbl_antwortmoeglichkeiten.objects.get(pk=int(aSub['sys_aufgabenm_pk']))
								aSaveAntwort.ist_gewaehlt = aSub['ist_gewaehlt']
								aSaveAntwort.ist_nat = aSub['ist_nat']
								aSaveAntwort.kontrolliert = aSub['kontrolliert']
								aSaveAntwort.veroeffentlichung = aSub['veroeffentlichung']
								if 'kommentar' in aSub:
									if aSub['kommentar']:
										aSaveAntwort.Kommentar = aSub['kommentar']
									else:
										aSaveAntwort.Kommentar = None
								if 'ist_Satz.Transkript' in aSub:
									if aSub['ist_Satz.Transkript']:
										if aSaveAntwort.ist_Satz:
											asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
											ssTyp = ' gespeichert!<br>'
											asSatzNew = False
										else:
											asSatz = KorpusDB.tbl_saetze()
											ssTyp = ' erstellt!<br>'
											asSatzNew = True
										asSatz.Transkript = aSub['ist_Satz.Transkript']
										asSatz.save()
										LogEntry.objects.log_action(
											user_id = request.user.pk,
											content_type_id = ContentType.objects.get_for_model(asSatz).pk,
											object_id = asSatz.pk,
											object_repr = str(asSatz),
											action_flag = ADDITION if asSatzNew else CHANGE
										)
										aSaveAntwort.ist_Satz = asSatz
										test+= 'Satz "'+str(aSaveAntwort.ist_Satz)+'" (PK: '+str(aSaveAntwort.ist_Satz.pk)+')'+ssTyp
								aSaveAntwort.Reihung = None
								aSaveAntwort.ist_bfl = False
								aSaveAntwort.bfl_durch_S = None
								aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=0)
								aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
								aSaveAntwort.save()
								LogEntry.objects.log_action(
									user_id = request.user.pk,
									content_type_id = ContentType.objects.get_for_model(aSaveAntwort).pk,
									object_id = aSaveAntwort.pk,
									object_repr = str(aSaveAntwort),
									action_flag = ADDITION if aSaveAntwortNew else CHANGE
								)
								test+= 'Antwort "'+str(aSaveAntwort)+'" (PK: '+str(aSaveAntwort.pk)+')'+sTyp+'<hr>'
						elif int(aAntwort['Aufgabenart']) >= 2 and int(aAntwort['Aufgabenart']) <= 4:	# Ergänzungsaufgabe(2) Puzzleaufgabe(3), Übersetzungsaufgabe (4)
							if int(aAntwort['antwort_pk']) > 0:
								aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=int(aAntwort['antwort_pk']))
								sTyp = ' gespeichert!<br>'
								aSaveAntwortNew = False
							else:
								aSaveAntwort = KorpusDB.tbl_antworten()
								sTyp = ' erstellt!<br>'
								aSaveAntwortNew = True
							aSaveAntwort.von_Inf = PersonenDB.tbl_informanten.objects.get(pk=int(aAntwort['von_Inf']))
							aSaveAntwort.zu_Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=int(aAntwort['zu_Aufgabe']))
							aSaveAntwort.ist_gewaehlt = False
							aSaveAntwort.ist_nat = False
							aSaveAntwort.kontrolliert = aAntwort['kontrolliert']
							aSaveAntwort.veroeffentlichung = aAntwort['veroeffentlichung']
							aSaveAntwort.Kommentar = aAntwort['kommentar']
							if 'ist_Satz.Transkript' in aAntwort:
								if aAntwort['ist_Satz.Transkript']:
									if aSaveAntwort.ist_Satz:
										asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
										ssTyp = ' gespeichert!<br>'
										asSatzNew = False
									else:
										asSatz = KorpusDB.tbl_saetze()
										ssTyp = ' erstellt!<br>'
										asSatzNew = True
									asSatz.Transkript = aAntwort['ist_Satz.Transkript']
									asSatz.save()
									LogEntry.objects.log_action(
										user_id = request.user.pk,
										content_type_id = ContentType.objects.get_for_model(asSatz).pk,
										object_id = asSatz.pk,
										object_repr = str(asSatz),
										action_flag = ADDITION if asSatzNew else CHANGE
									)
									aSaveAntwort.ist_Satz = asSatz
									test+= 'Satz "'+str(aSaveAntwort.ist_Satz)+'" (PK: '+str(aSaveAntwort.ist_Satz.pk)+')'+ssTyp
							aSaveAntwort.Reihung = None
							aSaveAntwort.ist_bfl = False
							aSaveAntwort.bfl_durch_S = None
							aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=0)
							aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
							aSaveAntwort.save()
							LogEntry.objects.log_action(
								user_id = request.user.pk,
								content_type_id = ContentType.objects.get_for_model(aSaveAntwort).pk,
								object_id = aSaveAntwort.pk,
								object_repr = str(aSaveAntwort),
								action_flag = ADDITION if aSaveAntwortNew else CHANGE
							)
							test+= 'Antwort "'+str(aSaveAntwort)+'" (PK: '+str(aSaveAntwort.pk)+')'+sTyp+'<hr>'
						else:
							test+='Aufgabenart '+str(aAntwort['Aufgabenart'])+' ist unbekannt!'
				aFormular = 'korpusdbmaske2/antworten_formular.html'
		Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		AufgabenMitAntworten = []
		Antwort = None
		if Aufgabe.Aufgabenart.pk == 1:	# Aufgabenart: Bewertungsaufgabe (1)
			for val in KorpusDB.tbl_antwortmoeglichkeiten.objects.filter(zu_Aufgabe=apk).order_by('Reihung'):
				try:
					antwort = KorpusDB.tbl_antworten.objects.get(zu_Aufgabe=apk,von_Inf=ipk,ist_am=val.pk)
				except KorpusDB.tbl_antworten.DoesNotExist:
					antwort = None
				AufgabenMitAntworten.append({'model':val,'antwort':antwort})
		elif Aufgabe.Aufgabenart.pk >= 2 and Aufgabe.Aufgabenart.pk <= 4:	# Ergänzungsaufgabe(2) Puzzleaufgabe(3), Übersetzungsaufgabe (4)
			Antwort = KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk,zu_Aufgabe=apk).first()
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk,id_InfErh__ID_Inf__pk=ipk)
		return render_to_response(aFormular,
			RequestContext(request, {'Informant':Informant,'Aufgabe':Aufgabe,'Antwort':Antwort,'AufgabenMitAntworten':AufgabenMitAntworten,'ErhInfAufgaben':ErhInfAufgaben,'aDUrl':aDUrl,'test':test,'error':error}),)
	aErhebung = 0		; Erhebungen = [{'model':val,'Acount':KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = val.pk).values('pk').annotate(Count('pk')).count()} for val in KorpusDB.tbl_erhebungen.objects.filter(Art_Erhebung__in = useArtErhebung)]
	aAufgabenset = 0	; Aufgabensets = None
	aAufgabe = 0		; Aufgaben = None
	Informanten = None
	if aAuswahl == 1:	# Filter: Erhebung
		aErhebung = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
		if aErhebung:
			InformantenCount=PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).count()
			Aufgabensets = []
			for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung,tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).distinct():
				Aufgabensets.append({'model':val,'Acount':KorpusDB.tbl_aufgaben.objects.filter(von_ASet = val.pk,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung,tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).count()})
			aAufgabenset = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
			if KorpusDB.tbl_aufgabensets.objects.filter(pk=aAufgabenset,tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung).count() == 0:
				aAufgabenset = 0
			if aAufgabenset:
				aAufgabe = int(request.POST.get('aaufgabe')) if 'aaufgabenset' in request.POST else 0
				if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
					Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
					return render_to_response('korpusdbmaske2/lmfa-l_informanten.html',
						RequestContext(request, {'aErhebung':aErhebung,'aAufgabenset':aAufgabenset,'aAufgabe':aAufgabe,'Informanten':Informanten,'aDUrl':aDUrl}),)
				if aAufgabenset == int(request.POST.get('laufgabenset')):
					Informanten = [{'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=val,zu_Aufgabe=aAufgabe,tbl_antwortentags__id_Tag=35).count()} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk = aErhebung).order_by('inf_sigle')]
				Aufgaben = []
				for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aAufgabenset,tbl_erhebung_mit_aufgaben__id_Erh__pk = aErhebung,tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung):
					(aproz,atags,aqtags) = val.status(useArtErhebung)
					if InformantenCount>0:
						aproz = 100/InformantenCount*aproz
					else:
						aproz = 0
					Aufgaben.append({'model':val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
	aInformant = 0
	selInformanten = None
	verfuegbareErhebungen = []
	if aAuswahl == 2:	# Filter: Informant
		selInformanten = []
		for val in PersonenDB.tbl_informanten.objects.all():
			aSelInformanten = {'model':val}
			aSelInformanten['count'] = KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk=val.pk,tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).count()
			try:
				aSelInformanten['done'] = KorpusDB.tbl_antworten.objects.filter(von_Inf=val.pk,zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).values('zu_Aufgabe').annotate(total=Count('zu_Aufgabe')).order_by('zu_Aufgabe').count()
			except:
				aSelInformanten['done'] = 0
			selInformanten.append(aSelInformanten)
		if 'ainformant' in request.POST:
			aInformant=int(request.POST.get('ainformant'))
			Aufgaben = []
			for val in KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk=aInformant,tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).order_by('Beschreibung_Aufgabe'):
				aAufgabeLine = {'model':val,'count':KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant,zu_Aufgabe=val.pk,zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in = useArtErhebung).count(),'tags':KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant,zu_Aufgabe=val.pk).exclude(tbl_antwortentags=None).count(),'qtag':KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant,zu_Aufgabe=val.pk,tbl_antwortentags__id_Tag=35).count()}
				try:
					aAufgabeLine['erhebungen'] = []
					for aErheb in KorpusDB.tbl_erhebung_mit_aufgaben.objects.filter(id_Aufgabe=val.pk):
						aErhebungenLine = {'pk':aErheb.id_Erh.pk,'title':str(aErheb.id_Erh)}
						aAufgabeLine['erhebungen'].append(aErhebungenLine)
						if not aErhebungenLine in verfuegbareErhebungen:
							verfuegbareErhebungen.append(aErhebungenLine)
				except:
					pass
				Aufgaben.append(aAufgabeLine)
			if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
				return render_to_response('korpusdbmaske2/lmfa-l_aufgaben.html',
					RequestContext(request, {'aInformant':aInformant,'Aufgaben':Aufgaben,'verfuegbareErhebungen':verfuegbareErhebungen,'aDUrl':aDUrl}),)
	# Ausgabe der Seite
	return render_to_response('korpusdbmaske2/start.html',
		RequestContext(request, {'aAuswahl':aAuswahl,'selInformanten':selInformanten,'aInformant':aInformant,'aErhebung':aErhebung,'Erhebungen':Erhebungen,'aAufgabenset':aAufgabenset,'Aufgabensets':Aufgabensets,'aAufgabe':aAufgabe,'Aufgaben':Aufgaben,'Informanten':Informanten,'aUrl':aUrl,'aDUrl':aDUrl,'test':test}),)

### Funktionen: ###
