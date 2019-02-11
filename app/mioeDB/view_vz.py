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
	if 'getmask' in request.POST:
		aMioeOrtId = int(request.POST.get('aMioeOrtId'))
		aVzId = int(request.POST.get('aVzId'))
		vzDaten = []
		aVz = False
		aMioeOrt = False
		if aVzId > 0:
			aVz = mioeDB.tbl_volkszaehlung.objects.get(pk=aVzId)
		if aMioeOrtId > 0:
			aMioeOrt = mioeDB.tbl_mioe_orte.objects.get(pk=aMioeOrtId)
		if aVzId > 0 and aMioeOrtId > 0:
			if 'save' in request.POST:
				return httpOutput('todo ...')
			# vzDaten = [{'model': val} for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk, zu_Aufgabe=apk)]
			# if len(vzDaten) < 1:
			# 	vzDaten.append({'model': KorpusDB.tbl_antworten})
			# vzDaten.append({'model': KorpusDB.tbl_antworten, 'addIt': True})
		return render_to_response(
			'mioedbvzmaske/vz_daten_formular.html',
			RequestContext(request, {'aVz': aVz, 'aMioeOrt': aMioeOrt, 'vzDaten': vzDaten, 'test': test}),)
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
