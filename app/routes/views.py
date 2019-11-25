from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Count
import KorpusDB.models as dbmodels
import PersonenDB.models as pdbmodels
import AnnotationsDB.models as adbmodels
import json
from DB.funktionenDB import httpOutput
import operator
from copy import deepcopy
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_duration
import time
import sys
from django.db import transaction


def einzelerhebungen(request):
	if not request.user.is_authenticated():
		return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	aEinzelErhebungen = []
	try:
		for aEinzelErhebung in dbmodels.tbl_inferhebung.objects.all():
			aInformanten = [{
				'pk': aInformant.ID_Inf_id,
				'Kuerzel': aInformant.ID_Inf.inf_sigle,
				'Kuerzel_anonym': aInformant.ID_Inf.inf_sigle,
				'Name': None,
				'Vorname': None,
			} for aInformant in aEinzelErhebung.tbl_inf_zu_erhebung_set.all()]
			aEinzelErhebungen.append({
				'pk': aEinzelErhebung.pk,
				'ID_Erh': aEinzelErhebung.ID_Erh_id,
				'id_transcript': aEinzelErhebung.id_Transcript_id,
				'Datum': aEinzelErhebung.Datum.strftime("%d.%m.%Y- %H:%M") if aEinzelErhebung.Datum else None,
				'Explorator': aEinzelErhebung.Explorator_id,
				'Kommentar': aEinzelErhebung.Kommentar,
				'Dateipfad': aEinzelErhebung.Dateipfad,
				'Audiofile': aEinzelErhebung.Audiofile,
				'Logfile': aEinzelErhebung.Logfile,
				'Ort': aEinzelErhebung.Ort_id,
				'OrtString': str(aEinzelErhebung.Ort),
				'Besonderheiten': aEinzelErhebung.Besonderheiten,
				'FX_Informanten': aInformanten
			})
	except Exception as e:
		return httpOutput(json.dumps({'error': str(type(e)) + ' - ' + str(e)}), 'application/json')
	return httpOutput(json.dumps({'einzelerhebungen': aEinzelErhebungen, 'error': None}), 'application/json')


@csrf_exempt
def transcriptCreate(request):
	if not request.user.is_authenticated():
		return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	try:
		nId = -1
		sData = json.loads(request.body.decode('utf-8'))
		aV_id_einzelerhebung = sData['id_einzelerhebung'] if 'id_einzelerhebung' in sData else 0
		aV_name = sData['name']
		aV_default_tier = sData['default_tier']
		if aV_id_einzelerhebung:
			aErhebung = dbmodels.tbl_inferhebung.objects.get(pk=aV_id_einzelerhebung)
			if aErhebung:
				try:
					aElement = adbmodels.transcript.objects.get(pk=int(sData['pk']) if 'pk' in sData else 0)
				except adbmodels.transcript.DoesNotExist:
					aElement = adbmodels.transcript()
				aElement.name = aV_name
				aElement.default_tier = aV_default_tier
				aElement.save()
				nId = aElement.pk
				aErhebung.id_Transcript = aElement
				aErhebung.save()
				if 'aTiers' in sData:
					for aTierPk, aTierData in sData['aTiers'].items():
						if 'status' in aTierData and aTierData['status'] == 'delete' and int(aTierPk) > 0:
							aTier = adbmodels.tbl_tier.objects.get(pk=int(aTierPk))
							aTier.delete()
							sData['aTiers'][aTierPk]['newStatus'] = 'deleted'
						else:
							if int(aTierPk) < 1:
								aTier = adbmodels.tbl_tier()
							else:
								aTier = adbmodels.tbl_tier.objects.get(pk=int(aTierPk))
							aTier.transcript_id_id = nId
							aTier.tier_name = aTierData['tier_name']
							aTier.save()
							if int(aTierPk) < 1:
								sData['aTiers'][aTierPk]['newPk'] = aTier.pk
								sData['aTiers'][aTierPk]['newStatus'] = 'inserted'
							else:
								sData['aTiers'][aTierPk]['newStatus'] = 'updated'
			else:
				return httpOutput(json.dumps({'error': 'Erhebung mit ID "' + str(aV_id_einzelerhebung) + '" nicht gefunden!'}), 'application/json')
		else:
			return httpOutput(json.dumps({'error': '"id_einzelerhebung" fehlt!'}), 'application/json')
	except Exception as e:
		return httpOutput(json.dumps({'error': str(type(e)) + ' - ' + str(e)}), 'application/json')
	return httpOutput(json.dumps({'transcript_id': str(nId), 'error': None}), 'application/json')


def transcripts(request):
	if not request.user.is_authenticated():
		return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	aTranscripts = []
	try:
		for aTranscript in adbmodels.transcript.objects.all():
			aTranscripts.append({'pk': aTranscript.pk, 'n': aTranscript.name, 'ut': aTranscript.update_time.strftime("%d.%m.%Y- %H:%M"), 'default_tier': aTranscript.default_tier})
	except Exception as e:
		return httpOutput(json.dumps({'error': str(type(e)) + ' - ' + str(e)}), 'application/json')
	return httpOutput(json.dumps({'transcripts': aTranscripts, 'error': None}), 'application/json')


def transcript(request, aPk, aNr):
	if not request.user.is_authenticated():
		return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	tpk = int(aPk)
	aNr = int(aNr)
	if tpk > 0:
		maxQuerys = 250
		dataout = {'aPk': aPk, 'aNr': aNr, 'error': None}
		# Startinformationen laden: (transcript, EinzelErhebung, Informanten, Saetze)
		if aNr == 0:
			aTranskriptData = adbmodels.transcript.objects.get(pk=tpk)
			aTranskript = {'pk': aTranskriptData.pk, 'ut': aTranskriptData.update_time.strftime("%d.%m.%Y- %H:%M"), 'n': aTranskriptData.name, 'default_tier': aTranskriptData.default_tier}
			aTiersData = adbmodels.tbl_tier.objects.filter(transcript_id=aTranskriptData)
			aTiers = {aTier.pk: {"tier_name": aTier.tier_name} for aTier in aTiersData}
			aEinzelErhebung = {}
			aEinzelErhebungData = dbmodels.tbl_inferhebung.objects.filter(id_Transcript_id=tpk)
			if aEinzelErhebungData:
				aEinzelErhebungData = aEinzelErhebungData[0]
				aEinzelErhebung = {
					'pk': aEinzelErhebungData.pk, 'trId': aEinzelErhebungData.id_Transcript_id, 'd': aEinzelErhebungData.Datum.strftime("%d.%m.%Y- %H:%M"), 'e': aEinzelErhebungData.Explorator_id, 'k': aEinzelErhebungData.Kommentar,
					'dp': aEinzelErhebungData.Dateipfad, 'af': aEinzelErhebungData.Audiofile,
					'lf': aEinzelErhebungData.Logfile, 'o': aEinzelErhebungData.Ort_id, 'os': str(aEinzelErhebungData.Ort), 'b': aEinzelErhebungData.Besonderheiten}
			aTokenTypes = {}
			for aTokenType in adbmodels.token_type.objects.filter(token__transcript_id_id=tpk):
				aTokenTypes[aTokenType.pk] = {'n': aTokenType.token_type_name}
			aInformanten = {}
			for aInf in adbmodels.token.objects.filter(transcript_id_id=tpk).values('ID_Inf').annotate(total=Count('ID_Inf')).order_by('ID_Inf'):
				aInfM = pdbmodels.tbl_informanten.objects.get(id=aInf['ID_Inf'])
				aInformanten[aInfM.pk] = {'k': aInfM.inf_sigle, 'ka': aInfM.inf_sigle}
			aSaetze = {}
			for aSatz in dbmodels.tbl_saetze.objects.filter(token__transcript_id_id=tpk):
				aSaetze[aSatz.pk] = {'t': aSatz.Transkript, 's': aSatz.Standardorth, 'k': aSatz.Kommentar}
			aTmNr = int(adbmodels.event.objects.prefetch_related('rn_token_event_id').filter(rn_token_event_id__transcript_id_id=tpk).distinct().order_by('start_time').count() / maxQuerys)
			dataout.update({'aTranskript': aTranskript, 'aTiers': aTiers, 'aEinzelErhebung': aEinzelErhebung, 'aTokenTypes': aTokenTypes, 'aInformanten': aInformanten, 'aSaetze': aSaetze, 'aTmNr': aTmNr})
		# Events laden:
		aEvents = []
		aTokens = {}
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
					't': aEIToken.text,
					'tt': aEIToken.token_type_id_id,
					'tr': aEIToken.token_reihung,
					'e': aEIToken.event_id_id,
					'to': aEIToken.text_in_ortho,
					'i': aEIToken.ID_Inf_id,
				}
				if aEIToken.ortho:
					aTokenData['o'] = aEIToken.ortho
				if aEIToken.phon:
					aTokenData['p'] = aEIToken.phon
				if aEIToken.sentence_id_id:
					aTokenData['s'] = aEIToken.sentence_id_id
				if aEIToken.sequence_in_sentence:
					aTokenData['sr'] = aEIToken.sequence_in_sentence
				if aEIToken.fragment_of_id:
					aTokenData['fo'] = aEIToken.fragment_of_id
				if aEIToken.likely_error:
					aTokenData['le'] = 1
				aTokens[aEIToken.pk] = aTokenData
			aEventsTiers = {}
			for aEventTier in aEvent.tbl_event_tier_set.all():
				if aEventTier.ID_Inf_id not in aEventsTiers:
					aEventsTiers[aEventTier.ID_Inf_id] = {}
				aEventsTiers[aEventTier.ID_Inf_id][aEventTier.pk] = {'t': aEventTier.text, 'ti': aEventTier.tier_id_id}
			aEvents.append({
				'pk': aEvent.pk,
				's': str(aEvent.start_time),
				'e': str(aEvent.end_time),
				'l': str(aEvent.layer if aEvent.layer else 0),
				'tid': aEITokens,
				'event_tiers': aEventsTiers
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
			nAntworten += dbmodels.tbl_antworten.objects.distinct().filter(ist_token_id__in=aTokenIdsTemp[:maxVars])
			aTokenIdsTemp = aTokenIdsTemp[maxVars:]
		while len(aTokenSetIdsTemp) > 0:
			nAntworten += dbmodels.tbl_antworten.objects.distinct().filter(ist_tokenset_id__in=aTokenSetIdsTemp[:maxVars])
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
				for xval in dbmodels.tbl_antwortentags.objects.filter(id_Antwort=nAntwort.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
					nAntTags.append({'e': xval['id_TagEbene'], 't': getTagFamilie(dbmodels.tbl_antwortentags.objects.filter(id_Antwort=nAntwort.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
				if nAntTags:
					aAntwort['pt'] = nAntTags
				aAntworten[nAntwort.pk] = (aAntwort)
		dataout.update({'nNr': nNr, 'aEvents': aEvents, 'aTokens': aTokens, 'aTokenSets': aTokenSets, 'aAntworten': aAntworten})
		return httpOutput(json.dumps(dataout), 'application/json')
		# return httpOutput(json.dumps({'aPk': aPk, 'aNr': aNr, 'error': None}), 'application/json')
	return httpOutput(json.dumps({'error': 'Fehlerhafte PK'}), 'application/json')


@csrf_exempt
def transcriptSave(request, aPk):
	# if not request.user.is_authenticated():
	# 	return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	tpk = int(aPk)
	# Testen: $.post( "/routes/transcript/save/1/", '{"aEvents": [{"pk": -1, "s": "0", "e": "0", "l": 0,"event_tiers": {"1": {"-1": {"ti": "-1","t": "test ..."}}}}],"aTiers": {"-1": {"tier_name": "test"}},"aTokens": {"-1": {"e": -1,"i": 2,"s": -1,"sr": -1,"t": "xxxx","to": "","tr": 6069,"tt": 1}}}').always(function(x) { console.log(x); });
	if tpk > 0:
		sData = json.loads(request.body.decode('utf-8'))
		eventPkChanges = {}
		aEventKey = {}
		starttime = time.time()
		sData['sys_timer'] = {}
		if 'aTiers' in sData:
			for aTierPk, aTierData in sData['aTiers'].items():
				if int(aTierPk) < 1:
					aTier = adbmodels.tbl_tier()
				else:
					aTier = adbmodels.tbl_tier.objects.get(pk=int(aTierPk))
				aTier.transcript_id_id = tpk
				aTier.tier_name = aTierData['tier_name']
				aTier.save()
				if int(aTierPk) < 1:
					sData['aTiers'][aTierPk]['newPk'] = aTier.pk
					sData['aTiers'][aTierPk]['newStatus'] = 'inserted'
				else:
					sData['aTiers'][aTierPk]['newStatus'] = 'updated'
		sData['sys_timer']['aTiers'] = time.time() - starttime
		starttime = time.time()
		if 'aEvents' in sData:
			for key, aEvent in enumerate(sData['aEvents']):
				try:
					aEventKey[sData['aEvents'][key]['pk']] = key
					if 'status' in aEvent and aEvent['status'] == 'delete':
						aElement = adbmodels.event.objects.get(id=sData['aEvents'][key]['pk'])
						aElement.delete()
						sData['aEvents'][key]['newStatus'] = 'deleted'
						# print('event', key, 'deleted')
					elif aEvent['pk'] < 1:
						eventUpdateAndInsert(sData, key, aEvent, aEventKey, eventPkChanges)
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					sData['aEvents'][key]['newStatus'] = 'error'
					sData['aEvents'][key]['error'] = str(exc_tb.tb_lineno) + ' | ' + str(type(e)) + ' - ' + str(e) + ' -  events'
					# print('event', key, 'error', sData['aEvents'][key]['error'])
			with transaction.atomic():
				for key, aEvent in enumerate(sData['aEvents']):
					try:
						if 'status' in aEvent and aEvent['status'] != 'delete' and aEvent['pk'] > 0:
							eventUpdateAndInsert(sData, key, aEvent, aEventKey, eventPkChanges)
					except Exception as e:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						sData['aEvents'][key]['newStatus'] = 'error'
						sData['aEvents'][key]['error'] = str(exc_tb.tb_lineno) + ' | ' + str(type(e)) + ' - ' + str(e) + ' -  events with atomic'
						# print('event', key, 'error', sData['aEvents'][key]['error'])
		sData['sys_timer']['aEvents'] = time.time() - starttime
		# print('aEvents', sData['sys_timer']['aEvents'], 'sec.')
		starttime = time.time()
		if 'aTokens' in sData:
			for key, aToken in sData['aTokens'].items():
				aId = int(key)
				try:
					if 'status' in aToken and aToken['status'] == 'delete':
						aElement = adbmodels.token.objects.get(id=aId)
						aElement.delete()
						sData['aTokens'][key]['newStatus'] = 'deleted'
						# print('token', key, 'deleted')
					elif aId < 1:
						tokenUpdateAndInsert(sData, key, aToken, aEventKey, aId, tpk)
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					sData['aTokens'][key]['newStatus'] = 'error'
					sData['aTokens'][key]['error'] = str(exc_tb.tb_lineno) + ' | ' + str(type(e)) + ' - ' + str(e) + ' - token'
					# print('token:', key, 'error:', sData['aTokens'][key]['error'], sData['aTokens'][key])
			with transaction.atomic():
				for key, aToken in sData['aTokens'].items():
					aId = int(key)
					try:
						if 'status' in aToken and aToken['status'] != 'delete' and aId > 0:
							tokenUpdateAndInsert(sData, key, aToken, aEventKey, aId, tpk)
					except Exception as e:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						sData['aTokens'][key]['newStatus'] = 'error'
						sData['aTokens'][key]['error'] = str(exc_tb.tb_lineno) + ' | ' + str(type(e)) + ' - ' + str(e) + ' - token with atomic'
						# print('token:', key, 'error:', sData['aTokens'][key]['error'], sData['aTokens'][key])
		sData['sys_timer']['aTokens'] = time.time() - starttime
		# print('aTokens', sData['sys_timer']['aTokens'], 'sec.')
		starttime = time.time()
		if 'aEvents' in sData:  # Update tid
			for key, aEvent in enumerate(sData['aEvents']):
				ePk = aEvent['newPk'] if 'newPk' in aEvent else aEvent['pk']
				sData['aEvents'][key]['tid'] = {}
				for av in adbmodels.token.objects.filter(event_id_id=ePk):
					if str(av.ID_Inf_id) not in sData['aEvents'][key]['tid']:
						sData['aEvents'][key]['tid'][str(av.ID_Inf_id)] = []
					sData['aEvents'][key]['tid'][str(av.ID_Inf_id)].append(av.pk)
		sData['sys_timer']['aEventsTid'] = time.time() - starttime
		# print('aEventsTid', sData['sys_timer']['aEventsTid'], 'sec.')
		return httpOutput(json.dumps(sData), 'application/json')
	return httpOutput(json.dumps({'error': 'Fehlerhafte PK'}), 'application/json')


def getTagFamilie(Tags):
	afam = []
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				pClose += 1
				del afam[-1]
		except:
			pass
		oTags.append({'t': value.id_Tag_id, 'i': value.pk, 'c': pClose})
		afam.append(value.id_Tag)
	return oTags


def eventUpdateAndInsert(sData, key, aEvent, aEventKey, eventPkChanges):
	if aEvent['pk'] < 1:
		aElement = adbmodels.event()
	else:
		aElement = adbmodels.event.objects.get(id=sData['aEvents'][key]['pk'])
	# Daten setzen
	aElement.start_time = parse_duration(sData['aEvents'][key]['s'])
	aElement.end_time = parse_duration(sData['aEvents'][key]['e'])
	aElement.layer = sData['aEvents'][key]['l'] if sData['aEvents'][key]['l'] > 0 else None
	# Speichern
	aElement.save()
	# Erneut einlesen
	# sData['aEvents'][key]['s'] = str(aElement.start_time)  # "0:01:35.098000"
	# sData['aEvents'][key]['e'] = str(aElement.end_time)
	# sData['aEvents'][key]['l'] = str(aElement.layer if aElement.layer else 0)
	if 'event_tiers' in sData['aEvents'][key]:
		for aEventTierInfKey, aEventTierInfData in sData['aEvents'][key]['event_tiers'].items():
			for aEventTierKey, aEventTierData in aEventTierInfData.items():
				if 'status' in aEventTierData and aEventTierData['status'] == 'delete' and int(aEventTierKey) > 0:
					aEventTier = adbmodels.tbl_event_tier.objects.get(pk=int(aEventTierKey))
					aEventTier.delete()
					sData['aEvents'][key]['event_tiers'][aEventTierInfKey][aEventTierKey]['newStatus'] = 'deleted'
				else:
					if int(aEventTierKey) < 1:
						aEventTier = adbmodels.tbl_event_tier()
					else:
						aEventTier = adbmodels.tbl_event_tier.objects.get(pk=int(aEventTierKey))
					aEventTier.event_id = aElement
					if aEventTierData['ti'] < 1:
						aEventTier.tier_id_id = sData['aTiers'][str(aEventTierData['ti'])]['newPk']
						sData['aEvents'][key]['event_tiers'][aEventTierInfKey][aEventTierKey]['ti'] = sData['aTiers'][str(aEventTierData['ti'])]['newPk']
					else:
						aEventTier.tier_id_id = aEventTierData['ti']
					aEventTier.ID_Inf_id = aEventTierInfKey
					aEventTier.text = aEventTierData['t']
					aEventTier.save()
					if int(aEventTierKey) < 1:
						sData['aEvents'][key]['event_tiers'][aEventTierInfKey][aEventTierKey]['newPk'] = aEventTier.pk
						sData['aEvents'][key]['event_tiers'][aEventTierInfKey][aEventTierKey]['newStatus'] = 'inserted'
					else:
						sData['aEvents'][key]['event_tiers'][aEventTierInfKey][aEventTierKey]['newStatus'] = 'updated'
	if aEvent['pk'] < 1:
		sData['aEvents'][key]['newPk'] = aElement.pk
		eventPkChanges[sData['aEvents'][key]['pk']] = aElement.pk
		sData['aEvents'][key]['newStatus'] = 'inserted'
		# print('event', key, 'inserted')
	else:
		sData['aEvents'][key]['newStatus'] = 'updated'
		# print('event', key, 'updated')


def tokenUpdateAndInsert(sData, key, aToken, aEventKey, aId, tpk):
	aEventPk = sData['aTokens'][key]['e']
	if sData['aTokens'][key]['e'] in aEventKey:
		if 'newPk' in sData['aEvents'][aEventKey[sData['aTokens'][key]['e']]]:
			aEventPk = sData['aEvents'][aEventKey[sData['aTokens'][key]['e']]]['newPk']
	if aId < 1:
		aElement = adbmodels.token()
		aElement.transcript_id_id = tpk
	else:
		aElement = adbmodels.token.objects.get(id=aId)
	# Daten setzen
	aElement.text = sData['aTokens'][key]['t']
	aElement.token_type_id_id = sData['aTokens'][key]['tt']
	aElement.token_reihung = sData['aTokens'][key]['tr']
	aElement.event_id_id = aEventPk
	aElement.text_in_ortho = sData['aTokens'][key]['to']
	aElement.ID_Inf_id = sData['aTokens'][key]['i']
	aElement.ortho = sData['aTokens'][key]['o'] if 'o' in sData['aTokens'][key] else None
	aElement.phon = sData['aTokens'][key]['p'] if 'p' in sData['aTokens'][key] else None
	aElement.sentence_id_id = sData['aTokens'][key]['s'] if 's' in sData['aTokens'][key] and sData['aTokens'][key]['s'] > 0 else None
	aElement.sequence_in_sentence = sData['aTokens'][key]['sr'] if 'sr' in sData['aTokens'][key] and sData['aTokens'][key]['sr'] > 0 else None
	aElement.fragment_of_id = sData['aTokens'][key]['fo'] if 'fo' in sData['aTokens'][key] and sData['aTokens'][key]['fo'] > 0 else None
	aElement.likely_error = True if 'le' in sData['aTokens'][key] and sData['aTokens'][key]['le'] > 0 else False
	# Speichern
	aElement.save()
	# Erneut einlesen
	# sData['aTokens'][key]['t'] = aElement.text
	# sData['aTokens'][key]['tt'] = aElement.token_type_id_id
	# sData['aTokens'][key]['tr'] = aElement.token_reihung
	# sData['aTokens'][key]['e'] = aElement.event_id_id
	# sData['aTokens'][key]['to'] = aElement.text_in_ortho
	# sData['aTokens'][key]['i'] = aElement.ID_Inf_id
	# if aElement.ortho:
	# 	sData['aTokens'][key]['o'] = aElement.ortho
	# if aElement.phon:
	# 	sData['aTokens'][key]['p'] = aElement.phon
	# elif 'o' in sData['aTokens'][key]:
	# 	del sData['aTokens'][key]['o']
	# if aElement.sentence_id_id:
	# 	sData['aTokens'][key]['s'] = aElement.sentence_id_id
	# elif 's' in sData['aTokens'][key]:
	# 	del sData['aTokens'][key]['s']
	# if aElement.sequence_in_sentence:
	# 	sData['aTokens'][key]['sr'] = aElement.sequence_in_sentence
	# elif 'sr' in sData['aTokens'][key]:
	# 	del sData['aTokens'][key]['sr']
	# if aElement.fragment_of_id:
	# 	sData['aTokens'][key]['fo'] = aElement.fragment_of_id
	# elif 'fo' in sData['aTokens'][key]:
	# 	del sData['aTokens'][key]['fo']
	# if aElement.likely_error:
	# 	sData['aTokens'][key]['le'] = 1
	# elif 'le' in sData['aTokens'][key]:
	# 	del sData['aTokens'][key]['le']
	if aId < 1:
		sData['aTokens'][key]['newPk'] = aElement.pk
		sData['aTokens'][key]['newStatus'] = 'inserted'
		# print('token', aId, 'inserted', sData['aTokens'][key]['newPk'], 'in event', aEventPk)
	else:
		sData['aTokens'][key]['newStatus'] = 'updated'
		# print('token', key, 'updated')


# Dateien
def files(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return httpOutput(json.dumps({'error': 'login'}), 'application/json')
	if not request.user.has_perm('DB.dateien'):
		return httpOutput(json.dumps({'error': 'no file permission'}), 'application/json')
	from DB.funktionenDateien import view_dateien
	return view_dateien(request, True)
