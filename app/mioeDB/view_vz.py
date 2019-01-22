"""Formular für Vokszählungen."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView


def view_vz(request):
	"""Anzeige für mioe Volkszählungs Maske."""
	# Eigenes Formular
	info = ''
	error = ''
	app_name = 'mioeDB'
	tabelle_name = 'tbl_vz_daten'
	permName = 'mioe'
	primaerId = 'mioe_vz'
	aktueberschrift = 'Volkszählung'
	asurl = '/mioedb/vz/'
	aufgabenform = []
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
