from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q
from django.db import connection
# from django.db.models import Count
import Datenbank.models as dbmodels
import AnnotationsDB.models as adbmodels
import json
from DB.funktionenDB import httpOutput
import datetime


def views_annosent(request):
	# Token Set löschen
	if 'delTokenSet' in request.POST:
		from .funktionenAnno import annoDelTokenSet
		return annoDelTokenSet(int(request.POST.get('tokenSetId')), adbmodels)
	# Token Set Speichern
	if 'saveTokenSet' in request.POST:
		from .funktionenAnno import annoSaveTokenSet
		return annoSaveTokenSet(json.loads(request.POST.get('tokens')), int(request.POST.get('tokenSetId')), adbmodels)
	# Antworten mit Tags speichern/ändern/löschen
	if 'saveAntworten' in request.POST:
		from .funktionenAnno import annoSaveAntworten
		annoSaveAntworten(json.loads(request.POST.get('antworten')), adbmodels, dbmodels)
	# Materialized View Informationen und Aktuallisierung
	if 'getMatViewData' in request.POST:
		if 'refresh' in request.POST and request.POST.get('refresh') == 'true':
			adbmodels.tbl_refreshlog_mat_adhocsentences.refresh()
		adavg = datetime.timedelta()
		adavgdg = 0
		for aRl in adbmodels.tbl_refreshlog_mat_adhocsentences.objects.all().order_by('-created_at')[:5]:
			adavg += aRl.duration
			adavgdg += 1
		if adavgdg > 0:
			adavg = adavg / adavgdg
		return httpOutput(json.dumps({'OK': True, 'mvDurchschnitt': adavg.total_seconds(), 'mvLastUpdate': str(adbmodels.tbl_refreshlog_mat_adhocsentences.objects.all().order_by('-created_at')[0].created_at.strftime("%d.%m.%Y %H:%M:%S"))}, 'application/json'))
	# getTokenSetsSatz
	if 'getTokenSetsSatz' in request.POST:
		from .funktionenAnno import getTokenSetsSatz
		return getTokenSetsSatz(request.POST.getlist('tokenSetsIds[]'), adbmodels)
	# getTokenSatz
	if 'getTokenSatz' in request.POST:
		from .funktionenAnno import getTokenSatz
		return getTokenSatz(request.POST.get('tokenId'), adbmodels)
	# Basisdaten für Filter laden
	if 'getBaseData' in request.POST:
		return httpOutput(json.dumps({'OK': True}, 'application/json'))
	# Einträge auslesen
	if 'getEntries' in request.POST or 'getXLS' in request.POST:
		if 'getXLS' in request.POST:
			aSeite = 0
			aEps = 999999999
		else:
			aSeite = int(request.POST.get('seite'))
			aEps = int(request.POST.get('eps'))
		aFilter = json.loads(request.POST.get('filter'))
		aSuche = json.loads(request.POST.get('suche'))
		aSortierung = json.loads(request.POST.get('sortierung'))
		aElemente = adbmodels.mat_adhocsentences.objects.all()
		# Suchen / Filtern
		aSucheMuss = []
		aSucheKann = []
		if int(aFilter['trans']) > 0:
			aSucheMuss.append(Q(transid=aFilter['trans']))
		if int(aFilter['inf']) > 0:
			aSucheMuss.append(Q(infid=aFilter['inf']))
		# [{'value': 'zwei', 'kannmuss': 'kann', 'methode': 'ci', 'name': 'sentorig'}, {'value': '', 'kannmuss': 'kann', 'methode': 'ci', 'name': 'sentorth'}, {'value': '', 'kannmuss': 'kann', 'methode': 'ci', 'name': 'sentttpos'}, {'value': '', 'kannmuss': 'kann', 'methode': 'ci', 'name': 'sentsptag'}]
		for aSuchFeld in aSuche:
			if aSuchFeld['value'].strip():
				aSuchValue = aSuchFeld['value'].strip()
				if 'regex' in aSuchFeld['methode']:
					aTyp = aSuchFeld['methode']
					aSuchValue = r"{0}".format(aSuchValue)
				else:
					aTyp = 'icontains' if aSuchFeld['methode'] == 'ci' else 'contains'
				print(aSuchFeld['methode'], aTyp)
				if aSuchFeld['kannmuss'] == 'muss':
					aSucheMuss.append(Q(**{aSuchFeld['name'] + '__' + aTyp: aSuchValue}))
				if aSuchFeld['kannmuss'] == 'nicht':
					aSucheMuss.append(~Q(**{aSuchFeld['name'] + '__' + aTyp: aSuchValue}))
				if aSuchFeld['kannmuss'] == 'kann':
					aSucheKann.append(Q(**{aSuchFeld['name'] + '__' + aTyp: aSuchValue}))
		if aSucheMuss:
			import operator
			aSucheMussX = aSucheMuss[0]
			for aMuss in aSucheMuss[1:]:
				aSucheMussX = operator.and_(aSucheMussX, aMuss)
		if aSucheKann:
			import operator
			aSucheKannX = aSucheKann[0]
			for aMuss in aSucheKann[1:]:
				aSucheKannX = operator.or_(aSucheKannX, aMuss)
		if aSucheMuss and aSucheKann:
			aElemente = aElemente.filter(aSucheMussX, aSucheKannX)
		elif aSucheMuss:
			aElemente = aElemente.filter(aSucheMussX)
		elif aSucheKann:
			aElemente = aElemente.filter(aSucheKannX)
		# Sortieren
		aElemente = aElemente.order_by(('-' if not aSortierung['asc'] else '') + aSortierung['spalte'])
		# Einträge ausgeben
		aMatIds = [aEintrag['id'] for aEintrag in aElemente.values('id')[aSeite * aEps:aSeite * aEps + aEps]]
		if 'getXLS' in request.POST:
			import xlwt
			response = HttpResponse(content_type='text/ms-excel')
			response['Content-Disposition'] = 'attachment; filename="as_' + datetime.datetime.now().today().strftime('%Y_%m_%d_%H_%M_%S') + '.xls"'
			aInfs = {aInf.id: aInf.Kuerzel for aInf in dbmodels.Informanten.objects.all()}
			aTranscripts = {aTranscript.id: aTranscript.name for aTranscript in adbmodels.transcript.objects.all()}
			aEintraege = []
			aQuery = adbmodels.mat_adhocsentences.objects.raw('''
				SELECT "mat_adhocsentences".*
				FROM "mat_adhocsentences"
				WHERE "mat_adhocsentences"."id" IN %s
				ORDER BY "mat_adhocsentences"."adhoc_sentence" ASC
			''', [tuple(aMatIds)])
			for aEintrag in aQuery:
				aEintraege.append({
					'adhoc_sentence': aEintrag.adhoc_sentence,
					'tokenids': ', '.join(str(v) for v in aEintrag.tokenids) if aEintrag.tokenids else aEintrag.tokenids,
					'inf': aInfs[aEintrag.infid],
					'infid': aEintrag.infid,
					'trans': aTranscripts[aEintrag.transid],
					'transid': aEintrag.transid,
					'tokreih': ', '.join(str(v) for v in aEintrag.tokreih) if aEintrag.tokreih else aEintrag.tokreih,
					'seqsent': ', '.join(str(v) for v in aEintrag.seqsent) if aEintrag.seqsent else aEintrag.seqsent,
					'sentorig': aEintrag.sentorig,
					'sentorth': aEintrag.sentorth,
					'left_context': aEintrag.left_context,
					'senttext': aEintrag.senttext,
					'right_context': aEintrag.right_context,
					'sentttlemma': aEintrag.sentttlemma,
					'sentttpos': aEintrag.sentttpos,
					'sentsplemma': aEintrag.sentsplemma,
					'sentsppos': aEintrag.sentsppos,
					'sentsptag': aEintrag.sentsptag,
					'sentspdep': aEintrag.sentspdep,
					'sentspenttype': aEintrag.sentspenttype
				})
			aColTitel = ['adhoc_sentence', 'inf', 'trans', 'sentorig', 'sentorth', 'left_context', 'senttext', 'right_context', 'sentttlemma', 'sentttpos', 'sentsplemma', 'sentsppos', 'sentsptag', 'sentspdep', 'sentspenttype', 'tokreih', 'seqsent', 'infid', 'transid', 'tokenids']
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('Anno-sent')
			row_num = 0
			columns = [(ct, 2000) for ct in aColTitel]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
			font_style = xlwt.XFStyle()
			for aEintrag in aEintraege:
				row_num += 1
				for cti in range(len(aColTitel)):
					ws.write(row_num, cti, aEintrag[aColTitel[cti]], font_style)
			wb.save(response)
			return response
		if not aMatIds:
			aEintraege = []
		else:
			aEintraege = [
				{
					'adhoc_sentence': aEintrag.adhoc_sentence,
					'tokenids': aEintrag.tokenids,
					'tokens': aEintrag.tokens,
					'infid': aEintrag.infid,
					'transid': aEintrag.transid,
					'tokreih': aEintrag.tokreih,
					'seqsent': aEintrag.seqsent,
					'sentorig': aEintrag.sentorig,
					'sentorth': aEintrag.sentorth,
					'left_context': aEintrag.left_context,
					'senttext': aEintrag.senttext,
					'right_context': aEintrag.right_context,
					'sentttlemma': aEintrag.sentttlemma,
					'sentttpos': aEintrag.sentttpos,
					'sentsplemma': aEintrag.sentsplemma,
					'sentsppos': aEintrag.sentsppos,
					'sentsptag': aEintrag.sentsptag,
					'sentspdep': aEintrag.sentspdep,
					'sentspenttype': aEintrag.sentspenttype
				}
				for aEintrag in adbmodels.mat_adhocsentences.objects.raw('''
					SELECT "mat_adhocsentences".*,
						(
							SELECT array_to_json(array_agg(row_to_json(atok)))
							FROM (
								SELECT "token".*,
								(
									SELECT array_to_json(array_agg(row_to_json(aantwort)))
										FROM (
											SELECT "Antworten".*,
											(
												SELECT array_to_json(array_agg(row_to_json(aAntwortenTags)))
													FROM (
														SELECT "AntwortenTags".*
														FROM "AntwortenTags"
														WHERE "AntwortenTags"."id_Antwort_id" = "Antworten"."id"
														ORDER BY "AntwortenTags"."id_TagEbene_id" ASC, "AntwortenTags"."Reihung" ASC
													) AS aAntwortenTags
											) AS AntwortenTags_raw
											FROM "Antworten"
											WHERE "Antworten"."ist_token_id" = "token"."id"
										) AS aantwort
								) AS antworten,
								(
									SELECT array_to_json(array_agg(row_to_json(atokenset)))
										FROM (
												SELECT "tokenset".*,
												(
													SELECT array_to_json(array_agg(row_to_json(aantwort)))
														FROM (
															SELECT "Antworten".*,
															(
																SELECT array_to_json(array_agg(row_to_json(aAntwortenTags)))
																	FROM (
																		SELECT "AntwortenTags".*
																		FROM "AntwortenTags"
																		WHERE "AntwortenTags"."id_Antwort_id" = "Antworten"."id"
																		ORDER BY "AntwortenTags"."id_TagEbene_id" ASC, "AntwortenTags"."Reihung" ASC
																	) AS aAntwortenTags
															) AS AntwortenTags_raw
															FROM "Antworten"
															WHERE "Antworten"."ist_tokenset_id" = "tokenset"."id"
														) AS aantwort
												) AS antworten,
												(
													SELECT array_to_json(array_agg(row_to_json(atokentoset_cache)))
														FROM (
															SELECT "tokentoset"."id_token_id"
															FROM "tokentoset"
															WHERE "tokentoset"."id_tokenset_id" = "tokenset"."id"
														) AS atokentoset_cache
												) AS tokentoset
													FROM "tokenset"
													LEFT OUTER JOIN "tokentoset" ON ( "tokenset"."id" = "tokentoset"."id_tokenset_id" )
													WHERE "tokentoset"."id_token_id" = "token"."id"
											UNION ALL
												SELECT "tokenset".*,
												(
													SELECT array_to_json(array_agg(row_to_json(aantwort)))
														FROM (
															SELECT "Antworten".*,
															(
																SELECT array_to_json(array_agg(row_to_json(aAntwortenTags)))
																	FROM (
																		SELECT "AntwortenTags".*
																		FROM "AntwortenTags"
																		WHERE "AntwortenTags"."id_Antwort_id" = "Antworten"."id"
																		ORDER BY "AntwortenTags"."id_TagEbene_id" ASC, "AntwortenTags"."Reihung" ASC
																	) AS aAntwortenTags
															) AS AntwortenTags_raw
															FROM "Antworten"
															WHERE "Antworten"."ist_tokenset_id" = "tokenset"."id"
														) AS aantwort
												) AS antworten,
												(
													SELECT array_to_json(array_agg(row_to_json(atokentoset_cache)))
														FROM (
															SELECT "tokentoset_cache"."id_token_id"
															FROM "tokentoset_cache"
															WHERE "tokentoset_cache"."id_tokenset_id" = "tokenset"."id"
														) AS atokentoset_cache
												) AS tokentoset
													FROM "tokenset"
													LEFT OUTER JOIN "tokentoset_cache" ON ( "tokenset"."id" = "tokentoset_cache"."id_tokenset_id" )
													WHERE "tokentoset_cache"."id_token_id" = "token"."id"
										) AS atokenset
								) AS tokensets
									FROM "token"
									WHERE "token"."id" = ANY("mat_adhocsentences"."tokenids")
									ORDER BY "token"."token_reihung" ASC
							) atok
						) AS "tokens"
					FROM "mat_adhocsentences"
					WHERE "mat_adhocsentences"."id" IN %s
					ORDER BY "mat_adhocsentences"."adhoc_sentence" ASC
				''', [tuple(aMatIds)])]
		# print(connection.queries)
		return httpOutput(json.dumps({'OK': True, 'seite': aSeite, 'eps': aEps, 'eintraege': aEintraege, 'zaehler': aElemente.count()}), 'application/json')
	return render_to_response('AnnotationsDB/annosent.html', RequestContext(request))
