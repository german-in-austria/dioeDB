"""Menü."""
from django.db.models import Count, Q
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
import time
import json


def getMenue(request, useOnlyErhebung, useArtErhebung, aufgabenOrderBy=['von_ASet', 'Variante'], fixAuswahl=[]):
	"""Menüdaten ermitteln."""
	start_time = time.time()
	aMenue = {
		'formular': None,
		'daten': {
			'fixAuswahl': fixAuswahl,
			'showAuswahl': (not fixAuswahl or len(fixAuswahl) != 1),
			'aAufgabenset': 0,
			'Aufgabensets': None,
			'aAufgabe': 0,
			'Aufgaben': None,
			'Informanten': None,
			'aInformant': 0,
			'selInformanten': None,
			'verfuegbareErhebungen': [],
			'aAuswahl': int(request.POST.get('aauswahl')) if 'aauswahl' in request.POST else 1 if not fixAuswahl else fixAuswahl[0],
			'aErhebung': 0,
		}
	}

	# Filter: Erhebung
	if aMenue['daten']['aAuswahl'] == 1 and (not fixAuswahl or aMenue['daten']['aAuswahl'] in fixAuswahl):
		aMenue['daten']['aErhebung'] = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
		ErhebungsFilter = {'Art_Erhebung__in': useArtErhebung}
		if useOnlyErhebung:
			ErhebungsFilter['pk__in'] = useOnlyErhebung
		aMenue['daten']['Erhebungen'] = [{
			'model': val,
			'Acount': KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=val.pk).values('pk').annotate(Count('pk')).count()
		} for val in KorpusDB.tbl_erhebungen.objects.filter(**ErhebungsFilter)]
		if useOnlyErhebung:
			if aMenue['daten']['aErhebung'] not in useOnlyErhebung:
				aMenue['daten']['aErhebung'] = 0
		if aMenue['daten']['aErhebung']:
			InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inf_zu_erhebung__id_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
			aMenue['daten']['Aufgabensets'] = []
			for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).distinct():
				aMenue['daten']['Aufgabensets'].append({
					'model': val,
					'Acount': KorpusDB.tbl_aufgaben.objects.filter(von_ASet=val.pk, tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count()
				})
			aMenue['daten']['aAufgabenset'] = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
			if KorpusDB.tbl_aufgabensets.objects.filter(pk=aMenue['daten']['aAufgabenset'], tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung']).count() == 0:
				aMenue['daten']['aAufgabenset'] = 0
			if aMenue['daten']['aAufgabenset']:
				aMenue['daten']['aAufgabe'] = int(request.POST.get('aaufgabe')) if 'aaufgabenset' in request.POST else 0
				if 'infantreset' in request.POST or aMenue['daten']['aAufgabenset'] == int(request.POST.get('laufgabenset')):		# InformantenAntwortenUpdate
					x_start_time = time.time()
					aMenue['daten']['Informanten'] = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).count(),
						'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
						'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe'], tbl_antwortentags__id_Tag_id=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inf_zu_erhebung__id_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle').distinct()]
					print('if "infantreset" in request.POST:', time.time() - x_start_time, 'Sekunden')
					if 'infantreset' in request.POST:
						aMenue['formular'] = 'korpusdbfunctions/lmfa-l_informanten.html'
						return aMenue
				aMenue['daten']['Aufgaben'] = []
				for val in KorpusDB.tbl_aufgaben.objects.raw('''
					SELECT "KorpusDB_tbl_aufgaben".*,
						(
							SELECT COUNT("KorpusDB_tbl_antworten"."von_Inf_id")
							FROM "KorpusDB_tbl_antworten"
							INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
							INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
							WHERE ( "KorpusDB_tbl_antworten"."zu_Aufgabe_id" = "KorpusDB_tbl_aufgaben"."id" AND
									"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s
							)
							GROUP BY "KorpusDB_tbl_antworten"."zu_Aufgabe_id", "KorpusDB_tbl_antworten"."Reihung"
							ORDER BY "KorpusDB_tbl_antworten"."Reihung" ASC LIMIT 1
						) AS aproz,
						(
							SELECT COUNT(*)
							FROM (
								SELECT "KorpusDB_tbl_antworten"."id" AS Col1, COUNT("KorpusDB_tbl_antworten"."von_Inf_id") AS "total"
								FROM "KorpusDB_tbl_antworten"
								INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
								INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
								WHERE (
									"KorpusDB_tbl_antworten"."zu_Aufgabe_id" = "KorpusDB_tbl_aufgaben"."id" AND
									"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s
								)
								GROUP BY "KorpusDB_tbl_antworten"."id"
							) subquery
						) AS atags_a,
						(
							SELECT COUNT(*)
							FROM (
								SELECT "KorpusDB_tbl_antworten"."id" AS Col1, COUNT("KorpusDB_tbl_antworten"."von_Inf_id") AS "total" FROM "KorpusDB_tbl_antworten"
								WHERE (
									"KorpusDB_tbl_antworten"."zu_Aufgabe_id" = "KorpusDB_tbl_aufgaben"."id" AND
									NOT (
										"KorpusDB_tbl_antworten"."id" IN (
											SELECT U0."id" AS Col1
											FROM "KorpusDB_tbl_antworten"
											U0 LEFT OUTER JOIN "KorpusDB_tbl_antwortentags"
											U1 ON ( U0."id" = U1."id_Antwort_id" )
											WHERE U1."id" IS NULL
										)
									)
								)
								GROUP BY "KorpusDB_tbl_antworten"."id"
							) subquery
						) AS atags_b,
						(
							SELECT COUNT(*)
							FROM (
								SELECT "KorpusDB_tbl_antworten"."id" AS Col1, COUNT("KorpusDB_tbl_antworten"."von_Inf_id") AS "total"
								FROM "KorpusDB_tbl_antworten"
								INNER JOIN "KorpusDB_tbl_antwortentags" ON ( "KorpusDB_tbl_antworten"."id" = "KorpusDB_tbl_antwortentags"."id_Antwort_id" )
								INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
								INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
								WHERE (
									"KorpusDB_tbl_antworten"."zu_Aufgabe_id" = "KorpusDB_tbl_aufgaben"."id" AND
									"KorpusDB_tbl_antwortentags"."id_Tag_id" = 35 AND
									"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s
								)
								GROUP BY "KorpusDB_tbl_antworten"."id"
							) subquery
						) AS aqtags
					FROM "KorpusDB_tbl_aufgaben"
					INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
					INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
					INNER JOIN "KorpusDB_tbl_aufgabensets" ON ( "KorpusDB_tbl_aufgaben"."von_ASet_id" = "KorpusDB_tbl_aufgabensets"."id" )
					WHERE (
						"KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = %s AND
						"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s AND
						"KorpusDB_tbl_aufgaben"."von_ASet_id" = %s
					)
					ORDER BY "KorpusDB_tbl_aufgabensets"."Kuerzel" ASC, "KorpusDB_tbl_aufgaben"."Variante" ASC
					''', [tuple(useArtErhebung), tuple(useArtErhebung), tuple(useArtErhebung), aMenue['daten']['aErhebung'], tuple(useArtErhebung), aMenue['daten']['aAufgabenset']]):
						if InformantenCount > 0 and val.aproz:
							aproz = 100 / InformantenCount * val.aproz
						else:
							aproz = 0
						aMenue['daten']['Aufgaben'].append({'model': val, 'aProz': (aproz if aproz else 0), 'aTags': (100 / val.atags_a * val.atags_b) if val.atags_a else 0, 'aQTags': val.aqtags})

	# Filter: Informant
	if aMenue['daten']['aAuswahl'] == 2 and (not fixAuswahl or aMenue['daten']['aAuswahl'] in fixAuswahl):
		# Informanten ermitteln:
		if useOnlyErhebung:
			qData = [tuple(useOnlyErhebung), tuple(useArtErhebung), tuple(useOnlyErhebung), tuple(useArtErhebung)]
		else:
			qData = [tuple(useArtErhebung), tuple(useArtErhebung)]
		aMenue['daten']['selInformanten'] = PersonenDB.tbl_informanten.objects.raw('''
			SELECT "PersonenDB_tbl_informanten".*,
				(
					SELECT COUNT(*)
					FROM "KorpusDB_tbl_aufgaben"
					INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
					INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
					INNER JOIN "KorpusDB_tbl_erhinfaufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhinfaufgaben"."id_Aufgabe_id" )
					INNER JOIN "KorpusDB_tbl_inferhebung" ON ( "KorpusDB_tbl_erhinfaufgaben"."id_InfErh_id" = "KorpusDB_tbl_inferhebung"."id" )
					INNER JOIN "KorpusDB_tbl_inf_zu_erhebung" ON ( "KorpusDB_tbl_inferhebung"."id" = "KorpusDB_tbl_inf_zu_erhebung"."id_inferhebung_id" )
					WHERE (''' + ('''
			 			"KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" IN %s AND''' if useOnlyErhebung else '') + '''
						"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s AND
						"KorpusDB_tbl_inf_zu_erhebung"."ID_Inf_id" = "PersonenDB_tbl_informanten"."id"
					)
				) AS aufgaben_count,
				(
					SELECT COUNT(*)
					FROM (
						SELECT "KorpusDB_tbl_antworten"."zu_Aufgabe_id" AS Col1, COUNT("KorpusDB_tbl_antworten"."zu_Aufgabe_id") AS "total"
						FROM "KorpusDB_tbl_antworten"
						INNER JOIN "KorpusDB_tbl_aufgaben" ON ( "KorpusDB_tbl_antworten"."zu_Aufgabe_id" = "KorpusDB_tbl_aufgaben"."id" )
						INNER JOIN "KorpusDB_tbl_erhebung_mit_aufgaben" ON ( "KorpusDB_tbl_aufgaben"."id" = "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Aufgabe_id" )
						INNER JOIN "KorpusDB_tbl_erhebungen" ON ( "KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" = "KorpusDB_tbl_erhebungen"."id" )
						WHERE (''' + ('''
			 				"KorpusDB_tbl_erhebung_mit_aufgaben"."id_Erh_id" IN %s AND''' if useOnlyErhebung else '') + '''
							"KorpusDB_tbl_erhebungen"."Art_Erhebung_id" IN %s AND
							"KorpusDB_tbl_antworten"."von_Inf_id" = "PersonenDB_tbl_informanten"."id"
						)
						GROUP BY "KorpusDB_tbl_antworten"."zu_Aufgabe_id"
					) subquery
				) AS aufgaben_done
			FROM "PersonenDB_tbl_informanten"
			ORDER BY "PersonenDB_tbl_informanten"."inf_sigle" ASC
		''', qData)

		if 'ainformant' in request.POST:
			aMenue['daten']['aInformant'] = int(request.POST.get('ainformant'))
			aMenue['daten']['Aufgaben'] = []
			atblaFilter = {'tbl_erhinfaufgaben__id_InfErh__tbl_inf_zu_erhebung__ID_Inf__pk': aMenue['daten']['aInformant'], 'tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in': useArtErhebung}
			if useOnlyErhebung:
				atblaFilter['tbl_erhebung_mit_aufgaben__id_Erh__pk__in'] = useOnlyErhebung
			for val in KorpusDB.tbl_aufgaben.objects.filter(**atblaFilter).order_by(*aufgabenOrderBy):
				aAufgabeLine = {
					'model': val,
					'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=aMenue['daten']['aInformant'], zu_Aufgabe=val.pk, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count(),
					'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=aMenue['daten']['aInformant'], zu_Aufgabe=val.pk).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
					'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=aMenue['daten']['aInformant'], zu_Aufgabe=val.pk, tbl_antwortentags__id_Tag=35).count()
				}
				try:
					aAufgabeLine['erhebungen'] = []
					for aErheb in KorpusDB.tbl_erhebung_mit_aufgaben.objects.select_related('id_Erh').filter(id_Aufgabe=val.pk):
						aErhebungenLine = {'pk': aErheb.id_Erh.pk, 'title': str(aErheb.id_Erh)}
						aAufgabeLine['erhebungen'].append(aErhebungenLine)
						if aErhebungenLine not in aMenue['daten']['verfuegbareErhebungen']:
							aMenue['daten']['verfuegbareErhebungen'].append(aErhebungenLine)
				except:
					pass
				aMenue['daten']['Aufgaben'].append(aAufgabeLine)
		if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
			aMenue['formular'] = 'korpusdbfunctions/lmfa-l_aufgaben.html',
		# print('Filter: Informant', time.time() - start_time, 'Sekunden')

	# Filter: Phänomen
	if aMenue['daten']['aAuswahl'] == 3 and (not fixAuswahl or aMenue['daten']['aAuswahl'] in fixAuswahl):
		aMenue['daten']['aPhaenomen'] = int(request.POST.get('aphaenomen')) if 'aphaenomen' in request.POST else 0
		ErhebungsFilter = {'Art_Erhebung__in': useArtErhebung}
		if useOnlyErhebung:
			ErhebungsFilter['pk__in'] = useOnlyErhebung
		aMenue['daten']['phaenomene'] = [{
			'model': val,
			'Acount': KorpusDB.tbl_erhebungen.objects.filter(**ErhebungsFilter).filter(Q(tbl_erhebung_mit_aufgaben__id_Aufgabe__von_ASet__zu_Phaenomen__pk=val.pk) | Q(tbl_erhebung_mit_aufgaben__id_Aufgabe__tbl_phaenzuaufgabe__id_phaenomen__pk=val.pk)).values('pk').annotate(Count('pk')).count()
		} for val in KorpusDB.tbl_phaenomene.objects.all()]
		if aMenue['daten']['aPhaenomen']:
			aMenue['daten']['aErhebung'] = int(request.POST.get('aerhebung')) if 'aerhebung' in request.POST else 0
			aMenue['daten']['Erhebungen'] = [{
				'model': val,
				'Acount': KorpusDB.tbl_aufgaben.objects.filter(tbl_erhebung_mit_aufgaben__id_Erh__pk=val.pk).filter(Q(von_ASet__zu_Phaenomen__pk=aMenue['daten']['aPhaenomen']) | Q(tbl_phaenzuaufgabe__id_phaenomen__pk=aMenue['daten']['aPhaenomen'])).values('pk').annotate(Count('pk')).count()
			} for val in KorpusDB.tbl_erhebungen.objects.filter(**ErhebungsFilter).filter(Q(tbl_erhebung_mit_aufgaben__id_Aufgabe__von_ASet__zu_Phaenomen__pk=aMenue['daten']['aPhaenomen']) | Q(tbl_erhebung_mit_aufgaben__id_Aufgabe__tbl_phaenzuaufgabe__id_phaenomen__pk=aMenue['daten']['aPhaenomen'])).distinct()]
			if aMenue['daten']['aErhebung']:
				aMenue['daten']['aAufgabe'] = int(request.POST.get('aaufgabe')) if 'aaufgabe' in request.POST else 0
				aAufgabeNew = True
				aMenue['daten']['Aufgaben'] = []
				InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inf_zu_erhebung__id_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
				for val in KorpusDB.tbl_aufgaben.objects.filter(tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).filter(Q(von_ASet__zu_Phaenomen__pk=aMenue['daten']['aPhaenomen']) | Q(tbl_phaenzuaufgabe__id_phaenomen__pk=aMenue['daten']['aPhaenomen'])).distinct().order_by('von_ASet', 'Variante'):
					(aproz, atags, aqtags) = val.status(useArtErhebung)
					if InformantenCount > 0:
						aproz = 100 / InformantenCount * aproz
					else:
						aproz = 0
					aMenue['daten']['Aufgaben'].append({'model': val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
					if val.pk == aMenue['daten']['aAufgabe']:
						aAufgabeNew = False
				if aAufgabeNew:
					aMenue['daten']['aAufgabe'] = 0
				if aMenue['daten']['aAufgabe']:
					aMenue['daten']['Informanten'] = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).count(),
						'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
						'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe'], tbl_antwortentags__id_Tag_id=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inf_zu_erhebung__id_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle').distinct()]
		if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
			aMenue['formular'] = 'korpusdbfunctions/lmfa-l_informanten.html'
			return aMenue

	# Filter: Spezieller Aufgabenfilter
	if aMenue['daten']['aAuswahl'] == 4 and (not fixAuswahl or aMenue['daten']['aAuswahl'] in fixAuswahl):
		aMenue['daten']['aErhebung'] = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
		ErhebungsFilter = {'Art_Erhebung__in': useArtErhebung}
		if useOnlyErhebung:
			ErhebungsFilter['pk__in'] = useOnlyErhebung
		aMenue['daten']['Erhebungen'] = [{
			'model': val,
			'Acount': KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=val.pk).values('pk').annotate(Count('pk')).count()
		} for val in KorpusDB.tbl_erhebungen.objects.filter(**ErhebungsFilter)]
		if useOnlyErhebung:
			if aMenue['daten']['aErhebung'] not in useOnlyErhebung:
				aMenue['daten']['aErhebung'] = 0
		if aMenue['daten']['aErhebung']:
			InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inf_zu_erhebung__id_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
			aMenue['daten']['Aufgabensets'] = []
			for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).distinct():
				aMenue['daten']['Aufgabensets'].append({
					'model': val,
					'Acount': KorpusDB.tbl_aufgaben.objects.filter(Aufgabenart_id=1, von_ASet=val.pk, tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count()
				})
			aMenue['daten']['aAufgabenset'] = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
			if KorpusDB.tbl_aufgabensets.objects.filter(pk=aMenue['daten']['aAufgabenset'], tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung']).count() == 0:
				aMenue['daten']['aAufgabenset'] = 0
			if aMenue['daten']['aAufgabenset']:
				aMenue['daten']['Aufgaben'] = []
				atblaFilter = {'Aufgabenart_id': 1, 'von_ASet': int(aMenue['daten']['aAufgabenset']), 'tbl_erhebung_mit_aufgaben__id_Erh__pk': aMenue['daten']['aErhebung'], 'tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in': useArtErhebung}
				if useOnlyErhebung:
					atblaFilter['tbl_erhebung_mit_aufgaben__id_Erh__pk__in'] = useOnlyErhebung
				for val in KorpusDB.tbl_aufgaben.objects.filter(**atblaFilter).order_by(*aufgabenOrderBy):
					aAufgabeLine = {
						'model': val
					}
					aMenue['daten']['Aufgaben'].append(aAufgabeLine)
		if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
			aMenue['formular'] = 'korpusdbfunctions/lmfa-l_aufgaben.html'
			return aMenue

	# Ende
	return aMenue
