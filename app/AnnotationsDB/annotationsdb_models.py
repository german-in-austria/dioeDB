from django.db import models


class event(models.Model):
	start_time			= models.DurationField(																				  verbose_name="Start Zeit")
	end_time			= models.DurationField(																				  verbose_name="End Zeit")
	layer				= models.IntegerField(						  null=True												, verbose_name="Layer")
	def __str__(self):
		return "{} - {} bis {}".format(self.layer, self.start_time, self.end_time)
	class Meta:
		db_table = "event"
		verbose_name = "Event"
		verbose_name_plural = "Events"
		ordering = ('start_time',)

class token(models.Model):
	token_type_id		= models.ForeignKey('token_type'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Token Type")
	ortho				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Ortho")
	lautg				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="lautgetreue Umschrift")
	phon				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="phonetische Umschrift")
	sonst				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="sonstige Umschrift")
	transcomment				= models.CharField(max_length=511			, blank=True, null=True							, verbose_name="kommentar zu Transkript")
	ID_Inf				= models.ForeignKey('Datenbank.Informanten'	, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="ID Informant")
	fragment_of			= models.ForeignKey('token', related_name='rn_token_fragment_of', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Fragment von")
	token_reihung		= models.IntegerField(						  null=True												, verbose_name="Token Reihung")
	event_id			= models.ForeignKey('event', related_name='rn_token_event_id', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Event ID")
	start_timepoint		= models.DurationField(																				  verbose_name="Start Zeitpunkt")
	end_timepoint		= models.DurationField(																				  verbose_name="End Zeitpunkt")
	transcript_id		= models.ForeignKey('transcript'			, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Transcript ID")
	likely_error		= models.BooleanField(default=False																	, verbose_name="Eventueller Fehler")
	sentence			= models.IntegerField(						, blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Sentence ID")
	sequence_in_sentence = models.IntegerField(						  null=True												, verbose_name="sequence_in_sentence")

	def __str__(self):
		return "\"{}\"".format(self.ortho)
	class Meta:
		db_table = "token"
		verbose_name = "Token"
		verbose_name_plural = "Tokens"
		ordering = ('sentence_id', 'token_reihung',)

class token_type(models.Model):
	token_type_name		= models.CharField(max_length=511																	, verbose_name="Token Typ Name")
	def __str__(self):
		return "{}".format(self.token_type_name)
	class Meta:
		db_table = "token_type"
		verbose_name = "Token Typ"
		verbose_name_plural = "Token Typen"
		ordering = ('id',)

class transcript(models.Model):
	name				= models.CharField(max_length=511			, blank=True, null=True									, verbose_name="Name")
	update_time			= models.DateTimeField(																				  verbose_name="Update Zeit")
	def __str__(self):
		return "{} ({})".format(self.name, self.update_time)
	class Meta:
		db_table = "transcript"
		verbose_name = "Transcript"
		verbose_name_plural = "Transcripte"
		ordering = ('id',)

class tbl_tokenset(models.Model):
	id_von_token		= models.ForeignKey('token', related_name='rn_id_von_token', blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Von Token ID")
	id_bis_token		= models.ForeignKey('token', related_name='rn_id_bis_token', blank=True, null=True	, on_delete=models.SET_NULL		, verbose_name="Bis Token ID")
	def __str__(self):
		return "{} - {}".format(self.id_von_token, self.id_bis_token)
	class Meta:
		db_table = "tokenset"
		verbose_name = "Token Set"
		verbose_name_plural = "Token Sets"
		ordering = ('id_von_token',)

class tbl_tokentoset(models.Model):
	id_tokenset			= models.ForeignKey('tbl_tokenset'									, on_delete=models.CASCADE		, verbose_name="Tokenset")
	id_token			= models.ForeignKey('token'											, on_delete=models.CASCADE		, verbose_name="Token")
	def __str__(self):
		return "{} <- {}".format(self.id_tokenset, self.id_token)
	class Meta:
		db_table = "tokentoset"
		verbose_name = "Token to Token Set"
		verbose_name_plural = "Token to Token Sets"
		ordering = ('id_tokenset',)
