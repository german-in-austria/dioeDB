from django.shortcuts import render
from django.shortcuts import get_object_or_404 , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from DB.funktionenDB import httpOutput
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from django.core import serializers
from django.db.models import Count
import json

def getTags(request):
	if not request.user.is_authenticated():
		return HttpResponse('Unauthorized', status=401)
	return httpOutput(serializers.serialize("json", KorpusDB.tbl_tags.objects.all()), mimetype='text/plain')

def test(request):
	if not request.user.is_authenticated():
		return HttpResponse('Unauthorized', status=401)
	if 'tag' in request.GET:
		try:
			atagid = int(request.GET.get('tag'))
			print([val for val in PersonenDB.tbl_informanten.objects.filter(tbl_antworten__tbl_antwortentags__id_Tag=atagid).values('inf_sigle').annotate(total=Count('inf_sigle'))])
			return httpOutput(json.dumps([val for val in PersonenDB.tbl_informanten.objects.filter(tbl_antworten__tbl_antwortentags__id_Tag=atagid).values('inf_sigle').annotate(total=Count('inf_sigle'))]), mimetype='text/plain')
		except Exception as e:
			return HttpResponse('Internal Server Error: '+str(e), status=500)
	else:
		return HttpResponse('Method Not Allowed', status=405)
	# return HttpResponse('Method Not Allowed', status=405)
