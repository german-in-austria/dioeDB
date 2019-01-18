from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.apps import apps
import collections
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from DB.forms import GetModelForm
from DB.funktionenDB import kategorienListe, felderAuslesen, verbundeneElemente, httpOutput
from django.conf import settings
import json
from django.db import connection

# Verwaltung - Startseite - Übersicht über alle verfügbaren Tabellen
def view_start(request):
	info = ''
	# Liste der verfuegbaren Tabellen:
	tabellen = collections.OrderedDict()
	applist = settings.DIOEDB_APPLIST
	for aapp in applist:
		if request.user.has_perm(aapp+'.edit'):
			tabellen[aapp] = []
			for model in apps.get_app_config(aapp).models.items():
				amodel = apps.get_model(aapp, model[0])
				if str(model[0])[:4]!='sys_':
					tabellen[aapp].append({'model':model[0],'titel':amodel._meta.verbose_name_plural,'count':amodel.objects.count()})
	# Ausgabe der Seite
	return render_to_response('DB/start.html',
		RequestContext(request, {'tabellen':(tabellen.items()),'database':settings.DATABASES['default']['ENGINE'],'info':info}),)

# Verwaltung - Ansicht - Übersicht über Tabelleneinträge mit Option zum bearbeiten
def view_view(request,app_name,tabelle_name):
	info = ''
	error = ''
	# Gibt es die Tabelle?
	try : amodel = apps.get_model(app_name, tabelle_name)
	except LookupError : return HttpResponseNotFound('<h1>Tabelle "'+tabelle_name+'" nicht gefunden!</h1>')

	# Liste der Buchstaben mit Anzahl der Elemente
	if 'getlmfal' in request.POST:
		# print(kategorienListe(amodel))
		return render_to_response('DB/lmfal.html',
			RequestContext(request, {'kategorien_liste':kategorienListe(amodel).items(),'appname':app_name,'tabname':tabelle_name,'info':info,'error':error}),)

	# Liste der Einträge des jeweiligen Buchstaben ausgeben
	if 'getlmfadl' in request.POST:
		return render_to_response('DB/lmfadl.html',
			RequestContext(request, {'lmfadl':kategorienListe(amodel,inhalt=request.POST.get('getlmfadl')),'info':info,'error':error}),)

	# Reine View des Tabelleneintrags !!!
	if 'gettableview' in request.POST:
		aElement = amodel.objects.get(pk=request.POST.get('gettableview'))
		return render_to_response('DB/view_table.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'fields':felderAuslesen(aElement,1),'usedby':verbundeneElemente(aElement),'amodel_meta':amodel._meta,'info':info,'error':error}),)

	# Reine View der Verweisliste!
	if 'getverweisliste' in request.POST:
		aElement = amodel.objects.get(pk=request.POST.get('getverweisliste'))
		return render_to_response('DB/view_table_verweisliste.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'usedby':verbundeneElemente(aElement,aField=request.POST.get('fieldname'),aMax=0),'amodel_meta':amodel._meta,'info':info,'error':error}),)

	# Ausgabe der Standard Seite mit geladenen Tabelleneintrag !
	if 'loadpk' in request.POST:
		aElement = amodel.objects.get(pk=request.POST.get('loadpk'))
		acontent = render_to_response('DB/view_table.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'fields':felderAuslesen(aElement,1),'usedby':verbundeneElemente(aElement),'amodel_meta':amodel._meta,'info':info,'error':error}),).content
		return render_to_response('DB/view.html',
			RequestContext(request, {'kategorien_liste':kategorienListe(amodel,mitInhalt=int(request.POST.get('loadpk')),arequest=request).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'acontent':acontent,'amodel_count':amodel.objects.count(),'info':info,'error':error}),)

	# Reines Formular des Tabelleneintrags
	if 'gettableeditform' in request.POST:
		if int(request.POST.get('gettableeditform')) > 0:
			aElement = amodel.objects.get(pk=request.POST.get('gettableeditform'))
			aform = GetModelForm(amodel,instance=aElement)
		else:
			aElement = amodel()
			aform = GetModelForm(amodel)
		return render_to_response('DB/edit_table.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'amodel_meta':amodel._meta,'aform':aform,'pktitel':aElement._meta.pk.verbose_name,'pkvalue':aElement.pk,'info':info,'error':error}),)

	# Formular ForeignKey Select
	if 'getforeignkeysel' in request.POST:
		try:
			aElement = amodel.objects.get(pk=request.POST.get('getforeignkeysel'))
			acontent = render_to_response('DB/view_table.html',
				RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'fields':felderAuslesen(aElement,1),'usedby':verbundeneElemente(aElement),'amodel_meta':amodel._meta,'info':info,'error':error}),).content
			return render_to_response('DB/foreignkeysel.html',
				RequestContext(request, {'kategorien_liste':kategorienListe(amodel,mitInhalt=int(request.POST.get('getforeignkeysel')),arequest=request).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'acontent':acontent,'info':info,'error':error}),)
		except ObjectDoesNotExist:
			return render_to_response('DB/foreignkeysel.html',
				RequestContext(request, {'kategorien_liste':kategorienListe(amodel).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'acontent':'','info':info,'error':error}),)

	# Formular speichern
	if 'saveform' in request.POST and request.user.has_perm(app_name+'.edit'):
		# Neues Formular speichern !!!!!!!!!
		if int(request.POST.get('savepk')) > 0:
			aElement = amodel.objects.get(pk=request.POST.get('savepk'))
			aform = GetModelForm(amodel,request.POST,instance=aElement)
		else:
			aElement = amodel()
			aform = GetModelForm(amodel,request.POST)
		if aform.is_valid():
			aElement = aform.save()
			LogEntry.objects.log_action(
				user_id = request.user.pk,
				content_type_id = ContentType.objects.get_for_model(aElement).pk,
				object_id = aElement.pk,
				object_repr = str(aElement),
				action_flag = CHANGE if int(request.POST.get('savepk')) > 0 else ADDITION
			)
			info = 'Datensatz gespeichert.'
			return render_to_response('DB/view_table.html',
				RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'fields':felderAuslesen(aElement,1),'usedby':verbundeneElemente(aElement),'amodel_meta':amodel._meta,'info':info,'error':error}),)
		else:
			error = 'Fehlerhafte Eingabe!'
		return render_to_response('DB/edit_table.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'amodel_meta':amodel._meta,'aform':aform,'pktitel':aElement._meta.pk.verbose_name,'pkvalue':aElement.pk,'info':info,'error':error}),)
	# Element loeschen
	if 'delobj' in request.POST and request.user.has_perm(app_name+'.edit'):
		aElement = amodel.objects.get(pk=request.POST.get('delobj'))
		error = str(aElement)+' (PK: '+str(aElement.pk)+') wurde geloescht!'
		aElement.delete()
		LogEntry.objects.log_action(
			user_id = request.user.pk,
			content_type_id = ContentType.objects.get_for_model(aElement).pk,
			object_id = aElement.pk,
			object_repr = str(aElement),
			action_flag = DELETION
		)
		return render_to_response('DB/view_empty.html',
			RequestContext(request, {'amodel_meta':amodel._meta,'appname':app_name,'tabname':tabelle_name,'info':info,'error':error}),)

	# Ausgabe der Standard Seite
	return render_to_response('DB/view.html',
		RequestContext(request, {'kategorien_liste':kategorienListe(amodel).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'amodel_count':amodel.objects.count(),'info':info,'error':error}),)

# Verwaltung - Reset id_seq für PostgreSQL
def view_resetidseq(request,app_name,tabelle_name):
	# Gibt es die Tabelle?
	try : amodel = apps.get_model(app_name, tabelle_name)
	except LookupError : return HttpResponseNotFound('<h1>Tabelle "'+tabelle_name+'" nicht gefunden!</h1>')
	# Reset id sequence
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT setval('\""+amodel._meta.db_table+"_id_seq\"',  (SELECT MAX(id) FROM \""+amodel._meta.db_table+"\")+1, FALSE)")
		output = json.dumps({'success':'success',})
	except Exception as e:
		output = json.dumps({'error':str(type(e))+' - '+str(e),})
	return httpOutput(output, mimetype='application/json')
