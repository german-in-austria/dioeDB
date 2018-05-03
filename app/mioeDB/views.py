"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse
#from PersonenDB.models import tbl_orte

# Create your views here.
def mioe(request):
	"""Eingabe mioe Orte."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_orte'
	permName = 'personen'
	primaerId = 'adm_lvl'
	aktueberschrift = 'Admin levels'
	asurl = '/mioedb/orte/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'Ort',
			'titel_plural': 'Ort',
			'app': 'PersonenDB',
			'tabelle': 'tbl_orte',
			'id': 'tbl_orte',
			'optionen': ['einzeln', 'elementFrameless'],

			'felder':['+id', 'ort_namekurz', 'adm_lvl', 'lat', 'gid', 'lon', 'histor' ],

			'feldoptionen':{
				'ort_namekurz': {'label_col': 2, 'input_col': 4},
				'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
				'lat': {'label_col': 2, 'input_col': 4},
				'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
				'lon': {'label_col': 2, 'input_col': 4},
				'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
			}
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
