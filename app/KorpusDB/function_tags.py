"""Tags."""
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db.models import Count, Q
from .models import sys_presettags
import KorpusDB.models as KorpusDB


def saveTags(request, aTags, aSaveAntwort):
	"""Tags speichern/bearbeiten/löschen."""
	test = ''
	for asTag in aTags:
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
	return test


def getTags(aPk):
	"""Tags zur aufgabe ermitteln."""
	xTags = []
	for xval in KorpusDB.tbl_antwortentags.objects.filter(id_Antwort_id=aPk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
		xTags.append({'ebene': KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags': getTagFamilie(KorpusDB.tbl_antwortentags.objects.filter(id_Antwort_id=aPk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
	return xTags


def getTagsData(aPk):
	"""Allgemeine Daten zu Tags ermitteln."""
	tagData = {}
	tagData['TagEbenen'] = KorpusDB.tbl_tagebene.objects.all()
	tagData['TagsList'] = getTagList(KorpusDB.tbl_tags, None)
	tagData['aPresetTags'] = []
	for val in sys_presettags.objects.filter(Q(sys_presettagszuaufgabe__id_Aufgabe_id=aPk) | Q(sys_presettagszuaufgabe__id_Aufgabe=None)).distinct():
		tagData['aPresetTags'].append({'model': val, 'tagfamilie': getTagFamiliePT([tzpval.id_Tag for tzpval in val.sys_tagszupresettags_set.select_related('id_Tag').all()])})
	return tagData


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
