"""Allgemeine Models."""
# -*- coding: utf-8 -*-
from django.db import models

models.options.DEFAULT_NAMES += ('verbose_genus',)  # m = maskulin, f = feminin, n = neutrum(default)
models.options.DEFAULT_NAMES += ('kategorienListeFilter', 'kategorienListeFXData',)  # Zusätzliche "data-fx-"-Felder für Filter
models.options.DEFAULT_NAMES += ('ipa',)  # Liste der Felder mit IPA Auswahlfeld


class tbl_personen(models.Model):
	nachname		= models.CharField(max_length=255																, verbose_name="Nachname")
	vorname			= models.CharField(max_length=255																, verbose_name="Vorname")
	geb_datum		= models.DateField(					  blank=True, null=True										, verbose_name="Geburtsdatum")
	isni			= models.IntegerField(				  blank=True, null=True										, verbose_name="ISNI")
	weiblich		= models.NullBooleanField(default=None, blank=True, null=True									, verbose_name="Weiblich")
	strasse_hausnr	= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="Strasse mit Nr.")
	akt_wohnort		= models.ForeignKey('tbl_orte'		, blank=True, null=True, on_delete=models.SET_NULL			, verbose_name="Aktueller Wohnort")
	plz				= models.CharField(max_length=6		, blank=True, null=True										, verbose_name="PLZ")
	mail1			= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="E-Mail 1")
	mail2			= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="E-Mail 2")
	festnetz1		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Festnetz 1")
	festnetz2		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Festnetz 2")
	mobil1			= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Mobil 1")
	mobil2			= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Mobil 2")

	def kategorienListeAddFX(amodel, suche, inhalt, mitInhalt, arequest, ausgabe):
		from django.shortcuts import render_to_response
		from django.template import RequestContext
		from DB.funktionenDB import kategorienListe
		import collections
		ausgabe = collections.OrderedDict()
		aReturn = kategorienListe(amodel, suche, inhalt, mitInhalt, arequest, addFX=0)
		if not inhalt:
			aElement = amodel.objects.exclude(id_person=None)
			ausgabe['nachSigle'] = {'count': aElement.count(), 'title': '<i>Nach Sigle sortiert</i>', 'enthaelt': 1}
			if mitInhalt > 0:
				ausgabe['nachSigle']['active'] = render_to_response('DB/lmfadl.html', RequestContext(arequest, {'lmfadl': kategorienListe(amodel, inhalt='nachSigle'), 'openpk': mitInhalt, 'scrollto': mitInhalt}),).content
			ausgabe.update(aReturn)
			return ausgabe
		else:
			if inhalt == 'nachSigle':
				return [{'model': aM} for aM in amodel.objects.exclude(id_person=None).order_by('id_person__inf_sigle')]
			else:
				return aReturn

	def meta(self):
		return self._meta

	def __str__(self):
		try:
			return "{}, {} - {}".format(self.nachname, self.vorname, self.id_person.inf_sigle)
		except:
			return "{}, {} - {}".format(self.nachname, self.vorname, 'None')

	class Meta:
		verbose_name = "Person"
		verbose_name_plural = "Personen"
		verbose_genus = "f"
		kategorienListeFXData = {'tbl_mitarbeiter': 'tbl_mitarbeiter_set__count()', 'id_person': 'id_person__pk', 'teams': 'id_person__inf_gruppe__gruppe_team__pk'}
		kategorienListeFilter = [
			{'titel': 'Art', 'config': {'type': 'select', 'options': [
				{'title': 'Alle', 'val': 'None'},
				{'title': 'Informanten', 'val': 'id_person>0'},
				{'title': 'Mitarbeiter', 'val': 'tbl_mitarbeiter>0'},
				{'title': 'Ohne Zuordnung', 'val': 'id_person<1&&tbl_mitarbeiter<1'},
			]}},
			{'titel': 'Teilprojekt', 'config': {'type': 'select', 'options': [
				{'title': 'Alle', 'val': 'None'},
				{'title': '!team_bez', 'val': 'teams==!pk', 'app': 'PersonenDB', 'table': 'tbl_teams'},
				{'title': 'Ohne Zuordnung', 'val': 'teams<1'},
			]}},
		]
		ordering = ('nachname',)
		default_permissions = ()
		permissions = (('edit', 'Kann PersonenDB in DB bearbeiten'), ('personen_maskView', 'Kann Maskeneingaben einsehen'), ('personen_maskAdd', 'Kann Maskeneingaben hinzufügen'), ('personen_maskEdit', 'Kann Maskeneingaben bearbeiten'),)


class tbl_orte(models.Model):
	ort_namekurz	= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="Ortsname (kurz)")
	ort_namelang	= models.CharField(max_length=255																, verbose_name="Ortsname (lang)")
	lat				= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="lat")
	lon				= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="lon")
	osm_id			= models.BigIntegerField(			  blank=True, null=True										, verbose_name="OSM-ID")
	osm_type		= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="OSM-Type")

	def __str__(self):
		return self.ort_namelang

	class Meta:
		db_table = "OrteDB_tbl_orte"
		verbose_name = "Ort"
		verbose_name_plural = "Orte"
		verbose_genus = "m"
		ordering = ('ort_namelang',)
		default_permissions = ()

class tbl_multiplikator_fuer_ort(models.Model):
	id_person		= models.ForeignKey('tbl_personen', on_delete=models.CASCADE									, verbose_name="Person")
	kontakt_ort		= models.ForeignKey('tbl_orte'																	, verbose_name="Kontakt Ort")
	plz				= models.CharField(max_length=6		, blank=True, null=True										, verbose_name="PLZ")
	kontakt_zu_p	= models.TextField(					  blank=True, null=True										, verbose_name="Kontakt zu Personengruppen")
	kontakt_zu_m	= models.ForeignKey('tbl_mitarbeiter', blank=True, null=True, on_delete=models.SET_NULL			, verbose_name="Kontakt zu Mitarbeiter")
	sonst_info		= models.TextField(					  blank=True, null=True										, verbose_name="Sonstige Information")
	kon_inf_altgruppe = models.ForeignKey('tbl_altersgruppen', blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Kontakt zu Altersgruppe")
	kommentar_m		= models.TextField(					  blank=True, null=True										, verbose_name="Kommentar")

	def __str__(self):
		return "{} in {}".format(self.id_person, self.kontakt_ort)

	class Meta:
		verbose_name = "Multiplikator für Ort"
		verbose_name_plural = "Multiplikatoren für Orte"
		verbose_genus = "m"
		ordering = ('id_person',)
		default_permissions = ()


class tbl_altersgruppen(models.Model):
	titel			= models.CharField(max_length=45																, verbose_name="Titel")
	von_jahr		= models.IntegerField(				  blank=True, null=True										, verbose_name="Von Jahr")
	bis_jahr		= models.IntegerField(				  blank=True, null=True										, verbose_name="Bis Jahr")
	kommentar		= models.TextField(					  blank=True, null=True										, verbose_name="Kommentar")

	def __str__(self):
		return "{} ({} - {})".format(self.titel, self.von_jahr, self.bis_jahr)

	class Meta:
		verbose_name = "Altersgruppe"
		verbose_name_plural = "Altersgruppen"
		verbose_genus = "f"
		ordering = ('von_jahr',)
		default_permissions = ()


class tbl_teams(models.Model):
	team_bez		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Team Bezeichnung")
	standort		= models.ForeignKey('tbl_orte'		, blank=True, null=True										, verbose_name="Standort")

	def __str__(self):
		return "{} ({})".format(self.team_bez, self.standort)

	class Meta:
		verbose_name = "Team"
		verbose_name_plural = "Teams"
		verbose_genus = "n"
		ordering = ('team_bez',)
		default_permissions = ()


class tbl_mitarbeiter(models.Model):
	id_person		= models.ForeignKey('tbl_personen', on_delete=models.CASCADE									, verbose_name="Person")
	funktion		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Funtkion")
	team			= models.ForeignKey('tbl_teams'		, blank=True, null=True, on_delete=models.SET_NULL			, verbose_name="Team")
	arbeitsort		= models.ForeignKey('tbl_orte'		, blank=True, null=True										, verbose_name="Arbeitsort")

	def __str__(self):
		return "{} - {} ({}|{})".format(self.id_person, self.funktion, self.team, self.arbeitsort)

	class Meta:
		verbose_name = "Mitarbeiter"
		verbose_name_plural = "Mitarbeiter"
		verbose_genus = "m"
		ordering = ('id_person',)
		default_permissions = ()


class tbl_informantinnen_gruppe(models.Model):
	gruppe_bez		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Gruppen Bezeichung")
	gruppe_team		= models.ForeignKey('tbl_teams'		, blank=True, null=True										, verbose_name="Team")
	gew_anzahl		= models.IntegerField(				  blank=True, null=True										, verbose_name="Gewünschte Anzahl")

	def __str__(self):
		return "{} ({})".format(self.gruppe_bez, self.gruppe_team)

	class Meta:
		verbose_name = "Informatinnen Gruppe"
		verbose_name_plural = "Informatinnen Gruppen"
		verbose_genus = "f"
		ordering = ('gruppe_bez',)
		default_permissions = ()


class tbl_terminarten(models.Model):
	teminart_bez	= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Bezeichung")
	terminart_kommentar	= models.CharField(max_length=45, blank=True, null=True										, verbose_name="Kommentar")

	def __str__(self):
		return "{}".format(self.teminart_bez)

	class Meta:
		verbose_name = "Terminart"
		verbose_name_plural = "Terminarten"
		verbose_genus = "f"
		ordering = ('teminart_bez',)
		default_permissions = ()


class tbl_akquise(models.Model):
	informant_akqu	= models.ForeignKey('tbl_informanten', on_delete=models.CASCADE									, verbose_name="Informant")
	kommentar_zu_inf = models.TextField(				  blank=True, null=True										, verbose_name="Kommentar")
	wichtige_informationen = models.TextField(			  blank=True, null=True										, verbose_name="Wichtige Informationen")
	AKQUISESTATUS_DATEN = (
		(0	, 'nicht kontaktiert'),
		(20	, 'informiert/kein termin'),
		(40	, 'interviewtermin fixiert'),
		(60	, 'interview abgeschlossen'),
		(80	, 'freundesgespräch offen'),
		(100, 'vollständig erhoben'),
	)
	akquise_status	= models.PositiveIntegerField(		  blank=True, null=True, choices=AKQUISESTATUS_DATEN		, verbose_name="Status")
	anrufe_weitere	= models.BooleanField(default=False																, verbose_name="Weitere Anrufe")
	kooparationsbereitschaft = models.IntegerField(		  blank=True, null=True										, verbose_name="Kooperationsbereitschaft (1-5)")

	def __str__(self):
		return "{} ({}%)".format(self.informant_akqu, self.akquise_status)

	class Meta:
		verbose_name = "Akquise"
		verbose_name_plural = "Akquisen"
		verbose_genus = "f"
		ordering = ('informant_akqu',)
		default_permissions = ()


class tbl_kontaktaufnahmen(models.Model):
	id_kontaktierender	= models.ForeignKey('tbl_mitarbeiter', on_delete=models.CASCADE								, verbose_name="Kontaktierender")
	zu_akquise			= models.ForeignKey('tbl_akquise', on_delete=models.CASCADE									, verbose_name="Zu Akquise")
	beschreibung		= models.TextField(					blank=True, null=True									, verbose_name="Beschreibung")
	zeit				= models.DateTimeField(																		  verbose_name="Zeit")
	Text				= models.TextField(					blank=True, null=True									, verbose_name="Text")
	KONTAKTART_DATEN = (
		('anruf', 'Anruf'),
		('mail', 'E-Mail'),
		('persoenlich', 'persönlich'),
	)
	kontaktart			= models.CharField(max_length=45, choices=KONTAKTART_DATEN									, verbose_name="Kontaktart")

	def __str__(self):
		return "{} ({})".format(self.zeit, self.zu_akquise)

	class Meta:
		verbose_name = "Kontaktaufnahme"
		verbose_name_plural = "Kontaktaufnahmen"
		verbose_genus = "f"
		ordering = ('zeit',)
		default_permissions = ()


class tbl_termine(models.Model):
	titel			= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Titel")
	termin_art		= models.ForeignKey('tbl_terminarten', on_delete=models.CASCADE									, verbose_name="Art")
	termin_lokalisierung = models.CharField(max_length=45, blank=True, null=True									, verbose_name="Lokalisierung")
	zu_dbort		= models.ForeignKey('tbl_orte'		, blank=True, null=True, on_delete=models.SET_NULL			, verbose_name="zu Ort")
	termin_beschreibung = models.TextField(				  blank=True, null=True										, verbose_name="Beschreibung")
	zeit_start		= models.DateTimeField(																			  verbose_name="Zeit Start")
	zeit_ende		= models.DateTimeField(																			  verbose_name="Zeit Ende")
	termin_vereinbart_in = models.ForeignKey('tbl_kontaktaufnahmen', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Kontaktaufnahme")
	COLORID_DATEN = (
		(5, 'PP02 - Wien'),			# (5, '#fbd75b'),
		(6, 'PP02 - Salzburg'), 	# (6, '#ffb878'),
		(11, 'PP03'),				# (11, '#dc2127'),
		(3, 'PP04'),				# (3, '#dbadff'),
		(7, 'PP08'),				# (7, '#46d6db'),
		(9, 'PP10'),				# (9, '#5484ed'),
		(1, '#a4bdfc'),				# (1, '#a4bdfc'),
		(2, '#7ae7bf'),				# (2, '#7ae7bf'),
		(4, '#ff887c'),				# (4, '#ff887c'),
		(8, '#e1e1e1'),				# (8, '#e1e1e1'),
		(10, '#51b749'),			# (10, '#51b749'),
	)
	color_id		= models.PositiveIntegerField(		  blank=True, null=True, choices=COLORID_DATEN				, verbose_name="PP_color")
	gc_event_id		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Google Calender Event ID")
	gc_updated		= models.BooleanField(default=False																, verbose_name="Google Calender Updated")
	gc_event_error	= models.CharField(max_length=1024	, blank=True, null=True										, verbose_name="Google Calender Error")

	def save(self, *args, **kwargs):
		from django.conf import settings
		import httplib2, datetime, pytz
		from googleapiclient.discovery import build
		from oauth2client.service_account import ServiceAccountCredentials
		calendarId = getattr(settings, 'GC_CALENDAR_ID', 'termine@dioe.at')
		CLIENT_SECRET_FILE = getattr(settings, 'GC_CLIENT_SECRET_FILE', 'secret/dioeDB - Google Kalender-55c31b432bed.json')
		self.gc_updated = False
		try:
			SCOPES = 'https://www.googleapis.com/auth/calendar'
			scopes = [SCOPES]
			credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes)
			http = credentials.authorize(httplib2.Http())
			service = build('calendar', 'v3', http=http)
			if isinstance(self.zeit_start, str):
				self.zeit_start = datetime.datetime.strptime(self.zeit_start, '%Y-%m-%d %H:%M')
			if isinstance(self.zeit_ende, str):
				self.zeit_ende = datetime.datetime.strptime(self.zeit_ende, '%Y-%m-%d %H:%M')
			attxt = ''
			for ateilnehmer in self.tbl_terminteilnehmer_set.all():
				xat = 'Person: ' + ateilnehmer.person.mail1
				for ainf in tbl_informanten.objects.filter(id_person=ateilnehmer.person.pk):
					xat = 'Informant: ' + ainf.inf_sigle
				attxt += str(xat) + (' - ' + ateilnehmer.teilnahme_art if ateilnehmer.teilnahme_art else '') + "\n"
			tzinfo = pytz.timezone('Europe/Vienna')
			abody = {
				'summary': self.titel + ' (' + str(self.termin_art) + ')',
				'description': attxt + "\n" + self.termin_beschreibung,
				'start': {'dateTime': tzinfo.localize(self.zeit_start).isoformat()},
				'end': {'dateTime': tzinfo.localize(self.zeit_ende).isoformat()},
				'colorId': self.color_id,
				'status': 'confirmed',
			}
			if self.gc_event_id:
				event = service.events().update(calendarId=calendarId, eventId=self.gc_event_id, body=abody).execute()
			else:
				event = service.events().insert(calendarId=calendarId, body=abody).execute()
			if 'id' in event:
				self.gc_event_id = event['id']
				self.gc_updated = True
			self.gc_event_error = 'Keine Fehler'
		except Exception as e:
			strE = str(e)
			self.gc_event_error = strE[1020] if len(strE) > 1022 else strE
			print("Termin konnte nicht mit Google Syncronisiert werden! " + strE)
		super(tbl_termine, self).save(*args, **kwargs)

	def __str__(self):
		if not self.gc_event_error == 'Keine Fehler' and self.gc_event_error is not None:
			return "{} - GC_Error".format(self.titel)
		else:
			return "{}".format(self.titel)

	class Meta:
		verbose_name = "Termin"
		verbose_name_plural = "Termine"
		verbose_genus = "m"
		ordering = ('zeit_start',)
		default_permissions = ()


class tbl_terminteilnehmer(models.Model):
	zu_termin		= models.ForeignKey('tbl_termine', on_delete=models.CASCADE										, verbose_name="Termin")
	person			= models.ForeignKey('tbl_personen', on_delete=models.CASCADE									, verbose_name="Person")
	teilnahme_art	= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Teilnahme Art")

	def __str__(self):
		return "{} - {} ({})".format(self.zu_termin, self.person, self.teilnahme_art)

	class Meta:
		verbose_name = "Terminteilnehmer"
		verbose_name_plural = "Terminteilnehmer"
		verbose_genus = "m"
		ordering = ('zu_termin',)
		default_permissions = ()


class tbl_person_in_verein(models.Model):
	id_person		= models.ForeignKey('tbl_personen', on_delete=models.CASCADE									, verbose_name="Person")
	id_verein		= models.ForeignKey('tbl_vereine'																, verbose_name="Verein")
	funktion		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Funktion")
	anmerkung		= models.CharField(max_length=45	, blank=True, null=True										, verbose_name="Anmerkung")

	def __str__(self):
		return "{}, {}".format(self.funktion, self.id_verein)

	class Meta:
		verbose_name = "Person in Verein"
		verbose_name_plural = "Personen in Vereine"
		verbose_genus = "f"
		ordering = ('id_person',)
		default_permissions = ()


class tbl_vereine(models.Model):
	vereinname		= models.CharField(max_length=255																, verbose_name="Vereinsname")
	verein_art		= models.IntegerField(				  blank=True, null=True										, verbose_name="Art des Vereins")
	verein_ort		= models.ForeignKey('tbl_orte'		, blank=True, null=True, on_delete=models.SET_NULL			, verbose_name="Ort des Vereins")

	def __str__(self):
		return "{} ({})".format(self.vereinname, self.verein_ort)

	class Meta:
		verbose_name = "Verein"
		verbose_name_plural = "Vereine"
		verbose_genus = "m"
		ordering = ('vereinname',)
		default_permissions = ()


class tbl_informanten(models.Model):
	id_person		= models.OneToOneField('tbl_personen', on_delete=models.CASCADE, related_name='id_person'		, verbose_name="Person")
	inf_sigle		= models.CharField(max_length=255, unique=True													, verbose_name="Informant/in Sigle")
	kompetenz_d		= models.IntegerField(				  blank=True, null=True										, verbose_name="Dialekt Kompetenz")
	kompetenz_s		= models.IntegerField(				  blank=True, null=True										, verbose_name="Standard Kompetenz")
	haeufigkeit_d	= models.IntegerField(				  blank=True, null=True										, verbose_name="Dialekt Häufigkeit")
	haeufigkeit_s	= models.IntegerField(				  blank=True, null=True										, verbose_name="Standard Häufigkeit")
	inf_ort			= models.ForeignKey('tbl_orte'		, blank=True, null=True, on_delete=models.SET_NULL, related_name='inf_ort', verbose_name="Informant/in Ort")
	akquiriert_am	= models.DateField(					  blank=True, null=True										, verbose_name="Akquiriert am")
	pretest			= models.BooleanField(default=False																, verbose_name="Pretest")
	geburtsort		= models.ForeignKey('tbl_orte', blank=True, null=True, on_delete=models.SET_NULL, related_name='geburtsort', verbose_name="Geburtsort")
	kontakt_durch	= models.ForeignKey('tbl_personen', blank=True, null=True, related_name='kontakt_durch'			, verbose_name="Kontakt durch")
	inf_gruppe		= models.ForeignKey('tbl_informantinnen_gruppe', blank=True, null=True, related_name='inf_gruppe'	, verbose_name="Informantinnen Gruppe")
	eignung			= models.IntegerField(				blank=True, null=True										, verbose_name="Eignung (1-5)")
	FAMILIENSTAND_DATEN = (
		('ledig', 'ledig'),
		('verheiratet', 'verheiratet'),
		('inpartnerschaft', 'in Partnerschaft'),
		('geschieden', 'geschieden'),
		('verwitwet', 'verwitwet'),
	)
	familienstand	= models.CharField(max_length=45, choices=FAMILIENSTAND_DATEN, blank=True, null=True			, verbose_name="Familienstand")
	ausserhalbwohnort = models.IntegerField(			blank=True, null=True										, verbose_name="Außerhalb Wohnort in Jahren")
	AUSBILDUNGMAX_DATEN = (
		('pflichtschule', 'Pflichtschule'),
		('berufsausbildung', 'Berufsausbildung'),
		('hochschulreife', 'Hochschulreife'),
		('hochschulabschluss', 'Hochschulabschluss'),
	)
	ausbildung_max	= models.CharField(max_length=45, choices=AUSBILDUNGMAX_DATEN, blank=True, null=True			, verbose_name="Ausbildung (Max.)")
	ausbildung_spez	= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="Ausbildung Spezifizierung")
	MIGRATIONSKLASSE_DATEN = (
		(0, 'keine Migration'),
		(1, 'Binnenmigration innerhalb Bundesland'),
		(2, 'Binnenmigration außerhalb Bundesland'),
		(3, 'Migration außerhalb Österreichs'),
	)
	migrationsklasse = models.PositiveIntegerField(		blank=True, null=True, choices=MIGRATIONSKLASSE_DATEN		, verbose_name="Migrationsklasse")
	kommentar		= models.TextField(					blank=True, null=True										, verbose_name="Kommentar")

	def __str__(self):
		return "{} - {}".format(self.inf_sigle, self.id_person)

	class Meta:
		verbose_name = "Informant"
		verbose_name_plural = "Informanten"
		verbose_genus = "m"
		ordering = ('inf_sigle',)
		default_permissions = ()


class tbl_informant_x_gewohnt_in(models.Model):
	id_informant	= models.ForeignKey('tbl_informanten', on_delete=models.CASCADE									, verbose_name="Informant")
	id_ort			= models.ForeignKey('tbl_orte'																	, verbose_name="Ort")
	WER_DATEN = (
		('informant', 'Informant'),
		('mutter', 'Mutter'),
		('vater', 'Vater'),
		('ehepartner', '(Ehe)partnerIn'),
	)
	wer				= models.CharField(max_length=45, choices=WER_DATEN												, verbose_name="Wer")
	reihung			= models.IntegerField(				  blank=True, null=True										, verbose_name="Reihung")
	plz				= models.CharField(max_length=6		, blank=True, null=True										, verbose_name="PLZ")
	von_jahr		= models.IntegerField(				  blank=True, null=True										, verbose_name="Von Jahr")
	bis_jahr		= models.IntegerField(				  blank=True, null=True										, verbose_name="Bis Jahr")
	dauer_jahr		= models.IntegerField(				  blank=True, null=True										, verbose_name="Dauer in Jahren")
	aufgewachsen	= models.BooleanField(default=False																, verbose_name="Aufgewachsen?")
	arbeitsort		= models.BooleanField(default=False																, verbose_name="Arbeitsort?")
	fahrtdauer		= models.IntegerField(				  blank=True, null=True										, verbose_name="Fahrtdauer in Stunden")
	kompetenz_d		= models.IntegerField(				  blank=True, null=True										, verbose_name="Dialekt Kompetenz")
	haeufigkeit_d	= models.IntegerField(				  blank=True, null=True										, verbose_name="Dialekt Häufigkeit")
	beziehungsdauer = models.IntegerField(				  blank=True, null=True										, verbose_name="Beziehungsdauer in Jahren")

	def __str__(self):
		return "{} in {}".format(self.get_wer_display(), self.id_ort)

	class Meta:
		verbose_name = "Informant x gewohnt in"
		verbose_name_plural = "Informanten x gewohnt in"
		verbose_genus = "m"
		ordering = ('id_informant', 'von_jahr')
		default_permissions = ()


class inf_ist_beruf(models.Model):
	id_informant	= models.ForeignKey('tbl_informanten', on_delete=models.CASCADE									, verbose_name="Informant")
	id_beruf		= models.ForeignKey('tbl_berufe'																, verbose_name="Beruf")
	inf_spezifizierung = models.CharField(max_length=255, blank=True, null=True										, verbose_name="Spezifizierung")
	reihung			= models.IntegerField(				blank=True, null=True										, verbose_name="Reihung")
	von_jahr		= models.IntegerField(				blank=True, null=True										, verbose_name="Von Jahr")
	bis_jahr		= models.IntegerField(				blank=True, null=True										, verbose_name="Bis Jahr")
	dauer_jahr		= models.IntegerField(				blank=True, null=True										, verbose_name="Dauer in Jahren")
	ist_aktuell		= models.BooleanField(default=False																, verbose_name="Ist Aktuell?")
	ist_ausbildung	= models.BooleanField(default=False																, verbose_name="Ist Ausbildung?")

	def __str__(self):
		return "{} von {} bis {}".format(self.id_beruf, self.von_jahr, self.bis_jahr)

	class Meta:
		verbose_name = "Ist Beruf"
		verbose_name_plural = "Ist Berufe"
		verbose_genus = "m"
		ordering = ('id_informant',)
		default_permissions = ()


class tbl_berufe(models.Model):
	bezeichnung		= models.CharField(max_length=255																, verbose_name="Bezeichnung")
	berufskategorie	= models.CharField(max_length=255	, blank=True, null=True										, verbose_name="Berufskategorie")
	kommunikationsgrad = models.IntegerField(			  blank=True, null=True										, verbose_name="Kommunikationsgrad")
	standardkompetenz = models.IntegerField(			  blank=True, null=True										, verbose_name="Standardkompetenz")

	def __str__(self):
		return "{} ({})".format(self.bezeichnung, self.berufskategorie)

	class Meta:
		verbose_name = "Beruf"
		verbose_name_plural = "Berufe"
		verbose_genus = "m"
		ordering = ('bezeichnung',)
		default_permissions = ()
