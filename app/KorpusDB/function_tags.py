"""Tags."""
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db.models import Count, Q
from .models import sys_presettags, sys_tagszupresettags
import KorpusDB.models as KorpusDB
from django.db.models.query import prefetch_related_objects
import time


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


def saveAMTags(request, aTags, aSaveAntwortmoeglichkeit):
	"""Tags speichern/bearbeiten/löschen."""
	test = ''
	for asTag in aTags:
		if int(asTag['id_tag']) == 0 or int(asTag['id_TagEbene']) == 0:
			if int(asTag['pk']) > 0:
				aDelAntwortenTag = KorpusDB.tbl_amtags.objects.get(pk=int(asTag['pk']))
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
				asAntwortenTag = KorpusDB.tbl_amtags.objects.get(pk=int(asTag['pk']))
				stTyp = ' gespeichert!<br>'
				asAntwortenTagNew = False
			else:							# Tag erstellen
				asAntwortenTag = KorpusDB.tbl_amtags()
				stTyp = ' erstellt!<br>'
				asAntwortenTagNew = True
			asAntwortenTag.id_am_id = aSaveAntwortmoeglichkeit
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


def getAMTags(aPk):
	"""Tags zur aAntwortmoeglichkeit ermitteln."""
	xTags = []
	for xval in KorpusDB.tbl_amtags.objects.filter(id_am_id=aPk).values('id_TagEbene').annotate(total=Count('id_TagEbene')).order_by('id_TagEbene'):
		xTags.append({'ebene': KorpusDB.tbl_tagebene.objects.filter(pk=xval['id_TagEbene']), 'tags': getTagFamilie(KorpusDB.tbl_amtags.objects.filter(id_am_id=aPk, id_TagEbene=xval['id_TagEbene']).order_by('Reihung'))})
	return xTags


def getTagsData(aPk):
	"""Allgemeine Daten zu Tags ermitteln."""
	tagData = {}
	tagData['TagEbenen'] = KorpusDB.tbl_tagebene.objects.all()
	# start_time = time.time()
	tagData['TagsList'] = getTagList(KorpusDB.tbl_tags, None)
	# print('getTagList', time.time() - start_time, 'Sekunden')
	tagData['aPresetTags'] = []
	# start_time = time.time()
	for val in sys_presettags.objects.filter(Q(sys_presettagszuaufgabe__id_Aufgabe_id=aPk) | Q(sys_presettagszuaufgabe__id_Aufgabe=None)).distinct():
		tagData['aPresetTags'].append({'model': val, 'tagfamilie': getTagFamiliePT(val.pk)})
	# print('sys_presettags.objects.filter', time.time() - start_time, 'Sekunden')
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
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1]):
				aGen -= 1
				pClose += 1
				del afam[-1]
		except:
			pass
		# print(''.rjust(aGen,'-')+'|'+str(value.id_Tag.Tag)+' ('+str(value.id_Tag.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag': value, 'aGen': aGen, 'pClose': pClose, 'pChilds': value.id_Tag.id_ParentTag.all().count()})
		afam.append(value.id_Tag_id)
		aGen += 1
	return oTags


def getTagFamiliePT(presetId):
	"""Ermittelt Tag Familie für PresetTags."""
	# Tags = [tzpval.id_Tag for tzpval in sys_tagszupresettags.objects.select_related('id_Tag').filter(id_PresetTags_id=presetId)]
	aElement = list(sys_tagszupresettags.objects.raw('''
		SELECT "KorpusDB_sys_tagszupresettags".*, "KorpusDB_tbl_tags".*,
			(
				SELECT COUNT(*)
				FROM "KorpusDB_tbl_tagfamilie"
				WHERE "KorpusDB_tbl_tagfamilie"."id_ParentTag_id" = "KorpusDB_tbl_tags"."id"
			) AS parent_tag_count,
			(
				SELECT array_to_json(array(
					SELECT "KorpusDB_tbl_tagfamilie"."id_ParentTag_id"
					FROM "KorpusDB_tbl_tagfamilie"
					WHERE "KorpusDB_tbl_tagfamilie"."id_ChildTag_id" = "KorpusDB_tbl_tags"."id"
				))
			) AS child_tags__parent_tag_ids
		FROM "KorpusDB_sys_tagszupresettags"
		INNER JOIN "KorpusDB_tbl_tags" ON ( "KorpusDB_sys_tagszupresettags"."id_Tag_id" = "KorpusDB_tbl_tags"."id" )
		WHERE "KorpusDB_sys_tagszupresettags"."id_PresetTags_id" = %s
		ORDER BY "KorpusDB_sys_tagszupresettags"."Reihung" ASC
	''', [presetId]))
	prefetch_related_objects(aElement, ['id_Tag'])
	Tags = [{'model': tzpval.id_Tag, 'parent_tag_count': tzpval.parent_tag_count, 'child_tags__parent_tag_ids': tzpval.child_tags__parent_tag_ids} for tzpval in aElement]
	afam = []
	aGen = 0
	oTags = []
	for Tag in Tags:
		pClose = 0
		try:
			while len(afam) > 0 and not afam[-1] in Tag['child_tags__parent_tag_ids']:
				aGen -= 1
				pClose += 1
				del afam[-1]
		except:
			pass
		# print(''.rjust(aGen,'-')+'|'+str(Tag['model'].Tag)+' ('+str(Tag['model'].pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag': Tag['model'], 'aGen': aGen, 'pClose': pClose, 'pChilds': Tag['parent_tag_count']})
		afam.append(Tag['model'].pk)
		aGen += 1
	return oTags


def getTagList(Tags, TagPK, deep=[]):
	"""Gibt Tag Liste zurück."""
	TagData = []
	if len(deep) < 50:
		if TagPK is None:
			for value in Tags.objects.prefetch_related('tbl_tagebenezutag_set').filter(id_ChildTag=None):
				child = getTagList(Tags, value.pk, deep + [str(value) + ' (' + str(value.pk) + ')'])
				TagData.append({'model': value, 'child': child})
		else:
			for value in Tags.objects.prefetch_related('tbl_tagebenezutag_set').filter(id_ChildTag__id_ParentTag=TagPK):
				child = getTagList(Tags, value.pk, deep + [str(value) + ' (' + str(value.pk) + ')'])
				TagData.append({'model': value, 'child': child})
	else:
		print('"getTagList" zu Tief!', str(TagPK), str(Tags))
		raise Exception('"getTagList" zu Tief! ' + str(TagPK) + ' ' + str(deep))
	return TagData
