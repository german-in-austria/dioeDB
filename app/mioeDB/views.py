"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView
# from mioeDB.models import *


def wb(request):
	"""Eingabe mioe wb."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_wb'
	permName = 'mioe'
	primaerId = 'num_wb'
	aktueberschrift = 'Wenkerbogen'
	asurl = '/mioedb/wb/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = []
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def vz(request):
	"""Eingabe mioe volkszählungen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_vz_daten'
	permName = 'mioe'
	primaerId = 'mioe_vz'
	aktueberschrift = 'Volkszählung'
	asurl = '/mioedb/vz/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = []
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def orte(request):
	"""Eingabe mioe Orte."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_mioe_orte'
	permName = 'mioe'
	primaerId = 'mioe_orte'
	aktueberschrift = 'MiÖ-Orte'
	asurl = '/mioedb/orte/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'MiÖ', 'titel_plural': 'Ort', 'app': 'mioeDB', 'tabelle': 'tbl_mioe_orte', 'id': 'mioe_orte', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'id_orte', 'adm_lvl', 'gid', 'histor'],
		'feldoptionen':{
			'id_orte': {},
			'adm_lvl': {},
			'gid': {},
			'histor': {},
		},
		'sub': [
			{
				'titel': 'MiÖ', 'titel_plural': 'Administrative Zuordnung', 'app': 'mioeDB', 'tabelle': 'tbl_adm_zuordnung', 'id': 'adm_zuordnung', 'optionen': ['einzeln', 'elementFrameless'],
				'felder':['+id', '|id_ort1=parent:id', 'id_ort2', 'id_quelle', 'vonDat_start', 'vonDat_end', 'bisDat_start', 'bisDat_end', 'kommentar'],
				'feldoptionen':{
					'id_ort2': {'label': 'Gehört zu', 'nl': True},
					'id_quelle': {},
					'vonDat_start': {'label_col': 3, 'input_col': 3},
					'vonDat_end': {'label_col': 3, 'input_col': 3, 'nl': True},
					'bisDat_start': {'label_col': 3, 'input_col': 3},
					'bisDat_end': {'label_col': 3, 'input_col': 3, 'nl': True},
					'kommentar': {},
				},
			},
		],
		'suboption': ['tab']
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
