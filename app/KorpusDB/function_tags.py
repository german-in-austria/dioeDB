"""Tags."""
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
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
