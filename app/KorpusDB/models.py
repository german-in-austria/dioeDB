# -*- coding: utf-8 -*-
from django.db import models

models.options.DEFAULT_NAMES += ('verbose_genus',)  # m = maskulin, f = feminin, n = neutrum(default)
models.options.DEFAULT_NAMES += ('kategorienListeFilter', 'kategorienListeFXData',)  # Zusätzliche "data-fx-"-Felder für Filter
models.options.DEFAULT_NAMES += ('ipa',)  # Liste der Felder mit IPA Auswahlfeld


class tbl_antworten(models.Model):
	von_Inf				= models.ForeignKey('PersonenDB.tbl_informanten'					, on_delete=models.CASCADE		, verbose_name="von Person")
	zu_Aufgabe			= models.ForeignKey('tbl_aufgaben'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="zu Aufgabe")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	ist_am				= models.ForeignKey('tbl_antwortmoeglichkeiten', blank=True, null=True, on_delete=models.SET_NULL	, verbose_name="Ist Antwortmöglichkeit")
	ist_gewaehlt		= models.BooleanField(default=False																	, verbose_name="Ist gewählt")
	ist_nat				= models.BooleanField(default=False																	, verbose_name="Ist NAT")
	ist_Satz			= models.ForeignKey('tbl_saetze'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Ist Satz")
	ist_bfl				= models.BooleanField(default=False																	, verbose_name="Ist BFL")
	ist_token			= models.ForeignKey('AnnotationsDB.tbl_token'	, blank=True, null=True	, on_delete=models.SET_NULL	, verbose_name="Ist Token")
	ist_tokenset		= models.ForeignKey('AnnotationsDB.tbl_tokenset', blank=True, null=True	, on_delete=models.SET_NULL	, verbose_name="Ist Tokenset")
	bfl_durch_S			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="BFL durch S")
	start_Antwort		= models.DurationField(																				  verbose_name="Start Antwort")
	stop_Antwort		= models.DurationField(																				  verbose_name="Stop Antwort")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")
	kontrolliert		= models.BooleanField(default=False																	, verbose_name="kontrolliert")
	veroeffentlichung	= models.BooleanField(default=False																	, verbose_name="veröffentlichung")

	def check_am_fest_tags(self):
		at_count = self.tbl_antwortentags_set.count()
		if not self.ist_gewaehlt:
			return at_count == 0
		else:
			amt_count = self.ist_am.tbl_amtags_set.count()
			if amt_count == 0:		# Vorgegebene Tags nicht vorhanden
				return at_count == 0		# Antworten Tags nicht vorhanden
			else:		# Vorgegebene Tags vorhanden
				if amt_count != at_count:		# Anzahl stimmt nicht überein
					return False
				else:		# Anzahl stimmt überein
					return ';'.join([','.join([str(v.id_Tag_id), str(v.id_TagEbene_id), str(v.Gruppe), str(v.Reihung)]) for v in self.ist_am.tbl_amtags_set.all()]) == ';'.join([','.join([str(v.id_Tag_id), str(v.id_TagEbene_id), str(v.Gruppe), str(v.Reihung)]) for v in self.ist_am.tbl_antwortentags_set.all()])		# Stimmen die Tags überein?
			return False

	def __str__(self):
		return "{}, {}".format(self.von_Inf, self.zu_Aufgabe)

	class Meta:
		verbose_name = "Antwort"
		verbose_name_plural = "Antworten"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()
		permissions = (('edit', 'Kann KorpusDB in DB bearbeiten'), ('auswertung', 'Kann KorpusDB auswerten'), ('antworten_maskView', 'Kann Maskeneingaben einsehen'), ('antworten_maskAdd', 'Kann Maskeneingaben hinzufuegen'), ('antworten_maskEdit', 'Kann Maskeneingaben bearbeiten'),)


class tbl_antwortmoeglichkeiten(models.Model):
	zu_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="zu_Aufgabe")
	Kuerzel				= models.CharField(max_length=255																	, verbose_name="Kürzel")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	frei				= models.BooleanField(default=False																	, verbose_name="Frei")
	vorg_satz_sd		= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Vorgegebener Satz Standarddeutsch")

	def __str__(self):
		return "{}, {}".format(self.Kuerzel, self.zu_Aufgabe)

	class Meta:
		verbose_name = "Antwortmöglichkeit"
		verbose_name_plural = "Antwortmöglichkeiten"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()


class tbl_amtags(models.Model):
	id_am				= models.ForeignKey('tbl_antwortmoeglichkeiten'						, on_delete=models.CASCADE		, verbose_name="ID zu Antwortmöglichkeit")
	id_Tag				= models.ForeignKey('tbl_tags'										, on_delete=models.CASCADE		, verbose_name="ID zu Tag")
	id_TagEbene			= models.ForeignKey('tbl_tagebene'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="ID zu Tag Ebene")
	Gruppe				= models.IntegerField(						  blank=True, null=True									, verbose_name="Gruppe")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")

	def __str__(self):
		return "{}<->{}".format(self.id_am, self.id_Tag)

	class Meta:
		verbose_name = "Antwortmöglichkeit Tag"
		verbose_name_plural = "Antwortmöglichkeit Tags"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()


class tbl_saetze(models.Model):
	Transkript			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Transkript")
	Standardorth		= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Standardorth")
	ipa					= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="IPA-Transkript")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{}, {} ({})".format(self.Transkript, self.Standardorth, self.Kommentar)

	class Meta:
		verbose_name = "Satz"
		verbose_name_plural = "Sätze"
		verbose_genus = "m"
		ipa = ['ipa']
		ordering = ('Transkript',)
		default_permissions = ()


class tbl_antwortentags(models.Model):
	id_Antwort			= models.ForeignKey('tbl_antworten'									, on_delete=models.CASCADE		, verbose_name="ID zu Antwort")
	id_Tag				= models.ForeignKey('tbl_tags'										, on_delete=models.CASCADE		, verbose_name="ID zu Tag")
	id_TagEbene			= models.ForeignKey('tbl_tagebene'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="ID zu Tag Ebene")
	Gruppe				= models.IntegerField(						  blank=True, null=True									, verbose_name="Gruppe")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")

	def __str__(self):
		return "{}<->{}".format(self.id_Antwort, self.id_Tag)

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
		return "{} <- {}".format(self.id_TagEbene, self.id_Tag)

	class Meta:
		verbose_name = "Tag Ebene zu Tag"
		verbose_name_plural = "Tag Ebenen zu Tags"
		verbose_genus = "f"
		ordering = ('id_TagEbene',)
		default_permissions = ()


class tbl_tags(models.Model):
	Tag					= models.CharField(max_length=255																	, verbose_name="Tag")
	Tag_lang			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Tag lang")
	zu_Phaenomen		= models.ForeignKey('tbl_phaenomene'		, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Zu Phänomen")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")
	AReihung			= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	Generation			= models.IntegerField(choices=[(i, i) for i in range(0, 10)], blank=True, null=True					, verbose_name="Generation")

	def __str__(self):
		return "{}".format(self.Tag)

	def kategorienListeFX(amodel, suche, inhalt, mitInhalt, arequest, ausgabe):
		from django.shortcuts import render_to_response
		from django.template import RequestContext
		from DB.funktionenDB import kategorienListe
		if not inhalt:
			aElement = amodel.objects.all()
			ausgabe['tagsAll'] = {'count': aElement.count(), 'title': 'TAGS - Alle', 'enthaelt': 1}
			if mitInhalt > 0:
				ausgabe['tagsAll']['active'] = render_to_response('DB/lmfadl.html', RequestContext(arequest, {'lmfadl': kategorienListe(amodel, inhalt='tagsAll'), 'openpk': mitInhalt, 'scrollto': mitInhalt}),).content
			aElement = amodel.objects.filter(id_ChildTag=None).exclude(id_ParentTag=None)
			ausgabe['tagsParentsWithChilds'] = {'count': aElement.count(), 'title': 'TAGS - Eltern mit Kindern'}
			aElement = amodel.objects.exclude(id_ChildTag=None).exclude(id_ParentTag=None)
			ausgabe['tagsChildsWithChilds'] = {'count': aElement.count(), 'title': 'TAGS - Kinder mit Kindern'}
			aElement = amodel.objects.filter(id_ParentTag=None).exclude(id_ChildTag=None)
			ausgabe['tagsChildsWithoutChilds'] = {'count': aElement.count(), 'title': 'TAGS - Kinder ohne Kinder'}
			aElement = amodel.objects.filter(id_ChildTag=None, id_ParentTag=None)
			ausgabe['tagsStandalone'] = {'count': aElement.count(), 'title': 'TAGS - Einzelgänger'}
			return ausgabe
		else:
			if inhalt == 'tagsParentsWithChilds':
				return [{'model': aM, 'title': str(aM) + ((' (' + str(aM.Tag_lang) + ')') if aM.Tag_lang else '')} for aM in amodel.objects.filter(id_ChildTag=None).exclude(id_ParentTag=None).order_by('Tag')]
			if inhalt == 'tagsChildsWithChilds':
				return [{'model': aM, 'title': str(aM) + ((' (' + str(aM.Tag_lang) + ')') if aM.Tag_lang else '')} for aM in amodel.objects.exclude(id_ChildTag=None).exclude(id_ParentTag=None).order_by('Tag')]
			if inhalt == 'tagsChildsWithoutChilds':
				return [{'model': aM, 'title': str(aM) + ((' (' + str(aM.Tag_lang) + ')') if aM.Tag_lang else '')} for aM in amodel.objects.filter(id_ParentTag=None).exclude(id_ChildTag=None).order_by('Tag')]
			if inhalt == 'tagsStandalone':
				return [{'model': aM, 'title': str(aM) + ((' (' + str(aM.Tag_lang) + ')') if aM.Tag_lang else '')} for aM in amodel.objects.filter(id_ChildTag=None, id_ParentTag=None).order_by('Tag')]
			return [{'model': aM, 'title': str(aM) + ((' <span style="font-size:13px;">(' + str(aM.Tag_lang) + ')</span>') if aM.Tag_lang else '')} for aM in amodel.objects.all().order_by('Tag')]

	def meta(self):
		return self._meta

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
		verbose_genus = "m"
		kategorienListeFXData = {'zu_phaenomen': 'zu_Phaenomen__pk'}
		kategorienListeFilter = [{'titel': 'Phänomen', 'config': {'type': 'select', 'options': [
			{'title': 'Alle', 'val': 'None'},
			{'title': '!Bez_Phaenomen', 'val': 'zu_phaenomen==!pk', 'app': 'KorpusDB', 'table': 'tbl_phaenomene'},
			{'title': 'Ohne Phänomen', 'val': 'zu_phaenomen<1'},
		]}}]
		ordering = ('AReihung',)
		default_permissions = ()
		permissions = (('tags_maskView', 'Kann Maskeneingaben einsehen'), ('tags_maskAdd', 'Kann Maskeneingaben hinzufuegen'), ('tags_maskEdit', 'Kann Maskeneingaben bearbeiten'),)


class tbl_tagfamilie(models.Model):
	id_ParentTag		= models.ForeignKey('tbl_tags', related_name='id_ParentTag'			, on_delete=models.CASCADE		, verbose_name="Parent ID zu Tag")
	id_ChildTag			= models.ForeignKey('tbl_tags', related_name='id_ChildTag'			, on_delete=models.CASCADE		, verbose_name="Child ID zu Tag")

	def __str__(self):
		return "{} <- {}".format(self.id_ParentTag, self.id_ChildTag)

	class Meta:
		verbose_name = "Tag Familie"
		verbose_name_plural = "Tag Familien"
		verbose_genus = "f"
		ordering = ('id_ParentTag',)
		default_permissions = ()


class tbl_phaenber(models.Model):
	Bez_Phaenber		= models.CharField(max_length=511																	, verbose_name="Bezeichnung Phänomen")
	Beschr_Phaenber		= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Beschreibung Phänomen")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{}".format(self.Bez_Phaenber)

	class Meta:
		verbose_name = "Phänomen Bereich"
		verbose_name_plural = "Phänomen Bereiche"
		verbose_genus = "n"
		ordering = ('Bez_Phaenber',)
		default_permissions = ()


class tbl_phaenomene(models.Model):
	Bez_Phaenomen		= models.CharField(max_length=511																	, verbose_name="Bezeichnung Phänomen")
	Beschr_Phaenomen	= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Beschreibung Phänomen")
	zu_PhaenBer			= models.ForeignKey('tbl_phaenber'			, blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Zu Phänomenen Ber")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{}".format(self.Bez_Phaenomen)

	class Meta:
		verbose_name = "Phänomen"
		verbose_name_plural = "Phänomene"
		verbose_genus = "n"
		ordering = ('Bez_Phaenomen',)
		default_permissions = ()


class tbl_phaenzuaufgabe(models.Model):
	id_phaenomen		= models.ForeignKey('tbl_phaenomene'								, on_delete=models.CASCADE		, verbose_name="Phänomen ID")
	id_aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="Aufgaben ID")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{} <- {}".format(self.id_phaenomen, self.id_aufgabe)

	class Meta:
		verbose_name = "Phänomen zu Aufgabe"
		verbose_name_plural = "Phänomen zu Aufgaben"
		verbose_genus = "n"
		ordering = ('id_phaenomen',)
		default_permissions = ()


class tbl_inferhebung(models.Model):
	ID_Erh				= models.ForeignKey('tbl_erhebungen'								, on_delete=models.CASCADE		, verbose_name="ID Erhebung")
	id_Transcript		= models.ForeignKey('AnnotationsDB.tbl_transcript', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="ID Transkript")
	ID_Inf				= models.ForeignKey('PersonenDB.tbl_informanten'					, on_delete=models.CASCADE		, verbose_name="ID Informaten")
	# ID_Inf kann später ggf. weg
	Datum				= models.DateField(																					  verbose_name="Datum")
	Explorator			= models.ForeignKey('PersonenDB.tbl_mitarbeiter', blank=True, null=True, on_delete=models.SET_NULL	, verbose_name="Explorator")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")
	Dateipfad			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Verzeichnis für Dateien")
	Audiofile			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Audiofile")
	time_beep			= models.DurationField(						  blank=True, null=True									, verbose_name="Time Beep")
	sync_time			= models.DurationField(						  blank=True, null=True									, verbose_name="Sync Time")
	Logfile				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Logfile")
	Ort					= models.ForeignKey('PersonenDB.tbl_orte'	, blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Ort")
	Besonderheiten		= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Besonderheiten")

	def __str__(self):
		return "{} {} <-> {}".format(self.Datum, ",".join([str(ize.ID_Inf) for ize in self.tbl_inf_zu_erhebung_set.all()]), self.ID_Erh)

	class Meta:
		verbose_name = "Einzel Erhebung"
		verbose_name_plural = "Einzel Erhebungen"
		verbose_genus = "f"
		ordering = ('ID_Inf',)
		default_permissions = ()


class tbl_inf_zu_erhebung(models.Model):
	ID_Inf				= models.ForeignKey('PersonenDB.tbl_informanten'				, on_delete=models.CASCADE		, verbose_name="Zu Informant")
	id_inferhebung		= models.ForeignKey('tbl_inferhebung'							, on_delete=models.CASCADE		, verbose_name="zu InfErhebung")

	def __str__(self):
		return "{}<->{}".format(self.ID_Inf, self.id_einzelerhebung)

	class Meta:
		verbose_name = "Informant zu Erhebung"
		verbose_name_plural = "Informanten zu Erhebungen"
		ordering = ('ID_Inf',)


class tbl_erhinfaufgaben(models.Model):
	id_InfErh			= models.ForeignKey('tbl_inferhebung'								, on_delete=models.CASCADE		, verbose_name="ID InfErhebung")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="ID Aufgaben")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	start_Aufgabe		= models.DurationField(																				  verbose_name="Start Aufgabe")
	stop_Aufgabe		= models.DurationField(																				  verbose_name="Stop Aufgabe")
	time_beep			= models.DurationField(						  blank=True, null=True									, verbose_name="Time Beep")
	sync_time			= models.DurationField(						  blank=True, null=True									, verbose_name="Sync Time")

	def __str__(self):
		return "{}<->{}".format(self.id_InfErh, self.id_Aufgabe)

	class Meta:
		verbose_name = "ErhInfAufgabe"
		verbose_name_plural = "ErhInfAufgaben"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()


class tbl_erhebungen(models.Model):
	Art_Erhebung		= models.ForeignKey('tbl_erhebungsarten'							, on_delete=models.CASCADE		, verbose_name="Art der Erhebung")
	Bezeichnung_Erhebung = models.CharField(max_length=511																	, verbose_name="Bezeichnung der Erhebung")
	Zeitraum			= models.CharField(max_length=511				, blank=True, null=True									, verbose_name="Zeitraum")
	Konzept_von			= models.ForeignKey('PersonenDB.tbl_mitarbeiter', blank=True, null=True	, on_delete=models.SET_NULL	, verbose_name="Konzept von")

	def __str__(self):
		return "{}".format(self.Bezeichnung_Erhebung)

	class Meta:
		verbose_name = "Erhebung"
		verbose_name_plural = "Erhebungen"
		verbose_genus = "f"
		ordering = ('Bezeichnung_Erhebung',)
		default_permissions = ()


class tbl_erhebungsarten(models.Model):
	Bezeichnung			= models.CharField(max_length=511																	, verbose_name="Bezeichnung der Erhebungsart")
	standardisiert		= models.BooleanField(default=False																	, verbose_name="Standardisiert")

	def __str__(self):
		return "{}".format(self.Bezeichnung)

	class Meta:
		verbose_name = "Erhebungsart"
		verbose_name_plural = "Erhebungsarten"
		verbose_genus = "f"
		ordering = ('Bezeichnung',)
		default_permissions = ()


class tbl_erhebung_mit_aufgaben(models.Model):
	id_Erh				= models.ForeignKey('tbl_erhebungen'								, on_delete=models.CASCADE		, verbose_name="von Erhebung")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="zu Aufgabe")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	ist_randomisiert	= models.BooleanField(default=False																	, verbose_name="Ist Randomisiert")

	def __str__(self):
		return "{}<->{}".format(self.id_Erh, self.id_Aufgabe)

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
	Beschreibung_Aufgabe = models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Beschreibung Aufgabe")
	Kontext				= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Kontext")
	Aufgabenstellung	= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Aufgabenstellung")
	Ergsatz_anf			= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Ergsatz_anf")
	Ergsatz_end			= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Ergsatz_end")
	Puzzle_Woerter		= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="Puzzle_Woerter")
	Aufgabenart			= models.ForeignKey('tbl_aufgabenarten'		, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Aufgabenart")

	def status(self, useArtErhebung):
		try:
			aproz = tbl_antworten.objects.filter(zu_Aufgabe=self.pk, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).values('zu_Aufgabe').annotate(total=models.Count('von_Inf'))[0]['total']
		except:
			aproz = 0
		try:
			atags = (100 / tbl_antworten.objects.filter(zu_Aufgabe=self.pk, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).values('pk').annotate(total=models.Count('von_Inf')).count() * tbl_antworten.objects.filter(zu_Aufgabe=self.pk).exclude(tbl_antwortentags=None).values('pk').annotate(total=models.Count('von_Inf')).count())
		except:
			atags = 0
		try:
			aqtags = tbl_antworten.objects.filter(zu_Aufgabe=self.pk, tbl_antwortentags__id_Tag_id=35, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).values('pk').annotate(total=models.Count('von_Inf')).count()
		except:
			aqtags = 0
		return [aproz, atags, aqtags]

	def __str__(self):
		return "{} - {} ({})".format(self.Variante, self.Beschreibung_Aufgabe, self.von_ASet)

	class Meta:
		verbose_name = "Aufgabe"
		verbose_name_plural = "Aufgaben"
		verbose_genus = "f"
		ordering = ('von_ASet',)
		default_permissions = ()


class tbl_aufgabenarten(models.Model):
	Bezeichnung			= models.CharField(max_length=255																	, verbose_name="Bezeichnung")

	def __str__(self):
		return "{}".format(self.Bezeichnung)

	class Meta:
		verbose_name = "Aufgabenart"
		verbose_name_plural = "Aufgabenarten"
		verbose_genus = "f"
		ordering = ('Bezeichnung',)
		default_permissions = ()


class tbl_aufgabensets(models.Model):
	Kuerzel				= models.CharField(max_length=255																	, verbose_name="Kürzel")
	Name_Aset			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Name Aufgabenset")
	Fokus				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Fokus")
	zu_Phaenomen		= models.ForeignKey('tbl_phaenomene'		, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Zu Phänomen")
	Art_ASet			= models.IntegerField(						  blank=True, null=True									, verbose_name="Art Aufgabenset")
	zusammengestellt_als = models.ForeignKey('tbl_aufgabenzusammenstellungen', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Zusammengestellt als")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return self.Kuerzel + (' (' + str(self.Art_ASet) + ')' if self.Art_ASet else '')

	class Meta:
		verbose_name = "Aufgabenset"
		verbose_name_plural = "Aufgabensets"
		verbose_genus = "n"
		ordering = ('Kuerzel',)
		default_permissions = ()
		permissions = (('aufgabensets_maskView', 'Kann Maskeneingaben einsehen'), ('aufgabensets_maskAdd', 'Kann Maskeneingaben hinzufuegen'), ('aufgabensets_maskEdit', 'Kann Maskeneingaben bearbeiten'),)


class tbl_aufgabenzusammenstellungen(models.Model):
	Bezeichnung_AZus	= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Bezeichnung")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")
	AZusCol				= models.CharField(max_length=255			, blank=True, null=True									, verbose_name="AZus Col")

	def __str__(self):
		return "{} ({})".format(self.Bezeichnung_AZus, self.AZusCol)

	class Meta:
		verbose_name = "Aufgabenzusammenstellung"
		verbose_name_plural = "Aufgabenzusammenstellungen"
		verbose_genus = "f"
		ordering = ('Bezeichnung_AZus',)
		default_permissions = ()


class tbl_azusbeinhaltetmedien(models.Model):
	id_AZus				= models.ForeignKey('tbl_aufgabenzusammenstellungen'				, on_delete=models.CASCADE		, verbose_name="von AZus")
	id_Mediatyp			= models.ForeignKey('tbl_mediatypen'								, on_delete=models.CASCADE		, verbose_name="von Mediatyp")
	Reihung				= models.CharField(max_length=255																	, verbose_name="Reihung")

	def __str__(self):
		return "{}<->{}".format(self.id_AZus, self.id_Mediatyp)

	class Meta:
		verbose_name = "AZusBeinhaltetMedien"
		verbose_name_plural = "AZusBeinhaltetMedien"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()


class tbl_aufgabenfiles(models.Model):
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="von Aufgabe")
	id_Mediatyp			= models.ForeignKey('tbl_mediatypen'								, on_delete=models.CASCADE		, verbose_name="von Mediatyp")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	ist_Anweisung		= models.BooleanField(default=False																	, verbose_name="Ist Anweisung")
	File_Link			= models.CharField(max_length=255																	, verbose_name="File Link")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{}<->{}".format(self.id_Aufgabe, self.id_Mediatyp)

	class Meta:
		verbose_name = "Aufgabenfile"
		verbose_name_plural = "Aufgabenfiles"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()


class tbl_mediatypen(models.Model):
	Bezeichnung			= models.CharField(max_length=255																	, verbose_name="Bezeichnung")
	Filetypes			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Filetypes")

	def __str__(self):
		return "{} ({})".format(self.Bezeichnung, self.Filetypes)

	class Meta:
		verbose_name = "Mediatyp"
		verbose_name_plural = "Mediatypen"
		verbose_genus = "m"
		ordering = ('Bezeichnung',)
		default_permissions = ()


class sys_presettags(models.Model):
	Bezeichnung			= models.CharField(max_length=255																	, verbose_name="Bezeichnung")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")
	Kommentar			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Kommentar")

	def __str__(self):
		return "{} ({})".format(self.Bezeichnung, self.Kommentar)

	def kategorienListeFX(amodel, suche, inhalt, mitInhalt, arequest, ausgabe):
		from django.shortcuts import render_to_response
		from django.template import RequestContext
		from DB.funktionenDB import kategorienListe
		if not inhalt:
			aElement = amodel.objects.all()
			ausgabe['presettagsAll'] = {'count': aElement.count(), 'title': 'Presets Tags - Alle', 'enthaelt': 1}
			if mitInhalt > 0:
				ausgabe['presettagsAll']['active'] = render_to_response(
					'DB/lmfadl.html',
					RequestContext(arequest, {'lmfadl': kategorienListe(amodel, inhalt='tagsAll'), 'openpk': mitInhalt, 'scrollto': mitInhalt}),).content
			aElement = amodel.objects.filter(sys_tagebenezupresettags=None, sys_presettagszuaufgabe=None)
			ausgabe['presettagsAllWithoutFilter'] = {'count': aElement.count(), 'title': 'Presets Tags ohne Zuweisung'}
			for aEbenenPreset in amodel.objects.exclude(sys_tagebenezupresettags=None).values('sys_tagebenezupresettags__id_TagEbene'):
				ausgabe['presettagsEbene' + str(aEbenenPreset['sys_tagebenezupresettags__id_TagEbene'])] = {'count': amodel.objects.filter(sys_tagebenezupresettags__id_TagEbene=int(aEbenenPreset['sys_tagebenezupresettags__id_TagEbene'])).count(), 'title': 'Ebene - ' + str(tbl_tagebene.objects.get(pk=aEbenenPreset['sys_tagebenezupresettags__id_TagEbene']))}
			print(amodel.objects.exclude(sys_presettagszuaufgabe=None).values('sys_presettagszuaufgabe__id_Aufgabe'))
			for aEbenenPreset in amodel.objects.exclude(sys_presettagszuaufgabe=None).values('sys_presettagszuaufgabe__id_Aufgabe'):
				ausgabe['presettagsAufgabe' + str(aEbenenPreset['sys_presettagszuaufgabe__id_Aufgabe'])] = {'count': amodel.objects.filter(sys_presettagszuaufgabe__id_Aufgabe=int(aEbenenPreset['sys_presettagszuaufgabe__id_Aufgabe'])).count(), 'title': 'Aufgabe - ' + str(tbl_aufgaben.objects.get(pk=aEbenenPreset['sys_presettagszuaufgabe__id_Aufgabe']))}
			return ausgabe
		else:
			if inhalt == 'presettagsAllWithoutFilter':
				return [{'model': aM} for aM in amodel.objects.filter(sys_tagebenezupresettags=None, sys_presettagszuaufgabe=None)]
			if inhalt[:15] == 'presettagsEbene':
				return [{'model': aM} for aM in amodel.objects.filter(sys_tagebenezupresettags__id_TagEbene=int(inhalt[15:]))]
			if inhalt[:17] == 'presettagsAufgabe':
				return [{'model': aM} for aM in amodel.objects.filter(sys_presettagszuaufgabe__id_Aufgabe=int(inhalt[17:]))]
			return [{'model': aM} for aM in amodel.objects.all()]

	class Meta:
		verbose_name = "Preset Tags"
		verbose_name_plural = "Presets Tags"
		verbose_genus = "f"
		ordering = ('Reihung',)
		default_permissions = ()
		permissions = (('presettags_maskView', 'Kann Maskeneingaben einsehen'), ('presettags_maskAdd', 'Kann Maskeneingaben hinzufuegen'), ('presettags_maskEdit', 'Kann Maskeneingaben bearbeiten'),)


class sys_tagszupresettags(models.Model):
	id_PresetTags		= models.ForeignKey('sys_presettags'								, on_delete=models.CASCADE		, verbose_name="ID zu PresetTags")
	id_Tag				= models.ForeignKey('tbl_tags'										, on_delete=models.CASCADE		, verbose_name="ID zu Tag")
	Reihung				= models.IntegerField(						  blank=True, null=True									, verbose_name="Reihung")

	def __str__(self):
		return "{} <- {}".format(self.id_PresetTags, self.id_Tag)

	class Meta:
		verbose_name = "Tag zu Preset Tags"
		verbose_name_plural = "Tags zu Preset Tags"
		verbose_genus = "m"
		ordering = ('Reihung',)
		default_permissions = ()


class sys_tagebenezupresettags(models.Model):
	id_PresetTags		= models.ForeignKey('sys_presettags'								, on_delete=models.CASCADE		, verbose_name="ID zu PresetTags")
	id_TagEbene			= models.ForeignKey('tbl_tagebene'									, on_delete=models.CASCADE		, verbose_name="ID zu Tag Ebene")

	def __str__(self):
		return "{} <- {}".format(self.id_PresetTags, self.id_TagEbene)

	class Meta:
		verbose_name = "Tag Ebene zu Preset Tags"
		verbose_name_plural = "Tag Ebenen zu Preset Tags"
		verbose_genus = "f"
		ordering = ('id_TagEbene',)
		default_permissions = ()


class sys_presettagszuaufgabe(models.Model):
	id_PresetTags		= models.ForeignKey('sys_presettags'								, on_delete=models.CASCADE		, verbose_name="ID zu PresetTags")
	id_Aufgabe			= models.ForeignKey('tbl_aufgaben'									, on_delete=models.CASCADE		, verbose_name="ID Aufgaben")

	def __str__(self):
		return "{} <- {}".format(self.id_Aufgabe, self.id_PresetTags)

	class Meta:
		verbose_name = "Preset Tags zu Aufgabe"
		verbose_name_plural = "Presets Tags zu Aufgaben"
		verbose_genus = "f"
		ordering = ('id_Aufgabe',)
		default_permissions = ()
