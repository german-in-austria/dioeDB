"""Anzeige für MioeDB."""
from django.shortcuts import redirect
from django.db import connection
from django.db.models import Count
import datetime
from DB.funktionenDB import formularView
from DB.funktionenAuswertung import auswertungView
import mioeDB.models as mioeDB


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

	def linkWbFxfunction(aval, siblings, aElement):
		"""Link für Wenkerbogen."""
		aval['feldoptionen'] = {'edit_html': '<div class="col-sm-offset-3 col-sm-9"><p class="form-control-static text-ellipsis"><a id="linkwb" href="#">Zum Wenkerbogen</a></p></div>'}
		if aElement.num_wb:
			aval['feldoptionen']['view_html'] = '<div class="col-sm-offset-3 col-sm-9"><p class="form-control-static text-ellipsis"><a href="https://regionalsprache.de/Wenkerbogen/WenkerbogenViewer.aspx?WbNr=' + str(aElement.num_wb) + '" target="_blank">Zum Wenkerbogen</a></p></div>'
		return aval

	aufgabenform = [{
		'titel': 'Wenkerbogen', 'titel_plural': 'Wenkerbögen', 'app': 'mioeDB', 'tabelle': 'tbl_wb', 'id': 'mioe_wb', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'num_wb', '!link_wb', 'typ_wb', 'datierung_start', 'datierung_end', 'id_mioe_ort', 'gid', 'schulort_orig', 'id_lehrer', 'uebersetzt_von', 'uebersetzt_klass', 'alter_geschl_uebesetzer', 'alter_geschl_lehrer', 'alter_uebesetzer', 'geburtsdatum_uebersetzer', 'geschlecht_uebersetzer', 'informationen_zu', 'andere_sprachen', 'welche_sprachen', 'sprachen_verhaeltnis', 'kommentar_wb', 'kommentar_wiss', 'geprueft', 'problematisch', 'link_rede'],
		'feldoptionen':{
			'link_wb': {'fxtype': {'fxfunction': linkWbFxfunction}, 'nl': True, 'view_html': '<div></div>', 'edit_html': '<div></div>'},
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
		'suboption': ['tab'],
		'addJS': [{'static': 'mioedbvzmaske/js/linkwb.js'}],
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def vz(request):
	"""Eingabe mioe Volkszählungen."""
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('mioeDB.mioe_maskView'):
		return redirect('Startseite:start')
	from .view_vz import view_vz
	return view_vz(request)


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
		'felder':['+id', 'id_orte', 'histor_ort', 'adm_lvl', 'gid', 'histor', 'importiert', 'kontrolliert'],
		'feldoptionen':{
			'id_orte': {},
			'histor_ort': {},
			'adm_lvl': {},
			'gid': {},
			'histor': {'label_col': 3, 'input_col': 2},
			'importiert': {'label_col': 1, 'input_col': 2},
			'kontrolliert': {'label_col': 1, 'input_col': 2, 'nl': True},
		},
		'sub': [
			{
				'titel': 'Administrative Zuordnung', 'titel_plural': 'Administrative Zuordnungen', 'app': 'mioeDB', 'tabelle': 'tbl_adm_zuordnung', 'id': 'adm_zuordnung', 'optionen': ['liste'],
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


def literatur(request):
	"""Eingabe mioe Literaturen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_literaturv'
	permName = 'mioe'
	primaerId = 'mioe_literatur'
	aktueberschrift = 'Literaturen'
	asurl = '/mioedb/literatur/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Literatur', 'titel_plural': 'Literatur', 'app': 'mioeDB', 'tabelle': 'tbl_literaturv', 'id': 'mioe_literatur', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'name', 'titel', 'literaturtyp', 'verlag', 'erscheinungsort', 'PublDat_start', 'PublDat_end'],
		'feldoptionen':{
			'name': {},
			'titel': {},
			'literaturtyp': {},
			'verlag': {},
			'erscheinungsort': {},
			'PublDat_start': {},
			'PublDat_end': {},
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def verlage(request):
	"""Eingabe mioe Verlage."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_verlage'
	permName = 'mioe'
	primaerId = 'mioe_verlage'
	aktueberschrift = 'Verlage'
	asurl = '/mioedb/verlage/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Verlag', 'titel_plural': 'Verlage', 'app': 'mioeDB', 'tabelle': 'tbl_verlage', 'id': 'mioe_verlage', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'verlagsname', 'verlagsort'],
		'feldoptionen':{
			'verlagsname': {},
			'verlagsort': {},
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def quelle(request):
	"""Eingabe mioe Quellen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_quelle'
	permName = 'mioe'
	primaerId = 'mioe_quelle'
	aktueberschrift = 'Quellen'
	asurl = '/mioedb/quelle/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Quelle', 'titel_plural': 'Quellen', 'app': 'mioeDB', 'tabelle': 'tbl_quelle', 'id': 'mioe_quelle', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'wenkerbogen', 'id_literatur'],
		'feldoptionen':{
			'wenkerbogen': {},
			'id_literatur': {},
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def religion(request):
	"""Eingabe mioe Religionen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_religion'
	permName = 'mioe'
	primaerId = 'mioe_religion'
	aktueberschrift = 'Religionen'
	asurl = '/mioedb/religion/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Religion', 'titel_plural': 'Religionen', 'app': 'mioeDB', 'tabelle': 'tbl_religion', 'id': 'mioe_religion', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'relig_name'],
		'feldoptionen':{
			'relig_name': {},
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def institutionen(request):
	"""Eingabe mioe Institutionen."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'mioeDB'
	tabelle_name = 'tbl_institutionen'
	permName = 'mioe'
	primaerId = 'mioe_institutionen'
	aktueberschrift = 'Institutionen'
	asurl = '/mioedb/institutionen/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [{
		'titel': 'Institution', 'titel_plural': 'Institutionen', 'app': 'mioeDB', 'tabelle': 'tbl_institutionen', 'id': 'mioe_institutionen', 'optionen': ['einzeln', 'elementFrameless'],
		'felder':['+id', 'id_ort', 'id_institutstyp', 'anz_klassen', 'id_quelle', 'kommentar'],
		'feldoptionen':{
			'id_ort': {},
			'id_institutstyp': {},
			'anz_klassen': {},
			'id_quelle': {},
			'kommentar': {},
		},
		'sub': [
			{
				'titel': 'Institution Daten', 'titel_plural': 'Institutionen Daten', 'app': 'mioeDB', 'tabelle': 'tbl_institut_daten', 'id': 'mioe_sprache_institut', 'optionen': ['liste'],
				'felder':['+id', '|id_institution=parent:id', 'id_varietaet', 'anzahl', 'id_quelle', 'id_art', 'kommentar'],
				'feldoptionen':{
					'id_varietaet': {},
					'anzahl': {},
					'id_quelle': {},
					'id_art': {},
					'kommentar': {},
				},
			},
		],
		'suboption': ['tab']
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)

def auswertung(request):
	"""Anzeige für Auswertung."""
	info = ''
	error = ''
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('mioeDB.mioe_maskView'):
		return redirect('Startseite:start')
	asurl = '/mioedb/auswertung/'
	cacheVzData = None
	cacheLastMioeOrt = None
	def fxFunctionMioeVzDaten(amodel=None, adata=None, data=None, getTitle=False):
		nonlocal cacheVzData
		nonlocal cacheLastMioeOrt
		if getTitle:
			aCols = []
			aVzByYears = mioeDB.tbl_volkszaehlung.objects.extra({'year': connection.ops.date_trunc_sql('year', 'erheb_datum')}).values('year').annotate(Count('pk')).order_by('year')
			for aVzYear in aVzByYears:
				aArtenListe = []
				aArtenListeKomplex = []
				if isinstance(aVzYear['year'], datetime.datetime):
					aYear = aVzYear['year'].year
				else:
					aYear = int(aVzYear['year'].split('-')[0])
				for aArtInVz in mioeDB.tbl_art_in_vz.objects.distinct().filter(id_vz__erheb_datum__year=aYear):
					if aArtInVz.id_art.id not in aArtenListe:
						aArtenListe.append(aArtInVz.id_art.id)
						aArtenListeKomplex.append({'titel': aArtInVz.id_art.art_name, 'id': aArtInVz.id_art.id, 'reihung': aArtInVz.reihung})
				aArtenListeKomplex = sorted(aArtenListeKomplex, key=lambda k: k['reihung'])
				for aArtVz in aArtenListeKomplex:
					aCols.append({'titel': str(aYear) + '_' + aArtVz['titel'], 'fxFunction': fxFunctionMioeVzDaten, 'data': {'id_art': aArtVz['id'], 'vzYear': aYear}})
			return aCols
		else:
			aVzDataAnzahl = None
			if cacheLastMioeOrt is not adata.id:
				cacheLastMioeOrt = adata.id
				cacheVzData = [xVzData for xVzData in mioeDB.tbl_vz_daten.objects.filter(id_mioe_ort=adata.id)]
			for cVzData in cacheVzData:
				if cVzData.id_vz.erheb_datum.year == data['vzYear'] and cVzData.id_art_id == data['id_art']:
					if cVzData.anzahl is not None:
						if aVzDataAnzahl is None:
							aVzDataAnzahl = 0
						aVzDataAnzahl += cVzData.anzahl
			return aVzDataAnzahl
	auswertungen = [
		{
			'id': 'mioeOrte', 'titel': 'Mioe Orte', 'app_name': 'mioeDB', 'tabelle_name': 'tbl_mioe_orte',
			'felder': ['id', 'id_orte__ort_namekurz||id_orte__ort_namelang', 'histor_ort', 'id_orte__lat', 'id_orte__lon', {'fxFunction': fxFunctionMioeVzDaten}],
			'filter': [
				# [{'id': 'volkszaehlung', 'field': '>mioeDB|tbl_volkszaehlung', 'type': 'select', 'queryFilter': 'tbl_vz_daten__id_vz__pk', 'verbose_name': 'Volkszählung', 'orderby': 'erheb_datum'}, ],
			],
			# 'orderby':{'id': ['id']},
		},
	]
	return auswertungView(auswertungen, asurl, request, info, error)


def mioeAuswertung(request):
	"""Anzeige für MioeDB Auswertung."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('mioeDB.mioe_maskView'):
		return redirect('Startseite:start')
	from .views_mioeauswertung import views_mioeAuswertung
	return views_mioeAuswertung(request)
