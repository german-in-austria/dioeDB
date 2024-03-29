"""Anzeige für PersonenDB."""
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def maske(request):
	"""Eingabe Personen/Informanten."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_personen'
	permName = 'personen'
	primaerId = 'person'
	aktueberschrift = 'Person'
	asurl = '/personendb/maske/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'Person', 'app': 'PersonenDB', 'tabelle': 'tbl_personen', 'id': 'person', 'optionen': ['einzeln', 'elementFrameless'],
			'felder': ['+id', 'nachname', 'vorname', 'geb_datum', 'weiblich', 'kontrolliert', 'akt_wohnort', 'strasse_hausnr', 'plz', 'festnetz1', 'mobil1', 'mail1', 'festnetz2', 'mobil2', 'mail2'],
			'feldoptionen':{
				'nachname': {'label_col': 2, 'input_col': 4},
				'vorname': {'label_col': 2, 'input_col': 4, 'nl': True},
				'geb_datum': {'label_col': 2, 'input_col': 4},
				'weiblich': {'label': 'Geschlecht', 'fxtype': {'type': 'select', 'select': [{'title': 'k.A.', 'value': None}, {'title': 'männlich', 'value': False}, {'title': 'weiblich', 'value': True}]}, 'label_col': 1, 'input_col': 2},
				'kontrolliert': {'label_col': 1, 'input_col': 2, 'nl': True},
				'akt_wohnort': {'label_col': 2, 'input_col': 10, 'label': 'Wohnort', 'nl': True},
				'strasse_hausnr': {'label_col': 2, 'input_col': 6, 'label': 'Strasse+Nr'},
				'plz': {'label_col': 1, 'input_col': 3, 'nl': True},
				'festnetz1': {'label_col': 1, 'input_col': 3, 'label': 'Telefon&nbsp;1'},
				'mobil1': {'label_col': 1, 'input_col': 3, 'label': 'Mobil&nbsp;1'},
				'mail1': {'label_col': 1, 'input_col': 3, 'label': 'E&#8209;Mail&nbsp;1', 'nl': True},
				'festnetz2': {'label_col': 1, 'input_col': 3, 'label': 'Telefon&nbsp;2'},
				'mobil2': {'label_col': 1, 'input_col': 3, 'label': 'Mobil&nbsp;2'},
				'mail2': {'label_col': 1, 'input_col': 3, 'label': 'E&#8209;Mail&nbsp;2', 'nl': True}
			},
			'sub': [
				{
					'titel': 'Informant', 'app': 'PersonenDB', 'tabelle': 'tbl_informanten', 'id': 'informant', 'optionen': ['einzeln', 'elementFrameless'],
					'felder':['+id', '|id_person=parent:id', 'inf_sigle', 'pretest', 'inf_gruppe', 'eignung', 'migrationsklasse', 'geburtsort', 'inf_ort', 'familienstand', 'ausserhalbwohnort', 'ausbildung_max', 'ausbildung_spez', 'kompetenz_d', 'haeufigkeit_d', 'kompetenz_s', 'haeufigkeit_s', 'akquiriert_am', 'kontakt_durch', 'kommentar'],
					'feldoptionen':{
						'inf_sigle': {'label_col': 2, 'input_col': 4, 'label': 'GWP Sigle'},
						'pretest': {'label_col': 2, 'input_col': 4, 'nl': True},
						'inf_gruppe': {'label': 'Inf. Gruppe', 'label_col': 2, 'input_col': 4},
						'eignung': {'label_col': 2, 'input_col': 4, 'nl': True},
						'migrationsklasse': {'label_col': 2, 'input_col': 4, 'nl': True},
						'geburtsort': {'label_col': 2, 'input_col': 4},
						'inf_ort': {'label_col': 2, 'input_col': 4, 'nl': True},
						'familienstand': {'label_col': 2, 'input_col': 4},
						'ausserhalbwohnort': {'label_col': 2, 'input_col': 4, 'nl': True},
						'ausbildung_max': {'label_col': 2, 'input_col': 4},
						'ausbildung_spez': {'label_col': 2, 'input_col': 4, 'nl': True},
						'kompetenz_d': {'label_col': 2, 'input_col': 4, 'label': 'Dialekt&nbsp;Kompetenz'},
						'haeufigkeit_d': {'label_col': 2, 'input_col': 4, 'label': 'Dialekt&nbsp;Häufigkeit', 'nl': True},
						'kompetenz_s': {'label_col': 2, 'input_col': 4, 'label': 'Standard&nbsp;Kompetenz'},
						'haeufigkeit_s': {'label_col': 2, 'input_col': 4, 'label': 'Standard&nbsp;Häufigkeit', 'nl': True},
						'akquiriert_am': {'label_col': 2, 'input_col': 4},
						'kontakt_durch': {'label_col': 2, 'input_col': 4, 'label': 'Kontaktper.', 'nl': True},
						'kommentar': {'label_col': 2, 'input_col': 10, 'nl': True}
					},
					'sub': [
						{
							'titel': 'Lokalisierung', 'titel_plural': 'Lokalisierungen', 'app': 'PersonenDB', 'tabelle': 'tbl_informant_x_gewohnt_in', 'filter': {'wer__exact': 'informant'}, 'id': 'wohnorte', 'optionen': ['liste'],
							'felder':['+id', '|id_informant=parent:id', 'wer', 'aufgewachsen', 'arbeitsort', 'fahrtdauer', 'id_ort', 'plz', 'von_jahr', 'bis_jahr', 'dauer_jahr', '|reihung=auto:reihung'],
							'feldoptionen':{
								'wer': {'label_col': 2, 'input_col': 10, 'nl': True},
								'aufgewachsen': {'label_col': 2, 'input_col': 4},
								'arbeitsort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'fahrtdauer': {'label_col': 8, 'input_col': 4, 'nl': True},
								'id_ort': {'label_col': 2, 'input_col': 4},
								'plz': {'label_col': 2, 'input_col': 4, 'nl': True},
								'von_jahr': {'label_col': 2, 'input_col': 2},
								'bis_jahr': {'label_col': 2, 'input_col': 2},
								'dauer_jahr': {'label_col': 2, 'input_col': 2, 'label': 'Dauer(Jahre)', 'nl': True}
							}
						},
						{
							'titel': 'Familie', 'app': 'PersonenDB', 'tabelle': 'tbl_informant_x_gewohnt_in', 'exclude': {'wer__exact': 'informant'}, 'id': 'wohnorte', 'optionen': ['liste'],
							'felder':['+id', '|id_informant=parent:id', 'wer', 'aufgewachsen', 'arbeitsort', '|fahrtdauer', 'id_ort', 'plz', 'von_jahr', 'bis_jahr', 'dauer_jahr', 'beziehungsdauer', 'kompetenz_d', 'haeufigkeit_d', '|reihung=auto:reihung'],
							'feldoptionen':{
								'wer': {'label_col': 2, 'input_col': 10, 'nl': True},
								'aufgewachsen': {'label_col': 2, 'input_col': 4},
								'arbeitsort': {'label_col': 2, 'input_col': 4, 'nl': True},
								'id_ort': {'label_col': 2, 'input_col': 4},
								'plz': {'label_col': 2, 'input_col': 4, 'nl': True},
								'von_jahr': {'label_col': 2, 'input_col': 2},
								'bis_jahr': {'label_col': 2, 'input_col': 2},
								'dauer_jahr': {'label_col': 2, 'input_col': 2, 'label': 'Dauer(Jahre)', 'nl': True},
								'kompetenz_d': {'label_col': 2, 'input_col': 4, 'label': 'Dialekt&nbsp;Kompetenz'},
								'haeufigkeit_d': {'label_col': 2, 'input_col': 4, 'label': 'Dialekt&nbsp;Häufigkeit', 'nl': True},
								'beziehungsdauer': {'label_col': 10, 'input_col': 2, 'nl': True}
							}
						},
						{
							'titel': 'Beruf', 'titel_plural': 'Berufe', 'app': 'PersonenDB', 'tabelle': 'inf_ist_beruf', 'id': 'berufe', 'optionen': ['liste'],
							'felder':['+id', '|id_informant=parent:id', 'id_beruf', 'ist_aktuell', 'ist_ausbildung', 'inf_spezifizierung', 'von_jahr', 'bis_jahr', 'dauer_jahr', '|reihung=auto:reihung'],
							'feldoptionen':{
								'id_beruf': {'label_col': 2, 'input_col': 10, 'foreignkeytarget': reverse('PersonenDB:berufe'), 'nl': True},
								'ist_aktuell': {'label_col': 2, 'input_col': 4},
								'ist_ausbildung': {'label_col': 2, 'input_col': 4, 'nl': True},
								'inf_spezifizierung': {'label_col': 2, 'input_col': 10, 'nl': True},
								'von_jahr': {'label_col': 2, 'input_col': 2},
								'bis_jahr': {'label_col': 2, 'input_col': 2},
								'dauer_jahr': {'label_col': 2, 'input_col': 2, 'label': 'Dauer(Jahre)', 'nl': True}
							}
						},
						{
							'titel': 'Akquise', 'app': 'PersonenDB', 'tabelle': 'tbl_akquise', 'id': 'akquise', 'optionen': ['einzeln', 'elementFrameless'],
							'felder':['+id', '|informant_akqu=parent:id', 'akquise_status', 'anrufe_weitere', 'kooparationsbereitschaft', 'kommentar_zu_inf', 'wichtige_informationen'],
							'feldoptionen':{
								'akquise_status': {'label_col': 1, 'input_col': 2, 'fxtype': {'type': 'prozent'}},
								'anrufe_weitere': {'label_col': 0, 'input_col': 2},
								'kooparationsbereitschaft': {'label_col': 4, 'input_col': 2, 'nl': True}
							},
							'sub': [
								{
									'titel': 'Kontaktaufnahme', 'titel_plural': 'Kontaktaufnahmen', 'app': 'PersonenDB', 'tabelle': 'tbl_kontaktaufnahmen', 'id': 'kontakt', 'optionen': ['liste'],
									'felder': ['+id', '|zu_akquise=parent:id', 'zeit', 'kontaktart', 'id_kontaktierender', 'beschreibung', 'Text'],
									'elementtitel':'{% load dioeTags %} - <span data-formtitel="zeit">{% getFeldVal aData.felder \'zeit\' %}</span> - <span data-formtitel="kontaktart">{% getFeldVal aData.felder \'kontaktart\' %}</span> - <span data-formtitel="id_kontaktierender">{% getFeldVal aData.felder \'id_kontaktierender\' %}</span>',
									'feldoptionen':{
										'zeit': {'label_col': 3, 'input_col': 3},
										'kontaktart': {'label_col': 1, 'input_col': 3, 'nl': True, 'label': 'Art'},
										'id_kontaktierender': {'label_col': 3, 'input_col': 9, 'nl': True}
									},
									'sub': [
										{
											'titel': 'Termin', 'titel_plural': 'Termine', 'app': 'PersonenDB', 'tabelle': 'tbl_termine', 'id': 'termine', 'optionen': ['liste', 'elementeclosed'],
											'felder': ['+id', '|termin_vereinbart_in=parent:id', 'titel', 'termin_art', 'termin_lokalisierung', 'zu_dbort', 'termin_beschreibung', 'zeit_start', 'zeit_ende', 'color_id'],
											'feldoptionen':{
												'zeit_ende': {'jsErrorCheck': [{'type': 'isGreaterSame', 'field': 'zeit_start'}], 'nl': True}
											},
											'elementtitel': '{% load dioeTags %} - <span data-formtitel="zeit_start">{% getFeldVal aData.felder \'zeit_start\' %}</span> bis <span data-formtitel="zeit_ende">{% getFeldVal aData.felder \'zeit_ende\' %}</span> - <span data-formtitel="titel">{% getFeldVal aData.felder \'titel\' %}</span>',
											'sub': [
												{
													'titel': 'Teilnehmer', 'app': 'PersonenDB', 'tabelle': 'tbl_terminteilnehmer', 'id': 'teilnehmer', 'optionen': ['liste', 'elementeclosed'],
													'felder': ['+id', '|zu_termin=parent:id', 'person', 'teilnahme_art'],
													'elementtitel': '{% load dioeTags %} - <span data-formtitel="person">{% getFeldVal aData.felder \'person\' %}</span> - <span data-formtitel="teilnahme_art">{% getFeldVal aData.felder \'teilnahme_art\' %}</span>',
												}
											]
										}
									]
								}
							],
							'suboption': ['tab']
						},
						{
							'titel': 'Fragebogen', 'titel_plural': 'Fragebögen', 'app': 'KorpusDB', 'tabelle': 'tbl_fragebogen', 'id': 'fragebogen', 'optionen': ['einzeln', 'elementFrameless'],
							'felder':['+id', '|id_Inf=parent:id', 'Int_Sk1', 'Int_Sk2', 'Int_Sk3', 'Int_Sk4', 'Int_Sk5', 'Int_Sk6', 'Int_Sk7', 'Int_Sk8', 'Int_Sk9', 'Int_Sk10', 'Int_Sk_11_1', 'Int_Sk_11_2', 'Int_Sk_11_3', 'Int_Sk_11_4', 'Int_Sk_11_5', 'Int_Sk_11_6', 'Spt_Sk1', 'Spt_Sk2', 'Spt_Sk3', 'Spt_Sk4', 'Spt_Sk5', 'Spt_Sk6', 'All_Sk', 'All_Q1', 'All_Q2', 'All_Q3', 'All_Q4', 'Com_Inf', 'Com_Exp', 'Erhfb_Exp_1', 'Erhfb_Exp_2', 'Erhfb_Exp_3', 'Erhfb_Exp_4', 'Erhfb_Exp_5', 'Erhfb_Exp_6', 'Erhfb_Exp_7', 'Erhfb_Exp_8', 'Erhfb_Exp_9', 'Erhfb_Exp_10', 'Erhfb_Exp_11', 'Erhfb_Exp_12', 'Erhfb_Exp_13', 'Erhfb_Exp_14', 'Erhfb_Exp_15', 'Erhfb_Exp_16', 'Erhfb_Exp_17', 'Erhfb_Exp_18', 'Erhfb_Exp_19', 'Erhfb_Exp_20', 'Erhfb_Exp_21', 'Erhfb_Exp_22', 'Erhfb_Exp_23', 'FG_SK_1', 'FG_SK_2', 'FG_SK_3', 'FG_SK_4', 'FG_SK_5', 'FG_SK_6', 'FG_SK_7', 'FG_SK_8', 'FG_SK_9', 'FG_SK_10', 'FG_List', 'FG_Q_1', 'FG_Q_2', 'Comm_FB', 'id_inferhebung'],
							'feldoptionen': {
							}
						}
					],
					'suboption': ['tab']
				},
				{
					'titel': 'Multiplikator', 'titel_plural': 'Multiplikatoren', 'app': 'PersonenDB', 'tabelle': 'tbl_multiplikator_fuer_ort', 'id': 'multiplikator', 'optionen': ['liste'],
					'felder': ['+id', '|id_person=parent:id', 'kontakt_ort', 'plz', 'kontakt_zu_p', 'kontakt_zu_m', 'sonst_info', 'kon_inf_altgruppe', 'kommentar_m']
				},
				{
					'titel': 'Mitarbeiter', 'app': 'PersonenDB', 'tabelle': 'tbl_mitarbeiter', 'id': 'mitarbeiter', 'optionen': ['liste'],
					'felder': ['+id', '|id_person=parent:id', 'funktion', 'arbeitsort', 'team']
				}
			],
			'suboption': ['tab']
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def termine(request):
	"""Eingabe Termine."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_termine'
	permName = 'personen'
	primaerId = 'termine'
	aktueberschrift = 'Termine'
	asurl = '/personendb/termine/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'Termin', 'titel_plural': 'Termine', 'app': 'PersonenDB', 'tabelle': 'tbl_termine', 'id': 'termine', 'optionen': ['einzeln', 'elementFrameless', 'noNewBtn'],
			'felder':['+id', 'titel', 'termin_art', 'termin_lokalisierung', 'zu_dbort', 'termin_beschreibung', 'zeit_start', 'zeit_ende', 'color_id', 'termin_vereinbart_in'],
			'feldoptionen':{'zeit_ende': {'jsErrorCheck': [{'type': 'isGreaterSame', 'field': 'zeit_start'}], 'nl': True}},
			'elementtitel': '{% load dioeTags %} - <span data-formtitel="zeit_start">{% getFeldVal aData.felder \'zeit_start\' %}</span> bis <span data-formtitel="zeit_ende">{% getFeldVal aData.felder \'zeit_ende\' %}</span> - <span data-formtitel="titel">{% getFeldVal aData.felder \'titel\' %}</span>',
			'sub': [
				{
					'titel': 'Teilnehmer', 'app': 'PersonenDB', 'tabelle': 'tbl_terminteilnehmer', 'id': 'teilnehmer', 'optionen': ['liste', 'elementeclosed'],
					'felder': ['+id', '|zu_termin=parent:id', 'person', 'teilnahme_art'],
					'elementtitel': '{% load dioeTags %} - <span data-formtitel="person">{% getFeldVal aData.felder \'person\' %}</span> - <span data-formtitel="teilnahme_art">{% getFeldVal aData.felder \'teilnahme_art\' %}</span>',
				}
			]
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def berufe(request):
	"""Eingabe Berufe."""
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_berufe'
	permName = 'personen'
	primaerId = 'berufe'
	aktueberschrift = 'Berufe'
	asurl = '/personendb/berufe/'
	if not request.user.has_perm(app_name + '.' + permName + '_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{
			'titel': 'Beruf', 'titel_plural': 'Berufe', 'app': 'PersonenDB', 'tabelle': 'tbl_berufe', 'id': 'berufe', 'optionen': ['einzeln', 'elementFrameless'],
			'felder':['+id', 'bezeichnung', 'berufskategorie', 'kommunikationsgrad', 'standardkompetenz']
		}
	]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)


def gcupdate(request):
	"""Google Kalender Update."""
	from DB.funktionenDB import httpOutput
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	update = ''
	from PersonenDB.models import tbl_termine
	update += 'Termine für Update: ' + str(tbl_termine.objects.filter(gc_updated=False).count()) + "\n"
	for atermin in tbl_termine.objects.filter(gc_updated=False)[:5]:
		atermin.save()
		update += str(atermin) + " - " + str(atermin.gc_event_error) + "\n"
	return httpOutput(update, mimetype='text/plain')
