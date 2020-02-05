"""Anzeige für AnnotationsTool."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.db.models.functions import Length
import KorpusDB.models as kdbmodels
import PersonenDB.models as pdbmodels
import AnnotationsDB.models as adbmodels
import json
from DB.funktionenDB import httpOutput
import operator
from copy import deepcopy
import datetime

spuren = [
	{'title': 'text', 'field': ['t'], 'default': {}},
	{'title': 'ortho', 'field': ['o'], 'default': {'text': ['o', 't']}},
	{'title': 'text_in_ortho', 'field': ['to'], 'dontshow': True},
	{'title': 'phon', 'field': ['ph']},
	{'title': 'ttpos', 'field': ['ttp']},
	{'title': 'ttlemma', 'field': ['ttl']},
	{'title': 'ttcheckword', 'field': ['ttcw']},
	{'title': 'sppos', 'field': ['spp']},
	{'title': 'sptag', 'field': ['spt']},
	{'title': 'splemma', 'field': ['spl']},
	{'title': 'spdep', 'field': ['spd']},
	{'title': 'sphead', 'field': ['sph']},
	{'title': 'spenttype', 'field': ['spet']}
]


def views_annotool(request, ipk=0, tpk=0):
	"""Daten für AnnotationsTool ausgeben."""
	ipk = int(ipk)
	tpk = int(tpk)
	# Speichern:
	if 'speichern' in request.POST:
		sData = json.loads(request.POST.get('speichern'))
		sData['errors'] = []
		print(sData)
		# deletedTokenSets löschen:
		if 'deletedTokenSets' in sData and sData['deletedTokenSets']:
			for key in sData['deletedTokenSets']:
				aId = key
				if aId > 0:
					try:
						adbmodels.tbl_tokenset.objects.get(id=aId).delete()
					except Exception as e:
						sData['errors'].append({'type': 'deletedTokenSets', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
		# changedTokens speichern:
		if 'changedTokens' in sData and sData['changedTokens']:
			for key, value in sData['changedTokens'].items():
				try:
					aId = int(key)
					aElement = adbmodels.token.objects.get(id=aId)
					for aSpur in spuren:
						setattr(aElement, aSpur['title'], (value[aSpur['field'][0]] if aSpur['field'][0] in value else None))
					setattr(aElement, 'token_type_id_id', (value['tt'] if 'tt' in value else None))
					setattr(aElement, 'token_reihung', (value['tr'] if 'tr' in value else None))
					setattr(aElement, 'event_id_id', (value['e'] if 'e' in value else None))
					setattr(aElement, 'ID_Inf_id', (value['i'] if 'i' in value else None))
					setattr(aElement, 'sentence_id_id', (value['s'] if 's' in value else None))
					setattr(aElement, 'sequence_in_sentence', (value['sr'] if 'sr' in value else None))
					setattr(aElement, 'fragment_of_id', (value['fo'] if 'fo' in value else None))
					setattr(aElement, 'likely_error', (value['le'] if 'le' in value else False))
					aElement.save()
					value['saved'] = True
				except Exception as e:
					sData['errors'].append({'type': 'changedTokens', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
		# changedTokenSets speichern:
		if 'changedTokenSets' in sData and sData['changedTokenSets']:
			for key, value in sData['changedTokenSets'].items():
				error = False
				try:
					aId = int(key)
					if aId > 0:
						aElement = adbmodels.tbl_tokenset.objects.get(id=aId)
					else:
						aElement = adbmodels.tbl_tokenset()
					setattr(aElement, 'id_von_token_id', (value['ivt'] if 'ivt' in value else None))
					setattr(aElement, 'id_bis_token_id', (value['ibt'] if 'ibt' in value else None))
					aElement.save()
				except Exception as e:
					error = True
					sData['errors'].append({'type': 'changedTokenSets', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
				if not error:
					value['nId'] = aElement.pk
					if 't' in value:
						for aTokenId in value['t']:
							try:
								try:
									aTokenToSet = adbmodels.tbl_tokentoset.objects.get(id_tokenset=value['nId'], id_token=aTokenId)
								except adbmodels.tbl_tokentoset.DoesNotExist:
									aTokenToSet = adbmodels.tbl_tokentoset()
									setattr(aTokenToSet, 'id_tokenset_id', value['nId'])
									setattr(aTokenToSet, 'id_token_id', aTokenId)
									aTokenToSet.save()
							except Exception as e:
								error = True
								sData['errors'].append({'type': 'changedTokenSets', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
						# tbl_tokentoset löschen wenn nicht mehr vorhanden:
						aTokenToSets = adbmodels.tbl_tokentoset.objects.filter(id_tokenset=value['nId'])
						for aTokenToSet in aTokenToSets:
							if aTokenToSet.id_token_id not in value['t']:
								aTokenToSet.delete()
					if not error:
						value['saved'] = True
					else:
						aElement.delete()
		# deletedAntworten löschen:
		if 'deletedAntworten' in sData and sData['deletedAntworten']:
			for key in sData['deletedAntworten']:
				aId = key
				if aId > 0:
					try:
						kdbmodels.tbl_antworten.objects.get(id=aId).delete()
					except Exception as e:
						sData['errors'].append({'type': 'deletedAntworten', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
		# changedAntworten speichern:
		if 'changedAntworten' in sData and sData['changedAntworten']:
			for key, value in sData['changedAntworten'].items():
				error = False
				aId = int(key)
				try:
					if aId > 0:
						aElement = kdbmodels.tbl_antworten.objects.get(id=aId)
					else:
						aElement = kdbmodels.tbl_antworten()
					setattr(aElement, 'von_Inf_id', (value['vi'] if 'vi' in value else None))
					if 'inat' in value:
						setattr(aElement, 'ist_nat', value['inat'])
					if 'is' in value:
						setattr(aElement, 'ist_Satz_id', value['is'])
					if 'ibfl' in value:
						setattr(aElement, 'ist_bfl', value['ibfl'])
					if 'it' in value:
						setattr(aElement, 'ist_token_id', value['it'])
					if 'its' in value:
						if ('changedTokenSets' in sData and str(value['its']) in sData['changedTokenSets'] and 'nId' in sData['changedTokenSets'][str(value['its'])]):
							setattr(aElement, 'ist_tokenset_id', sData['changedTokenSets'][str(value['its'])]['nId'])
							sData['changedAntworten'][key]['its'] = sData['changedTokenSets'][str(value['its'])]['nId']
						else:
							setattr(aElement, 'ist_tokenset_id', value['its'])
					if 'bds' in value:
						setattr(aElement, 'bfl_durch_S', value['bds'])
					setattr(aElement, 'start_Antwort', datetime.timedelta(microseconds=int(value['sa'] if 'sa' in value else 0)))
					setattr(aElement, 'stop_Antwort', datetime.timedelta(microseconds=int(value['ea'] if 'ea' in value else 0)))
					if 'k' in value:
						setattr(aElement, 'Kommentar', value['k'])
					aElement.save()
					value['nId'] = aElement.pk
					value['saved'] = True
				except Exception as e:
					error = True
					sData['errors'].append({'type': 'changedAntworten', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
				# AntwortenTags speichern
				if not error and 'tags' in value:
					try:
						if value['tags']:
							for eValue in value['tags']:
								aEbene = eValue['e']
								if aEbene > 0:
									for antwortenTag in kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=value['nId'], id_TagEbene=aEbene):
										delIt = True
										for tValue in eValue['t']:
											if int(tValue['i']) == antwortenTag.pk:
												delIt = False
										if delIt:
											antwortenTag.delete()
								reihung = 0
								if aEbene > 0:
									for tValue in eValue['t']:
										tagId = int(tValue['i'])
										if tagId > 0:
											aElement = kdbmodels.tbl_antwortentags.objects.get(id=tagId)
										else:
											aElement = kdbmodels.tbl_antwortentags()
										setattr(aElement, 'id_Antwort_id', value['nId'])
										setattr(aElement, 'id_Tag_id', tValue['t'])
										setattr(aElement, 'id_TagEbene_id', aEbene)
										setattr(aElement, 'Reihung', reihung)
										reihung += 1
										aElement.save()
								else:
									for tValue in eValue['t']:
										tagId = int(tValue['i'])
										if tagId > 0:
											aElement = kdbmodels.tbl_antwortentags.objects.get(id=tagId)
											aElement.delete()
					except Exception as e:
						error = True
						sData['errors'].append({'type': 'changedAntwortenTags', 'id': aId, 'error': str(type(e)) + ' - ' + str(e)})
					# Aktuelle AntwortenTags laden
					nAntTags = []
					for xval in kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=value['nId']).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
						nAntTags.append({'e': xval['id_TagEbene'], 't': getTagFamilie(kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=value['nId'], id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
					del sData['changedAntworten'][key]['tags']
					sData['changedAntworten'][key]['pt'] = nAntTags
		return httpOutput(json.dumps({'OK': True, 'gespeichert': sData}), 'application/json')
	# Transkript:
	if 'getTranskript' in request.POST:
		tpk = int(request.POST.get('getTranskript'))
	if tpk > 0:
		maxQuerys = 250
		dataout = {}
		# Startinformationen laden: (transcript, EinzelErhebung, Informanten, Saetze)
		if 'aType' in request.POST and request.POST.get('aType') == 'start':
			aTranskriptData = adbmodels.transcript.objects.get(pk=tpk)
			aTranskript = {
				'pk': aTranskriptData.pk,
				'ut': aTranskriptData.update_time.strftime("%d.%m.%Y- %H:%M"),
				'n': aTranskriptData.name,
				'dt': aTranskriptData.default_tier,
				'allTracks': spuren,
				'usedTracks': [],
				'tiers': [{'pk': aTD.id, 'tier_name': aTD.tier_name} for aTD in aTranskriptData.tbl_tier_set.all()]
			}
			# import time
			# start = time.time()
			for aSpur in spuren:
				if 'dontshow' not in aSpur or not aSpur['dontshow']:
					if adbmodels.token.objects.annotate(ortho_len=Length(aSpur['title'])).filter(transcript_id_id=tpk, ortho_len__gt=0).count() > 0:
						aTranskript['usedTracks'].append(aSpur['field'][0])
			aSpurDefault = aTranskript['allTracks'][0]
			for aSpur in aTranskript['allTracks']:
				aSpur['show'] = aSpur['field'][0] in aTranskript['usedTracks']
				# default Tier ermitteln:
				if aSpur['title'] == aTranskript['dt']:
					aSpurDefault = aSpur
				if 'default' in aSpur and aTranskript['dt'] in aSpur['default']:
					aSpur['field'] = aSpur['default'][aTranskript['dt']]
			aTranskript['allTracks'].insert(0, aTranskript['allTracks'].pop(aTranskript['allTracks'].index(aSpurDefault)))
			# print(aTranskript['allTracks'])
			# print(time.time() - start, 'Sec. - ', aTranskript['usedTracks'])
			aEinzelErhebung = {}
			aEinzelErhebungData = kdbmodels.tbl_inferhebung.objects.filter(id_Transcript_id=tpk)
			if aEinzelErhebungData:
				aEinzelErhebungData = aEinzelErhebungData[0]
				aEinzelErhebung = {
					'pk': aEinzelErhebungData.pk, 'trId': aEinzelErhebungData.id_Transcript_id, 'd': aEinzelErhebungData.Datum.strftime("%d.%m.%Y- %H:%M"), 'e': aEinzelErhebungData.Explorator_id, 'k': aEinzelErhebungData.Kommentar,
					'dp': aEinzelErhebungData.Dateipfad, 'af': aEinzelErhebungData.Audiofile,
					'lf': aEinzelErhebungData.Logfile, 'o': aEinzelErhebungData.Ort_id, 'b': aEinzelErhebungData.Besonderheiten}
			aTokenTypes = {}
			for aTokenType in adbmodels.token_type.objects.filter(token__transcript_id_id=tpk):
				aTokenTypes[aTokenType.pk] = {'n': aTokenType.token_type_name}
			aInformanten = {}
			for aInf in adbmodels.token.objects.filter(transcript_id_id=tpk).values('ID_Inf').annotate(total=Count('ID_Inf')).order_by('ID_Inf'):
				aInfM = pdbmodels.tbl_informanten.objects.get(id=aInf['ID_Inf'])
				aInformanten[aInfM.pk] = {'k': aInfM.inf_sigle, 'ka': aInfM.inf_sigle}
			aSaetze = {}
			for aSatz in kdbmodels.tbl_saetze.objects.filter(token__transcript_id_id=tpk):
				aSaetze[aSatz.pk] = {'t': aSatz.Transkript, 's': aSatz.Standardorth, 'k': aSatz.Kommentar}
			aTmNr = int(adbmodels.event.objects.prefetch_related('rn_token_event_id').filter(rn_token_event_id__transcript_id_id=tpk).distinct().order_by('start_time').count() / maxQuerys)
			dataout.update({'aTranskript': aTranskript, 'aEinzelErhebung': aEinzelErhebung, 'aTokenTypes': aTokenTypes, 'aInformanten': aInformanten, 'aSaetze': aSaetze, 'aTmNr': aTmNr})
		# Events laden:
		aNr = 0
		aEvents = []
		aTokens = {}
		if 'aNr' in request.POST:
			aNr = int(request.POST.get('aNr'))
		nNr = aNr
		startQuery = aNr * maxQuerys
		endQuery = startQuery + maxQuerys
		for aEvent in adbmodels.event.objects.prefetch_related('rn_token_event_id').filter(rn_token_event_id__transcript_id_id=tpk).distinct().order_by('start_time')[startQuery:endQuery]:
			aEITokens = {}
			for aEIToken in sorted(list(aEvent.rn_token_event_id.all()), key=operator.attrgetter("token_reihung")):
				if aEIToken.ID_Inf_id not in aEITokens:
					aEITokens[aEIToken.ID_Inf_id] = []
				aEITokens[aEIToken.ID_Inf_id].append(aEIToken.id)
				aTokenData = {
					'tt': aEIToken.token_type_id_id,
					'tr': aEIToken.token_reihung,
					'e': aEIToken.event_id_id,
					'i': aEIToken.ID_Inf_id,
					't': '',
					'o': '',
					'to': ''
				}
				for aSpur in spuren:
					if getattr(aEIToken, aSpur['title']):
						aTokenData[aSpur['field'][0]] = getattr(aEIToken, aSpur['title'])
				if aEIToken.sentence_id_id:
					aTokenData['s'] = aEIToken.sentence_id_id
				if aEIToken.sequence_in_sentence:
					aTokenData['sr'] = aEIToken.sequence_in_sentence
				if aEIToken.fragment_of_id:
					aTokenData['fo'] = aEIToken.fragment_of_id
				if aEIToken.likely_error:
					aTokenData['le'] = 1
				aTokens[aEIToken.pk] = aTokenData
			aEvents.append({
				'pk': aEvent.pk,
				's': str(aEvent.start_time),
				'e': str(aEvent.end_time),
				'l': str(aEvent.layer if aEvent.layer else 0),
				'tid': aEITokens,
				'et': [{'pk': tets.pk, 'i': tets.ID_Inf_id, 'ti': tets.tier_id_id, 'txt': tets.text} for tets in aEvent.tbl_event_tier_set.all()]
			})
		if len(aEvents) == maxQuerys:
			nNr += 1
		aTokenIds = [aTokenId for aTokenId in aTokens]
		maxVars = 500
		aTokenSets = {}
		nTokenSets = []
		aTokenIdsTemp = deepcopy(aTokenIds)
		# Token Sets zu Events laden:
		while len(aTokenIdsTemp) > 0:
			nTokenSets += adbmodels.tbl_tokenset.objects.distinct().filter(id_von_token_id__in=aTokenIdsTemp[:maxVars])
			nTokenSets += adbmodels.tbl_tokenset.objects.distinct().filter(tbl_tokentoset__id_token__in=aTokenIdsTemp[:maxVars])
			aTokenIdsTemp = aTokenIdsTemp[maxVars:]
		for nTokenSet in nTokenSets:
			if nTokenSet.pk not in aTokenSets:
				aTokenSet = {}
				if nTokenSet.id_von_token:
					aTokenSet['ivt'] = nTokenSet.id_von_token_id
				if nTokenSet.id_bis_token:
					aTokenSet['ibt'] = nTokenSet.id_bis_token_id
				nTokenToSets = []
				for nTokenToSet in nTokenSet.tbl_tokentoset_set.all():
					nTokenToSets.append(nTokenToSet.id_token_id)
				if nTokenToSets:
					aTokenSet['t'] = nTokenToSets
				aTokenSets[nTokenSet.pk] = (aTokenSet)
		# Antworten zu Tokens und Tokensets laden:
		aTokenSetIds = [aTokenSetId for aTokenSetId in aTokenSets]
		maxVars = 500
		aAntworten = {}
		nAntworten = []
		aTokenIdsTemp = deepcopy(aTokenIds)
		aTokenSetIdsTemp = deepcopy(aTokenSetIds)
		while len(aTokenIdsTemp) > 0:
			nAntworten += kdbmodels.tbl_antworten.objects.distinct().filter(ist_token_id__in=aTokenIdsTemp[:maxVars])
			aTokenIdsTemp = aTokenIdsTemp[maxVars:]
		while len(aTokenSetIdsTemp) > 0:
			nAntworten += kdbmodels.tbl_antworten.objects.distinct().filter(ist_tokenset_id__in=aTokenSetIdsTemp[:maxVars])
			aTokenSetIdsTemp = aTokenSetIdsTemp[maxVars:]
		for nAntwort in nAntworten:
			if nAntwort.pk not in aAntworten:
				aAntwort = {'vi': nAntwort.von_Inf_id}
				aAntwort['inat'] = nAntwort.ist_nat
				if nAntwort.ist_Satz:
					aAntwort['is'] = nAntwort.ist_Satz_id
				aAntwort['ibfl'] = nAntwort.ist_bfl
				if nAntwort.ist_token:
					aAntwort['it'] = nAntwort.ist_token_id
				if nAntwort.ist_tokenset:
					aAntwort['its'] = nAntwort.ist_tokenset_id
				aAntwort['bds'] = nAntwort.bfl_durch_S
				if nAntwort.start_Antwort:
					aAntwort['sa'] = str(nAntwort.start_Antwort)
				if nAntwort.stop_Antwort:
					aAntwort['ea'] = str(nAntwort.stop_Antwort)
				aAntwort['k'] = nAntwort.Kommentar
				# AntwortenTags laden:
				nAntTags = []
				for xval in kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=nAntwort.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
					nAntTags.append({'e': xval['id_TagEbene'], 't': getTagFamilie(kdbmodels.tbl_antwortentags.objects.filter(id_Antwort=nAntwort.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
				if nAntTags:
					aAntwort['pt'] = nAntTags
				aAntworten[nAntwort.pk] = (aAntwort)
		dataout.update({'nNr': nNr, 'aEvents': aEvents, 'aTokens': aTokens, 'aTokenSets': aTokenSets, 'aAntworten': aAntworten})
		return httpOutput(json.dumps(dataout), 'application/json')
	# Menü laden:
	if 'getMenue' in request.POST:
		if 'ainformant' in request.POST:
			ipk = int(request.POST.get('ainformant'))
		informantenMitTranskripte = []
		translist = list(adbmodels.token.objects.values('ID_Inf', 'transcript_id').distinct().order_by('ID_Inf'))
		for val in pdbmodels.tbl_informanten.objects.all():
			atc = 0
			for atl in translist:
				if atl['ID_Inf'] == val.pk:
					atc += 1
			informantenMitTranskripte.append({'model': {'pk': val.pk, 'model_str': str(val)}, 'Acount': atc})
		aTranskripte = []
		if ipk > 0:
			aTranskripte = [{'model': {'pk': val.pk, 'model_str': str(val), 'update_time': val.update_time.strftime("%d.%m.%Y- %H:%M"), 'name': val.name}, 'count': val.token_set.count()} for val in [adbmodels.transcript.objects.get(pk=atid['id']) for atid in adbmodels.transcript.objects.filter(token__ID_Inf=ipk).values('id').annotate(total=Count('id'))]]
		return httpOutput(json.dumps({'informantenMitTranskripte': informantenMitTranskripte, 'aInformant': ipk, 'aTranskripte': aTranskripte}), 'application/json')

	if 'getTranscriptsInfList' in request.POST:  # TOOL
		infList = [{
			'pk': aInf.pk,
			'modelStr': str(aInf),
			'transcriptsPKs': aInf.transcriptsPKs
		} for aInf in pdbmodels.tbl_informanten.objects.raw('''
			SELECT "PersonenDB_tbl_informanten".*,
				ARRAY(
					SELECT "token"."transcript_id_id"
						FROM "token"
						WHERE "token"."ID_Inf_id" = "PersonenDB_tbl_informanten"."id"
						GROUP BY "token"."transcript_id_id"
						ORDER BY "token"."transcript_id_id" ASC
				) AS "transcriptsPKs"
			FROM "PersonenDB_tbl_informanten"
			ORDER BY "PersonenDB_tbl_informanten"."id" ASC
		''')]
		transList = [{
			'pk': aTrans.pk,
			'modelStr': str(aTrans),
			'updateTime': aTrans.update_time.strftime("%d.%m.%Y- %H:%M"),
			'name': aTrans.name,
			'tokenCount': aTrans.tokenCount
		} for aTrans in adbmodels.transcript.objects.raw('''
			SELECT "transcript".*,
						(SELECT COUNT(*) FROM "token" WHERE "token".transcript_id_id = "transcript".id) AS "tokenCount"
					FROM "transcript"
					ORDER BY "transcript"."id" ASC
		''')]
		# from django.db import connection
		# print(connection.queries)
		return httpOutput(json.dumps({'informanten': infList, 'transcripts': transList}), 'application/json')

	return render_to_response('AnnotationsDB/startvue.html', RequestContext(request))


def getTagFamilie(Tags):
	"""Tag Familie ausgeben."""
	afam = []
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1]):
				pClose += 1
				del afam[-1]
		except:
			pass
		oTags.append({'t': value.id_Tag_id, 'i': value.pk, 'c': pClose})
		afam.append(value.id_Tag_id)
	return oTags
