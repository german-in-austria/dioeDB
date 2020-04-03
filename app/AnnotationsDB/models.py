from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db import transaction, connection
import datetime
import time


class event(models.Model):
	start_time			= models.DurationField(						  null=True, db_index=True								, verbose_name="Start Zeit")
	end_time			= models.DurationField(						  null=True												, verbose_name="End Zeit")
	layer				= models.IntegerField(						  null=True												, verbose_name="Layer")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")

	def __str__(self):
		return "{} - {} bis {}".format(self.layer, self.start_time, self.end_time)

	class Meta:
		db_table = "event"
		verbose_name = "Event"
		verbose_name_plural = "Events"
		ordering = ('start_time',)


class token(models.Model):
	text				= models.CharField(max_length=511			, db_index=True											, verbose_name="Das aktuelle Token")
	token_type_id		= models.ForeignKey('token_type'			, blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Token Type")
	ortho				= models.CharField(max_length=511			, blank=True, null=True, db_index=True					, verbose_name="Ortho")
	phon				= models.CharField(max_length=511			, blank=True, null=True, db_index=True					, verbose_name="phonetische Umschrift")
	ID_Inf				= models.ForeignKey('PersonenDB.tbl_informanten', blank=True, null=True	, on_delete=models.SET_NULL	, verbose_name="ID Informant")
	fragment_of			= models.ForeignKey('token', related_name='rn_token_fragment_of', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Fragment von")
	token_reihung		= models.IntegerField(						  null=True, db_index=True								, verbose_name="Token Reihung")
	event_id			= models.ForeignKey('event', related_name='rn_token_event_id', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Event ID")
	start_timepoint		= models.DurationField(						  null=True												, verbose_name="Start Zeitpunkt")
	end_timepoint		= models.DurationField(						  null=True												, verbose_name="End Zeitpunkt")
	transcript_id		= models.ForeignKey('transcript'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Transcript ID")
	likely_error		= models.BooleanField(default=False																	, verbose_name="Eventueller Fehler")
	sentence			= models.IntegerField(						  blank=True, null=True									, verbose_name="Sentence ID (delete!)")
	sentence_id			= models.ForeignKey('KorpusDB.tbl_saetze'	, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Sentence ID")
	sequence_in_sentence = models.IntegerField(						  null=True												, verbose_name="sequence_in_sentence")
	text_in_ortho		= models.TextField(							  blank=True, null=True									, verbose_name="Text in Ortho")
	lautg				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="lautgetreue Umschrift (delete!)")
	sonst				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="sonstige Umschrift (delete!)")
	transcomment		= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="kommentar zu Transkript (delete!)")
	ttpos				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="TreeTagger POS")
	ttlemma				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="TreeTagger Lemma")
	ttcheckword			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="TreeTagger Checkword")
	sppos				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy POS")
	sptag				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy Tag")
	splemma				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy Lemma")
	spdep				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy Dependency Relation")
	sphead				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy Dependency Relation")
	spenttype			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Spacy Named Entity Type")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")

	def __str__(self):
		return "\"{}\"".format(self.ortho)

	class Meta:
		db_table = "token"
		verbose_name = "Token"
		verbose_name_plural = "Tokens"
		ordering = ('sentence_id', 'token_reihung',)


class token_type(models.Model):
	token_type_name		= models.CharField(max_length=511																	, verbose_name="Token Typ Name")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")

	def __str__(self):
		return "{}".format(self.token_type_name)

	class Meta:
		db_table = "token_type"
		verbose_name = "Token Typ"
		verbose_name_plural = "Token Typen"
		ordering = ('id',)


class transcript(models.Model):
	name				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Name")
	update_time			= models.DateTimeField(auto_now_add=True															, verbose_name="Update Zeit")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")
	TIER_DATEN = (
		('text', 'text'),
		('ortho', 'ortho'),
		('phon', 'phon'),
	)
	default_tier		= models.CharField(max_length=511, choices=TIER_DATEN, blank=True, null=True						, verbose_name="default_tier")

	def __str__(self):
		return "{} ({})".format(self.name, self.update_time)

	class Meta:
		db_table = "transcript"
		verbose_name = "Transkript"
		verbose_name_plural = "Transkripte"
		ordering = ('name',)
		permissions = (
			('transcript_maskView', 'Kann Maskeneingaben einsehen'),
			('transcript_maskAdd', 'Kann Maskeneingaben hinzufuegen'),
			('transcript_maskEdit', 'Kann Maskeneingaben bearbeiten'),
			('transcript_auswertung_makeXLSX', 'Kann XLSX Datei auf Server erstellen'),
		)

class tbl_tier(models.Model):
	tier_name			= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Tier Name")
	transcript_id		= models.ForeignKey('transcript'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Transcript ID")

	def __str__(self):
		return "{} -> {}".format(self.tier_name, self.transcript_id)

	class Meta:
		db_table = "tier"
		verbose_name = "Tier"
		verbose_name_plural = "Tier"
		ordering = ('transcript_id',)


class tbl_event_tier(models.Model):
	event_id			= models.ForeignKey('event'					, blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Event ID")
	tier_id				= models.ForeignKey('tbl_tier'				, blank=True, null=True, on_delete=models.SET_NULL		, verbose_name="Tier ID")
	ID_Inf				= models.ForeignKey('PersonenDB.tbl_informanten', blank=True, null=True, on_delete=models.SET_NULL	, verbose_name="ID Informant")
	text				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="default_tier")

	def __str__(self):
		return "{} -> {} ({})".format(self.tier_id, self.event_id, self.ID_Inf)

	class Meta:
		db_table = "event_tier"
		verbose_name = "Event Tier"
		verbose_name_plural = "Event Tier"
		ordering = ('event_id',)


class tbl_tokenset(models.Model):
	id_von_token		= models.ForeignKey('token', related_name='rn_id_von_token', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Von Token ID")
	id_bis_token		= models.ForeignKey('token', related_name='rn_id_bis_token', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Bis Token ID")
	updated				= models.DateTimeField(auto_now=True																				, verbose_name="Letztes Änderung")

	def refreshCache():
		dg = 0
		for aTokenset in tbl_tokenset.objects.all():
			aTokenset.save()
			dg += 1
		return dg

	def save(self, *args, **kwargs):
		# tbl_tokentoset_cache aktuallisieren ...
		super().save(*args, **kwargs)
		tbl_tokentoset_cache.objects.filter(id_tokenset=self.pk).delete()
		if self.id_von_token and self.id_bis_token:
			if self.id_von_token.ID_Inf.pk != self.id_bis_token.ID_Inf.pk:
				raise Exception("self.id_von_token.ID_Inf.pk != self.id_bis_token.ID_Inf.pk")
			if self.id_von_token.transcript_id.pk != self.id_bis_token.transcript_id.pk:
				raise Exception("self.id_von_token.transcript_id.pk != self.id_bis_token.transcript_id.pk")
			if self.id_von_token.token_reihung > self.id_bis_token.token_reihung:
				(self.id_bis_token.token_reihung, self.id_von_token.token_reihung) = (self.id_von_token.token_reihung, self.id_bis_token.token_reihung)
			with transaction.atomic():
				for aToken in token.objects.values('pk').filter(ID_Inf=self.id_von_token.ID_Inf, transcript_id=self.id_von_token.transcript_id.pk, token_reihung__gte=self.id_von_token.token_reihung, token_reihung__lte=self.id_bis_token.token_reihung).order_by('token_reihung'):
					tbl_tokentoset_cache(id_tokenset=self, id_token_id=aToken['pk']).save()

	def __str__(self):
		return "{} - {}".format(self.id_von_token, self.id_bis_token)

	class Meta:
		db_table = "tokenset"
		verbose_name = "Token Set"
		verbose_name_plural = "Token Sets"
		ordering = ('updated',)


class tbl_tokentoset(models.Model):
	id_tokenset			= models.ForeignKey('tbl_tokenset'									, on_delete=models.CASCADE		, verbose_name="Tokenset")
	id_token			= models.ForeignKey('token'											, on_delete=models.CASCADE		, verbose_name="Token")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")

	def __str__(self):
		return "{} <- {}".format(self.id_tokenset, self.id_token)

	class Meta:
		db_table = "tokentoset"
		verbose_name = "Token to Token Set"
		verbose_name_plural = "Token to Token Sets"
		ordering = ('id_tokenset',)


class tbl_tokentoset_cache(models.Model):
	id_tokenset			= models.ForeignKey('tbl_tokenset'									, on_delete=models.CASCADE		, verbose_name="Tokenset")
	id_token			= models.ForeignKey('token'											, on_delete=models.CASCADE		, verbose_name="Token")
	updated				= models.DateTimeField(auto_now=True																, verbose_name="Letztes Änderung")

	def __str__(self):
		return "{} <- {}".format(self.id_tokenset, self.id_token)

	class Meta:
		db_table = "tokentoset_cache"
		verbose_name = "Token to Token Set Cache"
		verbose_name_plural = "Token to Token Sets Cache"
		ordering = ('id_tokenset',)


class mat_adhocsentences(models.Model):
	id					= models.AutoField(primary_key=True)
	adhoc_sentence		= models.BigIntegerField(					  null=True												, verbose_name="adhoc_sentence")
	tokenids			= ArrayField(models.IntegerField(			  null=True												, verbose_name="tokenids"))
	infid				= models.IntegerField(						  null=True												, verbose_name="infid")
	transid				= models.IntegerField(						  null=True												, verbose_name="transid")
	tokreih				= ArrayField(models.IntegerField(			  null=True												, verbose_name="tokreih"))
	seqsent				= ArrayField(models.IntegerField(			  null=True												, verbose_name="seqsent"))
	sentorig			= models.TextField(							  blank=True, null=True									, verbose_name="sentorig")
	sentorth			= models.TextField(							  blank=True, null=True									, verbose_name="sentorth")
	left_context		= models.TextField(							  blank=True, null=True									, verbose_name="left_context")
	senttext			= models.TextField(							  blank=True, null=True									, verbose_name="senttext")
	right_context		= models.TextField(							  blank=True, null=True									, verbose_name="right_context")
	sentttlemma			= models.TextField(							  blank=True, null=True									, verbose_name="sentttlemma")
	sentttpos			= models.TextField(							  blank=True, null=True									, verbose_name="sentttpos")
	sentsplemma			= models.TextField(							  blank=True, null=True									, verbose_name="sentsplemma")
	sentsppos			= models.TextField(							  blank=True, null=True									, verbose_name="sentsppos")
	sentsptag			= models.TextField(							  blank=True, null=True									, verbose_name="sentsptag")
	sentspdep			= models.TextField(							  blank=True, null=True									, verbose_name="sentspdep")
	sentspenttype		= models.TextField(							  blank=True, null=True									, verbose_name="sentspenttype")

	class Meta:
		db_table = "mat_adhocsentences"
		managed = False
		verbose_name = "mat_adhocsentences"
		verbose_name_plural = "mat_adhocsentences"
		ordering = ('adhoc_sentence',)


class tbl_refreshlog_mat_adhocsentences(models.Model):
	created_at			= models.DateTimeField(auto_now_add=True, db_index=True												, verbose_name="Erstellt")
	duration			= models.DurationField(																				  verbose_name="Dauer")

	def __str__(self):
		return "{} ({})".format(self.created_at, self.duration)

	@transaction.atomic
	def refresh():
		start_time = time.monotonic()
		with connection.cursor() as cursor:
			cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mat_adhocsentences")
		end_time = time.monotonic()
		tbl_refreshlog_mat_adhocsentences.objects.create(duration=datetime.timedelta(seconds=end_time - start_time))
		return end_time - start_time

	class Meta:
		db_table = "tbl_refreshlog_mat_adhocsentences"
		verbose_name = "tbl_refreshlog_mat_adhocsentences"
		verbose_name_plural = "tbl_refreshlog_mat_adhocsentences"
		ordering = ('created_at',)
