from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.apps import apps
import collections
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from DB.forms import GetModelForm
from DB.funktionenDB import httpOutput
from django.conf import settings
import json
from django.db import connection
import pprint

def view_diagramm(request):
	info = ''
	error = ''
	# Models auslesen
	tabellen = []
	applist = settings.DIOEDB_APPLIST
	for aapp in applist:
		if request.user.has_perm(aapp+'.edit'):
			for model in apps.get_app_config(aapp).models.items():
				amodel = apps.get_model(aapp, model[0])
				if str(model[0])[:4]!='sys_':
					aFields = []
					for f in amodel._meta.get_fields():
						if not f.auto_created or amodel._meta.pk.name==f.name:
							aField = {'field_name':f.name,
									  'verbose_name':f._verbose_name,
									  'internal_type':f.get_internal_type(),
									  'unique':f.unique,
									  'blank':f.blank,
									  'null':f.null,
									 }
							if amodel._meta.pk.name==f.name:
								aField['pk'] = True
							if f.is_relation:
								aField['related_db_table'] = f.related_model._meta.db_table
							aFields.append(aField)
					tabellen.append({'model':model[0],
								    'app':aapp,
								    'verbose_name':amodel._meta.verbose_name,
								    'verbose_name_plural':amodel._meta.verbose_name_plural,
								    'count':amodel.objects.count(),
								    'db_table':amodel._meta.db_table,
								    'get_fields':aFields,
								   })
	tabellen = json.dumps(tabellen)
	# Ausgabe der Seite
	return render_to_response('DB/diagramm.html',
		RequestContext(request, {'tabellen':tabellen,'error':error,'info':info}),)
