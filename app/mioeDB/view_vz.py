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
		aArtenInVZ = []
		aVz = False
		aMioeOrt = False
		if aVzId > 0:
			aVz = mioeDB.tbl_volkszaehlung.objects.get(pk=aVzId)
		if aMioeOrtId > 0:
			aMioeOrt = mioeDB.tbl_mioe_orte.objects.get(pk=aMioeOrtId)
		if aVzId > 0 and aMioeOrtId > 0:
			if 'save' in request.POST:
				return httpOutput('todo ...')
			for aArtInVZ in mioeDB.tbl_art_in_vz.objects.filter(id_vz_id=aVzId):
				aArtenInVZ.append({'model': aArtInVZ})
		return render_to_response(
			'mioedbvzmaske/vz_daten_formular.html',
			RequestContext(request, {'aVz': aVz, 'aMioeOrt': aMioeOrt, 'aArtenInVZ': aArtenInVZ, 'vzDaten': vzDaten, 'test': test}),)
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
