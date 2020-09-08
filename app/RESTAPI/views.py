"""RESTAPI."""
from django.http import HttpResponse
from DB.funktionenDB import httpOutput
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from django.core import serializers
from django.db.models import Count
import json


def getTags(request):
	"""Beispiel: Alle Tags als JSON ausgeben."""
	# if not request.user.is_authenticated():
	# 	return HttpResponse('Unauthorized', status=401)
	return httpOutput(serializers.serialize("json", KorpusDB.tbl_tags.objects.all()), mimetype='text/plain')


def getAntworten(request):
	"""Alle Antworten als JSON ausgeben."""
	# if not request.user.is_authenticated():
	# 	return HttpResponse('Unauthorized', status=401)
	# Beispiele:
	# /restapi/getAntworten?get=tbl_antworten&start=0&len=100&filter=erhebung:4,aufgabenset:44		- Abruf von tbl_antworten von Eintrag 0 bis 99 von Erhebung id 4 und Aufgabenset id 44
	# /restapi/getAntworten?get=tbl_antworten&start=0&len=100&filter=erhebung:4,aufgabenset:44&tagname=true		- Abruf mit id_Tag_Name
	# /restapi/getAntworten?info=filter					- Abruf der Verfügbaren Filter
	# /restapi/getAntworten?get=tbl_tags				- Abruf der ersten 100 Tags
	# /restapi/getAntworten?get=tbl_tags&start=100		- Abruf der zweiten 100 Tags
	# /restapi/getAntworten?get=tbl_tags&len=1000		- Abruf der ersten 1000 Tags
	aOutput = {}
	aStart = int(request.GET.get('start')) if 'start' in request.GET else 0
	aLen = int(request.GET.get('len')) if 'len' in request.GET else 100
	# Filter (nur für tbl_antworten)
	aElemente = KorpusDB.tbl_antworten.objects.all()
	if 'filter' in request.GET:  # filter=aufgabenset:0,erhebung:0
		aFilter = [af.split(':') for af in request.GET.get('filter').split(',')]
		for af in aFilter:
			if af[0] == 'erhebung' and int(af[1]) > 0:
				aElemente = aElemente.filter(zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh_id=int(af[1]))
			if af[0] == 'aufgabenset' and int(af[1]) > 0:
				aElemente = aElemente.filter(zu_Aufgabe__von_ASet_id=int(af[1]))
	# Tabellen abrufen
	if 'get' in request.GET:  # Mögliche Werte: tbl_antworten, tbl_tags, tbl_tagebene, tbl_erhebungsarten (Auch gleichzeitig wenn Kommasepariert ohne Leerzeichen)
		aGet = request.GET.get('get').split(',')
		if 'tbl_antworten' in aGet:
			aOutput['tbl_antworten'] = []
			rLen = aStart
			for aElement in aElemente.select_related('ist_Satz').distinct()[aStart:aStart + aLen]:
				rLen += 1
				aOutput['tbl_antworten'].append({
					'pk': aElement.pk,
					'von_Inf_id': aElement.von_Inf_id,
					'zu_Aufgabe_id': aElement.zu_Aufgabe_id,
					'Reihung': aElement.Reihung,
					# 'ist_am': aElement.ist_am,
					'ist_gewaehlt': aElement.ist_gewaehlt,
					'ist_nat': aElement.ist_nat,
					'ist_Satz': {
						'pk': aElement.ist_Satz.pk,
						'Transkript': aElement.ist_Satz.Transkript,
						'Standardorth': aElement.ist_Satz.Standardorth,
						'ipa': aElement.ist_Satz.ipa,
						'Kommentar': aElement.ist_Satz.Kommentar,
					} if aElement.ist_Satz else None,
					'ist_bfl': aElement.ist_bfl,
					'bfl_durch_S': aElement.bfl_durch_S,
					'start_Antwort': str(aElement.start_Antwort),
					'stop_Antwort': str(aElement.stop_Antwort),
					'Kommentar': aElement.Kommentar,
					'kontrolliert': aElement.kontrolliert,
					'veroeffentlichung': aElement.veroeffentlichung,
					'tbl_antwortentags_set': [{
						'pk': aTag.pk,
						'id_Tag': aTag.id_Tag_id,
						'id_Tag_Name': str(aTag.id_Tag) if 'tagname' in request.GET and request.GET.get('tagname') == 'true' else None,
						'Tag_Generation': aTag.id_Tag.Generation,
						'id_TagEbene': aTag.id_TagEbene_id,
						'Gruppe': aTag.Gruppe,
						'Reihung': aTag.Reihung,
					} for aTag in aElement.tbl_antwortentags_set.select_related('id_Tag' if 'tagname' in request.GET and request.GET.get('tagname') == 'true' else None).all()]
				})
			aOutput['tbl_antworten_count'] = {
				'all': aElemente.distinct().count(),
				'ofall': KorpusDB.tbl_antworten.objects.all().count(),
				'start': aStart,
				'end': rLen - 1,
				'len': aLen,
			}
		if 'tbl_tags' in aGet:
			aOutput['tbl_tags'] = []
			rLen = aStart
			for aTag in KorpusDB.tbl_tags.objects.all()[aStart:aStart + aLen]:
				rLen += 1
				aOutput['tbl_tags'].append({
					'pk': aTag.pk,
					'Tag': aTag.Tag,
					'Tag_lang': aTag.Tag_lang,
					'zu_Phaenomen': {
						'pk': aTag.zu_Phaenomen.pk,
						'Bez_Phaenomen': aTag.zu_Phaenomen.Bez_Phaenomen,
					} if aTag.zu_Phaenomen else None,
					'Kommentar': aTag.Kommentar,
					'AReihung': aTag.AReihung,
					'Generation': aTag.Generation,
				})
			aOutput['tbl_tags_count'] = {
				'all': KorpusDB.tbl_tags.objects.all().count(),
				'start': aStart,
				'end': rLen - 1,
				'len': aLen,
			}
		if 'tbl_tagebene' in aGet:
			aOutput['tbl_tagebene'] = []
			rLen = aStart
			for aTagEbene in KorpusDB.tbl_tagebene.objects.all()[aStart:aStart + aLen]:
				rLen += 1
				aOutput['tbl_tagebene'].append({
					'pk': aTagEbene.pk,
					'Name': aTagEbene.Name,
					'Reihung': aTagEbene.Reihung,
				})
			aOutput['tbl_tagebene_count'] = {
				'all': KorpusDB.tbl_tagebene.objects.all().count(),
				'start': aStart,
				'end': rLen - 1,
				'len': aLen,
			}
		if 'tbl_erhebungsarten' in aGet:
			aOutput['tbl_erhebungsarten'] = []
			rLen = aStart
			for aErhebungsart in KorpusDB.tbl_erhebungsarten.objects.all()[aStart:aStart + aLen]:
				rLen += 1
				aOutput['tbl_erhebungsarten'].append({
					'pk': aErhebungsart.pk,
					'Bezeichnung': aErhebungsart.Bezeichnung,
					'standardisiert': aErhebungsart.standardisiert,
				})
			aOutput['tbl_erhebungsarten_count'] = {
				'all': KorpusDB.tbl_erhebungsarten.objects.all().count(),
				'start': aStart,
				'end': rLen - 1,
				'len': aLen,
			}
	# Informationen abrufen
	if 'info' in request.GET:  # Mögliche Werte: filter (Auch gleichzeitig wenn Kommasepariert ohne Leerzeichen)
		aInfo = request.GET.get('info').split(',')
		if 'filter' in aInfo:
			aOutput['filter'] = []
			aFilter = []
			for aErhebung in KorpusDB.tbl_erhebungen.objects.all():
				aAufgabensets = []
				for aAufgabenset in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aErhebung.pk).distinct():
					aAufgabensets.append({
						'pk': aAufgabenset.pk,
						'Kuerzel': aAufgabenset.Kuerzel,
						'Name_Aset': aAufgabenset.Name_Aset,
						'Fokus': aAufgabenset.Fokus,
						'Art_ASet': aAufgabenset.Art_ASet,
						'Kommentar': aAufgabenset.Kommentar,
					})
				aFilter.append({
					'pk': aErhebung.pk,
					'Art_Erhebung': aErhebung.Art_Erhebung_id,
					'Bezeichnung_Erhebung': aErhebung.Bezeichnung_Erhebung,
					'Zeitraum': aErhebung.Zeitraum,
					'Konzept_von': str(aErhebung.Konzept_von),
					'Aufgabensets': aAufgabensets,
				})
			aOutput['filter'].append(aFilter)
	return httpOutput(json.dumps(aOutput), mimetype='application/json')


def getErhebungsorte(request):
	"""Alle Orte mit Erhebungen."""
	# if not request.user.is_authenticated():
	# 	return HttpResponse('Unauthorized', status=401)
	# Beispiele:
	# /restapi/getErhebungsorte								- Listet alle Orte mit Erhebungen auf
	# /restapi/getErhebungsorte?inferhebung=146,148,980		- Gibt alle "InfErhebungen" mit Sprechern und Transkripten aus
	if 'inferhebung' in request.GET and len(request.GET.get('inferhebung').split(',')) > 0:
		aInfErhebungenIds = [int(id) for id in request.GET.get('inferhebung').split(',')]
		aInfErhebungen = [{
			'id': aInfErh.id,
			'Dateipfad': aInfErh.Dateipfad,
			'Audiofile': aInfErh.Audiofile,
			'transcript': {
				'id': aInfErh.id_Transcript.id,
				'name': aInfErh.id_Transcript.name
			} if aInfErh.id_Transcript else None,
			'erhebung': {
				'id': aInfErh.ID_Erh.id,
				'Art_Erhebung': {'id': aInfErh.ID_Erh.Art_Erhebung.id, 'Bezeichnung': aInfErh.ID_Erh.Art_Erhebung.Bezeichnung} if aInfErh.ID_Erh.Art_Erhebung else None,
				'Bezeichnung_Erhebung': aInfErh.ID_Erh.Bezeichnung_Erhebung,
				'Zeitraum': aInfErh.ID_Erh.Zeitraum,
				'Konzept_von': {'id': aInfErh.ID_Erh.Konzept_von.id, 'str': str(aInfErh.ID_Erh.Konzept_von)} if aInfErh.ID_Erh.Konzept_von else None
			},
			'Datum': str(aInfErh.Datum),
			'Kommentar': aInfErh.Kommentar,
			'Besonderheiten': aInfErh.Besonderheiten,
			'sprecher': [{'id': ize.ID_Inf_id, 'str': str(ize.ID_Inf)} for ize in aInfErh.tbl_inf_zu_erhebung_set.all()]
		} for aInfErh in KorpusDB.tbl_inferhebung.objects.filter(id__in=aInfErhebungenIds).distinct()]
		return httpOutput(json.dumps({'infErhebungen': aInfErhebungen}), mimetype='text/plain')
	aOrte = []
	for aOrt in PersonenDB.tbl_orte.objects.filter(tbl_inferhebung__ID_Erh__isnull=False).distinct():
		aErhList = aOrt.tbl_inferhebung_set.filter(ID_Erh__isnull=False).values('ID_Erh').distinct()
		aOrte.append({
			'id': aOrt.id,
			'ort_namekurz': aOrt.ort_namekurz,
			'ort_namelang': aOrt.ort_namelang,
			'lat': aOrt.lat,
			'lon': aOrt.lon,
			'osm_id': aOrt.osm_id,
			'osm_type': aOrt.osm_type,
			'importiert': aOrt.importiert,
			'erhebungen': [{
				'id': aErh.id,
				'Art_Erhebung': {'id': aErh.Art_Erhebung.id, 'Bezeichnung': aErh.Art_Erhebung.Bezeichnung} if aErh.Art_Erhebung else None,
				'Bezeichnung_Erhebung': aErh.Bezeichnung_Erhebung,
				'Zeitraum': aErh.Zeitraum,
				'Konzept_von': {'id': aErh.Konzept_von.id, 'str': str(aErh.Konzept_von.Konzept_von)} if aErh.Konzept_von else None
			} for aErh in KorpusDB.tbl_erhebungen.objects.filter(id__in=aErhList)],
			'inferhebungen': [{
				'id': aInfErh.id,
				'hasTranskript': True if aInfErh.id_Transcript_id else False
			} for aInfErh in aOrt.tbl_inferhebung_set.filter(ID_Erh__isnull=False, Audiofile__isnull=False).exclude(Audiofile='').distinct()]
		})
	return httpOutput(json.dumps({'orte': aOrte}), mimetype='text/plain')


def test(request):
	"""Beispiel: Alle Informanten auf deren Antworten die angefragte Tag angewendet wurde."""
	# if not request.user.is_authenticated():
	# 	return HttpResponse('Unauthorized', status=401)
	if 'tag' in request.GET:
		try:
			atagid = int(request.GET.get('tag'))
			# print([val for val in PersonenDB.tbl_informanten.objects.filter(tbl_antworten__tbl_antwortentags__id_Tag=atagid).values('inf_sigle').annotate(total=Count('inf_sigle'))])
			return httpOutput(json.dumps(
				[val for val in PersonenDB.tbl_informanten.objects.filter(tbl_antworten__tbl_antwortentags__id_Tag=atagid).values('inf_sigle').annotate(total=Count('inf_sigle'))]
			), mimetype='text/plain')
		except Exception as e:
			return HttpResponse('Internal Server Error: ' + str(e), status=500)
	else:
		return HttpResponse('Method Not Allowed', status=405)
