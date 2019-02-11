"""Formular für Vokszählungen."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from DB.funktionenDB import httpOutput
import mioeDB.models as mioeDB
import json


def view_vz(request):
	"""Anzeige für mioe Volkszählungs Maske."""
	aUrl = '/mioedb/vz/'
	aDUrl = 'mioeDB:varietaet'
	test = ''
	# Menü - tbl_volkszaehlung
	if 'getmenue' in request.POST:
		aMioeOrt = int(request.POST.get('getmenue'))
		aVzListe = []
		for aVz in mioeDB.tbl_volkszaehlung.objects.filter(id_ort_id=aMioeOrt):
			aVzListe.append({'id': aVz.pk, 'title': str(aVz), 'erheb_datum': str(aVz.erheb_datum)})
		return httpOutput(json.dumps({'success': 'success', 'mioeOrte': aVzListe}))
	if 'getmask' in request.POST:
		aVzId = int(request.POST.get('getmask'))
		if 'save' in request.POST:
			return httpOutput('todo ...')
		aVz = mioeDB.tbl_volkszaehlung.objects.get(pk=aVzId)
		vzDaten = []
		# vzDaten = [{'model': val} for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk, zu_Aufgabe=apk)]
		# if len(vzDaten) < 1:
		# 	vzDaten.append({'model': KorpusDB.tbl_antworten})
		# vzDaten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
		return render_to_response(
			'mioedbvzmaske/vz_daten_formular.html',
			RequestContext(request, {'aVz': aVz, 'vzDaten': vzDaten, 'test': test}),)
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
