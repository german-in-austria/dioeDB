from django.shortcuts import render_to_response
from django.template import RequestContext
from DB.funktionenDB import httpOutput
import datetime
import os

def view_csv(request):
	info = ''
	error = ''
	return render_to_response('korpusdb/csv_start.html',
		RequestContext(request, {'info':info,'error':error}),)
