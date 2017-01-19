# -*- coding: utf-8 -*-
from django.db import models

class sys_wartungssperre(models.Model):
	zeit			= models.DateTimeField(																			  verbose_name="Zeit")
	titel			= models.CharField(max_length=255,	blank=True, null=True, default="Wartung in Kuerze!"			, verbose_name="Titel")
	text			= models.TextField(					blank=True, null=True, default="Es folgt in Kürze eine Wartung! Bitte loggen Sie sich rechtzeitig aus!"	, verbose_name="Text")
	stitel			= models.CharField(max_length=255,	blank=True, null=True, default="Laufende Wartung!"			, verbose_name="Sperrtitel")
	stext			= models.TextField(					blank=True, null=True, default="Momentan ist eine Wartung im Gange, bitte versuchen Sie es später noch einmal!"	, verbose_name="Sperrtext")
	erledigt		= models.BooleanField(									   default=False						, verbose_name="Erledigt")
	def __str__(self):
		return '{}, "{}", "{}"'.format(self.zeit,self.titel,self.stitel)
	class Meta:
		verbose_name = "Wartungssperre"
		verbose_name_plural = "Wartungssperren"
		ordering = ('erledigt','zeit',)
