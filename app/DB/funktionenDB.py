from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
import collections
from django.apps import apps
from copy import deepcopy
import json
import pprint

# Schneller HttpOutput
def httpOutput(aoutput):
	txtausgabe = HttpResponse(aoutput)
	txtausgabe['Content-Type'] = 'text/plain'
	return txtausgabe

# Liste der Eintraege erstellen #
def kategorienListe(amodel,suche='',inhalt='',mitInhalt=0,arequest=[]):
	ausgabe = collections.OrderedDict()
	if str(amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()) != 'CharField':
		if not inhalt:
			aElement = amodel.objects.all()
			abc = amodel._meta.get_field(amodel._meta.ordering[0]).get_internal_type()
			ausgabe[abc]={'count':aElement.count()}
			if mitInhalt>0:
				ausgabe[abc]['active'] = render_to_response('db/lmfadl.html',
					RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=abc),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			return ausgabe
		else:
			return amodel.objects.all()
	kategorien = collections.OrderedDict() ; kategorien['Andere'] = '^a-zaeoeueaeoeue' ; kategorien['istartswith'] = 'abcdefghijklmnopqrstuvwxyz' ; kategorien['ae'] = 'aeae' ; kategorien['oe'] = 'oeoe' ; kategorien['ue'] = 'ueue'
	if not inhalt: # Liste fuer Kategrien ausgeben
		for key,value in kategorien.items():
			if key == 'istartswith':
				for abc in value:
					if suche : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':abc,amodel._meta.ordering[0]+'__contains':suche})
					else : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':abc})
					ausgabe[abc] = {'count':aElement.count()}
					if mitInhalt>0:
						if aElement.filter(pk=mitInhalt).count():
							ausgabe[abc]['active'] = render_to_response('db/lmfadl.html',
								RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=abc),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
			else:
				if suche : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+value+'].+)',amodel._meta.ordering[0]+'__contains':suche})
				else : aElement = amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+value+'].+)'})
				ausgabe[key] = {'count':aElement.count()}
				if mitInhalt>0:
					if aElement.filter(pk=mitInhalt).count():
						ausgabe[key]['active'] = render_to_response('db/lmfadl.html',
							RequestContext(arequest, {'lmfadl':kategorienListe(amodel,inhalt=key),'openpk':mitInhalt,'scrollto':mitInhalt}),).content
	else: # Inhalte fuer Kategorie ausgeben
		if inhalt in kategorien : ausgabe = amodel.objects.filter(**{amodel._meta.ordering[0]+'__iregex':'^(['+kategorien[inhalt]+'].+)'})
		else : ausgabe = amodel.objects.filter(**{amodel._meta.ordering[0]+'__istartswith':inhalt})
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
def verbundeneElemente(aElement):
	usedby = []
	for f in aElement._meta.get_fields():
		if (f.one_to_many) and f.auto_created:
			usedby.append({'model_typ':'one_to_many','model_app_label':f.related_model._meta.app_label,'model_name':f.related_model.__name__,'related_name':f.related_name,'model_verbose_name':f.related_model._meta.verbose_name,'model_verbose_name':f.related_model._meta.verbose_name_plural,
				'elemente':[{'pk':o.pk,'value':str(o)} for o in getattr(aElement, f.get_accessor_name()).all()]})
		elif (f.one_to_one) and f.auto_created:
			aElemente = []
			try:
				aFieldElement = getattr(aElement, f.get_accessor_name())
				aElemente = [{'pk':aFieldElement.pk,'value':str(aFieldElement)}]
			except: pass
			usedby.append({'model_typ':'one_to_one','model_app_label':f.related_model._meta.app_label,'model_name':f.related_model.__name__,'related_name':f.related_name,'model_verbose_name':f.related_model._meta.verbose_name,'model_verbose_name':f.related_model._meta.verbose_name_plural,
				'elemente': aElemente})
	return usedby

###################
# Formular-System #
###################

# Formular View #
def formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aform,request,info='',error=''):
	amodel = apps.get_model(app_name, tabelle_name)

	# Formular speichern
	if 'saveform' in request.POST:
		return formularSpeichervorgang(request,aform,primaerId,app_name+'.'+permName)

	# Reine View oder Formular des Tabelleneintrags
	if 'gettableview' in request.POST or 'gettableeditform' in request.POST:
		aformid = request.POST.get('gettableview') or request.POST.get('gettableeditform')
		aforms = formularDaten(aform,aformid)
		# info = '<div class="code">'+pprint.pformat(aforms)+'</div>'
		return render_to_response('db/form_view.html',
			RequestContext(request, {'apk':str(aformid),'amodel_meta':amodel._meta,'aforms':aforms,'xforms':aform,'acount':0,'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'editmode':'gettableeditform' in request.POST,'info':info,'error':error}),)
	# Startseite mit Eintrag
	if 'loadpk' in request.POST:
		aformid = int(request.POST.get('loadpk'))
		aforms = formularDaten(aform,aformid)
		acontent = render_to_response('db/form_view.html',
			RequestContext(request, {'apk':str(aformid),'amodel_meta':amodel._meta,'aforms':aforms,'xforms':aform,'acount':0,'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'editmode':'gettableeditform' in request.POST,'info':info,'error':error}),).content
		return render_to_response('db/form_base_view.html',
			RequestContext(request, {'kategorien_liste':kategorienListe(amodel,mitInhalt=aformid,arequest=request).items(),'acontent':acontent,'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'amodel_count':amodel.objects.count(),'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'aktueberschrift':aktueberschrift,'asurl':asurl,'info':info,'error':error}),)

	# Startseite
	return render_to_response('db/form_base_view.html',
		RequestContext(request, {'kategorien_liste':kategorienListe(amodel).items(),'appname':app_name,'tabname':tabelle_name,'amodel_meta':amodel._meta,'amodel_count':amodel.objects.count(),'maskEdit':request.user.has_perm(app_name+'.'+permName+'_maskEdit'),'maskAdd':request.user.has_perm(app_name+'.'+permName+'_maskAdd'),'aktueberschrift':aktueberschrift,'asurl':asurl,'info':info,'error':error}),)


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
			if 'fx' in aInhalt and aInhalt['fx']:
				pass	### <--- Fuer fx Inhalte !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			else:
				aModelFeld = aModel._meta.get_field(pFeld)
				aInhalt['name'] = aModelFeld.name
				aInhalt['verbose_name'] = aModelFeld.verbose_name
				aInhalt['type'] = aModelFeld.get_internal_type()
				if aModelFeld.choices:
					aInhalt['choices'] = aModelFeld.choices
				if aInhalt['type'] == 'ForeignKey' or aInhalt['type'] == 'OneToOneField':
					aInhalt['typeoptions']={'app':aModelFeld.related_model._meta.app_label,'name':aModelFeld.related_model.__name__}
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
					aData['felder'] = aFelder
					if 'sub' in aForm:
						aData['sub'] = formularDaten(aForm['sub'],0,aFelder,iFirst=False)
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
						value['val'] = int(value['val'])
					else:
						value['val'] = None
					aformsdata['input'][key]['val'] = value['val']
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
	sfsavedatas = flatFormularSort(fsavedatas)
	for afsavedata in sfsavedatas:
		if 'delit' in afsavedata:			   # Loeschen
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