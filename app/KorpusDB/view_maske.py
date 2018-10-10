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
from .function_menue import getMenue
from .function_tags import saveTags


def view_maske(request, ipk=0, apk=0):
	"""Ansicht für EingabeSTP."""
	aFormular = 'korpusdbmaske/start_formular.html'
	aUrl = '/korpusdb/maske/'
	aDUrl = 'KorpusDB:maske'
	useArtErhebung = [3, 4, 5]
	useOnlyErhebung = []
	for aUKDBES in request.user.user_korpusdb_erhebung_set.all():
		useOnlyErhebung.append(aUKDBES.erhebung_id)
	test = ''
	error = ''
	apk = int(apk)
	ipk = int(ipk)
	if apk > 0 and ipk > 0:
		# Speichern
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
							# Tags speichern/bearbeiten/löschen
							test += saveTags(request, aAntwort['tags'], aSaveAntwort)
							test += 'Antwort "' + str(aSaveAntwort) + '" (PK: ' + str(aSaveAntwort.pk) + ')' + sTyp + '<hr>'
				aFormular = 'korpusdbmaske/antworten_formular.html'
		# Formulardaten ermitteln
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
			aPresetTags.append({'model': val, 'tagfamilie': getTagFamiliePT([tzpval.id_Tag for tzpval in val.sys_tagszupresettags_set.select_related('id_Tag').all()])})
		return render_to_response(
			aFormular,
			RequestContext(request, {'Informant': Informant, 'Aufgabe': Aufgabe, 'Antworten': Antworten, 'TagEbenen': TagEbenen, 'TagsList': TagsList, 'ErhInfAufgaben': ErhInfAufgaben, 'PresetTags': aPresetTags, 'aDUrl': aDUrl, 'test': test, 'error': error}),)
	# Menü
	aMenue = getMenue(request, useOnlyErhebung, useArtErhebung, ['von_ASet', 'Variante'])
	if aMenue['formular']:
		return render_to_response(
			aMenue['formular'],
			RequestContext(request, {'menueData': aMenue['daten'], 'aDUrl': aDUrl}),)
	# Ausgabe der Seite
	return render_to_response(
		'korpusdbmaske/start.html',
		RequestContext(request, {'menueData': aMenue['daten'], 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)


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
			iCTcach = [xval.id_ParentTag_id for xval in value.id_ChildTag.all()]
			while len(afam) > 0 and not afam[-1].pk in iCTcach:
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
