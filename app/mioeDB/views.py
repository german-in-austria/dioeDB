"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse

# Create your views here.
def mioe(request):
	"""Eingabe mioe Orte."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	# to get model
	app_name = 'mioeDB'
	tabelle_name = 'tbl_adm_lvl'

	permName = 'personen'
	#TODO was ist das?
	primaerId = 'adm_lvl'

	# only string
	aktueberschrift = 'Admin levels'
	asurl = '/mioedb/orte/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'Adm lvl',
			'titel_plural': 'Adm lvls',
			'app': 'mioeDB',
			'tabelle': 'tbl_adm_lvl',
			'id': 'tbl_adm_lvl',
			'optionen': ['einzeln', 'elementFrameless'],
			'felder':['+id', 'name']
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
