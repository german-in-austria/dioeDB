from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Count
from django.conf import settings
from django.db import connection
from django.db.models import Q
import KorpusDB.models as kdbmodels
import PersonenDB.models as pdbmodels
import AnnotationsDB.models as adbmodels
import datetime
import time
from .funktionenAnno import getAntwortenSatzUndTokens
import subprocess
import os


def views_auswertung(request, aErhebung, aTagEbene, aSeite):
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	canMakeXlsx = request.user.has_perm('AnnotationsDB.transcript_auswertung_makeXLSX')
	getXls = False
	xlsSeite = None
	xlsLaenge = None
	if 'get' in request.GET and request.GET.get('get') == 'xls':
		getXls = True
		if 'xlsseite' in request.GET and 'xlslaenge' in request.GET:
			xlsSeite = int(request.GET.get('xlsseite'))
			xlsLaenge = int(request.GET.get('xlslaenge'))
	aTagEbene = int(aTagEbene)
	aErhebung = int(aErhebung)
	aSeite = int(aSeite)
	if aTagEbene > 0 and canMakeXlsx and 'get' in request.GET and request.GET.get('get') == 'xlsfile':
		subprocess.Popen([settings.DIOEDB_DB_PYTHON, os.path.join(settings.BASE_DIR, 'manage.py'), 'auswertung_xls', str(aErhebung), str(aTagEbene)])
	# start = time.time()
	[art, data] = views_auswertung_func(aErhebung, aTagEbene, aSeite, getXls, canMakeXlsx, xlsSeite, xlsLaenge, True)
	# print('views_auswertung_func', time.time() - start)
	if art == 'xls':
		return data
	if art == 'html':
		return render_to_response('AnnotationsDB/auswertungstart.html', RequestContext(request, data))


def views_auswertung_func(aErhebung, aTagEbene, aSeite, getXls, canMakeXlsx, xlsSeite, xlsLaenge, html=False):
	# start = time.time()
	nTagEbenen = {}
	aTagEbenen = []
	with connection.cursor() as cursor:
		cursor.execute('''
			SELECT tagebene.*, (
				SELECT COUNT(DISTINCT "KorpusDB_tbl_antworten".id)
				FROM "KorpusDB_tbl_antworten"
				INNER JOIN "KorpusDB_tbl_antwortentags" ON ("KorpusDB_tbl_antworten"."id" = "KorpusDB_tbl_antwortentags"."id_Antwort_id" )
				''' + ('''INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ("KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" = "KorpusDB_tbl_antworten"."zu_Aufgabe_id")
				INNER JOIN "KorpusDB_tbl_erhebungen" ON ("KorpusDB_tbl_erhebungen"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id")''' if aErhebung > 0 else '') + '''
				WHERE "KorpusDB_tbl_antwortentags"."id_TagEbene_id" = tagebene.id
				''' + (('AND "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = ' + str(aErhebung)) if aErhebung > 0 else '') + '''
			) as count
			FROM (
				SELECT "KorpusDB_tbl_tagebene"."id", "KorpusDB_tbl_tagebene"."Name", "KorpusDB_tbl_tagebene"."Reihung"
				FROM "KorpusDB_tbl_tagebene"
				ORDER BY "KorpusDB_tbl_tagebene"."Reihung" ASC
			) as tagebene
		''')
		aTagEbenen = [{'pk': x[0], 'title': x[1], 'count': x[3]} for x in cursor.fetchall()]
	for aTE in aTagEbenen:
		nTagEbenen[aTE['pk']] = aTE['title']
	# print('Ebenen', time.time() - start)
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
							FROM "KorpusDB_tbl_tagfamilie" c
							WHERE c."id_ParentTag_id" = "KorpusDB_tbl_tags"."id"
						) as childs,
						array(
							SELECT p."id_ParentTag_id"
							FROM "KorpusDB_tbl_tagfamilie" p
							WHERE p."id_ChildTag_id" = "KorpusDB_tbl_tags"."id"
						) as parents,
						"KorpusDB_tbl_tags"."id", "KorpusDB_tbl_tags"."Tag", "KorpusDB_tbl_tags"."Tag_lang", "KorpusDB_tbl_tags"."zu_Phaenomen_id", "KorpusDB_tbl_tags"."Kommentar", "KorpusDB_tbl_tags"."AReihung", "KorpusDB_tbl_tags"."Generation"
					FROM "KorpusDB_tbl_tags"
					ORDER BY "KorpusDB_tbl_tags"."AReihung" ASC, "KorpusDB_tbl_tags"."Tag" ASC
				) as x
			''')
			allTags = {x[0]['id']: x[0] for x in cursor.fetchall()}
		nTags = {allTags[x]['id']: allTags[x]['Tag'] for x in allTags}
		# Antworten
		aAntwortenM = kdbmodels.tbl_antworten.objects.select_related('zu_Aufgabe', 'ist_token', 'von_Inf').filter(tbl_antwortentags__id_TagEbene_id=aTagEbene)
		if aErhebung > 0:
			# aAntwortenM = aAntwortenM.filter(zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh_id=aErhebung)
			aAntwortenM = aAntwortenM.filter(Q(zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh_id=aErhebung) | Q(ist_token__transcript_id__tbl_inferhebung__ID_Erh_id=aErhebung))
		aAntwortenM = aAntwortenM.distinct()
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
			# aTuLs = kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=aAntwort.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene')
			with connection.cursor() as cursor:
				cursor.execute('''
					SELECT "KorpusDB_tbl_antwortentags"."id_TagEbene_id", COUNT("KorpusDB_tbl_antwortentags"."id_TagEbene_id") AS "total"
					FROM "KorpusDB_tbl_antwortentags"
					WHERE "KorpusDB_tbl_antwortentags"."id_Antwort_id" = %s
					GROUP BY "KorpusDB_tbl_antwortentags"."id_TagEbene_id"
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
				for x in kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=aAntwort.pk, id_TagEbene=xval['id_TagEbene']).values('id_Tag_id').order_by('Reihung'):
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
				aTokens, aTokensEvent, aTokensText, aTokensOrtho, aTokensPhon, aTokensFallback, aAntwortType,
				transName, aTransId, aTransErhebung,
				aSaetze, aOrtho, aIpa, prev_text, vSatz, next_text, nSatz, o_f_token_reihung, r_f_token_reihung, o_l_token_reihung, r_l_token_reihung, o_l_token_type, transcript_id, informanten_id, aSatzAudio
			] = getAntwortenSatzUndTokens(aAntwort, adbmodels, kdbmodels)
			# print('getAntwortenSatzUndTokens', time.time() - tetstart)  # 0.002 Sek
			# Datensatz
			aTokensStart = None
			aTokensEnde = None
			if aTokensEvent and aTokensEvent[0] > 0 and aTokensEvent[-1] > 0:
				tmpEventTime = adbmodels.event.objects.filter(pk=aTokensEvent[0]).values('start_time', 'end_time')
				if tmpEventTime:
					aTokensStart = tmpEventTime[0]['start_time']
					if aTokensEvent[0] != aTokensEvent[-1]:
						tmpEventTime = adbmodels.event.objects.filter(pk=aTokensEvent[-1]).values('start_time', 'end_time')
					if tmpEventTime:
						aTokensEnde = tmpEventTime[0]['end_time']
			# print('aTokensStart, aTokensEnde', str(aTokensStart), str(aTokensEnde))
			aAuswertungen.append({
				'aNr': aNr,
				'aTrans': transName,
				'aTransId': aTransId,
				'aTransErhebung': aTransErhebung['str'] if aTransErhebung else None,
				'aAntwortId': str(aAntwort.pk),
				'aAntwortType': aAntwortType,
				'aAntwortKommentar': aAntwort.Kommentar if aAntwort.Kommentar else None,
				'aAufgabeId': aAntwort.zu_Aufgabe_id,
				'aAufgabeBeschreibung': aAntwort.zu_Aufgabe.Beschreibung_Aufgabe if aAntwort.zu_Aufgabe_id else None,
				'aAufgabeVariante': aAntwort.zu_Aufgabe.Variante if aAntwort.zu_Aufgabe_id else None,
				'aAufgabeErhebung': str(aAntwort.zu_Aufgabe.tbl_erhebung_mit_aufgaben_set.all()[0].id_Erh) if aAntwort.zu_Aufgabe_id and aAntwort.zu_Aufgabe.tbl_erhebung_mit_aufgaben_set.all().count() > 0 else None,
				'aInf': aAntwort.von_Inf.inf_sigle,
				'aInfId': aAntwort.von_Inf.pk,
				'aInfGebDatum': str(aAntwort.von_Inf.id_person.geb_datum) if aAntwort.von_Inf.id_person else None,
				'aInfWeiblich': str(aAntwort.von_Inf.id_person.weiblich) if aAntwort.von_Inf.id_person else None,
				'aInfGruppe': aAntwort.von_Inf.inf_gruppe.gruppe_bez if aAntwort.von_Inf.inf_gruppe else None,
				'aInfOrt': str(aAntwort.von_Inf.inf_ort),
				'aTokensFallback': ' '.join(str(x) if x else '…' for x in aTokensFallback),
				'aTokensText': ' '.join(str(x) if x else '…' for x in aTokensText),
				'aTokensOrtho': ' '.join(str(x) if x else '…' for x in aTokensOrtho),
				'aTokensPhon': ' '.join(str(x) if x else '…' for x in aTokensPhon),
				'aTokens': ', '.join(str(x) for x in aTokens),
				'aTokensStart': str(aTokensStart),
				'aTokensEnde': str(aTokensEnde),
				'aAntTags': aAntTags,
				'nAntTags': nAntTags,
				'aOrtho': aOrtho,
				'aIpa': aIpa,
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
			columns.append(('tErh', 2000))
			columns.append(('Informant', 2000))
			columns.append(('iId', 2000))
			columns.append(('iGebDatum', 2000))
			columns.append(('iWeiblich', 2000))
			columns.append(('iGruppe', 2000))
			columns.append(('iOrt', 2000))
			columns.append(('antId', 2000))
			columns.append(('antType', 2000))
			columns.append(('antKommentar', 2000))
			columns.append(('aufId', 2000))
			columns.append(('aufBe', 2000))
			columns.append(('aufVar', 2000))
			columns.append(('aufErh', 2000))
			columns.append(('vorheriger Satz', 2000))
			columns.append(('Sätze', 2000))
			columns.append(('nächster Satz', 2000))
			columns.append(('Sätze in Ortho', 2000))
			columns.append(('Sätze in IPA', 2000))
			columns.append(('Ausgewählte Tokens', 2000))
			columns.append(('text (lu)', 2000))
			columns.append(('ortho', 2000))
			columns.append(('phon', 2000))
			columns.append(('Ausgewählte Tokens (Id)', 2000))
			columns.append(('aTokensStart', 2000))
			columns.append(('aTokensEnde', 2000))
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
				ws.write(row_num, 0, xls_max_chars(obj['aNr']), font_style)
				ws.write(row_num, 1, xls_max_chars(obj['aTrans']), font_style)
				ws.write(row_num, 2, xls_max_chars(obj['aTransId']), font_style)
				ws.write(row_num, 3, xls_max_chars(obj['aTransErhebung']), font_style)
				ws.write(row_num, 4, xls_max_chars(obj['aInf']), font_style)
				ws.write(row_num, 5, xls_max_chars(obj['aInfId']), font_style)
				ws.write(row_num, 6, xls_max_chars(obj['aInfGebDatum']), font_style)
				ws.write(row_num, 7, xls_max_chars(obj['aInfWeiblich']), font_style)
				ws.write(row_num, 8, xls_max_chars(obj['aInfGruppe']), font_style)
				ws.write(row_num, 9, xls_max_chars(obj['aInfOrt']), font_style)
				ws.write(row_num, 10, xls_max_chars(int(obj['aAntwortId'])), font_style)
				ws.write(row_num, 11, xls_max_chars(obj['aAntwortType']), font_style)
				ws.write(row_num, 12, xls_max_chars(obj['aAntwortKommentar']), font_style)
				ws.write(row_num, 13, xls_max_chars(int(obj['aAufgabeId'])) if obj['aAufgabeId'] else None, font_style)
				ws.write(row_num, 14, xls_max_chars(obj['aAufgabeBeschreibung']), font_style)
				ws.write(row_num, 15, xls_max_chars(int(obj['aAufgabeVariante'])) if obj['aAufgabeVariante'] else None, font_style)
				ws.write(row_num, 16, xls_max_chars(obj['aAufgabeErhebung']), font_style)
				ws.write(row_num, 17, xls_max_chars(obj['vSatz']), font_style)
				ws.write(row_num, 18, xls_max_chars(obj['aSaetze']), font_style)
				ws.write(row_num, 19, xls_max_chars(obj['nSatz']), font_style)
				ws.write(row_num, 20, xls_max_chars(obj['aOrtho']), font_style)
				ws.write(row_num, 21, xls_max_chars(obj['aIpa']), font_style)
				ws.write(row_num, 22, xls_max_chars(obj['aTokensFallback']), font_style)
				ws.write(row_num, 23, xls_max_chars(obj['aTokensText']), font_style)
				ws.write(row_num, 24, xls_max_chars(obj['aTokensOrtho']), font_style)
				ws.write(row_num, 25, xls_max_chars(obj['aTokensPhon']), font_style)
				ws.write(row_num, 26, xls_max_chars(obj['aTokens']), font_style)
				ws.write(row_num, 27, xls_max_chars(obj['aTokensStart']), font_style)
				ws.write(row_num, 28, xls_max_chars(obj['aTokensEnde']), font_style)
				if obj['aAntTags']:
					ws.write(row_num, 29, xls_max_chars(obj['aAntTags']['t']), font_style)
				dg = 0
				for nATT in nAntTagsTitle:
					if nATT['i'] in obj['nAntTags']:
						ws.write(row_num, 30 + dg, xls_max_chars(obj['nAntTags'][nATT['i']]['t']), font_style)
					dg += 1
			if html:
				wb.save(response)
				return ['xls', response]
			else:
				return ['xlsdata', wb]
	return ['html', {'aErhebung': aErhebung, 'aErhebungen': [{'pk': aErh.id, 'title': str(aErh)} for aErh in kdbmodels.tbl_erhebungen.objects.all()], 'aTagEbene': aTagEbene, 'prev': prev, 'next': next, 'tagEbenen': aTagEbenen, 'aAuswertungen': aAuswertungen, 'aAntTagsTitle': aAntTagsTitle, 'nAntTagsTitle': nAntTagsTitle, 'aCount': aCount, 'canMakeXlsx': canMakeXlsx}]


def xls_max_chars(aVal):
	"""Bei String Länge auf maximum setzen."""
	if type(aVal) == str and len(aVal) > 32600:
		return 'err: too long! - ' + aVal[:32600] + '...'
	else:
		return aVal
