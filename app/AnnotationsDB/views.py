"""Ansichten der AnnotationsDB."""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def auswertung(request, aTagEbene, aSeite):
	"""Auswertung anzeigen."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_auswertung import views_auswertung
	return views_auswertung(request, aTagEbene, aSeite)


def annotool(request, ipk=0, tpk=0):
	"""Annotations Tool Daten."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annotool import views_annotool
	return views_annotool(request, ipk, tpk)


def tool(request):
	"""Annotations Tool Template."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	return render_to_response('AnnotationsDB/toolstart.html', RequestContext(request))


def annosent(request):
	"""AnnoSent."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annosent import views_annosent
	return views_annosent(request)


def annocheck(request):
	"""AnnoCheck."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annocheck import views_annocheck
	return views_annocheck(request)
