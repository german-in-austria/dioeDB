from django.db import models
from PersonenDB.models import tbl_orte
from datetime import datetime

# Create your models here.
# m = maskulin, f = feminin, n = neutrum(default)
models.options.DEFAULT_NAMES += ('verbose_genus',)
# Zusätzliche "data-fx-"-Felder für Filter
models.options.DEFAULT_NAMES += ('kategorienListeFilter', 'kategorienListeFXData',)
# Liste der Felder mit IPA Auswahlfeld
models.options.DEFAULT_NAMES += ('ipa',)

# ToDo what to cascade and what not? best practice
# ToDo class Meta default permissions? what must be there?


# --- 1 level tables---
# names of administrativ entities
class tbl_adm_lvl(models.Model):
	name			= models.CharField(max_length=255																		, verbose_name="Administrative Einheit")
	def __str__(self):
		return "{}".format(self.name)
	class Meta:
		db_table = "MioeDB_tbl_adm_lvl"
		verbose_name = "Administrative Einheit"
		verbose_name_plural = "Administrative Einheit"
		verbose_genus = "f"
		ordering = ('name',)
		default_permissions = ()
		permissions = (('mioe_edit', 'Kann mioeDB in DB bearbeiten'), ('mioe_view', 'Kann mioeDB auslesen'), ('mioe_maskView', 'Kann MiÖ Maskeneingaben einsehen'), ('mioe_maskAdd', 'Kann MiÖ Maskeneingaben hinzufuegen'), ('mioe_maskEdit', 'Kann MiÖ Maskeneingaben bearbeiten'),)


# type of the variations
class tbl_variet_typ(models.Model):
	typ_name		= models.CharField(max_length=255																		, verbose_name="Varietätstyp")
	def __str__(self):
		return "{}".format(self.typ_name)
	class Meta:
		db_table = "MioeDB_tbl_variet_typ"
		verbose_name = "Varietätstyp"
		verbose_name_plural = "Varietätstype"
		verbose_genus = "m"
		ordering = ('typ_name',)
		default_permissions = ()


# religions
class tbl_religion(models.Model):
	relig_name		= models.CharField(max_length=255																		, verbose_name="Religion")
	def __str__(self):
		return "{}".format(self.relig_name)
	class Meta:
		db_table = "MioeDB_tbl_religion"
		verbose_name = "Religion"
		verbose_name_plural = "Religionen"
		verbose_genus = "f"
		ordering = ('relig_name',)
		default_permissions = ()


# instituts types (schools ...)
class tbl_institutstyp(models.Model):
	schule			= models.BooleanField(																					  verbose_name="Schule")
	typ				= models.CharField(max_length=255																		, verbose_name="Institutstyp")
	def __str__(self):
		return "{}".format(self.typ)
	class Meta:
		db_table = "MioeDB_tbl_institutstyp"
		verbose_name = "Institutstyp"
		verbose_name_plural = "Institutstypen"
		verbose_genus = "m"
		ordering = ('typ',)
		default_permissions = ()


# --- 2 level tables---
# additional fields for administrativ mioe entries
class tbl_mioe_orte(models.Model):
	id_orte			= models.ForeignKey('PersonenDB.tbl_orte', blank=True, null=True										, verbose_name="Ort")
	# ToDo do we need gid here at all? it is also in wb
	gid				= models.IntegerField(blank=True, null=True																, verbose_name="REDE-ID")
	adm_lvl			= models.ForeignKey('tbl_adm_lvl'																		, verbose_name="Administrative Ebene")
	histor			= models.BooleanField(default=False																		, verbose_name="Ist historischer Ort")
	histor_ort		= models.CharField(max_length=255, blank=True, null=True												, verbose_name="Historischer Ort")

	def __str__(self):
		return (self.id_orte.ort_namekurz or self.id_orte.ort_namelang) if self.id_orte else self.histor_ort

	def kategorienListeFX(amodel, suche, inhalt, mitInhalt, arequest, ausgabe):
		from django.shortcuts import render_to_response
		from django.template import RequestContext
		from DB.funktionenDB import kategorienListe
		from django.db.models import Q, F
		import collections
		# Alphabetisch
		kategorien = collections.OrderedDict()
		kategorien['Andere'] = '^a-zäöüÄÖÜ'
		kategorien['istartswith'] = 'abcdefghijklmnopqrstuvwxyz'
		kategorien['ä'] = 'äÄ'
		kategorien['ö'] = 'öÖ'
		kategorien['ü'] = 'üÜ'
		if not inhalt:  # Liste fuer Kategrien ausgeben
			for key, value in kategorien.items():
				if key == 'istartswith':
					for abc in value:
						if suche:
							aElement = amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__istartswith': abc, amodel._meta.ordering[0] + '__contains': suche}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__istartswith': abc, amodel._meta.ordering[1] + '__contains': suche}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__istartswith': abc, amodel._meta.ordering[1] + '__contains': suche}))
						else:
							aElement = amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__istartswith': abc}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__istartswith': abc}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__istartswith': abc}))
						ausgabe[abc] = {'count': aElement.count()}
						if mitInhalt > 0:
							if aElement.filter(pk=mitInhalt).count():
								ausgabe[abc]['active'] = render_to_response(
									'DB/lmfadl.html',
									RequestContext(arequest, {'lmfadl': kategorienListe(amodel, inhalt=abc), 'openpk': mitInhalt, 'scrollto': mitInhalt}),).content
				else:
					if suche:
						aElement = amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__iregex': '^([' + value + '].+)', amodel._meta.ordering[0] + '__contains': suche}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__iregex': '^([' + value + '].+)', amodel._meta.ordering[1] + '__ort_namekurz__contains': suche}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__iregex': '^([' + value + '].+)', amodel._meta.ordering[1] + '__ort_namelang__contains': suche}))
					else:
						aElement = amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__iregex': '^([' + value + '].+)'}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__iregex': '^([' + value + '].+)'}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__iregex': '^([' + value + '].+)'}))
					ausgabe[key] = {'count': aElement.count()}
					if mitInhalt > 0:
						if aElement.filter(pk=mitInhalt).count():
							ausgabe[key]['active'] = render_to_response(
								'DB/lmfadl.html',
								RequestContext(arequest, {'lmfadl': kategorienListe(amodel, inhalt=key), 'openpk': mitInhalt, 'scrollto': mitInhalt}),).content
		else:  # Inhalte fuer Kategorie ausgeben
			if inhalt in kategorien:
				ausgabe = [{'model': aM} for aM in amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__iregex': '^([' + kategorien[inhalt] + '].+)'}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__iregex': '^([' + kategorien[inhalt] + '].+)'}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__iregex': '^([' + kategorien[inhalt] + '].+)'})).order_by('histor_ort', 'id_orte__ort_namelang')]
			else:
				ausgabe = [{'model': aM} for aM in amodel.objects.filter(Q(**{amodel._meta.ordering[0] + '__istartswith':inhalt}) | Q(**{amodel._meta.ordering[1] + '__ort_namekurz__istartswith':inhalt}) | Q(**{amodel._meta.ordering[1] + '__ort_namelang__istartswith':inhalt})).order_by('histor_ort', 'id_orte__ort_namelang')]
		return ausgabe

	class Meta:
		db_table = "MioeDB_tbl_mioe_orte"
		verbose_name = "MiÖ Ort"
		verbose_name_plural = "MiÖ Orte"
		verbose_genus = "m"
		ordering = ('histor_ort', 'id_orte',)
		default_permissions = ()


# variations
class tbl_varietaet(models.Model):
	variet_name		= models.CharField(max_length=255																				, verbose_name="Sprache")
	iso_code		= models.CharField(max_length=255, blank=True, null=True														, verbose_name="ISO-Code")
	id_typ			= models.ForeignKey('tbl_variet_typ'																			, verbose_name="Varietätstyp")
	id_varietaet	= models.ForeignKey('tbl_varietaet', blank=True, null=True														, verbose_name="Varietät")
	def __str__(self):
		return "{}".format(self.variet_name)
	class Meta:
		db_table = "MioeDB_tbl_varietaet"
		verbose_name = "Varietät"
		verbose_name_plural = "Varietäten"
		verbose_genus = "f"
		ordering = ('id_typ', 'variet_name',)
		default_permissions = ()


# --- 3 level tables---
# type of data
class tbl_art_daten(models.Model):
	art_name		= models.CharField(max_length=255																				, verbose_name="Art von Daten")
	id_varietaet	= models.ForeignKey('tbl_varietaet', blank=True, null=True														, verbose_name="Varietät")
	id_religion		= models.ForeignKey('tbl_religion', blank=True, null=True														, verbose_name="Religion")
	def __str__(self):
		return self.art_name + ((' ' + self.id_varietaet.variet_name) if self.id_varietaet else '') + ((' ' + self.id_religion.relig_name) if self.id_religion else '')
	class Meta:
		db_table = "MioeDB_tbl_art_daten"
		verbose_name = "Art von Daten"
		verbose_name_plural = "Arten von Daten"
		verbose_genus = "f"
		ordering = ('art_name',)
		default_permissions = ()


# mioe persons
class tbl_mioe_personen(models.Model):
	id_personen		= models.ForeignKey('PersonenDB.tbl_personen'																	, verbose_name="Person")
	funktion		= models.CharField(blank=True, null=True, max_length=255														, verbose_name="Funktion")
	geburtsort_angabe = models.CharField(blank=True, null=True, max_length=255														, verbose_name="Geburtsort Angabe")
	geburtsort		= models.ForeignKey('tbl_mioe_orte', blank=True, null=True														, verbose_name="Geburtsort")
	def __str__(self):
		return "{} - {}".format(self.id_personen.nachname, self.id_personen.vorname,)
	class Meta:
		db_table = "MioeDB_tbl_mioe_personen"
		verbose_name = "Mioe Person"
		verbose_name_plural = "Mioe Personen"
		verbose_genus = "f"
		ordering = ('id_personen',)
		default_permissions = ()


# polls
class tbl_wb(models.Model):
	num_wb			= models.IntegerField(																							  verbose_name="Wenkerbogen Nummer")
	typ_wb			= models.CharField(max_length=1																					, verbose_name="Wenkerbogen Typ")
	datierung_start	= models.DateField(blank=True, null=True																		, verbose_name="Datierung start")
	datierung_end	= models.DateField(blank=True, null=True																		, verbose_name="Datierung end")
	id_mioe_ort		= models.ForeignKey('tbl_mioe_orte', on_delete=models.CASCADE													, verbose_name="MiÖ-Ort")
	gid				= models.IntegerField(blank=True, null=True																		, verbose_name="REDE-ID")
	schulort_orig	= models.CharField(max_length=255																				, verbose_name="Schulort (Angabe)")
	id_lehrer		= models.ForeignKey('tbl_mioe_personen', blank=True, null=True, on_delete=models.CASCADE						, verbose_name="Lehrer")
	uebersetzt_von	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Übersetzt von")
	uebersetzt_klass = models.CharField(max_length=255, blank=True, null=True														, verbose_name="Übersetzt Klass")
	alter_geschl_uebesetzer = models.CharField(max_length=255, blank=True, null=True												, verbose_name="Alter, Geschlecht Übesetzer")
	alter_geschl_lehrer = models.CharField(max_length=255, blank=True, null=True													, verbose_name="Alter, Geschlecht Lehrer")
	alter_uebesetzer = models.IntegerField(blank=True, null=True																	, verbose_name="Alter Übesetzer")
	geburtsdatum_uebersetzer = models.DateField(blank=True, null=True																, verbose_name="Geburtsdatum Übesetzer")
	geschlecht_uebersetzer = models.CharField(max_length=255, blank=True, null=True													, verbose_name="Geschlecht Übesetzer")
	informationen_zu = models.CharField(max_length=255, blank=True, null=True														, verbose_name="Informationen zu")
	andere_sprachen	= models.BooleanField(																							  verbose_name="Andere Sprachen")
	welche_sprachen	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Welche Sprachen")
	sprachen_verhaeltnis = models.CharField(max_length=255, blank=True, null=True													, verbose_name="Sprachen Verhältnis")
	kommentar_wb	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar Wenkerbogen")
	kommentar_wiss	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar Wiss.")
	geprueft		= models.BooleanField(default=False																				, verbose_name="Geprüft")
	problematisch	= models.BooleanField(default=False																				, verbose_name="Problematisch")
	link_rede		= models.CharField(max_length=255, blank=True, null=True														, verbose_name="REDE Link")
	def __str__(self):
		return "{} - {}".format(self.id_mioe_ort, self.num_wb)
	class Meta:
		db_table = "MioeDB_tbl_wb"
		verbose_name = "Wenkerbogen"
		verbose_name_plural = "Wenkerbögen"
		verbose_genus = "m"
		ordering = ('num_wb',)
		default_permissions = ()


# --- 5 level tables ---
# polls languages
class tbl_wb_sprache(models.Model):
	id_wb			= models.ForeignKey('tbl_wb'																					, verbose_name="Wenkerbogen")
	id_varietaet	= models.ForeignKey('tbl_varietaet'																				, verbose_name="Varietät")
	anteil			= models.FloatField(																							  verbose_name="Anteil")
	def __str__(self):
		return "{} - {}%".format(self.id_varietaet.variet_name, self.anteil)
	class Meta:
		db_table = "MioeDB_tbl_wb_sprache"
		verbose_name = "Wenkerbogen Sprache"
		verbose_name_plural = "Wenkerbögen Sprachen"
		verbose_genus = "f"
		ordering = ('id_wb',)
		default_permissions = ()


# sources of info
class tbl_quelle(models.Model):
	wenkerbogen		= models.ForeignKey('tbl_wb', blank=True, null=True, on_delete=models.CASCADE									, verbose_name="Wenkerbogen")
	id_literatur	= models.ForeignKey('tbl_literaturv', blank=True, null=True														, verbose_name="Literatur")
	def __str__(self):
		if self.wenkerbogen is not None:
			return "wb: {}".format(self.wenkerbogen)
		else:
			return "lit: {}".format(self.id_literatur)
	class Meta:
		db_table = "MioeDB_tbl_quelle"
		verbose_name = "Quelle"
		verbose_name_plural = "Quellen"
		verbose_genus = "f"
		ordering = ('id',)
		default_permissions = ()


# worktable for literatur_id; needed for VZ; should be extended later
class tbl_literaturv(models.Model):
	name			= models.CharField(max_length=255																				, verbose_name="Arbeitsname")
	PublDat_start	= models.DateField(blank=True, null=True																		, verbose_name="Publikationsdatum start")
	PublDat_end		= models.DateField(blank=True, null=True																		, verbose_name="Publikationsdatum end")
	def __str__(self):
		return "{} ({} - {})".format(self.name, self.PublDat_start, self.PublDat_end)
	class Meta:
		db_table = "MioeDB_tbl_literaturv"
		verbose_name = "Literatur vorläufig"
		verbose_name_plural = "Literaturen vorläufig"
		verbose_genus = "f"
		ordering = ('id',)
		default_permissions = ()


# polls are also for
class tbl_wb_auch_fuer(models.Model):
	id_wb			= models.ForeignKey('tbl_wb'																					, verbose_name="Wenkerbogen",)
	id_wbort		= models.ForeignKey('tbl_mioe_orte', blank=True, null=True														, verbose_name="Wenkerort")
	id_lehrer		= models.ForeignKey('tbl_mioe_personen', blank=True, null=True													, verbose_name="Lehrer")
	kommentar_wb	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar Wenkerbogen")
	kommentar_wiss	= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar Wiss.")
	def __str__(self):
		return "{}: {}, {}".format(self.id_wb.num_wb, self.id_wbort.id_orte.ort_namekurz, self.id_lehrer.id_personen.nachname)
	class Meta:
		db_table = "MioeDB_tbl_wb_auch_fuer"
		verbose_name = "Wenkerbogen auch fuer"
		verbose_name_plural = "Wenkerbögen auch fuer"
		verbose_genus = "m"
		ordering = ('id_wb',)
		default_permissions = ()


# --- 5 level tables ---
class tbl_volkszaehlung(models.Model):
	id_ort			= models.ForeignKey('tbl_mioe_orte'																				, verbose_name="Ort")
	id_quelle		= models.ForeignKey('tbl_quelle'																				, verbose_name="Quelle")
	erheb_datum		= models.DateField(blank=True, null=True																		, verbose_name="Erhebungsdatum")
	def __str__(self):
		return "{}".format(self.id_quelle)
	class Meta:
		db_table = "MioeDB_tbl_volkszaehlung"
		verbose_name = "Volkszählung"
		verbose_name_plural = "Volkszählungen"
		verbose_genus = "f"
		ordering = ('id_ort', 'id_quelle')
		default_permissions = ()


# administativ relation
class tbl_adm_zuordnung(models.Model):
	id_ort1			= models.ForeignKey('tbl_mioe_orte', related_name="%(class)s_ort1"												, verbose_name="Administrative Einheit 1")
	id_ort2			= models.ForeignKey('tbl_mioe_orte', related_name="%(class)s_ort2"												, verbose_name="Administrative Einheit 2")
	id_quelle		= models.ForeignKey('tbl_quelle', blank=True, null=True															, verbose_name="Quelle")
	vonDat_start	= models.DateField(blank=True, null=True																		, verbose_name="Datierung von (start)")
	vonDat_end		= models.DateField(blank=True, null=True																		, verbose_name="Datierung von (end)")
	bisDat_start	= models.DateField(blank=True, null=True																		, verbose_name="Datierung bis (start)")
	bisDat_end		= models.DateField(blank=True, null=True																		, verbose_name="Datierung bis (end)")
	kommentar		= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar")
	def __str__(self):
		return "{}".format(self.id_ort1)
	class Meta:
		db_table = "MioeDB_tbl_adm_zuordnung"
		verbose_name = "Administrative Zuordnung"
		verbose_name_plural = "Administrative Zuordnung"
		verbose_genus = "f"
		ordering = ('id',)
		default_permissions = ()


# names variations
class tbl_name_var(models.Model):
	var_name		= models.CharField(max_length=255																				, verbose_name="Namensvariante")
	id_varietaet	= models.ForeignKey('tbl_varietaet', blank=True, null=True														, verbose_name="Varietät")
	id_mioe_ort		= models.ForeignKey('tbl_mioe_orte', blank=True, null=True														, verbose_name="Ort")
	id_quelle		= models.ForeignKey('tbl_quelle', blank=True, null=True															, verbose_name="Quelle")
	kommentar		= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar")
	def __str__(self):
		return "{} - {}".format(self.id_mioe_ort, self.var_name)
	class Meta:
		db_table = "MioeDB_tbl_name_var"
		verbose_name = "Namensvariante"
		verbose_name_plural = "Namensvarianten"
		verbose_genus = "f"
		ordering = ('id_mioe_ort',)
		default_permissions = ()


# n:m Table name_variation to quelle
class tbl_name_var_quelle(models.Model):
	id_quelle		= models.ForeignKey('tbl_quelle', blank=False, null=False														, verbose_name="ID Quelle")
	id_name_var		= models.ForeignKey('tbl_name_var', blank=False, null=False														, verbose_name="ID Namensvariante")
	def __str__(self):
		return "{} zu {}".format(self.id_quelle, self.id_name_var)
	class Meta:
		db_table = "MioeDB_tbl_name_var_quelle"
		verbose_name = "Quelle zu Namensvariante"
		verbose_name_plural = "Quellen zu Namensvariante"
		ordering = ('id',)
		default_permissions = ()


# --- 6 level tables ---
# institutions or schools
class tbl_institutionen(models.Model):
	id_ort			= models.ForeignKey('tbl_mioe_orte'																				, verbose_name="Ort")
	id_institutstyp	= models.ForeignKey('tbl_institutstyp'																			, verbose_name="Institutstyp")
	anz_klassen		= models.IntegerField(blank=True, null=True																		, verbose_name="Anzahl von Klassen")
	id_quelle		= models.ForeignKey('tbl_quelle'																				, verbose_name="Quelle")
	kommentar		= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Kommentar")
	def __str__(self):
		return "{}: {} mit {} Klassen".format(self.id_ort, self.id_institutstyp.typ, self.id_quelle.erheb_datum)
	class Meta:
		db_table = "MioeDB_tbl_instatutionen"
		verbose_name = "Institution"
		verbose_name_plural = "Institutionen"
		verbose_genus = "f"
		ordering = ('id_ort',)
		default_permissions = ()


# population and language data
class tbl_vz_daten(models.Model):
	id_vz			= models.ForeignKey('tbl_volkszaehlung'																			, verbose_name="Volkszählung")
	id_mioe_ort		= models.ForeignKey('tbl_mioe_orte'																				, verbose_name="Ort")
	id_art			= models.ForeignKey('tbl_art_daten'																				, verbose_name="Art von Daten")
	abw_bez			= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Abweichende Bezeichnung in VZ")
	anzahl			= models.IntegerField(blank=True, null=True																		, verbose_name="Anzahl")
	def __str__(self):
		return "{} {}: {} - {}".format(self.id_vz.erheb_datum, self.id_mioe_ort, self.id_art.art_name, self.anzahl)
	class Meta:
		unique_together = ("id_vz", "id_mioe_ort", "id_art")
		db_table = "MioeDB_tbl_vz_daten"
		verbose_name = "Volkszählungsdaten"
		verbose_name_plural = "Volkszählungsdaten"
		verbose_genus = "f"
		ordering = ('id_vz', 'id_mioe_ort',)
		default_permissions = ()


class tbl_art_in_vz(models.Model):
	id_vz			= models.ForeignKey('tbl_volkszaehlung'																			, verbose_name="Volkszählung")
	id_art			= models.ForeignKey('tbl_art_daten'																				, verbose_name="Art von Daten")
	bez				= models.CharField(max_length=255, blank=True, null=True														, verbose_name="Bezeichnung")
	reihung			= models.IntegerField(blank=True, null=True																		, verbose_name="Reihung")
	def __str__(self):
		return "{} {}: {}".format(self.id_vz.erheb_datum, self.id_art.art_name, self.bez)
	class Meta:
		db_table = "MioeDB_tbl_art_in_vz"
		verbose_name = "Art in Volkszählung"
		verbose_name_plural = "Arten in Volkszählung"
		verbose_genus = "f"
		ordering = ('id_vz', 'reihung', 'id_art',)
		default_permissions = ()


# --- 7 level tables ---
# language institutions
class tbl_sprache_institut(models.Model):
	id_institution	= models.ForeignKey('tbl_institutionen'																			, verbose_name="Institutionen pro Sprache")
	id_varietaet	= models.ForeignKey('tbl_varietaet'																				, verbose_name="Varietät")
	anz_schule		= models.IntegerField(blank=True, null=True																		, verbose_name="Anzahl von Schulen")
	def __str__(self):
		return "{}: {} mit {} Klassen".format(self.id_institution.id_ort, self.id_varietaet.variet_name, self.anz_schule)
	class Meta:
		db_table = "MioeDB_tbl_sprache_institut"
		verbose_name = "Institutionen pro Sprache"
		verbose_name_plural = "Institutionen pro Sprache"
		verbose_genus = "f"
		ordering = ('id_institution',)
		default_permissions = ()
