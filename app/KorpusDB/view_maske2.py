"""Für EingabeFB."""
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
import json
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from DB.funktionenDB import std_log_action
from .function_menue import getMenue
from .function_tags import saveTags, getTags, getTagsData


def view_maske2(request, ipk=0, apk=0):
	"""Ansicht für EingabeSTP."""
	aFormular = 'korpusdbmaske2/start_formular.html'
	aUrl = '/korpusdb/maske2/'
	aDUrl = 'KorpusDB:maske2'
	useArtErhebung = [6, 7]
	useOnlyErhebung = []
	for aUKDBES in request.user.user_korpusdb_erhebung_set.all():
		useOnlyErhebung.append(aUKDBES.erhebung_id)
	test = ''
	error = ''
	apk = int(apk)
	ipk = int(ipk)
	if apk > 0 and ipk > 0:
		# Speichern
		if 'save' in request.POST:
			if request.POST.get('save') == 'Aufgaben':
				for aAntwort in json.loads(request.POST.get('aufgaben')):
					if 'delit' in aAntwort:		# Löschen
						test += 'Löschen funktioniert nicht!'
					else:						# Speichern/Erstellen
						if int(aAntwort['Aufgabenart']) == 1:  # Aufgabenart: Bewertungsaufgabe (1)
							for aSub in aAntwort['sub']:
								if 'delit' in aSub and int(aSub['delit']) == 1:
									if int(aSub['sys_antworten_pk']) > 0:
										aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=int(aSub['sys_antworten_pk']))
										if aSaveAntwort.ist_Satz:
											asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
											aSaveAntwort.ist_Satz = None
											if asSatz.tbl_antworten_set.all().count() == 1:
												test += 'Satz "' + str(asSatz) + '" (PK: ' + str(asSatz.pk) + ') <b>gelöscht!</b><br>'
												asSatz.delete()
												std_log_action(request, asSatz, 'delete')
										aSaveAntwort.delete()
										test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ') <b>gelöscht!</b><hr>'
										std_log_action(request, aSaveAntwort, 'delete')
								else:
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
											std_log_action(request, asSatz, 'add' if asSatzNew else 'change')
											aSaveAntwort.ist_Satz = asSatz
											test += 'Satz "' + str(aSaveAntwort.ist_Satz) + '" (PK: ' + str(aSaveAntwort.ist_Satz.pk) + ')' + ssTyp
										elif aSaveAntwort.ist_Satz:
											asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
											aSaveAntwort.ist_Satz = None
											if asSatz.tbl_antworten_set.all().count() == 1:
												test += 'Satz "' + str(asSatz) + '" (PK: ' + str(asSatz.pk) + ') <b>gelöscht!</b><br>'
												asSatz.delete()
												std_log_action(request, asSatz, 'delete')
									aSaveAntwort.Reihung = aSub['dg']
									aSaveAntwort.ist_bfl = False
									aSaveAntwort.bfl_durch_S = None
									aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=0)
									aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
									aSaveAntwort.save()
									std_log_action(request, aSaveAntwort, 'add' if aSaveAntwortNew else 'change')
									test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ')' + sTyp + '<hr>'
						elif int(aAntwort['Aufgabenart']) >= 2 and int(aAntwort['Aufgabenart']) <= 4:  # Ergänzungsaufgabe(2) Puzzleaufgabe(3), Übersetzungsaufgabe (4)
							for aAnt in aAntwort['sub']:
								if 'delit' in aAnt and int(aAnt['delit']) == 1:
									if int(aAnt['antwort_pk']) > 0:
										aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=int(aAnt['antwort_pk']))
										if aSaveAntwort.ist_Satz:
											asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
											aSaveAntwort.ist_Satz = None
											if asSatz.tbl_antworten_set.all().count() == 1:
												test += 'Satz "' + str(asSatz) + '" (PK: ' + str(asSatz.pk) + ') <b>gelöscht!</b><br>'
												asSatz.delete()
												std_log_action(request, asSatz, 'delete')
										test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ') <b>gelöscht!</b><hr>'
										aSaveAntwort.delete()
										std_log_action(request, aSaveAntwort, 'delete')
								else:
									if int(aAnt['antwort_pk']) > 0:
										aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=int(aAnt['antwort_pk']))
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
									aSaveAntwort.kontrolliert = aAnt['kontrolliert']
									aSaveAntwort.veroeffentlichung = aAnt['veroeffentlichung']
									aSaveAntwort.Kommentar = aAnt['kommentar']
									if 'ist_Satz.Transkript' in aAnt:
										if aAnt['ist_Satz.Transkript']:
											if aSaveAntwort.ist_Satz:
												asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
												ssTyp = ' gespeichert!<br>'
												asSatzNew = False
											else:
												asSatz = KorpusDB.tbl_saetze()
												ssTyp = ' erstellt!<br>'
												asSatzNew = True
											asSatz.Transkript = aAnt['ist_Satz.Transkript']
											asSatz.save()
											std_log_action(request, asSatz, 'add' if asSatzNew else 'change')
											aSaveAntwort.ist_Satz = asSatz
											test += 'Satz "' + str(aSaveAntwort.ist_Satz) + '" (PK: ' + str(aSaveAntwort.ist_Satz.pk) + ')' + ssTyp
										elif aSaveAntwort.ist_Satz:
											asSatz = KorpusDB.tbl_saetze.objects.get(pk=aSaveAntwort.ist_Satz.pk)
											aSaveAntwort.ist_Satz = None
											if asSatz.tbl_antworten_set.all().count() == 1:
												test += 'Satz "' + str(asSatz) + '" (PK: ' + str(asSatz.pk) + ') <b>gelöscht!</b><br>'
												asSatz.delete()
												std_log_action(request, asSatz, 'delete')
									aSaveAntwort.Reihung = None
									aSaveAntwort.ist_bfl = False
									aSaveAntwort.bfl_durch_S = None
									aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=0)
									aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
									aSaveAntwort.save()
									std_log_action(request, aSaveAntwort, 'add' if aSaveAntwortNew else 'change')
									test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ')' + sTyp + '<hr>'
						else:
							test += 'Aufgabenart ' + str(aAntwort['Aufgabenart']) + ' ist unbekannt!'
				aFormular = 'korpusdbmaske2/antworten_formular.html'
		# Formulardaten ermitteln
		Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		AufgabenMitAntworten = []
		if Aufgabe.Aufgabenart.pk == 1:  # Aufgabenart: Bewertungsaufgabe (1)
			for val in KorpusDB.tbl_antwortmoeglichkeiten.objects.filter(zu_Aufgabe=apk).order_by('Reihung'):
				Antworten = []
				for aAntwort in KorpusDB.tbl_antworten.objects.filter(zu_Aufgabe=apk, von_Inf=ipk, ist_am=val.pk):
					Antworten.append({'model': aAntwort, 'xtags': getTags(aAntwort.pk), 'chkamft': aAntwort.check_am_fest_tags()})
				if len(Antworten) < 1:
					Antworten.append({'model': KorpusDB.tbl_antworten})
				if val.frei:
					Antworten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
				AufgabenMitAntworten.append({'model': val, 'antworten': Antworten})
		elif Aufgabe.Aufgabenart.pk >= 2 and Aufgabe.Aufgabenart.pk <= 4:  # Ergänzungsaufgabe(2) Puzzleaufgabe(3), Übersetzungsaufgabe (4)
			Antworten = [{'model': val} for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk, zu_Aufgabe=apk)]
			if len(Antworten) < 1:
				Antworten.append({'model': KorpusDB.tbl_antworten})
			Antworten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk, id_InfErh__ID_Inf__pk=ipk)
		return render_to_response(
			aFormular,
			RequestContext(request, {'Informant': Informant, 'Aufgabe': Aufgabe, 'Antworten': Antworten, 'AufgabenMitAntworten': AufgabenMitAntworten, 'ErhInfAufgaben': ErhInfAufgaben, 'aDUrl': aDUrl, 'test': test, 'error': error}),)
	# Menü
	aMenue = getMenue(request, useOnlyErhebung, useArtErhebung, ['tbl_erhebung_mit_aufgaben__Reihung'], [1, 2, 3])
	if aMenue['formular']:
		return render_to_response(
			aMenue['formular'],
			RequestContext(request, {'menueData': aMenue['daten'], 'aDUrl': aDUrl}),)

	# Ausgabe der Seite
	return render_to_response(
		'korpusdbmaske2/start.html',
		RequestContext(request, {'menueData': aMenue['daten'], 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)

# Funktionen:
