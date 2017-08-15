from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db import models, connection
from django.db.models import Count, Q, Sum
import collections
from django.apps import apps
from copy import deepcopy
import json
import pprint
import datetime
import math
import os
from django.conf import settings

Monate = ('Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember')

# Schneller HttpOutput
def httpOutput(aoutput,mimetype='text/plain'):
	txtausgabe = HttpResponse(aoutput)
	txtausgabe['Content-Type'] = mimetype
	return txtausgabe

# Liste der Einträge erstellen #
def kategorienListe(amodel,suche='',inhalt='',mitInhalt=0,arequest=[],addFX=1):
	ausgabe = collections.OrderedDict()
	# Für Spezielle Kategorien Listen mit Standard gemischt
	if addFX == 1 and hasattr(amodel,'kategorienListeAddFX'):
		return amodel.kategorienListeAddFX(amodel,suche,inhalt,mitInhalt,arequest,ausgabe)
	# Für Spezielle Kategorien Listen
	if hasattr(amodel,'kategorienListeFX'):
		return amodel.kategorienListeFX(amodel,suche,inhalt,mitInhalt,arequest,ausgabe)
	# Für ForeignKey
	if str(amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()) == 'ForeignKey':
		if not inhalt:
			aElement = amodel.objects.all()
			ausgabe['all']={'count':aElement.count(),'title':'Alle','enthaelt':1}
			if mitInhalt>0:
				ausgabe['all']['active'] = render_to_response('DB/lmfadl.html',
					RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt='all'),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			aFKAnnotate = amodel.objects.values(amodel._meta.ordering[0]).annotate(total=Count(amodel._meta.ordering[0])).order_by(amodel._meta.ordering[0])
			for xval in aFKAnnotate:
				aFKModel = amodel._meta.get_field(amodel._meta.ordering[0]).related_model.objects.get(pk=xval[amodel._meta.ordering[0]])
				abc = 'fk'+str(aFKModel.pk)
				ausgabe[abc] = {'count':xval['total'],'title':str(aFKModel)}
			return ausgabe
		else:
			aElement = amodel.objects.all()
			if inhalt[:2] == 'fk':
				apk = int(inhalt[2:])
				aElement = amodel.objects.filter(**{amodel._meta.ordering[0]:apk})
			return [{'model':aM} for aM in aElement]
	# Für DateTimeField
	if str(amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()) == 'DateTimeField':
		if not inhalt:
			aElement = amodel.objects.all()
			ausgabe['all']={'count':aElement.count(),'title':'Alle','enthaelt':1}
			if mitInhalt>0:
				ausgabe['all']['active'] = render_to_response('DB/lmfadl.html',
					RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt='all'),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			for aMonatsDaten in amodel.objects.extra({'month':connection.ops.date_trunc_sql('month', amodel._meta.ordering[0])}).values('month').annotate(Count('pk')).order_by('-month'):
				if isinstance(aMonatsDaten['month'], str):
					(aJahr,aMonat,nix) = aMonatsDaten['month'].split('-',2)
				else:
					aMonat = aMonatsDaten['month'].strftime("%m")
					aJahr = aMonatsDaten['month'].strftime("%Y")
				abc = 'date'+aJahr+'-'+aMonat
				ausgabe[abc]={'count':aMonatsDaten['pk__count'],'title':aJahr+' - '+Monate[int(aMonat)-1]}
			return ausgabe
		else:
			aElement = amodel.objects.all()
			if inhalt[:4] == 'date':
				(aJahr,aMonat) = inhalt[4:].split('-',1)
				aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__year':aJahr,amodel._meta.ordering[0]+'__month':aMonat})
			return [{'model':aM} for aM in aElement]
	# Nicht alphabetisch
	if str(amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()) != 'CharField':
		if not inhalt:
			aElement = amodel.objects.all()
			abc = amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()
			ausgabe[abc]={'count':aElement.count(),'enthaelt':1,'suchein':1}
			if mitInhalt>0:
				ausgabe[abc]['active'] = render_to_response('DB/lmfadl.html',
					RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=abc),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			return ausgabe
		else:
			return [{'model':aM} for aM in amodel.objects.all()]
	# Alphabetisch
	kategorien = collections.OrderedDict() ; kategorien['Andere'] = '^a-zäöüÄÖÜ' ; kategorien['istartswith'] = 'abcdefghijklmnopqrstuvwxyz' ; kategorien['ä'] = 'äÄ' ; kategorien['ö'] = 'öÖ' ; kategorien['ü'] = 'üÜ'
	if not inhalt: # Liste fuer Kategrien ausgeben
		for key,value in kategorien.items():
			if key == 'istartswith':
				for abc in value:
					if suche : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':abc,amodel._meta.ordering[0]+'__contains':suche})
					else : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':abc})
					ausgabe[abc] = {'count':aElement.count()}
					if mitInhalt>0:
						if aElement.filter(pk=mitInhalt).count():
							ausgabe[abc]['active'] = render_to_response('DB/lmfadl.html',
								RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=abc),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			else:
				if suche : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+value+'].+)',amodel._meta.ordering[0]+'__contains':suche})
				else : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+value+'].+)'})
				ausgabe[key] = {'count':aElement.count()}
				if mitInhalt>0:
					if aElement.filter(pk=mitInhalt).count():
						ausgabe[key]['active'] = render_to_response('DB/lmfadl.html',
							RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=key),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
	else: # Inhalte fuer Kategorie ausgeben
		if inhalt in kategorien: ausgabe = [{'model':aM} for aM in amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+kategorien[inhalt]+'].+)'})]
		else : ausgabe = [{'model':aM} for aM in amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':inhalt})]
	return ausgabe

# Feld auslesen #
def feldAuslesen(aElement,fName,inhalte=0):
	for f in aElement._meta.fields:
		if f.name == fName:
			return feldAuslesenF(aElement,f,inhalte)
def feldAuslesenF(aElement,f,inhalte=0):
	afield = {}
	afield['name'] = f.name
	afield['verbose_name'] = f.verbose_name
	afield['type'] = f.get_internal_type()
	afield['max_length'] = f.max_length
	if inhalte == 1:
		aFieldElement = getattr(aElement, f.name)
		afield['value'] = aFieldElement
		try : afield['value_extras'] = {'app':aFieldElement._meta.app_label,'name':aFieldElement.__class__.__name__,'pk':aFieldElement.pk}
		except AttributeError : pass
	else:
		pass ############################### <-- Hier muss was fuer 'value_extras' hin!!!!!
	return afield

# Felder auslesen #
def felderAuslesen(aElement,inhalte=0):
	fields = []
	for f in aElement._meta.fields:
		fields.append(feldAuslesenF(aElement,f,inhalte))
	return fields

# Gefilterte Felder auslesen #
def gefilterteFelderAuslesen(aElement,fNamen,inhalte=0):
	fields = []
	for f in aElement._meta.fields:
		if f.name in fNamen:
			fields.append(feldAuslesenF(aElement,f,inhalte))
	return fields

# Verbundene Elemente ermitteln #
def verbundeneElemente(aElement,aField='',aMax = getattr(settings, 'DIOEDB_MAXVERWEISE', 10)):
	usedby = []
	if aField:
		aFields = [aElement._meta.get_field(aField)]
	else:
		aFields = aElement._meta.get_fields()
	for f in aFields:
		if (f.one_to_many) and f.auto_created:
			aElemente = getattr(aElement, f.get_accessor_name()).all()
			if aMax > 0:
				aElementeX = aElemente[:aMax]
			else:
				aElementeX = aElemente
			usedby.append({'model_typ':'one_to_many','model_app_label':f.related_model._meta.app_label,'model_name':f.related_model.__name__,'related_name':f.related_name,'accessor_name':f.get_accessor_name(),'field_name':f.name,'model_verbose_name':f.related_model._meta.verbose_name,'model_verbose_name':f.related_model._meta.verbose_name_plural,
				'elemente':[{'pk':o.pk,'value':str(o)} for o in aElementeX],'elemente_count':aElemente.count(),'elemente_weiter':(aMax if aElemente.count()>aMax else None)})
		elif (f.one_to_one) and f.auto_created:
			aElemente = []
			try:
				aFieldElement = getattr(aElement, f.get_accessor_name())
				aElemente = [{'pk':aFieldElement.pk,'value':str(aFieldElement)}]
			except: pass
			usedby.append({'model_typ':'one_to_one','model_app_label':f.related_model._meta.app_label,'model_name':f.related_model.__name__,'related_name':f.related_name,'accessor_name':f.get_accessor_name(),'field_name':f.name,'model_verbose_name':f.related_model._meta.verbose_name,'model_verbose_name':f.related_model._meta.verbose_name_plural,
				'elemente': aElemente})
	return usedby

###################
# Formular-System #
###################

# Formular View #
def formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aform,request,info='',error=''):
	amodel = apps.get_model(app_name, tabelle_name)

	# Zusatzoptionen laden
	addCSS = [] ; addJS = [] ; csvImport = {}
	for val in aform:
		if 'addCSS' in val:
			addCSS+= val['addCSS']
		if 'addJS' in val:
			addJS+= val['addJS']
		if 'import' in val:
			csvImport = val['import']

	# Importfunktion!
	if 'enabled' in csvImport and csvImport['enabled'] == True and request.user.has_perm('DB.csvimport'):
		from .models import sys_importdatei
		from .funktionenDateien import removeLeftSlash
		addJS = [{'static':'db/js/dateien_funktionen.js'},{'static':'db/js/csv_import.js'}] + addJS
		mDir = getattr(settings, 'PRIVATE_STORAGE_ROOT', None)
		if not mDir:
			return HttpResponseServerError('PRIVATE_STORAGE_ROOT wurde nicht gesetzt!')
		uplDir = os.path.join(mDir,'csv','automatik')
		# Datei hochladen
		if 'csvupload' in request.POST:
			from django.core.files.storage import FileSystemStorage
			import unicodedata
			zu_pk = int(request.POST.get('csvupload'))
			fs = FileSystemStorage(location=mDir)
			for afile in request.FILES.getlist('dateien'):
				asavename = os.path.join(uplDir,afile.name)
				asavename = unicodedata.normalize('NFKD', asavename).encode('ascii', 'ignore').decode("utf-8")
				filename = fs.save(asavename, afile)
				newsysid = sys_importdatei(zu_app=app_name,zu_tabelle=tabelle_name,zu_pk=zu_pk,datei=os.path.normpath(filename[len(uplDir):]),zeit=datetime.datetime.now(),erledigt=False)
				newsysid.save()
			return httpOutput('OK')
		# Verknüpfte Dateien auflisten
		if 'gettableview' in request.POST or 'gettableeditform' in request.POST or 'loadpk' in request.POST:
			aformid = request.POST.get('gettableview') or request.POST.get('gettableeditform') or request.POST.get('loadpk')
			csvImport['dateien'] = []
			for asysid in sys_importdatei.objects.filter(zu_app=app_name,zu_tabelle=tabelle_name,zu_pk=aformid):
				csvImport['dateien'].append({'model':asysid,'isfile':os.path.isfile(os.path.join(uplDir,removeLeftSlash(asysid.datei)))})
		# Import Ansicht
		
	else:
		csvImport = {}

	# Formular speichern
	if 'saveform' in request.POST:
		return formularSpeichervorgang(request,aform,primaerId,app_name+'.'+permName)

	# Reine View oder Formular des Tabelleneintrags
	if 'gettableview' in request.POST or 'gettableeditform' in request.POST:
		aformid = request.POST.get('gettableview') or request.POST.get('gettableeditform')
		aforms = formularDaten(aform,aformid)
		# info = '<div class="code">'+pprint.pformat(aforms)+'</div>'
		return render_to_response('DB/form_view.html',
			RequestContext(request, {'apk':str(aformid),'amodel_meta':amodel._meta,'aforms':aforms,'xforms':aform,'acount':0,'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'editmode':'gettableeditform' in request.POST,'csvImport':csvImport,'info':info,'error':error}),)
	# Reine View der Verweisliste!
	if 'getverweisliste' in request.POST:
		aElement = amodel.objects.get(pk=request.POST.get('getverweisliste'))
		return render_to_response('DB/view_table_verweisliste.html',
			RequestContext(request, {'aelement':aElement,'aelementapp':aElement._meta.app_label,'aelementtabelle':aElement.__class__.__name__,'usedby':verbundeneElemente(aElement,aField=request.POST.get('fieldname'),aMax=0),'amodel_meta':amodel._meta,'info':info,'error':error}),)

	# Startseite mit Eintrag
	if 'loadpk' in request.POST:
		aformid = int(request.POST.get('loadpk'))
		aforms = formularDaten(aform,aformid)
		acontent = render_to_response('DB/form_view.html',
			RequestContext(request, {'apk':str(aformid),'amodel_meta':amodel._meta,'aforms':aforms,'xforms':aform,'acount':0,'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'editmode':'gettableeditform' in request.POST,'csvImport':csvImport,'info':info,'error':error}),).content
		return render_to_response('DB/form_base_view.html',
			RequestContext(request, {'kategorien_liste':kategorienListe(amodel,mitInhalt=aformid,arequest=request).items(),'acontent':acontent,'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'amodel_count':amodel.objects.count(),'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'aktueberschrift':aktueberschrift,'asurl':asurl,'info':info,'error':error}),)

	return render_to_response('DB/form_base_view.html',
		RequestContext(request, {'kategorien_liste':kategorienListe(amodel).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'amodel_count':amodel.objects.count(),'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'aktueberschrift':aktueberschrift,'asurl':asurl,'addCSS':addCSS,'addJS':addJS,'info':info,'error':error}),)


# Formular Basisdaten erstellen #
def formularDaten(vorlage,pId=0,pData=None,iFlat=False,aParentId=None,iFirst=True):
	global formNr
	if iFirst:
		formNr=0
	pForms = []
	fForms = {}
	for aForm in vorlage:
		aModel = apps.get_model(aForm['app'], aForm['tabelle'])
		formNr = formNr + 1
		pForm = {'titel':aForm['titel'],'app':aForm['app'],'tabelle':aForm['tabelle'],'id':aForm['id'],'optionen':aForm['optionen'],'nr':formNr}
		if 'titel_plural' in aForm:
			pForm['titel_plural'] = aForm['titel_plural']
		else:
			pForm['titel_plural'] = aForm['titel']
		if 'exclude' in aForm:
			pForm['exclude'] = aForm['exclude']
		if 'filter' in aForm:
			pForm['filter'] = aForm['filter']
		if 'suboption' in aForm:
			pForm['suboption'] = aForm['suboption']
		if 'elementtitel' in aForm:
			pForm['elementtitel'] = aForm['elementtitel']
		if aParentId:
			pForm['parent'] = aParentId
		if iFlat:
			pForm['felder'] = {}
		else:
			pForm['bData'] = {'felder':[]}
		for aFeld in aForm['felder']:		# Basisfelder auswerten
			aInhalt = {}
			pFeld = aFeld
			if pFeld[:1] == '|':			# Feld ist hidden?
				pFeld = pFeld[1:]
				aInhalt['hidden'] = True
			elif pFeld[:1] == '+':			# Einblendbares Feld?
				pFeld = pFeld[1:]
				aInhalt['einblendbar'] = True
			elif pFeld[:1] == '!':			# Feld ohne Datenbankanbindung?
				pFeld = pFeld[1:]
				aInhalt['fx'] = True
			if '=' in pFeld:				# Feld enthaelt einen Vorgabewert?
				pFeld , aInhalt['process'] = pFeld.split('=',1)
			if 'feldoptionen' in aForm:
				if pFeld in aForm['feldoptionen']:
					aInhalt['feldoptionen'] = aForm['feldoptionen'][pFeld]
			if 'fx' in aInhalt and aInhalt['fx']:	# Feld ohne Datenbankanbindung setzten
				aInhalt['name'] = pFeld
				aInhalt['verbose_name'] = pFeld
				if iFlat:
					pForm['felder'][aInhalt['name']] = aInhalt
				else:
					pForm['bData']['felder'].append(aInhalt)
			else:									# Feld mit Datenbankanbindung setzten
				aModelFeld = aModel._meta.get_field(pFeld)
				aInhalt['name'] = aModelFeld.name
				aInhalt['verbose_name'] = aModelFeld.verbose_name
				aInhalt['type'] = aModelFeld.get_internal_type()
				if aModelFeld.choices:
					aInhalt['choices'] = aModelFeld.choices
				if aInhalt['type'] == 'ForeignKey' or aInhalt['type'] == 'OneToOneField':
					aInhalt['typeoptions']={'app':aModelFeld.related_model._meta.app_label,'name':aModelFeld.related_model.__name__}
					if ('feldoptionen' in aInhalt and 'foreignkey_select' in aInhalt['feldoptionen']):
						aModelList = []
						for aModelFeldElement in aModelFeld.related_model.objects.all():
							nListFx = {'model':aModelFeldElement}
							if 'data' in aInhalt['feldoptionen']['foreignkey_select']:
								nListFx['data'] = {}
								for key, val in aInhalt['feldoptionen']['foreignkey_select']['data'].items():
									pval=None
									try:
										pval = getattr(aModelFeldElement,val)
									except:
										pass
									nListFx['data'][key] = pval
							aModelList.append(nListFx)
						aInhalt['selectlist'] = {'is':1,'listfx':aModelList}
					elif (aModelFeld.related_model.__name__ != 'tbl_orte' and aModelFeld.related_model.objects.all().count() < 50):
						aInhalt['selectlist'] = {'is':1,'list':aModelFeld.related_model.objects.all()}
					# print(aInhalt)
				if aModelFeld.max_length:
					aInhalt['max_length'] = aModelFeld.max_length
				if not aModelFeld.blank:
					aInhalt['is_required'] = True
				if iFlat:
					pForm['felder'][aInhalt['name']] = aInhalt
				else:
					pForm['bData']['felder'].append(aInhalt)
		if 'sub' in aForm:					# Wenn es ein Unterformular gibt dieses verarbeiten
			if aForm['sub']:
				if iFlat:
					fForms.update(formularDaten(aForm['sub'],0,iFlat=True,aParentId=aForm['id'],iFirst=False))
				else:
					pForm['bData']['sub'] = formularDaten(aForm['sub'],0,iFirst=False)
		if pId != 0 or pData:				# Content laden
			if pId != 0:					# Wenn die pId angegeben wurde
				aElemente = aModel.objects.filter(pk=pId)
			else:							# Wenn pData angegeben wurde
				filter = {}
				for aFeld in pForm['bData']['felder']:
					if 'process' in aFeld:
						pObj , pFeld = aFeld['process'].split(':',1)
						if pObj == 'parent':
							aValue = next((item for item in pData if item["name"] == pFeld))['value']
							if aValue:
								if not type(aValue) is int:
									aValue = aValue.pk
							filter[aFeld['name']+'__exact'] = aValue
						else:
							pass	# <-- Wenn's mal nicht die Eltern sind ...
				if filter:
					aElemente = aModel.objects.filter(**filter)
				else:
					aElemente = aModel.objects.all()
			if aElemente:
				if 'filter' in pForm:
					for ffeld, fvalue in pForm['filter'].items():
						aElemente = aElemente.filter(**{ffeld:fvalue})
				if 'exclude' in pForm:
					for ffeld, fvalue in pForm['exclude'].items():
						aElemente = aElemente.exclude(**{ffeld:fvalue})
				pForm['cData'] = []
				aData = {}
				for aElement in aElemente:	# Elemente fuellen
					aFelder = deepcopy(pForm['bData']['felder'])
					aData['isContent'] = True
					for aFeld in aFelder:
						if not ('fx' in aFeld and aFeld['fx']):
							if aFeld['type'] == 'ForeignKey' or aFeld['type'] == 'OneToOneField':
								aValue = getattr(aElement, aFeld['name'])
								if aValue:
									aFeld['value'] = aValue
									try : aFeld['value_extras'] = {'app':aValue._meta.app_label,'name':aValue.__class__.__name__,'pk':aValue.pk}
									except AttributeError : pass
								else:
									aFeld['value']=None
							else:
								aFeld['value']=getattr(aElement, aFeld['name'])
					for aFeld in aFelder:
						if 'feldoptionen' in aFeld and aFeld['feldoptionen'] and 'fxtype' in aFeld['feldoptionen'] and aFeld['feldoptionen']['fxtype'] and 'fxfunction' in aFeld['feldoptionen']['fxtype']:
							aFeld = aFeld['feldoptionen']['fxtype']['fxfunction'](aFeld,aFelder)
					aData['felder'] = aFelder
					if 'sub' in aForm:
						aData['sub'] = formularDaten(aForm['sub'],0,aFelder,iFirst=False)
						if 'suboption' in pForm and 'tab' in pForm['suboption']:
							for aSub in aData['sub']:
								if 'cData' in aSub:
									aSub['erstesAktive'] = True
									break
					pForm['cData'].append(deepcopy(aData))
		if iFlat:
			fForms[pForm['id']] = pForm
		else:
			pForms.append(pForm)
	if iFlat:
		return fForms
	else:
		return pForms

def isSubSave(node):
	if isinstance(node, list):
		for x in node:
			if isSubSave(x) == True:
				return True
	elif isinstance(node, dict):
		if ('saveit' in node and node['saveit'] == True) or ('haserror' in node and node['haserror'] == True):
			return True
		if 'subs' in node:
			if isSubSave(node['subs']) == True:
				return True
	return False
def formularFlat(aform):
	fform = []
	if isinstance(aform, list):
		for x in aform:
			fform = fform + formularFlat(x)
	elif isinstance(aform, dict):
		xform = deepcopy(aform)
		xform.pop('subs', None)
		fform.append(xform)
		if 'subs' in aform:
			fform = fform + formularFlat(aform['subs'])
	return fform
def flatFormularSort(afform):
	xfform = deepcopy(afform)
	asortdg = 0
	def reNumFormular(rnfforms,mNr):
		for rnfform in rnfforms:
			if rnfform['sort']>mNr:
				rnfform['sort']=rnfform['sort']+1
	for aform in xfform:
		asortdg = asortdg + 1
		aform['sort'] = asortdg
	for aform in xfform:
		if 'saveafter' in aform:
			if isinstance(aform['saveafter'][0], dict):
				asafter = aform['saveafter'][0]['id']
			else:
				asafter = aform['saveafter'][0]
			for sform in xfform:
				if sform['id'] == asafter:
					reNumFormular(xfform,sform['sort'])
					aform['sort'] = sform['sort']+1
				elif 'saveafter' in sform:
					if isinstance(sform['saveafter'][0], dict):
						aasafter = sform['saveafter'][0]['id']
					else:
						aasafter = sform['saveafter'][0]
					if aform['id'] == aasafter:
						reNumFormular(xfform,aform['sort'])
						sform['sort'] = aform['sort']+1
	for aform in xfform:
		for sform in xfform:
			if aform['id'] == sform['id']:
				if aform['sort'] < sform['sort']:
					reNumFormular(xfform,aform['sort'])
					sform['sort'] = aform['sort']+1
				else:
					reNumFormular(xfform,sform['sort'])
					aform['sort'] = sform['sort']+1
	return sorted(xfform, key=lambda k: k['sort'])
def flatFormularFind(afform,sId,sNr=0):
	for aform in afform:
		if aform['id'] == sId:
			if aform['nr'] == sNr or sNr == 0:
				return aform
	return False
def flatFormularError(fsavedatas):
	for asavedata in fsavedatas:
		if 'haserror' in asavedata and asavedata['haserror'] == True:
			return True
def flatFormularErrorTxt(fsavedatas):
	aerror = []
	for d in fsavedatas:
		if 'errortxt' in d:
			aerror = aerror + d['errortxt']
	return aerror

# Formular Auswertung als Vorbereitung zum speichern #
def formularAuswertung(aformsdata,formVorlageFlat,delit=False,iFirst=True,aParent=None):
	global aNr
	if iFirst:
		aNr=0
	if type(aformsdata) is list:
		tformsdata = []
		for aformdata in aformsdata:
			tformsdata.append(formularAuswertung(aformdata,formVorlageFlat,delit,iFirst=False,aParent=aParent))
		return tformsdata
	else:
		aNr = aNr + 1
		aformsdata['nr'] = aNr
		if delit == True or ('delit' in aformsdata and aformsdata['delit'] == True):
			delit = True
			aformsdata['delit'] = True
		aFormData = formVorlageFlat[aformsdata['id']]	# Finde die passende formVorlage
		valueCount = 0
		if not delit:
			savedChildren = False
			hasError = False
			errorTxt = []
			for key, value in aformsdata['input'].items():
				if 'process' in aFormData['felder'][key]:	# Ist der input processed?
					pObj , pFeld = aFormData['felder'][key]['process'].split(':',1)
					if pObj != 'auto' and key != 'id':
						if pObj == 'parent':
							if aParent:
								if not 'saveafter' in aformsdata:
									aformsdata['saveafter'] = []
								aformsdata['saveafter'].append(aParent)
							else:
								hasError = True
								errorTxt.append(['sys','System Fehler: '+aformsdata['id']+' ('+aformsdata['nr']+'): "'+aFormData['felder'][key]['process']+'" hat keinen "parent"!'])
						else:
							if not 'saveafter' in aformsdata:
								aformsdata['saveafter'] = []
							aformsdata['saveafter'].append(pObj)
				if aFormData['felder'][key]['type'] == 'ForeignKey' or aFormData['felder'][key]['type'] == 'OneToOneField' or aFormData['felder'][key]['type'] == 'AutoField' or aFormData['felder'][key]['type'] == 'IntegerField' or aFormData['felder'][key]['type'] == 'PositiveIntegerField':
					if value['val']:
						try : value['val'] = int(value['val'])
						except : value['val'] = 0
					else:
						value['val'] = None
					aformsdata['input'][key]['val'] = value['val']
				if aFormData['felder'][key]['type'] == 'DurationField':
					if value['val'] == None:
						value['val'] = None
					else:
						value['val'] = datetime.timedelta(microseconds=int(float(value['val'])*1000000))
				if not 'process' in aFormData['felder'][key]:
					if value['val'] and not key=='id':
						valueCount = valueCount + 1
					elif (aFormData['felder'][key]['type'] == 'IntegerField' or aFormData['felder'][key]['type'] == 'PositiveIntegerField') and not value['val'] == None:
						valueCount = valueCount + 1
					else:
						if 'is_required' in aFormData['felder'][key] and aFormData['felder'][key]['is_required']:
							hasError = True
							if 'id' in value:
								xvalid = '#'+value['id']
							else:
								xvalid = 'sys'
							errorTxt.append([xvalid,'Fehler: Feld "'+aFormData['felder'][key]['verbose_name']+'" muss angegeben werden!'])
			aformsdata['valueCount'] = valueCount
			if aParent:
				aformsdata['parent'] = aParent['id']
			if 'subs' in aformsdata:
				aformsdata['subs'] = formularAuswertung(aformsdata['subs'],formVorlageFlat,delit,iFirst=False,aParent={'id':aformsdata['id'],'nr':aformsdata['nr']})
				savedChildren = isSubSave(aformsdata['subs'])
			if not delit and (valueCount>0 or savedChildren):
				if hasError:
					aformsdata['haserror'] = True
					aformsdata['errortxt'] = errorTxt
				else:
					aformsdata['saveit'] = True
		else:
			if 'subs' in aformsdata:
				aformsdata['subs'] = formularAuswertung(aformsdata['subs'],formVorlageFlat,delit,iFirst=False,aParent={'id':aformsdata['id'],'nr':aformsdata['nr']})
		return aformsdata

def formularSpeichern(fsavedatas,formVorlageFlat,request,permpre):
	resave = []
	sfsavedatas = flatFormularSort(fsavedatas)
	for afsavedata in sfsavedatas:
		resaveit = False
		if 'delit' in afsavedata:			   # Loeschen
			try : int(afsavedata['input']['id']['val'])
			except : afsavedata['input']['id']['val'] = 0
			if int(afsavedata['input']['id']['val']) > 0:
				try : emodel = apps.get_model(formVorlageFlat[afsavedata['id']]['app'], formVorlageFlat[afsavedata['id']]['tabelle'])
				except LookupError : return HttpResponseNotFound('<h1>Tabelle "'+formVorlageFlat[afsavedata['id']]['tabelle']+'" in App "'+formVorlageFlat[afsavedata['id']]['app']+'" nicht gefunden!</h1>')
				try : aElement = emodel.objects.get(id=int(afsavedata['input']['id']['val']))
				except : aElement = None
				if aElement:
					aElement.delete()
					LogEntry.objects.log_action(
						user_id = request.user.pk,
						content_type_id = ContentType.objects.get_for_model(aElement).pk,
						object_id = aElement.pk,
						object_repr = str(aElement),
						action_flag = DELETION
		   			)
				afsavedata['input']['id']['val'] = 0
		elif 'saveit' in afsavedata:			# Speichern
			try : int(afsavedata['input']['id']['val'])
			except : afsavedata['input']['id']['val'] = 0
			saveIt = False
			try : emodel = apps.get_model(formVorlageFlat[afsavedata['id']]['app'], formVorlageFlat[afsavedata['id']]['tabelle'])
			except LookupError : return HttpResponseNotFound('<h1>Tabelle "'+formVorlageFlat[afsavedata['id']]['tabelle']+'" in App "'+formVorlageFlat[afsavedata['id']]['app']+'" nicht gefunden!</h1>')
			if int(afsavedata['input']['id']['val']) > 0:
				aElement = emodel.objects.get(id=int(afsavedata['input']['id']['val']))
				isLoaded = True
			else:
				aElement = emodel()
				saveIt = True
				isLoaded = False
				if formVorlageFlat[afsavedata['id']]['app'] == 'PersonenDB' and formVorlageFlat[afsavedata['id']]['tabelle'] == 'tbl_termine':
					resaveit = True
			for key , value in afsavedata['input'].items():
				if key != 'id':
					if isLoaded:
						ovalue = getattr(aElement,key)
					else:
						ovalue = None
					nvalue = value['val']
					aItemData = formVorlageFlat[afsavedata['id']]['felder'][key]
					if aItemData['type'] == 'DateField' or aItemData['type'] == 'DateTimeField':
						if nvalue=='':
							nvalue = None
					if aItemData['type'] == 'ForeignKey' or aItemData['type'] == 'OneToOneField':
						if 'process' in aItemData:
							pObj , pFeld = aItemData['process'].split(':',1)
							if pObj != 'auto' and key != 'id':
								aprocForm = None
								if pObj == 'parent':
									aprocForm = flatFormularFind(sfsavedatas,afsavedata['parent'],next((item for item in afsavedata['saveafter'] if item.get("id") == afsavedata['parent']))['nr'])
								else:
									aprocForm = flatFormularFind(sfsavedatas,pObj)
								if aprocForm and int(aprocForm['input'][pFeld]['val']) > 0:
									nvalue = aprocForm['input'][pFeld]['val']
								else:
									nvalue = 0
						if ovalue:
							ovalue = ovalue.pk
						else:
							ovalue = 0
					if (aItemData['type'] == 'BooleanField' or aItemData['type'] == 'NullBooleanField') and ('feldoptionen' in aItemData and 'fxtype' in aItemData['feldoptionen'] and aItemData['feldoptionen']['fxtype']['type'] == "select"):
						if nvalue == "True":
							nvalue = True
						elif nvalue == "False":
							nvalue = False
						elif nvalue == "None":
							nvalue = None
					afsavedata['input'][key]['val'] = nvalue
					if ovalue != nvalue:
						saveIt = True
						if aItemData['type'] == 'ForeignKey' or aItemData['type'] == 'OneToOneField':
							if int(nvalue) > 0:
								setattr(aElement, key+'_id', nvalue)
							else:
								setattr(aElement, key, None)
						else:
							setattr(aElement, key, nvalue)
			if saveIt:
				aElement.save()
				LogEntry.objects.log_action(
					user_id = request.user.pk,
					content_type_id = ContentType.objects.get_for_model(aElement).pk,
					object_id = aElement.pk,
					object_repr = str(aElement),
					action_flag = CHANGE if int(afsavedata['input']['id']['val']) > 0 else ADDITION
				)
				afsavedata['input']['id']['val'] = getattr(aElement,'id') or 0
				if resaveit:
				 	resave.append(aElement)
	for aresave in resave:
		aresave.save()
	return sfsavedatas

def formularSpeichervorgang(request,formArray,primaerId,permpre):
	if not request.user.has_perm(permpre+'maskEdit') and not request.user.has_perm(permpre+'_maskAdd'):
		return httpOutput('ERROR - Keine Zugriffsrechte!')
	asaveforms = json.loads(request.POST.get('saveform'))							# Json auswerten
	formVorlageFlat = formularDaten(formArray,0,iFlat=True)							# Formulvorlage flach laden
	asavedatas = formularAuswertung(asaveforms,formVorlageFlat)						# Formulardaten auswerten
	fsavedatas = formularFlat(asavedatas)											# Formularauswertung flach machen
	#pprint.pprint(fsavedatas)
	if flatFormularError(fsavedatas):												# Fehler?
		return httpOutput('Error:'+json.dumps(flatFormularErrorTxt(fsavedatas)))
	sfsavedatas = formularSpeichern(fsavedatas,formVorlageFlat,request,permpre)		# Speichern
	return httpOutput('OK'+str(flatFormularFind(sfsavedatas,primaerId)['input']['id']['val'] or 0))

# Formular View #
def auswertungView(auswertungen,asurl,request,info='',error=''):
	aauswertung = False
	maxPerSite = 25
	isCachTagEbenen = []
	isCachTagList = False
	if len(auswertungen)==1:
		aauswertung = auswertungen[0]
	elif 'auswertung' in request.POST:
		aauswertung = next(x for x in auswertungen if x['id'] == request.POST.get('auswertung'))
	# Auswertung Ansicht
	if aauswertung:
		amodel = apps.get_model(aauswertung['app_name'], aauswertung['tabelle_name'])
		# Auswertungs Daten
		# Spezialfunktionen in "felder"
		naFelder = []
		for aFeld in aauswertung['felder']:
			if "!TagEbenen" in aFeld:
				aTagEbenenTyp = "!TagEbenenFid" if "!TagEbenenFid" in aFeld else "!TagEbenenF" if "!TagEbenenF" in aFeld else "!TagEbenen"
				from KorpusDB.models import tbl_tagebene
				for aEbene in tbl_tagebene.objects.all():
					naFelder.append(aFeld.replace(aTagEbenenTyp, aTagEbenenTyp+'='+str(aEbene.pk)+'('+aEbene.Name+')'))
					if not aEbene.pk in isCachTagEbenen:
						isCachTagEbenen.append(aEbene.pk)
			else:
				naFelder.append(aFeld)
			if "!TagListe" in aFeld:
				isCachTagList = True
		aauswertung['felder'] = naFelder
		# Sortierung laden / erstellen
		if not 'orderby' in aauswertung:
			aauswertung['orderby'] = {}
		for aFeld in aauswertung['felder']:
			if not '_set' in aFeld and not '!' in aFeld:
				if not aFeld in aauswertung['orderby']:
					aauswertung['orderby'][aFeld] = [aFeld]
		aauswertung['allcount'] = amodel.objects.count()
		# Tabelle laden mit eventuellen Relationen
		aRelated = []
		pFields = [x.name for x in amodel._meta.fields]
		for aFeld in aauswertung['felder']:
			if "__" in aFeld:
				fFeld = aFeld.split("__")[0]
			else:
				fFeld = aFeld
			if fFeld in pFields and not fFeld in aRelated:
				try:
					if(amodel._meta.get_field(fFeld).is_relation):
						aRelated.append(fFeld)
				except: pass
		if aRelated:
			adataSet = amodel.objects.select_related(*aRelated).all()
		else:
			adataSet = amodel.objects.all()
		# Filter
		afIDcount = 0
		if 'filter' in aauswertung:
			for afilterline in aauswertung['filter']:
				for afilter in afilterline:
					if not 'id' in afilter:
						afilter['id'] = 'fc'+str(afIDcount)
						afIDcount+=1
			if 'filter' in request.POST:
				afopts = json.loads(request.POST.get('filter'))
				for afilterline in aauswertung['filter']:
					for afilter in afilterline:
						for afopt in afopts:
							if afilter['id'] == afopt['id']:
								afilter['val'] = int(afopt['val'])
								if 'queryFilter' in afilter:
									adataSet = adataSet.filter(**{afilter['queryFilter']:afilter['val']})
		# Seiten
		aauswertung['count'] = adataSet.count()
		aauswertung['seiten'] = 1
		if aauswertung['count']>maxPerSite:
			aauswertung['seiten'] = math.ceil(aauswertung['count'] / maxPerSite)
		aauswertung['daten'] = []
		aauswertung['aktuelleseite'] = 1
		if 'aseite' in request.POST:
			aauswertung['aktuelleseite'] = int(request.POST.get('aseite'))
		astart = (aauswertung['aktuelleseite']-1) * maxPerSite
		aauswertung['seitenstart'] = astart
		aende = astart+maxPerSite
		if 'download' in request.POST:												# Alle Datensätze
			astart = None
			aende = None
		# Sortierung
		if 'orderby' in request.POST and request.POST.get('orderby'):
			aauswertung['aOrderby'] = request.POST.get('orderby')
			if aauswertung['aOrderby'][0] == "-":
				aauswertung['aOrderby'] = aauswertung['aOrderby'][1:]
				aauswertung['aOrderbyD'] = 'desc'
			else:
				aauswertung['aOrderbyD'] = 'asc'
			if aauswertung['aOrderby'] in aauswertung['orderby']:
				aOrderby = aauswertung['orderby'][aauswertung['aOrderby']]
				if aauswertung['aOrderbyD'] == 'desc':
					aOrderby = ['-'+x for x in aOrderby]
				adataSet = adataSet.order_by(*aOrderby)
		# Datensätze auslesen
		from KorpusDB.models import tbl_antwortentags, tbl_tagebene
		for adata in adataSet[astart:aende]:
			adataline=[]
			if isCachTagList:
				CachTagList=[]
				for xval in tbl_antwortentags.objects.filter(id_Antwort=adata.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
					aTagEbene = tbl_tagebene.objects.filter(pk=xval['id_TagEbene'])[0]
					CachTagList.append({str(aTagEbene.pk)+'|'+aTagEbene.Name:[str(x.id_Tag_id)+'|'+x.id_Tag.Tag for x in tbl_antwortentags.objects.select_related('id_Tag').filter(id_Antwort=adata.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung')]})
			if isCachTagEbenen:
				CachTagEbenen = {}
				for aEbenePk in isCachTagEbenen:
					CachTagEbenen[aEbenePk] = [str(x.id_Tag_id)+'|'+x.id_Tag.Tag for x in tbl_antwortentags.objects.select_related('id_Tag').filter(id_Antwort=adata.pk, id_TagEbene=aEbenePk).order_by('Reihung')]
			for aFeld in aauswertung['felder']:										# Felder auswerten
				xFeld = None
				if "__" in aFeld:
					aAttr = adata
					for sFeld in aFeld.split("__"):
						if sFeld[0] == "!":
							if "!TagEbenen" in sFeld:
								aEbenePk = int(sFeld.split('=')[1].split('(')[0])
								notID = 1
								if sFeld.split('=')[0][-2:] == "id":
									notID = 0
								if "!TagEbenenF" in sFeld:
									aAttr = ", ".join([x.split('|',1)[notID] for x in CachTagEbenen[aEbenePk]])
									if not aAttr:
										aAttr = None
								else:
									aAttr = str(CachTagEbenen[aEbenePk])
							elif "!TagListe" in sFeld:
								notID = 1
								if sFeld[-2:] == "id":
									notID = 0
								if "!TagListeF" in sFeld:
									aAttr = ''
									for aTags in CachTagList:
										for aEbene in aTags:
											aAttr+= aEbene.split('|',1)[notID]+': '+", ".join([x.split('|',1)[notID] for x in aTags[aEbene]])+"|"
									if not aAttr:
										aAttr = None
								else:
									aAttr = str(CachTagList)
						else:
							aAttr = getattr(aAttr, sFeld)
				else:
					aAttr = getattr(adata, aFeld)
				if isinstance(aAttr, models.Model):
					aAttr = str(aAttr)
				elif isinstance(aAttr, datetime.date) or isinstance(aAttr, datetime.datetime):
					aAttr = aAttr.isoformat()
				adataline.append(aAttr)
			aauswertung['daten'].append(adataline)
		# Download
		if 'download' in request.POST:
			# CSV
			if request.POST.get('download') == "csv":
				import csv
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="'+aauswertung['titel']+'.csv"'
				writer = csv.writer(response,delimiter=';')
				writer.writerow(aauswertung['felder'])
				for arow in aauswertung['daten']:
					writer.writerow(arow)
				return response
			elif request.POST.get('download') == "xls":
				import xlwt
				response = HttpResponse(content_type='text/ms-excel')
				response['Content-Disposition'] = 'attachment; filename="'+aauswertung['titel']+'.xls"'
				wb = xlwt.Workbook(encoding='utf-8')
				ws = wb.add_sheet(aauswertung['titel'])
				row_num = 0
				columns = [(afeld, 2000) for afeld in aauswertung['felder']]
				font_style = xlwt.XFStyle()
				font_style.font.bold = True
				for col_num in range(len(columns)):
					ws.write(row_num, col_num, columns[col_num][0], font_style)
				font_style = xlwt.XFStyle()
				for obj in aauswertung['daten']:
					row_num += 1
					row = obj
					for col_num in range(len(row)):
						ws.write(row_num, col_num, row[col_num], font_style)
				wb.save(response)
				return response
			else:
				return HttpResponseNotFound('<h1>Dateitype unbekannt!</h1>')
		# Datenliste
		if 'getdatalist' in request.POST:
			return render_to_response('DB/auswertung_datalist.html',
				RequestContext(request, {'getdatalist':1,'aauswertung':aauswertung,'asurl':asurl,'info':info,'error':error}),)
		# Auswertung Ansicht
		fmodel = apps.get_model(aauswertung['app_name'], aauswertung['tabelle_name'])
		if 'filter' in aauswertung:
			afIDcount = 0
			for afilterline in aauswertung['filter']:
				for afilter in afilterline:
					if afilter['field'][0] == '>':
						zdata = afilter['field'][1:].split('|')
						zmodel = apps.get_model(zdata[0], zdata[1])
						afilter['modelQuery'] = zmodel.objects.all()
					else:
						if afilter['field'] in pFields:
							if not 'verbose_name' in afilter:
								afilter['verbose_name'] = fmodel._meta.get_field(afilter['field']).verbose_name
							if afilter['type']=='select':
								afilter['modelQuery'] = fmodel._meta.get_field(afilter['field']).model.objects.all()
						else:
							if "__" in afilter['field']:
								zdata = fmodel
								for sFeld in afilter['field'].split("__"):
									zdata = zdata._meta.get_field(sFeld).related_model
								afilter['modelQuery'] = zdata.objects.all()
							else:
								if not 'verbose_name' in afilter:
									afilter['verbose_name'] = getattr(fmodel, afilter['field']).related.related_model._meta.verbose_name
								if afilter['type']=='select':
									afilter['modelQuery'] = getattr(fmodel, afilter['field']).related.related_model.objects.all()
					if 'modelQuery' in afilter and 'selectFilter' in afilter:
						simpleFilter = True
						for key, val in afilter['selectFilter'].items():
							if str(val)[0] == '!':
								afilter['needID'] = val[1:]
								aFilterElement = getFilterElement(aauswertung['filter'],afilter['needID'])
								if 'val' in aFilterElement:
									afilter['selectFilter'][key] = aFilterElement['val']
									afilter['modelQuery'] = afilter['modelQuery'].filter(**afilter['selectFilter'])
								else:
									afilter['modelQuery'] = []
								simpleFilter = False
						if simpleFilter:
							afilter['modelQuery'] = afilter['modelQuery'].filter(**afilter['selectFilter'])
		return render_to_response('DB/auswertung_view.html',
			RequestContext(request, {'aauswertung':aauswertung,'asurl':asurl,'info':info,'error':error}),)
	# Startseite
	for aauswertung in auswertungen:
		amodel = apps.get_model(aauswertung['app_name'], aauswertung['tabelle_name'])
		aauswertung['count'] = amodel.objects.count()
	return render_to_response('DB/auswertung_start.html',
		RequestContext(request, {'auswertungen':auswertungen,'asurl':asurl,'info':info,'error':error}),)

def getFilterElement(sAllFilter,sID):
	for sFilterline in sAllFilter:
		for sFilter in sFilterline:
			if sFilter['id'] == sID:
				return sFilter
	return False
