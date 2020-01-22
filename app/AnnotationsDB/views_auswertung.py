from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Count
from django.conf import settings
from django.db import connection
import Datenbank.models as dbmodels
import AnnotationsDB.models as adbmodels
import datetime
import time
from .funktionenAnno import getAntwortenSatzUndTokens
import subprocess
import os


def views_auswertung(request, aTagEbene, aSeite):
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	getXls = False
	xlsSeite = None
	xlsLaenge = None
	if 'get' in request.GET and request.GET.get('get') == 'xls':
		getXls = True
		if 'xlsseite' in request.GET and 'xlslaenge' in request.GET:
			xlsSeite = int(request.GET.get('xlsseite'))
			xlsLaenge = int(request.GET.get('xlslaenge'))
	aTagEbene = int(aTagEbene)
	aSeite = int(aSeite)
	if aTagEbene > 0 and 'get' in request.GET and request.GET.get('get') == 'xlsfile':
		subprocess.Popen([settings.DISS_DB_PYTHON, os.path.join(settings.BASE_DIR, 'manage.py'), 'auswertung_xls', str(aTagEbene)])
	[art, data] = views_auswertung_func(aTagEbene, aSeite, getXls, xlsSeite, xlsLaenge, True)
	if art == 'xls':
		return data
	if art == 'html':
		return render_to_response('AnnotationsDB/auswertungstart.html', RequestContext(request, data))


def views_auswertung_func(aTagEbene, aSeite, getXls, xlsSeite, xlsLaenge, html=False):
	nTagEbenen = {}
	aTagEbenen = []
	for aTE in dbmodels.TagEbene.objects.all().order_by('Reihung'):
		nTagEbenen[aTE.pk] = str(aTE)
		aTagEbenen.append({'pk': aTE.pk, 'title': str(aTE), 'count': dbmodels.Antworten.objects.filter(
			antwortentags__id_TagEbene_id=aTE.pk).distinct().count()}
		)
	aAuswertungen = []
	aAntTagsTitle = None
	nAntTagsTitle = None
	prev = -1
	next = -1
	aCount = 0
	if aTagEbene > 0:
		maxPerPage = 15
		# Tags
		with connection.cursor() as cursor:
			cursor.execute('''
				SELECT to_json(x.*)
				FROM (
					SELECT
						array(
							SELECT c."id_ChildTag_id"
							FROM "TagFamilie" c
							WHERE c."id_ParentTag_id" = "Tags"."id"
						) as childs,
						array(
							SELECT p."id_ParentTag_id"
							FROM "TagFamilie" p
							WHERE p."id_ChildTag_id" = "Tags"."id"
						) as parents,
						"Tags"."id", "Tags"."Tag", "Tags"."Tag_lang", "Tags"."zu_Tag_id", "Tags"."zu_Phaenomen_id", "Tags"."Kommentar", "Tags"."AReihung", "Tags"."Generation"
					FROM "Tags"
					ORDER BY "Tags"."AReihung" ASC, "Tags"."Tag" ASC
				) as x
			''')
			allTags = {x[0]['id']: x[0] for x in cursor.fetchall()}
		nTags = {allTags[x]['id']: allTags[x]['Tag'] for x in allTags}
		# Antworten
		aAntwortenM = dbmodels.Antworten.objects.filter(
			antwortentags__id_TagEbene_id=aTagEbene
		).distinct()
		aCount = aAntwortenM.count()
		# Seiten
		if aSeite > 0:
			prev = aSeite - 1
		if aCount > (aSeite + 1) * maxPerPage:
			next = aSeite + 1
		# Antworten ... weiter
		aAntTagsTitle = nTagEbenen[aTagEbene]
		nAntTagsTitle = []
		aNr = aSeite * maxPerPage
		if xlsSeite and xlsLaenge:
			aSeite = xlsSeite - 1
			maxPerPage = xlsLaenge
		# start = time.time()
		for aAntwort in aAntwortenM if getXls and not (xlsSeite and xlsLaenge) else aAntwortenM[aSeite * maxPerPage:aSeite * maxPerPage + maxPerPage]:
			aNr += 1
			# Tag Ebene mit Tags
			# tetstart = time.time()
			nAntTags = {}
			aAntTags = None
			# aTuLs = dbmodels.AntwortenTags.objects.filter(id_Antwort=aAntwort.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene')
			with connection.cursor() as cursor:
				cursor.execute('''
					SELECT "AntwortenTags"."id_TagEbene_id", COUNT("AntwortenTags"."id_TagEbene_id") AS "total"
					FROM "AntwortenTags"
					WHERE "AntwortenTags"."id_Antwort_id" = %s
					GROUP BY "AntwortenTags"."id_TagEbene_id"
				''', [aAntwort.pk])
				aTuL = [{'id_TagEbene': x[0], 'total': x[1]} for x in cursor.fetchall()]
			# Tagebenen sortieren
			aTuLs = []
			for aTE in aTagEbenen:
				for aTuLx in aTuL:
					if aTE['pk'] == aTuLx['id_TagEbene']:
						aTuLs.append(aTuLx)
			# Tags der Tagebenen auflisten
			for xval in aTuLs:
				xDat = {'e': {'t': nTagEbenen[xval['id_TagEbene']], 'i': xval['id_TagEbene']}}
				xDat['t'] = ''
				dg = 0
				afam = []
				aGen = 0
				for x in dbmodels.AntwortenTags.objects.filter(id_Antwort=aAntwort.pk, id_TagEbene=xval['id_TagEbene']).values('id_Tag_id').order_by('Reihung'):
					xTag = allTags[x['id_Tag_id']]
					try:
						while not afam[-1]['id'] in xTag['parents']:
							aGen -= 1
							del afam[-1]
					except:
						pass
					afam.append(xTag)
					if dg > 0:
						if aGen == 0:
							xDat['t'] += '|'
						elif aGen == 1:
							xDat['t'] += ';'
						elif aGen == 2:
							xDat['t'] += ','
						else:
							xDat['t'] += ' '
					xDat['t'] += nTags[x['id_Tag_id']]
					aGen += 1
					dg += 1
				if xval['id_TagEbene'] == aTagEbene:
					aAntTags = xDat
				else:
					nAntTags[xDat['e']['i']] = xDat
					if xDat['e'] not in nAntTagsTitle:
						nAntTagsTitle.append(xDat['e'])
			# print('Tag Ebene mit Tags', time.time() - tetstart)  # 0.004 Sek
			# tetstart = time.time()
			[
				aTokens, aTokensText, aTokensOrtho, aAntwortType,
				transName, aTransId,
				aSaetze, aOrtho, prev_text, vSatz, next_text, nSatz, o_f_token_reihung, r_f_token_reihung, o_l_token_reihung, r_l_token_reihung, o_l_token_type, transcript_id, informanten_id
			] = getAntwortenSatzUndTokens(aAntwort, adbmodels)
			# print('getAntwortenSatzUndTokens', time.time() - tetstart)  # 0.002 Sek
			# Datensatz
			aAuswertungen.append({
				'aNr': aNr,
				'aTrans': transName,
				'aTransId': aTransId,
				'aAntwortId': str(aAntwort.pk),
				'aAntwortType': aAntwortType,
				'aAufgabeId': aAntwort.zu_Aufgabe_id,
				'aAufgabeBeschreibung': aAntwort.zu_Aufgabe.Beschreibung_Aufgabe if aAntwort.zu_Aufgabe_id else None,
				'aAufgabeVariante': aAntwort.zu_Aufgabe.Variante if aAntwort.zu_Aufgabe_id else None,
				'aInf': aAntwort.von_Inf.Kuerzel,
				'aInfId': aAntwort.von_Inf.pk,
				'aTokensText': ' '.join(str(x) for x in aTokensText),
				'aTokens': ', '.join(str(x) for x in aTokens),
				'aAntTags': aAntTags,
				'nAntTags': nAntTags,
				'aOrtho': aOrtho,
				'aSaetze': aSaetze,
				'vSatz': vSatz,
				'nSatz': nSatz
			})
		# print('aAuswertungen', time.time() - start)  # 1,7 Sekunden -> 1,1 Sekunden
		if getXls:
			import xlwt
			response = HttpResponse(content_type='text/ms-excel')
			response['Content-Disposition'] = 'attachment; filename="tagebene_' + str(aTagEbene) + '_' + datetime.date.today().strftime('%Y%m%d_%H%M%S') + (('_' + str(xlsSeite) + '_' + str(xlsLaenge)) if xlsSeite and xlsLaenge else '') + '.xls"'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet(aAntTagsTitle)
			row_num = 0
			columns = []
			columns.append(('Nr', 2000))
			columns.append(('Transkript', 2000))
			columns.append(('tId', 2000))
			columns.append(('Informant', 2000))
			columns.append(('iId', 2000))
			columns.append(('antId', 2000))
			columns.append(('antType', 2000))
			columns.append(('aufId', 2000))
			columns.append(('aufBe', 2000))
			columns.append(('aufVar', 2000))
			columns.append(('vorheriger Satz', 2000))
			columns.append(('Sätze', 2000))
			columns.append(('nächster Satz', 2000))
			columns.append(('Sätze in Ortho', 2000))
			columns.append(('Ausgewählte Tokens', 2000))
			columns.append(('Ausgewählte Tokens (Id)', 2000))
			columns.append((aAntTagsTitle, 2000))
			for nATT in nAntTagsTitle:
				columns.append((nATT['t'], 2000))
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
			font_style = xlwt.XFStyle()
			for obj in aAuswertungen:
				row_num += 1
				ws.write(row_num, 0, obj['aNr'], font_style)
				ws.write(row_num, 1, obj['aTrans'], font_style)
				ws.write(row_num, 2, obj['aTransId'], font_style)
				ws.write(row_num, 3, obj['aInf'], font_style)
				ws.write(row_num, 4, obj['aInfId'], font_style)
				ws.write(row_num, 5, int(obj['aAntwortId']), font_style)
				ws.write(row_num, 6, obj['aAntwortType'], font_style)
				ws.write(row_num, 7, int(obj['aAufgabeId']) if obj['aAufgabeId'] else None, font_style)
				ws.write(row_num, 8, obj['aAufgabeBeschreibung'], font_style)
				ws.write(row_num, 9, int(obj['aAufgabeVariante']) if obj['aAufgabeVariante'] else None, font_style)
				ws.write(row_num, 10, obj['vSatz'], font_style)
				ws.write(row_num, 11, obj['aSaetze'], font_style)
				ws.write(row_num, 12, obj['nSatz'], font_style)
				ws.write(row_num, 13, obj['aOrtho'], font_style)
				ws.write(row_num, 14, obj['aTokensText'], font_style)
				ws.write(row_num, 15, obj['aTokens'], font_style)
				if obj['aAntTags']:
					ws.write(row_num, 16, obj['aAntTags']['t'], font_style)
				dg = 0
				for nATT in nAntTagsTitle:
					if nATT['i'] in obj['nAntTags']:
						ws.write(row_num, 17 + dg, obj['nAntTags'][nATT['i']]['t'], font_style)
					dg += 1
			if html:
				wb.save(response)
				return ['xls', response]
			else:
				return ['xlsdata', wb]
	return ['html', {'aTagEbene': aTagEbene, 'prev': prev, 'next': next, 'tagEbenen': aTagEbenen, 'aAuswertungen': aAuswertungen, 'aAntTagsTitle': aAntTagsTitle, 'nAntTagsTitle': nAntTagsTitle, 'aCount': aCount}]
