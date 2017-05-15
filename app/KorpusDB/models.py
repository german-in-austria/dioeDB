# -*- coding: utf-8 -*-
from django.db import models
from sortedm2m.fields import SortedManyToManyField

models.options.DEFAULT_NAMES +=('verbose_genus',) # m = maskulin, f = feminin, n = neutrum(default)

class tbl_antworten(models.Model):
	von_Inf				= models.ForeignKey('PersonenDB.tbl_personen'						, on_delete=models.CASCADE		, verbose_name="von Person")
	zu_Aufgabe			= models.ForeignKey('tbl_aufgaben',			blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="zu Aufgabe")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	ist_am				= models.ForeignKey('tbl_antwortmoeglichkeiten',	blank=True, null=True, on_delete=models.SET_NULL	, verbose_name="Ist Antwortmöglichkeit")
	ist_gewaehlt		= models.BooleanField(default=False																	, verbose_name="Ist gewählt")
	ist_nat				= models.BooleanField(default=False																	, verbose_name="Ist NAT")
	ist_Satz			= models.ForeignKey('tbl_saetze',			blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Ist Satz")
	ist_bfl				= models.BooleanField(default=False																	, verbose_name="Ist BFL")
	bfl_durch_S			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="BFL durch S")
	start_Antwort		= models.DurationField(																				  verbose_name="Start Antwort")
	stop_Antwort		= models.DurationField(																				  verbose_name="Stop Antwort")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	def __str__(self):
		return "{}, {}".format(self.von_Inf,self.zu_Aufgabe)
	class Meta:
		verbose_name = "Antwort"
		verbose_name_plural = "Antworten"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()
		permissions = (('edit', 'Kann KorpusDB in DB bearbeiten'),('antworten_maskView', 'Kann Maskeneingaben einsehen'),('antworten_maskAdd', 'Kann Maskeneingaben hinzufuegen'),('antworten_maskEdit', 'Kann Maskeneingaben bearbeiten'),)

class tbl_antwortmoeglichkeiten(models.Model):
	zu_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="zu_Aufgabe")
	Kuerzel				= models.CharField(max_length=255																	, verbose_name="Kürzel")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	frei				= models.BooleanField(default=False																	, verbose_name="Frei")
	def __str__(self):
		return "{}, {}".format(self.Kuerzel,self.zu_Aufgabe)
	class Meta:
		verbose_name = "Antwortmöglichkeit"
		verbose_name_plural = "Antwortmöglichkeiten"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_saetze(models.Model):
	Transkript			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Transkript")
	Standardorth		= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Standardorth")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	def __str__(self):
		return "{}, {} ({})".format(self.Transkript,self.Standardorth,self.Kommentar)
	class Meta:
		verbose_name = "Satz"
		verbose_name_plural = "Sätze"
		verbose_genus = "m"
		ordering = ('Transkript',)
		default_permissions = ()

class tbl_antwortentags(models.Model):
	id_Antwort			= models.ForeignKey('tbl_antworten'									, on_delete=models.CASCADE		, verbose_name="ID zu Antwort")
	id_Tag				= models.ForeignKey('tbl_tags'										, on_delete=models.CASCADE		, verbose_name="ID zu Tag")
	id_TagEbene			= models.ForeignKey('tbl_tagebene',			blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="ID zu Tag Ebene")
	Gruppe				= models.IntegerField(						blank=True, null=True									, verbose_name="Gruppe")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	def __str__(self):
		return "{}<->{}".format(self.id_Antwort,self.id_Tag)
	class Meta:
		verbose_name = "Antworten Tag"
		verbose_name_plural = "Antworten Tags"
		verbose_genus = "m"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_tagebene(models.Model):
	Name				= models.CharField(max_length=255																	, verbose_name="Name")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	def __str__(self):
		return "{}".format(self.Name)
	class Meta:
		verbose_name = "Tag Ebene"
		verbose_name_plural = "Tag Ebenen"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_tagebenezutag(models.Model):
	id_TagEbene			= models.ForeignKey('tbl_tagebene'									, on_delete=models.CASCADE		, verbose_name="ID zu Tag Ebene")
	id_Tag				= models.ForeignKey('tbl_tags'										, on_delete=models.CASCADE		, verbose_name="ID zu Tag")
	def __str__(self):
		return "{} <- {}".format(self.id_TagEbene,self.id_Tag)
	class Meta:
		verbose_name = "Tag Ebene zu Tag"
		verbose_name_plural = "Tag Ebenen zu Tags"
		verbose_genus = "f"
		ordering = ('id_TagEbene',)
		default_permissions = ()

class tbl_tags(models.Model):
	Tag					= models.CharField(max_length=255																	, verbose_name="Tag")
	Tag_lang			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Tag lang")
	zu_Phaenomen		= models.ForeignKey('tbl_phaenomene',		blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Zu Phänomen")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	AReihung			= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	Generation			= models.IntegerField(choices=[(i, i) for i in range(0, 10)], blank=True, null=True					, verbose_name="Generation")
	def __str__(self):
		return "{}".format(self.Tag)
	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
		verbose_genus = "m"
		ordering = ('AReihung',)
		default_permissions = ()
		permissions = (('tags_maskView', 'Kann Maskeneingaben einsehen'),('tags_maskAdd', 'Kann Maskeneingaben hinzufuegen'),('tags_maskEdit', 'Kann Maskeneingaben bearbeiten'),)

class tbl_tagfamilie(models.Model):
	id_ParentTag		= models.ForeignKey('tbl_tags', related_name='id_ParentTag'			, on_delete=models.CASCADE		, verbose_name="Parent ID zu Tag")
	id_ChildTag			= models.ForeignKey('tbl_tags', related_name='id_ChildTag'			, on_delete=models.CASCADE		, verbose_name="Child ID zu Tag")
	def __str__(self):
		return "{} <- {}".format(self.id_ParentTag,self.id_ChildTag)
	class Meta:
		verbose_name = "Tag Familie"
		verbose_name_plural = "Tag Familien"
		verbose_genus = "f"
		ordering = ('id_ParentTag',)
		default_permissions = ()

class tbl_phaenomene(models.Model):
	Bez_Phaenomen		= models.CharField(max_length=511																	, verbose_name="Bezeichnung Phänomen")
	Beschr_Phaenomen	= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Beschreibung Phänomen")
	zu_PhaenBer			= models.IntegerField(						blank=True, null=True									, verbose_name="Zu Phänomenen Ber")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	def __str__(self):
		return "{}".format(self.Bez_Phaenomen)
	class Meta:
		verbose_name = "Phänomen"
		verbose_name_plural = "Phänomene"
		verbose_genus = "n"
		ordering = ('Bez_Phaenomen',)
		default_permissions = ()

class tbl_inferhebung(models.Model):
	ID_Erh				= models.ForeignKey('tbl_erhebungen'								, on_delete=models.CASCADE		, verbose_name="ID Erhebung")
	ID_Inf				= models.ForeignKey('PersonenDB.tbl_personen'						, on_delete=models.CASCADE		, verbose_name="ID Person")
	Datum				= models.DateField(																					  verbose_name="Datum")
	Explorator			= models.IntegerField(																				  verbose_name="Explorator")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	Dateipfad			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Verzeichniss für Dateien")
	Audiofile			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Audiofile")
	Logfile				= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Logfile")
	Ort					= models.ForeignKey('PersonenDB.tbl_orte',	blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Ort")
	Besonderheiten		= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Besonderheiten")
	def __str__(self):
		return "{} {}<->{}".format(self.Datum,self.ID_Erh,self.ID_Inf)
	class Meta:
		verbose_name = "InfErhebung"
		verbose_name_plural = "InfErhebungen"
		verbose_genus = "f"
		ordering = ('Datum',)
		default_permissions = ()

class tbl_erhinfaufgaben(models.Model):
	id_InfErh			= models.ForeignKey('tbl_inferhebung'								, on_delete=models.CASCADE		, verbose_name="ID InfErhebung")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="ID Aufgaben")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	start_Aufgabe		= models.DurationField(																				  verbose_name="Start Aufgabe")
	stop_Aufgabe		= models.DurationField(																				  verbose_name="Stop Aufgabe")
	first_click			= models.DurationField(																				  verbose_name="First Click")
	def __str__(self):
		return "{}<->{}".format(self.id_InfErh,self.id_Aufgabe)
	class Meta:
		verbose_name = "ErhInfAufgabe"
		verbose_name_plural = "ErhInfAufgaben"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_erhebungen(models.Model):
	Art_Erhebung		= models.IntegerField(						blank=True, null=True									, verbose_name="Art der Erhebung")
	Bezeichnung_Erhebung= models.CharField(max_length=511																	, verbose_name="Bezeichnung der Erhebung")
	Zeitraum			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Zeitraum")
	Konzept_von			= models.IntegerField(						blank=True, null=True									, verbose_name="Konzept von")
	def __str__(self):
		return "{}".format(self.Bezeichnung_Erhebung)
	class Meta:
		verbose_name = "Erhebung"
		verbose_name_plural = "Erhebungen"
		verbose_genus = "f"
		ordering = ('Bezeichnung_Erhebung',)
		default_permissions = ()

class tbl_erhebung_mit_aufgaben(models.Model):
	id_Erh				= models.ForeignKey('tbl_erhebungen'								, on_delete=models.CASCADE		, verbose_name="von Erhebung")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben',			blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="zu Aufgabe")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	ist_randomisiert	= models.BooleanField(default=False																	, verbose_name="Ist Randomisiert")
	def __str__(self):
		return "{}<->{}".format(self.id_Erh,self.id_Aufgabe)
	class Meta:
		verbose_name = "Erhebung mit Aufgaben"
		verbose_name_plural = "Erhebungen mit Aufgaben"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_aufgaben(models.Model):
	von_ASet			= models.ForeignKey('tbl_aufgabensets'								, on_delete=models.CASCADE		, verbose_name="von Aufgabenset")
	Variante			= models.IntegerField(																				  verbose_name="Variante")
	ist_dialekt			= models.BooleanField(default=False																	, verbose_name="Ist Dialekt")
	Beschreibung_Aufgabe= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Beschreibung Aufgabe")
	def __str__(self):
		return "{} - {} ({})".format(self.Variante,self.Beschreibung_Aufgabe,self.von_ASet)
	class Meta:
		verbose_name = "Aufgabe"
		verbose_name_plural = "Aufgaben"
		verbose_genus = "f"
		ordering = ('von_ASet',)
		default_permissions = ()

class tbl_aufgabensets(models.Model):
	Kuerzel				= models.CharField(max_length=255																	, verbose_name="Kürzel")
	Name_Aset			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Name Aufgabenset")
	Fokus				= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Fokus")
	zu_Phaenomen		= models.ForeignKey('tbl_phaenomene',		blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Zu Phänomen")
	Art_ASet			= models.IntegerField(						blank=True, null=True									, verbose_name="Art Aufgabenset")
	zusammengestellt_als= models.ForeignKey('tbl_aufgabenzusammenstellungen',blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Zusammengestellt als")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	def __str__(self):
		return "{} ({})".format(self.Kuerzel,self.Art_ASet)
	class Meta:
		verbose_name = "Aufgabenset"
		verbose_name_plural = "Aufgabensets"
		verbose_genus = "n"
		ordering = ('Kuerzel',)
		default_permissions = ()
		permissions = (('aufgabensets_maskView', 'Kann Maskeneingaben einsehen'),('aufgabensets_maskAdd', 'Kann Maskeneingaben hinzufuegen'),('aufgabensets_maskEdit', 'Kann Maskeneingaben bearbeiten'),)

class tbl_aufgabenzusammenstellungen(models.Model):
	Bezeichnung_AZus	= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Bezeichnung")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	AZusCol				= models.CharField(max_length=255,			blank=True, null=True									, verbose_name="AZus Col")
	def __str__(self):
		return "{} ({})".format(self.Bezeichnung_AZus,self.AZusCol)
	class Meta:
		verbose_name = "Aufgabenzusammenstellung"
		verbose_name_plural = "Aufgabenzusammenstellungen"
		verbose_genus = "f"
		ordering = ('Bezeichnung_AZus',)
		default_permissions = ()

class tbl_azusbeinhaltetmedien(models.Model):
	id_AZus				= models.ForeignKey('tbl_aufgabenzusammenstellungen'				, on_delete=models.CASCADE		, verbose_name="von AZus")
	id_Mediatyp			= models.ForeignKey('tbl_mediatypen'								, on_delete=models.CASCADE		, verbose_name="von Mediatyp")
	Reihung				= models.CharField(max_length=255,																	  verbose_name="Reihung")
	def __str__(self):
		return "{}<->{}".format(self.id_AZus,self.id_Mediatyp)
	class Meta:
		verbose_name = "AZusBeinhaltetMedien"
		verbose_name_plural = "AZusBeinhaltetMedien"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_aufgabenfiles(models.Model):
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="von Aufgabe")
	id_Mediatyp			= models.ForeignKey('tbl_mediatypen'								, on_delete=models.CASCADE		, verbose_name="von Mediatyp")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	ist_Anweisung		= models.BooleanField(default=False																	, verbose_name="Ist Anweisung")
	File_Link			= models.CharField(max_length=255,																	  verbose_name="File Link")
	Kommentar			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Kommentar")
	def __str__(self):
		return "{}<->{}".format(self.id_Aufgabe,self.id_Mediatyp)
	class Meta:
		verbose_name = "Aufgabenfile"
		verbose_name_plural = "Aufgabenfiles"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class tbl_mediatypen(models.Model):
	Bezeichnung			= models.CharField(max_length=255																	, verbose_name="Bezeichnung")
	Filetypes			= models.CharField(max_length=511,			blank=True, null=True									, verbose_name="Filetypes")
	def __str__(self):
		return "{} ({})".format(self.Bezeichnung,self.Filetypes)
	class Meta:
		verbose_name = "Mediatyp"
		verbose_name_plural = "Mediatypen"
		verbose_genus = "m"
		ordering = ('Bezeichnung',)
		default_permissions = ()

class sys_presettags(models.Model):
	id_Tags				= SortedManyToManyField('tbl_tags'							                                  		, verbose_name="IDs zu Tag")
	Reihung				= models.IntegerField(						blank=True, null=True									, verbose_name="Reihung")
	def __str__(self):
		return "{}. {}".format(self.Reihung,", ".join(p.Tag for p in self.id_Tags.all()))
	class Meta:
		verbose_name = "Preset Tags"
		verbose_name_plural = "Presets Tags"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()

class sys_presettagszuaufgabe(models.Model):
	id_PresetTags		= models.ForeignKey('sys_presettags'								, on_delete=models.CASCADE		, verbose_name="ID zu PresetTags")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="ID Aufgaben")
	def __str__(self):
		return "{} <- {}".format(self.id_Aufgabe,self.id_PresetTags)
	class Meta:
		verbose_name = "Preset Tags zu Aufgabe"
		verbose_name_plural = "Presets Tags zu Aufgaben"
		verbose_genus = "m"
		ordering = ('id_Aufgabe',)
		default_permissions = ()
