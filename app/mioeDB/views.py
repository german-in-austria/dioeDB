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
	# aufgabenform = [
	# 	{
	# 		'titel': 'MiÖ',
	# 		'titel_plural': 'Volkszählung',
	# 		'app': 'mioeDB',
	# 		'tabelle': 'tbl_vz_daten',
	# 		'id': 'mioe_vz',
	# 		'optionen': ['einzeln', 'elementFrameless'],
	# 		'felder':['+id', 'id_mioe_ort', 'id_vz', 'id_art',  'anzahl' ],
	# 		'feldoptionen':{
	# 			'id_mioe_ort': {'label_col': 3, 'input_col': 7, 'nl': True},
	# 			'id_vz': {'label_col': 3, 'input_col': 4, 'nl': True},
	# 			'id_art': {'label_col': 3, 'input_col': 4, 'nl': True},
	# 			'anzahl': {'label_col': 3, 'input_col': 2, 'nl': True},
	# 		},
	# 		'suboption':'tab',
	# 		'sub': [
	# 			{
	# 				'titel': 'Daten',
	# 				'titel_plural': 'Andere Daten',
	# 				'app': 'mioeDB',
	# 				'tabelle': 'tbl_vz_daten',
	# 				'id': 'vz',
	# 				'optionen': ['liste'],
	# 				'felder':['+id','|id_mioe_ort=parent:id_mioe_ort', '|id_vz=parent:id_vz', 'id_art',  'anzahl' ],
	# 				'feldoptionen':{
	# 					'id_art': {'label_col': 2, 'input_col': 4, },
	# 					'anzahl': {'label_col': 2, 'input_col': 2, },
	# 				},
	# 			},
	# 			{
	# 				'titel': 'Schule',
	# 				'titel_plural': 'Schule',
	# 				'app': 'mioeDB',
	# 				'tabelle': 'tbl_schule',
	# 				'id': 'schultyp',
	# 				'optionen': ['liste'],
	# 				'felder':['+id','|id_mioe_ort=parent:id_mioe_ort', '|id_quelle=parent:id_vz', 'schultyp',  'anz_klassen' ],
	# 				'feldoptionen':{
	# 					'schultyp': {'label_col': 2, 'input_col': 4, },
	# 					'anz_klassen': {'label_col': 3, 'input_col': 2, },
	# 				},
	# 				'suboption':'tab',
	# 				'sub': [
	# 					{
	# 						'titel': 'Schulsprache',
	# 						'titel_plural': 'Schulsprachen',
	# 						'app': 'mioeDB',
	# 						'tabelle': 'tbl_schule_sprache',
	# 						'id': 'id_schule',
	# 						'optionen': ['liste'],
	# 						'felder':['+id','|id_schule=parent:id',
	# 							'id_sprache',	'anz_schulen' ],
	# 						'feldoptionen':{
	# 							'id_sprache': {'label_col': 2, 'input_col': 4, },
	# 							'anz_schulen': {'label_col': 3, 'input_col': 2, },
	# 					},
	# 					}
	# 				]
	# 			}
	# 		]
	# 	}
	# ]

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
	aufgabenform = []
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
