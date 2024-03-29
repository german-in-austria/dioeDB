"""Anzeige für Startseite."""
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext
from .models import sys_wartungssperre
import datetime
import json


def start(request):
	"""Startseite."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from DB.models import sys_user_addon
	from PersonenDB.models import tbl_termine
	userOnline = [{
		'model': val,
		'timer': int((datetime.datetime.now() - val.last_visit).total_seconds())
	} for val in sys_user_addon.objects.filter(last_visit__gte=datetime.datetime.now() - datetime.timedelta(minutes=5)).order_by('-last_visit')]
	userOnlineWho = []
	if request.user.is_superuser:
		userOnlineWho = userOnline
	return render_to_response(
		'startseite/start.html',
		RequestContext(request, {
			'userOnlineCount': len(userOnline),
			'userOnlineWho': userOnlineWho,
			'gc_notOK': tbl_termine.objects.filter(gc_updated=False).count()
		}),)


def sysStatusView(request):
	"""Statuswerte ausgeben"""
	txtausgabe = HttpResponse(json.dumps(sysstatus(request)))
	txtausgabe['Content-Type'] = 'text/plain'
	return txtausgabe


# Funktionen #
def sysstatus(request):
	"""Systemstatus ermitteln."""
	sysstatus = {}
	sysstatus['sys'] = 'OK'
	try:
		sys_ws = sys_wartungssperre.objects.order_by('zeit').filter(erledigt=False).filter(zeit__lte=datetime.datetime.now() + datetime.timedelta(minutes=30))[0]
		if sys_ws.zeit <= datetime.datetime.now() and not request.user.is_superuser:
			sysstatus['sperre'] = True
		sysstatus['wartung'] = {
			'zeit': str(sys_ws.zeit),
			'restzeit': int((sys_ws.zeit - datetime.datetime.now()).total_seconds() / 60),
			'titel': sys_ws.titel,
			'text': sys_ws.text,
			'stitel': sys_ws.stitel,
			'stext': sys_ws.stext
		}
	except:
		pass
	return sysstatus
