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
	primaerId = 'mioe_wb'
	aktueberschrift = 'Wenkerbogen'
	asurl = '/mioedb/wb/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Wenkerbogen', 'titel_plural': 'Wenkerbögen', 'app': 'mioeDB', 'tabelle': 'tbl_wb', 'id': 'mioe_wb', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'num_wb', 'typ_wb', 'datierung_start', 'datierung_end', 'id_mioe_ort', 'gid', 'schulort_orig', 'id_lehrer', 'uebersetzt_von', 'uebersetzt_klass', 'alter_geschl_uebesetzer', 'alter_geschl_lehrer', 'alter_uebesetzer', 'geburtsdatum_uebersetzer', 'geschlecht_uebersetzer', 'informationen_zu', 'andere_sprachen', 'welche_sprachen', 'sprachen_verhaeltnis', 'kommentar_wb', 'kommentar_wiss', 'geprueft', 'problematisch', 'link_rede'],
		'feldoptionen':{
		},
		'sub': [
			{
				'titel': 'WB Sprachangabe', 'titel_plural': 'WB Sprachangaben', 'app': 'mioeDB', 'tabelle': 'tbl_wb_sprache', 'id': 'wb_sprache', 'optionen': ['liste'],
				'felder':['+id', '|id_wb=parent:id', 'id_varietaet', 'anteil'],
				'feldoptionen':{
					'anteil': {'fxtype': {'type': 'prozent'}, 'steps': '0.01', 'multiplicator': 100},
				},
			},
			{
				'titel': 'Bogen auch für', 'titel_plural': 'Bogen auch für', 'app': 'mioeDB', 'tabelle': 'tbl_wb_auch_fuer', 'id': 'wb_auch_fuer', 'optionen': ['liste'],
				'felder':['+id', '|id_wb=parent:id', 'id_wbort', 'id_lehrer', 'kommentar_wb', 'kommentar_wiss'],
				'feldoptionen':{
				},
			},
		],
		'suboption': ['tab']
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def vz(request):
	"""Eingabe mioe volkszählungen."""
	# Eigenes Formular
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
		'titel': 'Ort', 'titel_plural': 'Orte', 'app': 'mioeDB', 'tabelle': 'tbl_mioe_orte', 'id': 'mioe_orte', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'id_orte', 'histor_ort', 'adm_lvl', 'gid', 'histor'],
		'feldoptionen':{
			'id_orte': {},
			'histor_ort': {},
			'adm_lvl': {},
			'gid': {},
			'histor': {},
		},
		'sub': [
			{
				'titel': 'Administrative Zuordnung', 'titel_plural': 'Administrative Zuordnungen', 'app': 'mioeDB', 'tabelle': 'tbl_adm_zuordnung', 'id': 'adm_zuordnung', 'optionen': ['einzeln', 'elementFrameless'],
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
			{
				'titel': 'Namensvariante', 'titel_plural': 'Namensvarianten', 'app': 'mioeDB', 'tabelle': 'tbl_name_var', 'id': 'name_variation', 'optionen': ['liste'],
				'felder':['+id', '|id_mioe_ort=parent:id', 'var_name', 'id_quelle', 'kommentar'],
				'feldoptionen':{
					'var_name': {},
					'id_quelle': {},
					'kommentar': {},
				},
			},
		],
		'suboption': ['tab']
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def varietaet(request):
	"""Eingabe mioe Varietäten."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_varietaet'
	permName = 'mioe'
	primaerId = 'mioe_varietaet'
	aktueberschrift = 'Varietäten'
	asurl = '/mioedb/varietaet/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Varietät', 'titel_plural': 'Varietäten', 'app': 'mioeDB', 'tabelle': 'tbl_varietaet', 'id': 'mioe_varietaet', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'variet_name', 'iso_code', 'id_typ', 'id_varietaet'],
		'feldoptionen':{
			'variet_name': {'label': 'Varietät-Bezeichnung', 'nl': True},
			'iso_code': {},
			'id_typ': {},
			'id_varietaet': {'label': 'Parent-Varietät', 'nl': True},
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
