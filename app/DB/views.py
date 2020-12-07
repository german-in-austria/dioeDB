from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from DB.funktionenDB import httpOutput
import json

# Verwaltung - Startseite - Übersicht über alle verfügbaren Tabellen
def start(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_start
	return view_start(request)

# Verwaltung - Ansicht - Übersicht über Tabelleneinträge mit Option zum bearbeiten
def view(request,app_name,tabelle_name):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_view
	return view_view(request,app_name,tabelle_name)

# Verwaltung - Reset id_seq für PostgreSQL
def resetidseq(request,app_name,tabelle_name):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_resetidseq
	return view_resetidseq(request,app_name,tabelle_name)

# UML-Klassendiagramm
def diagramm(request):
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_diagramm import view_diagramm
	return view_diagramm(request)

# Suche (OSM)
def search(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_search import view_search
	return view_search(request)

# Dateien
def dateien(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('DB.dateien'):
		return redirect('Startseite:start')
	from .funktionenDateien import view_dateien
	return view_dateien(request)


@csrf_exempt
def tagsystemvue(request):
	import KorpusDB.models as dbmodels
	output = {}
	if 'getBase' in request.POST:
		tagebenen = []
		for TagEbene in dbmodels.tbl_tagebene.objects.all():
			tagebenen.append({'pk': TagEbene.pk, 't': TagEbene.Name})
		output['tagebenen'] = tagebenen
		phaenomene = {}
		for phaenomen in dbmodels.tbl_phaenomene.objects.all():
			phaenomene[phaenomen.pk] = {
				'b': phaenomen.Bez_Phaenomen,
				'bs': phaenomen.Beschr_Phaenomen,
				'zpb': phaenomen.zu_PhaenBer_id,
				'k': phaenomen.Kommentar
			}
		output['phaenomene'] = phaenomene
	if 'getTags' in request.POST:
		tags = {}
		tagsReihung = []
		for tag in dbmodels.tbl_tags.objects.prefetch_related('tbl_tagebenezutag_set', 'id_ParentTag', 'id_ChildTag').all():
			tagsReihung.append(tag.pk)
			tags[tag.pk] = {
				't': tag.Tag,
				'tl': tag.Tag_lang,
				'k': tag.Kommentar,
				'r': tag.AReihung,
				'g': tag.Generation,
			}
			if tag.zu_Phaenomen:
				tags[tag.pk]['zppk'] = tag.zu_Phaenomen_id
			try:
				tmpTezt = []
				for tezt in tag.tbl_tagebenezutag_set.all():
					tmpTezt.append(tezt.id_TagEbene_id)
				if tmpTezt:
					tags[tag.pk]['tezt'] = tmpTezt
			except:
				pass
			try:
				tmpChilds = []
				for aCTags in tag.id_ParentTag.all().order_by('id_ParentTag__AReihung'):
					tmpChilds.append(aCTags.id_ChildTag_id)
				if tmpChilds:
					tags[tag.pk]['c'] = tmpChilds
			except:
				pass
			try:
				tmpParents = []
				for aCTags in tag.id_ChildTag.all().order_by('id_ChildTag__AReihung'):
					tmpParents.append(aCTags.id_ParentTag_id)
				if tmpParents:
					tags[tag.pk]['p'] = tmpParents
			except:
				pass
		output['tags'] = {'tags': tags, 'tagsReihung': tagsReihung}
	if 'getPresets' in request.POST:
		aPresetTags = []
		for val in dbmodels.sys_presettags.objects.all():
			tfVal = getTagFamiliePT([x.id_Tag for x in val.sys_tagszupresettags_set.all()])
			if tfVal:
				aPresetTags.append({'tf': tfVal, 'b': val.Bezeichnung})
		output['presets'] = aPresetTags
	return httpOutput(json.dumps(output), mimetype='application/json')


def getTagFamiliePT(Tags):
	afam = []
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				pClose += 1
				del afam[-1]
		except:
			pass
		oTags.append({'t': value.pk, 'c': pClose})
		afam.append(value)
	return oTags
