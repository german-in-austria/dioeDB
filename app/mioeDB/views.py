"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse
#from mioeDB.models import *

# Create your views here.
def wb(request):
	"""Eingabe mioe wb."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_wb'
	permName = 'personen'
	primaerId = 'num_wb'
	aktueberschrift = 'Wenkerbogen'
	asurl = '/mioedb/wb/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = []

	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)

# def admzuord(request):
# 	"""Eingabe mioe wb."""
# 	info = ''
# 	error = ''
# 	if not request.user.is_authenticated():
# 		return redirect('dioedb_login')
# 	app_name = 'mioeDB'
# 	tabelle_name = 'tbl_adm_zuordnung'
# 	permName = 'personen'
# 	primaerId = 'adm_zuordnung'
# 	aktueberschrift = 'Administrative Zuordnung'
# 	asurl = '/mioedb/admzuord/'
# 	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
# 		return redirect('Startseite:start')

# 	aufgabenform = [
# 									{
# 								'titel': 'MiÖ',
# 								'titel_plural': 'Administrative Zuordnung',
# 								'app': 'mioeDB',
# 								'tabelle': 'tbl_adm_zuordnung',
# 								'id': 'adm_zuordnung',
# 								'optionen': ['einzeln', 'elementFrameless'],
# 								'felder':['+id', 'id_adm1', 'id_adm2', 'id_quelle' ],
# 								'feldoptionen':{
# 									'id_adm1':{'label_col': 3, 'input_col': 7,
# 										'label': 'Einheit', 'nl': True},
# 									'id_adm2': {'label_col': 3, 'input_col': 7,
# 										'label': 'ist in', 'nl': True},
# 									'id_quelle': {'label_col': 3, 'input_col': 5, 'nl': True},
# 								},
# 							}
# 	]

# 	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)

def vz(request):
	"""Eingabe mioe volkszählungen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_vz_daten'
	permName = 'personen'
	primaerId = 'id_vz'
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
	# 		'id': 'id_vz',
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

def mioe(request):
	"""Eingabe mioe Orte."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_mioe_orte'
	permName = 'personen'
	primaerId = 'id_ort'
	aktueberschrift = 'MiÖ-Orte'
	asurl = '/mioedb/orte/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = []
	# aufgabenform = [
	# 				{
	# 				'titel': 'MiÖ',
	# 				'titel_plural': 'Ort',
	# 				'app': 'mioeDB',
	# 				'tabelle': 'tbl_mioe_orte',
	# 				'id': 'id_orte',
	# 				'optionen': ['einzeln', 'elementFrameless'],
	# 				'felder':['+id', 'id_orte', 'adm_lvl', 'gid', 'histor' ],
	# 				'feldoptionen':{
	# 					'id_orte': {'label_col': 3, 'input_col': 7, 'nl': True},
	# 					'adm_lvl': {'label_col': 3, 'input_col': 4, 'nl': True},
	# 					'gid': {'label_col': 3, 'input_col': 2, 'nl': True},
	# 					'histor': {'label_col': 3, 'input_col': 4, 'nl': True},
	# 				},
	# 				'sub':[
	# 					{
	# 							'titel': 'MiÖ',
	# 							'titel_plural': 'Administrative Zuordnung',
	# 							'app': 'mioeDB',
	# 							'tabelle': 'tbl_adm_zuordnung',
	# 							'id': 'adm_zuordnung',
	# 							'optionen': ['einzeln', 'elementFrameless'],
	# 							'felder':['+id', '|id_ort1=parent:id', 'id_ort2', 'id_quelle' ],
	# 							'feldoptionen':{
	# 								'id_ort2': {'label_col': 3, 'input_col': 7,
	# 									'label': 'Gehört zu', 'nl': True},
	# 								'id_quelle': {'label_col': 3, 'input_col': 5, 'nl': True},
	# 							},
	# 					},
	# 				],
	# 				'suboption':['tab']
	# 			},
	# ]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
