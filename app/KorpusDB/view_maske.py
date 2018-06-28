"""Für EingabeSTP."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db.models import Count, Q
import datetime
import json
from .models import sys_presettags
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB


def view_maske(request, ipk=0, apk=0):
	"""Ansicht für EingabeSTP."""
	aFormular = 'korpusdbmaske/start_formular.html'
	aUrl = '/korpusdb/maske/'
	aDUrl = 'KorpusDB:maske'
	useArtErhebung = [3, 4, 5]
	test = ''
	error = ''
	apk = int(apk)
	ipk = int(ipk)
	aAuswahl = 1
	if 'aauswahl' in request.POST:
		aAuswahl = int(request.POST.get('aauswahl'))
	if apk > 0 and ipk > 0:
		if 'save' in request.POST:
			if request.POST.get('save') == 'ErhInfAufgaben':
				saveErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.get(pk=int(request.POST.get('pk')))
				saveErhInfAufgaben.start_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('start_Aufgabe') if request.POST.get('start_Aufgabe') else 0) * 1000000))
				saveErhInfAufgaben.stop_Aufgabe = datetime.timedelta(microseconds=int(float(request.POST.get('stop_Aufgabe') if request.POST.get('stop_Aufgabe') else 0) * 1000000))
				saveErhInfAufgaben.save()
				LogEntry.objects.log_action(
					user_id=request.user.pk,
					content_type_id=ContentType.objects.get_for_model(saveErhInfAufgaben).pk,
					object_id=saveErhInfAufgaben.pk,
					object_repr=str(saveErhInfAufgaben),
					action_flag=CHANGE
				)
				aFormular = 'korpusdbmaske/audio_formular.html'
			elif request.POST.get('save') == 'Aufgaben':
				for aAntwort in json.loads(request.POST.get('aufgaben')):
					if 'delit' in aAntwort and int(aAntwort['id_Antwort']) > 0:		# Löschen
						aDelAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
						test += str(aDelAntwort) + ' Löschen!<br>'
						if aDelAntwort.ist_Satz:
							aDelAntwort.ist_Satz.delete()
							test += 'Satz gelöscht<br>'
						aDelAntwort.delete()
						test += '<hr>'
					else:						# Speichern/Erstellen
						if aAntwort['Kommentar'] or aAntwort['ist_Satz_Standardorth'] or aAntwort['ist_bfl'] or aAntwort['kontrolliert'] or aAntwort['veroeffentlichung'] or aAntwort['bfl_durch_S'] or aAntwort['ist_Satz_ipa'] or aAntwort['ist_Satz_Transkript'] or aAntwort['start_Antwort'] or aAntwort['stop_Antwort'] or aAntwort['tags']:
							if int(aAntwort['id_Antwort']) > 0:		# Speichern
								aSaveAntwort = KorpusDB.tbl_antworten.objects.get(pk=aAntwort['id_Antwort'])
								sTyp = ' gespeichert!<br>'
								aSaveAntwortNew = False
							else:									# Erstellen
								aSaveAntwort = KorpusDB.tbl_antworten()
								sTyp = ' erstellt!<br>'
								aSaveAntwortNew = True
							aSaveAntwort.ist_gewaehlt = False
							aSaveAntwort.ist_nat = False
							aSaveAntwort.von_Inf = PersonenDB.tbl_informanten.objects.get(pk=int(aAntwort['von_Inf']))
							aSaveAntwort.zu_Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=int(aAntwort['zu_Aufgabe']))
							aSaveAntwort.Reihung = int(aAntwort['reihung'])
							aSaveAntwort.ist_bfl = aAntwort['ist_bfl']
							aSaveAntwort.kontrolliert = aAntwort['kontrolliert']
							aSaveAntwort.veroeffentlichung = aAntwort['veroeffentlichung']
							aSaveAntwort.bfl_durch_S = aAntwort['bfl_durch_S']
							aSaveAntwort.start_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['start_Antwort'] if aAntwort['start_Antwort'] else 0) * 1000000))
							aSaveAntwort.stop_Antwort = datetime.timedelta(microseconds=int(float(aAntwort['stop_Antwort'] if aAntwort['stop_Antwort'] else 0) * 1000000))
							aSaveAntwort.Kommentar = aAntwort['Kommentar']
							if int(aAntwort['ist_Satz_pk']) > 0:  # Satz bearbeiten
								asSatz = KorpusDB.tbl_saetze.objects.get(pk=aAntwort['ist_Satz_pk'])
								ssTyp = ' gespeichert!<br>'
								asSatzNew = False
							else:									# Satz erstellen
								asSatz = KorpusDB.tbl_saetze()
								ssTyp = ' erstellt!<br>'
								asSatzNew = True
							asSatz.Transkript = aAntwort['ist_Satz_Transkript']
							asSatz.Standardorth = aAntwort['ist_Satz_Standardorth']
							asSatz.ipa = aAntwort['ist_Satz_ipa']
							asSatz.save()
							LogEntry.objects.log_action(
								user_id=request.user.pk,
								content_type_id=ContentType.objects.get_for_model(asSatz).pk,
								object_id=asSatz.pk,
								object_repr=str(asSatz),
								action_flag=ADDITION if asSatzNew else CHANGE
							)
							aSaveAntwort.ist_Satz = asSatz
							test += 'Satz "' + str(aSaveAntwort.ist_Satz) + '" (PK: ' + str(aSaveAntwort.ist_Satz.pk) + ')' + ssTyp
							aSaveAntwort.save()
							LogEntry.objects.log_action(
								user_id=request.user.pk,
								content_type_id=ContentType.objects.get_for_model(aSaveAntwort).pk,
								object_id=aSaveAntwort.pk,
								object_repr=str(aSaveAntwort),
								action_flag=ADDITION if aSaveAntwortNew else CHANGE
							)
							for asTag in aAntwort['tags']:
								if int(asTag['id_tag']) == 0 or int(asTag['id_TagEbene']) == 0:
									if int(asTag['pk']) > 0:
										aDelAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										test += 'AntwortenTag "' + str(aDelAntwortenTag) + '" (PK: ' + str(aDelAntwortenTag.pk) + ') gelöscht!<br>'
										aDelAntwortenTag.delete()
										LogEntry.objects.log_action(
											user_id=request.user.pk,
											content_type_id=ContentType.objects.get_for_model(aDelAntwortenTag).pk,
											object_id=aDelAntwortenTag.pk,
											object_repr=str(aDelAntwortenTag),
											action_flag=DELETION
										)
								else:
									if int(asTag['pk']) > 0:		# Tag bearbeiten
										asAntwortenTag = KorpusDB.tbl_antwortentags.objects.get(pk=int(asTag['pk']))
										stTyp = ' gespeichert!<br>'
										asAntwortenTagNew = False
									else:							# Tag erstellen
										asAntwortenTag = KorpusDB.tbl_antwortentags()
										stTyp = ' erstellt!<br>'
										asAntwortenTagNew = True
									asAntwortenTag.id_Antwort = aSaveAntwort
									asAntwortenTag.id_Tag = KorpusDB.tbl_tags.objects.get(pk=int(asTag['id_tag']))
									asAntwortenTag.id_TagEbene = KorpusDB.tbl_tagebene.objects.get(pk=int(asTag['id_TagEbene']))
									asAntwortenTag.Reihung = int(asTag['reihung'])
									asAntwortenTag.save()
									LogEntry.objects.log_action(
										user_id=request.user.pk,
										content_type_id=ContentType.objects.get_for_model(asAntwortenTag).pk,
										object_id=asAntwortenTag.pk,
										object_repr=str(asAntwortenTag),
										action_flag=ADDITION if asAntwortenTagNew else CHANGE
									)
									test += 'AntwortenTag "' + str(asAntwortenTag) + '" (PK: ' + str(asAntwortenTag.pk) + ')' + stTyp
							test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ')' + sTyp + '<hr>'
				aFormular = 'korpusdbmaske/antworten_formular.html'
		Informant = PersonenDB.tbl_informanten.objects.get(pk=ipk)
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		eAntwort = KorpusDB.tbl_antworten()
		eAntwort.von_Inf = Informant
		eAntwort.zu_Aufgabe = Aufgabe
		TagEbenen = KorpusDB.tbl_tagebene.objects.all()
		TagsList = getTagList(KorpusDB.tbl_tags, None)
		Antworten = []
		for val in KorpusDB.tbl_antworten.objects.filter(von_Inf=ipk, zu_Aufgabe=apk).order_by('Reihung'):
			xtags = []
			for xval in KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
				xtags.append({'ebene': KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags': getTagFamilie(KorpusDB.tbl_antwortentags.objects.filter(id_Antwort=val.pk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
			Antworten.append({'model': val, 'xtags': xtags})
		Antworten.append(eAntwort)
		ErhInfAufgaben = KorpusDB.tbl_erhinfaufgaben.objects.filter(id_Aufgabe=apk, id_InfErh__ID_Inf__pk=ipk)
		aPresetTags = []
		for val in sys_presettags.objects.filter(Q(sys_presettagszuaufgabe__id_Aufgabe=Aufgabe) | Q(sys_presettagszuaufgabe__id_Aufgabe=None)).distinct():
			aPresetTags.append({'model': val, 'tagfamilie': getTagFamiliePT([tzpval.id_Tag for tzpval in val.sys_tagszupresettags_set.all()])})
		return render_to_response(
			aFormular,
			RequestContext(request, {'Informant': Informant, 'Aufgabe': Aufgabe, 'Antworten': Antworten, 'TagEbenen': TagEbenen, 'TagsList': TagsList, 'ErhInfAufgaben': ErhInfAufgaben, 'PresetTags': aPresetTags, 'aDUrl': aDUrl, 'test': test, 'error': error}),)
	aErhebung = 0
	Erhebungen = [{
		'model': val,
		'Acount': KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=val.pk).values('pk').annotate(Count('pk')).count()
	} for val in KorpusDB.tbl_erhebungen.objects.filter(Art_Erhebung__in=useArtErhebung)]
	aAufgabenset = 0
	Aufgabensets = None
	aAufgabe = 0
	Aufgaben = None
	Informanten = None
	if aAuswahl == 1:  # Filter: Erhebung
		aErhebung = int(request.POST.get('aerhebung')) if 'aaufgabenset' in request.POST else 0
		if aErhebung:
			InformantenCount = PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aErhebung).count()
			Aufgabensets = []
			for val in KorpusDB.tbl_aufgabensets.objects.filter(tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aErhebung, tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).distinct():
				Aufgabensets.append({
					'model': val,
					'Acount': KorpusDB.tbl_aufgaben.objects.filter(von_ASet=val.pk, tbl_erhebung_mit_aufgaben__id_Erh__pk=aErhebung, tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count()
				})
			aAufgabenset = int(request.POST.get('aaufgabenset')) if 'aaufgabenset' in request.POST else 0
			if KorpusDB.tbl_aufgabensets.objects.filter(pk=aAufgabenset, tbl_aufgaben__tbl_erhebung_mit_aufgaben__id_Erh__pk=aErhebung).count() == 0:
				aAufgabenset = 0
			if aAufgabenset:
				aAufgabe = int(request.POST.get('aaufgabe')) if 'aaufgabenset' in request.POST else 0
				if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
					Informanten = [{
						'model': val,
						'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aAufgabe).count(), 'tags': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aAufgabe).exclude(tbl_antwortentags=None).count(), 'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aAufgabe, tbl_antwortentags__id_Tag=35).count()
					} for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aErhebung).order_by('inf_sigle')]
					return render_to_response(
						'korpusdbmaske/lmfa-l_informanten.html',
						RequestContext(request, {'aErhebung': aErhebung, 'aAufgabenset': aAufgabenset, 'aAufgabe': aAufgabe, 'Informanten': Informanten, 'aDUrl': aDUrl}),)
				if aAufgabenset == int(request.POST.get('laufgabenset')):
					Informanten = []
					for val in PersonenDB.tbl_informanten.objects.filter(tbl_inferhebung__ID_Erh__pk=aErhebung).order_by('inf_sigle'):
						aCount = 0
						tCount = 0
						for xval in KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aAufgabe):
							aCount += 1
							if xval.tbl_antwortentags_set.count() > 0:
								tCount += 1
						Informanten.append({
							'model': val,
							'count': aCount,
							'tags': tCount,
							'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=val, zu_Aufgabe=aAufgabe, tbl_antwortentags__id_Tag_id=35).count()
						})
				Aufgaben = []
				for val in KorpusDB.tbl_aufgaben.objects.filter(von_ASet=aAufgabenset, tbl_erhebung_mit_aufgaben__id_Erh__pk=aErhebung, tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).order_by('von_ASet', 'Variante'):
					(aproz, atags, aqtags) = val.status(useArtErhebung)
					if InformantenCount > 0:
						aproz = 100 / InformantenCount * aproz
					else:
						aproz = 0
					Aufgaben.append({'model': val, 'aProz': aproz, 'aTags': atags, 'aQTags': aqtags})
	aInformant = 0
	selInformanten = None
	verfuegbareErhebungen = []
	if aAuswahl == 2:  # Filter: Informant
		selInformanten = []
		for val in PersonenDB.tbl_informanten.objects.all():
			aSelInformanten = {'model': val}
			aSelInformanten['count'] = KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk=val.pk, tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count()
			try:
				aSelInformanten['done'] = KorpusDB.tbl_antworten.objects.filter(von_Inf=val.pk, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).values('zu_Aufgabe').annotate(total=Count('zu_Aufgabe')).order_by('zu_Aufgabe').count()
			except:
				aSelInformanten['done'] = 0
			selInformanten.append(aSelInformanten)
		if 'ainformant' in request.POST:
			aInformant = int(request.POST.get('ainformant'))
			Aufgaben = []
			for val in KorpusDB.tbl_aufgaben.objects.filter(tbl_erhinfaufgaben__id_InfErh__ID_Inf__pk=aInformant, tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).order_by('von_ASet', 'Variante'):
				tagscount = 0
				for aAntwortfc in KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant, zu_Aufgabe=val.pk):
					if aAntwortfc.tbl_antwortentags_set.count() > 0:
						tagscount += 1
				aAufgabeLine = {
					'model': val,
					'count': KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant, zu_Aufgabe=val.pk, zu_Aufgabe__tbl_erhebung_mit_aufgaben__id_Erh__Art_Erhebung__in=useArtErhebung).count(),
					'tags': tagscount,
					'qtag': KorpusDB.tbl_antworten.objects.filter(von_Inf=aInformant, zu_Aufgabe=val.pk, tbl_antwortentags__id_Tag=35).count()
				}
				try:
					aAufgabeLine['erhebungen'] = []
					for aErheb in KorpusDB.tbl_erhebung_mit_aufgaben.objects.filter(id_Aufgabe=val.pk):
						aErhebungenLine = {'pk': aErheb.id_Erh.pk, 'title': str(aErheb.id_Erh)}
						aAufgabeLine['erhebungen'].append(aErhebungenLine)
						if aErhebungenLine not in verfuegbareErhebungen:
							verfuegbareErhebungen.append(aErhebungenLine)
				except:
					pass
				Aufgaben.append(aAufgabeLine)
			if 'infantreset' in request.POST:		# InformantenAntwortenUpdate
				return render_to_response(
					'korpusdbmaske/lmfa-l_aufgaben.html',
					RequestContext(request, {'aInformant': aInformant, 'Aufgaben': Aufgaben, 'verfuegbareErhebungen': verfuegbareErhebungen, 'aDUrl': aDUrl}),)
	# Ausgabe der Seite
	return render_to_response(
		'korpusdbmaske/start.html',
		RequestContext(request, {'aAuswahl': aAuswahl, 'selInformanten': selInformanten, 'aInformant': aInformant, 'aErhebung': aErhebung, 'Erhebungen': Erhebungen, 'aAufgabenset': aAufgabenset, 'Aufgabensets': Aufgabensets, 'aAufgabe': aAufgabe, 'Aufgaben': Aufgaben, 'Informanten': Informanten, 'verfuegbareErhebungen': verfuegbareErhebungen, 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)


# Funktionen: #
def getTagFamilie(Tags):
	"""Ermittelt Tag Familie für AntwortenTags."""
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen -= 1
				pClose += 1
				del afam[-1]
		except:
			pass
		# print(''.rjust(aGen,'-')+'|'+str(value.id_Tag.Tag)+' ('+str(value.id_Tag.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag': value, 'aGen': aGen, 'pClose': pClose, 'pChilds': value.id_Tag.id_ParentTag.all().count()})
		afam.append(value.id_Tag)
		aGen += 1
	return oTags


def getTagFamiliePT(Tags):
	"""Ermittelt Tag Familie für PresetTags."""
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen -= 1
				pClose += 1
				del afam[-1]
		except:
			pass
		# print(''.rjust(aGen,'-')+'|'+str(value.Tag)+' ('+str(value.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag': value, 'aGen': aGen, 'pClose': pClose, 'pChilds': value.id_ParentTag.all().count()})
		afam.append(value)
		aGen += 1
	return oTags


def getTagList(Tags, TagPK):
	"""Gibt Tag Liste zurück."""
	TagData = []
	if TagPK is None:
		for value in Tags.objects.filter(id_ChildTag=None):
			child = getTagList(Tags, value.pk)
			TagData.append({'model': value, 'child': child})
	else:
		for value in Tags.objects.filter(id_ChildTag__id_ParentTag=TagPK):
			child = getTagList(Tags, value.pk)
			TagData.append({'model': value, 'child': child})
	return TagData
