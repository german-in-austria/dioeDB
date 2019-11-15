"""MioeDB Auswertung."""
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext


def views_mioeAuswertung(request):
	"""Anzeige für MioeDB Auswertung."""
	return render_to_response(
		'mioedbvzmaske/mioeauswertungstart.html',
		RequestContext(request, {'xxx': 'xxx'}))
