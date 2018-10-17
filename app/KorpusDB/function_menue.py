"""Menü."""
from django.db.models import Count, Q
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB


def getMenue(request, useOnlyErhebung, useArtErhebung, aufgabenOrderBy=['von_ASet', 'Variante'], fixAuswahl=[]):
	"""Menüdaten ermitteln."""
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
			InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
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
				if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
					aMenue['daten']['Informanten'] = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).count(),
						'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
						'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe'], tbl_antwortentags__id_Tag_id=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle').distinct()]
					aMenue['formular'] = 'korpusdbfunctions/lmfa-l_informanten.html'
					return aMenue
				if aMenue['daten']['aAufgabenset'] == int(request.POST.get('laufgabenset')):
					aMenue['daten']['Informanten'] = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).count(),
						'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
						'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe'], tbl_antwortentags__id_Tag_id=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle').distinct()]
				aMenue['daten']['Aufgaben'] = []
				for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aMenue['daten']['aAufgabenset'], tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).order_by('von_ASet', 'Variante'):
					(aproz, atags, aqtags) = val.status(useArtErhebung)
					if InformantenCount > 0:
						aproz = 100 / InformantenCount * aproz
					else:
						aproz = 0
					aMenue['daten']['Aufgaben'].append({'model': val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})

	# Filter: Informant
	if aMenue['daten']['aAuswahl'] == 2 and (not fixAuswahl or aMenue['daten']['aAuswahl'] in fixAuswahl):
		aMenue['daten']['selInformanten'] = []
		for val in PersonenDB.tbl_informanten.objects.all():
			aSelInformantenFilter = {'tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk': val.pk, 'tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in': useArtErhebung}
			if useOnlyErhebung:
				aSelInformantenFilter['tbl_erhebung_mit_aufgaben__id_Erh__pk__in'] = useOnlyErhebung
			aSelInformanten = {'model': val}
			aSelInformanten['count'] = KorpusDB.tbl_aufgaben.objects.filter(**aSelInformantenFilter).count()
			try:
				aSelInformantenFilter = {'von_Inf': val.pk, 'zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in': useArtErhebung}
				if useOnlyErhebung:
					aSelInformantenFilter['zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__pk__in'] = useOnlyErhebung
				aSelInformanten['done'] = KorpusDB.tbl_antworten.objects.filter(**aSelInformantenFilter).values('zu_Aufgabe').annotate(total=Count('zu_Aufgabe')).order_by('zu_Aufgabe').count()
			except:
				aSelInformanten['done'] = 0
			aMenue['daten']['selInformanten'].append(aSelInformanten)
		if 'ainformant' in request.POST:
			aMenue['daten']['aInformant'] = int(request.POST.get('ainformant'))
			aMenue['daten']['Aufgaben'] = []
			atblaFilter = {'tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk': aMenue['daten']['aInformant'], 'tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in': useArtErhebung}
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
				InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
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
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle').distinct()]
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
			InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).count()
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
