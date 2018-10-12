"""Für EingabeFB."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
import datetime
import json
import KorpusDB.models as KorpusDB
import PersonenDB.models as PersonenDB
from .function_menue import getMenue
from .function_tags import saveTags, getTags, getTagsData


def view_aufmoegtags(request, ipk=0, apk=0):
	"""Ansicht für EingabeSTP."""
	aFormular = 'korpusdbaufmoegtags/start_formular.html'
	aUrl = '/korpusdb/aufmoegtags/'
	aDUrl = 'KorpusDB:aufmoegtags'
	useArtErhebung = [6, 7]
	useOnlyErhebung = []
	for aUKDBES in request.user.user_korpusdb_erhebung_set.all():
		useOnlyErhebung.append(aUKDBES.erhebung_id)
	test = ''
	error = ''
	apk = int(apk)
	if apk > 0:
		# # Speichern
		# if 'save' in request.POST:
		# 	pass
		# Formulardaten ermitteln
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		# Tags
		tagData = getTagsData(apk)
		print(tagData)
		return render_to_response(
			aFormular,
			RequestContext(request, {'Aufgabe': Aufgabe, 'TagEbenen': tagData['TagEbenen'], 'TagsList': tagData['TagsList'], 'PresetTags': tagData['aPresetTags'], 'aDUrl': aDUrl, 'test': test, 'error': error}),)
	# Menü
	aMenue = getMenue(request, useOnlyErhebung, useArtErhebung, ['tbl_erhebung_mit_aufgaben__Reihung'], [4])
	if aMenue['formular']:
		return render_to_response(
			aMenue['formular'],
			RequestContext(request, {'menueData': aMenue['daten'], 'aDUrl': aDUrl}),)

	# Ausgabe der Seite
	return render_to_response(
		'korpusdbaufmoegtags/start.html',
		RequestContext(request, {'menueData': aMenue['daten'], 'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)

# Funktionen:
