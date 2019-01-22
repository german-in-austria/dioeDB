"""Formular für Vokszählungen."""
from django.shortcuts import render_to_response
from django.template import RequestContext


def view_vz(request):
	"""Anzeige für mioe Volkszählungs Maske."""
	aUrl = '/mioedb/vz/'
	aDUrl = 'mioeDB:varietaet'
	test = ''
	# Menü
	aMenue = {'daten': []}
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'menueData': aMenue['daten'], 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
