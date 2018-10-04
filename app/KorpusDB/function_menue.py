"""Menü."""
from django.db.models import Count, Q
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB


def getMenue(request, useOnlyErhebung, useArtErhebung, aufgabenOrderBy=['von_ASet', 'Variante']):
	aMenue = {
		'formular': None,
		'daten': {
			'nix': 'nix',
			'aAufgabenset': 0,
			'Aufgabensets': None,
			'aAufgabe': 0,
			'Aufgaben': None,
			'Informanten': None,
			'aInformant': 0,
			'selInformanten': None,
			'verfuegbareErhebungen': None,
			'aAuswahl': int(request.POST.get('aauswahl')) if 'aauswahl' in request.POST else 1,
			'aErhebung': 0,
		}
	}
	if aMenue['daten']['aAuswahl'] == 1:  # Filter: Erhebung
		aMenue['daten']['aErhebung'] = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
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
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle')]
					aMenue['formular'] = 'korpusdbfunctions/lmfa-l_informanten.html'
					return aMenue
				if aMenue['daten']['aAufgabenset'] == int(request.POST.get('laufgabenset')):
					aMenue['daten']['Informanten'] = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).count(),
						'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe']).annotate(tbl_antwortentags_count=Count('tbl_antwortentags')).filter(tbl_antwortentags_count__gt=0).count(),
						'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aMenue['daten']['aAufgabe'], tbl_antwortentags__id_Tag_id=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aMenue['daten']['aErhebung']).order_by('inf_sigle')]
				aMenue['daten']['Aufgaben'] = []
				for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aMenue['daten']['aAufgabenset'], tbl_erhebung_mit_aufgaben__id_Erh__pk=aMenue['daten']['aErhebung'], tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).order_by('von_ASet', 'Variante'):
					(aproz, atags, aqtags) = val.status(useArtErhebung)
					if InformantenCount > 0:
						aproz = 100 / InformantenCount * aproz
					else:
						aproz = 0
					aMenue['daten']['Aufgaben'].append({'model': val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
	if aMenue['daten']['aAuswahl'] == 2:  # Filter: Informant
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
				return aMenue
	return aMenue
