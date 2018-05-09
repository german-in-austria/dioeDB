"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse
#from mioeDB.models import *

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
	primaerId = 'ort_namekurz'
	aktueberschrift = 'Admin levels'
	asurl = '/mioedb/orte/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'MiÖ',
			'titel_plural': 'Eingabemaske MiÖ-Modul 2',
			'app': 'mioeDB',
			'tabelle': 'tbl_mioe_orte',
			'id': 'tbl_mioe_orte',
			'optionen': ['einzeln', 'elementFrameless'],

			'felder':[],
			'sub': [
				{
					'titel': 'MiÖ',
					'titel_plural': 'Ort',
					'app': 'mioeDB',
					'tabelle': 'tbl_mioe_orte',
					'id': 'tbl_mioe_orte',
					'optionen': ['einzeln', 'elementFrameless'],
					# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
					'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
					'feldoptionen':{
						'id_ort': {'label_col': 3, 'input_col': 5, 'nl': True},
						'adm_lvl': {'label_col': 3, 'input_col': 5, 'nl': True},
						'gid': {'label_col': 3, 'input_col': 5, 'nl': True},
						# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
					},
					'sub':[
						{
							'titel': 'MiÖ',
							'titel_plural': 'Aktuelle administraive Zugehörigkeit',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 3, 'input_col': 5, 'nl': True},
								'adm_lvl': {'label_col': 3, 'input_col': 5, 'nl': True},
								'gid': {'label_col': 3, 'input_col': 5, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							}
						},
					]
				},
				{
					'titel': 'Ort',
					'titel_plural': 'VZ-Daten zum Ort',
					'app': 'mioeDB',
					'tabelle': 'tbl_mioe_orte',
					'id': 'tbl_mioe_orte',
					'optionen': ['einzeln', 'elementFrameless'],
					'felder':[],
					'suboption': ['tab'],
					'sub': [
						{
							'titel': 'MiÖ',
							'titel_plural': 'VZ 1880',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
								'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							},
						},
						{
							'titel': 'MiÖ',
							'titel_plural': 'VZ 1890',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
								'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							},
						},
						{
							'titel': 'MiÖ',
							'titel_plural': 'VZ 1900',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
								'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							},
						},
						{
							'titel': 'MiÖ',
							'titel_plural': 'VZ 1910',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
								'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							},
						},
						{
							'titel': 'MiÖ',
							'titel_plural': 'VZ 1934',
							'app': 'mioeDB',
							'tabelle': 'tbl_mioe_orte',
							'id': 'tbl_mioe_orte',
							'optionen': ['einzeln', 'elementFrameless'],
							# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
							'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
							'feldoptionen':{
								'id_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'adm_lvl': {'label_col': 2, 'input_col': 4, 'nl': True},
								'gid': {'label_col': 2, 'input_col': 4, 'nl': True},
								# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
							},
						},
					]
				},
				{
					'titel': 'Ort',
					'titel_plural': 'WB zum Ort',
					'app': 'mioeDB',
					'tabelle': 'tbl_mioe_orte',
					'id': 'tbl_mioe_orte',
					'optionen': ['einzeln', 'elementFrameless'],
					# 'felder':['+id', 'id_ort', 'adm_lvl', 'gid', 'histor' ],
					'felder':['+id', 'id_ort', 'adm_lvl', 'gid' ],
					'feldoptionen':{
						'id_ort': {'label_col': 4, 'input_col': 4, 'nl': True},
						'adm_lvl': {'label_col': 4, 'input_col': 4, 'nl': True},
						'gid': {'label_col': 4, 'input_col': 4, 'nl': True},
						# 'histor': {'label_col': 2, 'input_col': 4, 'nl': True},
					}
				},
			]
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)