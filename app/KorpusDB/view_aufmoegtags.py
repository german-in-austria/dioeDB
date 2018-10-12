"""Für EingabeFB."""
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import KorpusDB.models as KorpusDB
from .function_menue import getMenue
from .function_tags import saveAMTags, getAMTags, getTagsData


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
		# Speichern
		if 'save' in request.POST:
			if request.POST.get('save') == 'AufgabenmoeglichkeitenTags':
				for aAufgabenmoeglichkeit in json.loads(request.POST.get('aufgabenmoeglichkeiten')):
					test += saveAMTags(request, aAufgabenmoeglichkeit['tags'], aAufgabenmoeglichkeit['id_Antwortmoeglichkeit'])
		# Formulardaten ermitteln
		Aufgabe = KorpusDB.tbl_aufgaben.objects.get(pk=apk)
		aAntwortmoeglichkeiten = []
		for aAntwortmoeglichkeit in Aufgabe.tbl_antwortmoeglichkeiten_set.all():
			aAntwortmoeglichkeiten.append({'model': aAntwortmoeglichkeit, 'xtags': getAMTags(aAntwortmoeglichkeit.pk)})
		# Tags
		tagData = getTagsData(apk)
		return render_to_response(
			aFormular,
			RequestContext(request, {'Aufgabe': Aufgabe, 'aAntwortmoeglichkeiten': aAntwortmoeglichkeiten, 'TagEbenen': tagData['TagEbenen'], 'TagsList': tagData['TagsList'], 'PresetTags': tagData['aPresetTags'], 'aDUrl': aDUrl, 'test': test, 'error': error}),)
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
