from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db import models
from django.apps import apps
from django.db.models import Count
from copy import deepcopy
import json
import datetime
import math
from django.db import connection, reset_queries
from KorpusDB.models import tbl_antwortentags, tbl_tagebene

# Formular View #
def auswertungView(auswertungen,asurl,request,info='',error=''):
	aauswertung = False
	maxPerSite = 25
	maxPerQuery = 500
	isCachTagEbenen = []
	isCachTagList = []
	isCachTagListPk = {}
	if len(auswertungen)==1:
		aauswertung = auswertungen[0]
	elif 'auswertung' in request.POST:
		aauswertung = next(x for x in auswertungen if x['id'] == request.POST.get('auswertung'))
	# Auswertung Ansicht
	if aauswertung:
		amodel = apps.get_model(aauswertung['app_name'], aauswertung['tabelle_name'])
		aRelated = []
		aPreRelated = []
		# Auswertungs Daten
		# Spezialfunktionen in "felder"
		naFelder = []
		for aFeld in aauswertung['felder']:
			if "!TagEbenen" in aFeld:
				aTagEbenenTyp = "!TagEbenenFid" if "!TagEbenenFid" in aFeld else "!TagEbenenF" if "!TagEbenenF" in aFeld else "!TagEbenen"
				for aEbene in tbl_tagebene.objects.all():
					naFelder.append(aFeld.replace(aTagEbenenTyp, aTagEbenenTyp+'='+str(aEbene.pk)+'('+aEbene.Name+')'))
					if not aEbene.pk in isCachTagEbenen:
						isCachTagEbenen.append(aEbene.pk)
				if isCachTagEbenen:
					from django.db.models import Prefetch
					emptyCachTagEbenen={}
					for aEbenePk in isCachTagEbenen:
						emptyCachTagEbenen[aEbenePk] = []
					aPreRelated.append('tbl_antwortentags_set__id_Tag')
			else:
				naFelder.append(aFeld)
			if "!TagListe" in aFeld:
				for aEbene in tbl_tagebene.objects.order_by('Reihung').all():
					if not aEbene.pk in isCachTagList:
						isCachTagList.append(aEbene.pk)
						isCachTagListPk[aEbene.pk] = str(aEbene)
				aPreRelated.append('tbl_antwortentags_set__id_Tag')
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
		pFields = [x.name for x in amodel._meta.fields]
		for aFeld in aauswertung['felder']:
			if "__" in aFeld:
				fFeld = aFeld.split("__")
			else:
				fFeld = [aFeld]
			if fFeld[0] in pFields:
				lFeld = ''
				cDg = 0
				rmodel = amodel
				for cFeld in fFeld:
					lFeld+=('__' if cDg>0 else '')+cFeld
					try:
						if not cFeld[-3:]=='_id' and rmodel._meta.get_field(cFeld).is_relation:
							try:
								if not lFeld in aRelated:
									aRelated.append(lFeld)
								rmodel = rmodel._meta.get_field(cFeld).related_model()
							except:
								break
					except: pass
					cDg+=1
		if aRelated:
			adataSet = amodel.objects.select_related(*aRelated).prefetch_related(*aPreRelated).all()
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
		repeatIt = 1
		tstart = astart
		tende = aende
		if aende == None:
			if tstart == None:
				tstart = 0
			aende = adataSet.count()
			tende = aende
			if tende>maxPerQuery:
				tende = maxPerQuery
		while repeatIt == 1:
			for adata in adataSet[tstart:tende]:
				# conqueri = connection.queries
				# print(conqueri)
				# print(len(conqueri))
				# reset_queries()
				# print('reset_queries()')
				adataline=[]
				if isCachTagList:
					CachTagList=[]
					XCachTagList = {}
					for xval in adata.tbl_antwortentags_set.all():
						if not xval.id_TagEbene_id in XCachTagList:
							XCachTagList[xval.id_TagEbene_id] = []
						XCachTagList[xval.id_TagEbene_id].append(str(xval.id_Tag_id)+'|'+xval.id_Tag.Tag)
					for aEbene in isCachTagList:
						if aEbene in XCachTagList:
							CachTagList.append({str(aEbene)+'|'+isCachTagListPk[aEbene]:XCachTagList[aEbene]})
				if isCachTagEbenen:
					CachTagEbenen = deepcopy(emptyCachTagEbenen)
					for aTags in adata.tbl_antwortentags_set.all():
						CachTagEbenen[aTags.id_TagEbene_id].append(str(aTags.id_Tag_id)+'|'+aTags.id_Tag.Tag)
				for aFeld in aauswertung['felder']:										# Felder auswerten
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
								try:
									aAttr = getattr(aAttr, sFeld)
								except:
									aAttr = None
									break
					else:
						try:
							aAttr = getattr(adata, aFeld)
						except:
							aAttr = None
					if isinstance(aAttr, models.Model):
						aAttr = str(aAttr)
					elif isinstance(aAttr, datetime.date) or isinstance(aAttr, datetime.datetime):
						aAttr = aAttr.isoformat()
					adataline.append(aAttr)
				aauswertung['daten'].append(adataline)
			if tende >= aende:
				repeatIt = 0
			else:
				tstart = tende
				tende = tstart+maxPerQuery
				if tende > aende:
					tende = aende
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
