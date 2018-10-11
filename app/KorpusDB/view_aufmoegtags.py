"""Für EingabeFB."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
import datetime
import json
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from .function_menue import getMenue


def view_aufmoegtags(request, ipk=0, apk=0):
	"""Ansicht für EingabeSTP."""
	# aFormular = 'korpusdbaufmoegtags/start_formular.html'
	aUrl = '/korpusdb/aufmoegtags/'
	aDUrl = 'KorpusDB:aufmoegtags'
	useArtErhebung = [6, 7]
	useOnlyErhebung = []
	for aUKDBES in request.user.user_korpusdb_erhebung_set.all():
		useOnlyErhebung.append(aUKDBES.erhebung_id)
	test = ''
	# error = ''
	# apk = int(apk)
	# ipk = int(ipk)
	# if apk > 0 and ipk > 0:
	# 	# Speichern
	# 	if 'save' in request.POST:
	# 		pass
	# 	# Formulardaten ermitteln
	# 	Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
	# 	Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
	# 	AufgabenMitAntworten = []
	# 	if Aufgabe.Aufgabenart.pk == 1:  # Aufgabenart: Bewertungsaufgabe (1)
	# 		for val in KorpusDB.tbl_antwortmoeglichkeiten.objects.filter(zu_Aufgabe=apk).order_by('Reihung'):
	# 			Antworten = []
	# 			for aAntwort in KorpusDB.tbl_antworten.objects.filter(zu_Aufgabe=apk, von_Inf=ipk, ist_am=val.pk):
	# 				Antworten.append({'model': aAntwort})
	# 			if len(Antworten) < 1:
	# 				Antworten.append({'model': KorpusDB.tbl_antworten})
	# 			if val.frei:
	# 				Antworten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
	# 			AufgabenMitAntworten.append({'model': val, 'antworten': Antworten})
	# 	elif Aufgabe.Aufgabenart.pk >= 2 and Aufgabe.Aufgabenart.pk <= 4:  # Ergänzungsaufgabe(2) Puzzleaufgabe(3), Übersetzungsaufgabe (4)
	# 		Antworten = [{'model': val} for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk, zu_Aufgabe=apk)]
	# 		if len(Antworten) < 1:
	# 			Antworten.append({'model': KorpusDB.tbl_antworten})
	# 		Antworten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
	# 	ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk, id_InfErh__ID_Inf__pk=ipk)
	# 	return render_to_response(
	# 		aFormular,
	# 		RequestContext(request, {'Informant': Informant, 'Aufgabe': Aufgabe, 'Antworten': Antworten, 'AufgabenMitAntworten': AufgabenMitAntworten, 'ErhInfAufgaben': ErhInfAufgaben, 'aDUrl': aDUrl, 'test': test, 'error': error}),)
	# Menü
	aMenue = getMenue(request, useOnlyErhebung, useArtErhebung, ['tbl_erhebung_mit_aufgaben__Reihung'], [4])
	if aMenue['formular']:
		return render_to_response(
			aMenue['formular'],
			RequestContext(request, {'menueData': aMenue['daten'], 'aDUrl': aDUrl}),)

	# Ausgabe der Seite
	return render_to_response(
		'korpusdbaufmoegtags/start.html',
		RequestContext(request, {'menueData': aMenue['daten'], 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)

# Funktionen:
