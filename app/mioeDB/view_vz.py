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
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
