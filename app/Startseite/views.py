from django.shortcuts import get_object_or_404 , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from .models import sys_wartungssperre
import datetime
import json

def start(request):
	if not request.user.is_authenticated():
		return redirect('dioedb_login')

	return render_to_response('startseite/start.html',
		RequestContext(request,),)

def sysStatusView(request):
	txtausgabe = HttpResponse(json.dumps(sysstatus(request)))
	txtausgabe['Content-Type'] = 'text/plain'
	return txtausgabe

# Funktionen #
def sysstatus(request):		# Systemstatus ermitteln
	sysstatus = {}
	sysstatus['sys'] = 'OK'
	try:
		sys_ws = sys_wartungssperre.objects.order_by('zeit').filter(erledigt=False).filter(zeit__lte=datetime.datetime.now() + datetime.timedelta(minutes=30))[0]
		if sys_ws.zeit <= datetime.datetime.now() and not request.user.is_superuser:
			sysstatus['sperre']=True
		sysstatus['wartung'] = {'zeit':str(sys_ws.zeit),'restzeit':int((sys_ws.zeit-datetime.datetime.now()).total_seconds()/60),'titel':sys_ws.titel,'text':sys_ws.text,'stitel':sys_ws.stitel,'stext':sys_ws.stext}
	except:
		pass
	return sysstatus