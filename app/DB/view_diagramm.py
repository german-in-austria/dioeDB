"""Anzeige eines Diagramms der Models."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.apps import apps
from DB.funktionenDB import httpOutput
from django.conf import settings
import json
from .models import sys_diagramm_tabellenpositionen


def view_diagramm(request):
	"""Standard Anzeige für Model Diagramme."""
	info = ''
	error = ''
	# Modelposition speichern
	if 'speichere' in request.POST:
		if request.POST.get('speichere') == 'positionen':
			positionen = json.loads(request.POST.get('positionen'))
			for position in positionen:
				if request.user.has_perm(position['app'] + '.edit'):
					try:
						amodel = sys_diagramm_tabellenpositionen.objects.get(zu_app=position['app'], zu_model=position['model'])
					except:
						amodel = sys_diagramm_tabellenpositionen()
						amodel.zu_app = position['app']
						amodel.zu_model = position['model']
					amodel.xt = position['xt']
					amodel.yt = position['yt']
					amodel.save()
			return httpOutput('OK')
	# Models auslesen
	tabellen = []
	applist = settings.DIOEDB_APPLIST
	uApps = []
	for aapp in applist:
		if request.user.has_perm(aapp + '.edit'):
			uApps.append(aapp)
			for model in apps.get_app_config(aapp).models.items():
				if str(model[0])[:4] != 'sys_':
					amodel = apps.get_model(aapp, model[0])
					aFields = []
					xt = 0
					yt = 0
					try:
						asdtp = sys_diagramm_tabellenpositionen.objects.get(zu_app=aapp, zu_model=str(model[0]))
						xt = asdtp.xt
						yt = asdtp.yt
					except:
						pass
					for f in amodel._meta.get_fields():
						if not f.auto_created or amodel._meta.pk.name == f.name:
							aField = {
								'field_name': f.name,
								'verbose_name': f._verbose_name,
								'internal_type': f.get_internal_type(),
								'unique': f.unique,
								'blank': f.blank,
								'null': f.null,
							}
							if amodel._meta.pk.name == f.name:
								aField['pk'] = True
							if f.is_relation:
								aField['related_db_table'] = f.related_model._meta.db_table
							aFields.append(aField)
					tabellen.append({
						'model': model[0],
						'app': aapp,
						'verbose_name': str(amodel._meta.verbose_name),
						'verbose_name_plural': str(amodel._meta.verbose_name_plural),
						'count': amodel.objects.count(),
						'db_table': amodel._meta.db_table,
						'get_fields': aFields,
						'xt': xt,
						'yt': yt,
					})
	tabellen = json.dumps(tabellen)
	# Apps Liste vorbereiten
	uAppsObj = {}
	dg = 0
	for uApp in uApps:
		uAppsObj[uApp] = {'visible': True, 'dg': dg}
		dg += 1
	uAppsObj = json.dumps(uAppsObj)
	# Ausgabe der Seite
	return render_to_response(
		'DB/diagramm.html',
		RequestContext(request, {'tabellen': tabellen, 'apps': uApps, 'appsObject': uAppsObj, 'error': error, 'info': info}),
	)
