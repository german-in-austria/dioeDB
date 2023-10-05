"""Ansichten der AnnotationsDB."""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template import loader
from DB.funktionenDB import formularView
import AnnotationsDB.models as AnnotationsDB
import KorpusDB.models as KorpusDB
import re

def auswertung(request, aErhebung, aTagEbene, aSeite):
	"""Auswertung anzeigen."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_auswertung import views_auswertung
	return views_auswertung(request, aErhebung, aTagEbene, aSeite)


def annotool(request, ipk=0, tpk=0):
	"""Annotations Tool Daten."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annotool import views_annotool
	return views_annotool(request, ipk, tpk)


def tool(request):
	"""Annotations Tool Template."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	return render_to_response('AnnotationsDB/toolstart.html', RequestContext(request))


def annosent(request):
	"""AnnoSent."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annosent import views_annosent
	return views_annosent(request)


def annocheck(request):
	"""AnnoCheck."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	from .views_annocheck import views_annocheck
	return views_annocheck(request)


def eventtier(request):
	"""Event Tier."""
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	if not request.user.has_perm('AnnotationsDB.transcript_maskView'):
		return redirect('Startseite:start')
	info = ''
	error = ''
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_informanten'
	permName = 'informanten'
	primaerId = 'informant'
	aktueberschrift = 'Informanten/Event Tier'
	asurl = '/annotationsdb/eventtier/'

	def tagImportFxFunction(aval, siblings, aElement):
		"""Html Ausgabe stxsm Datei."""
		import os
		from django.conf import settings
		errText = []
		warningText = []
		aTest = ''
		tagCache = {}
		eventTierCount = AnnotationsDB.tbl_event_tier.objects.filter(ID_Inf_id=aElement.id).count()
		eventTierImportedCount = 0
		eventTierImportCound = 0
		eventTierImportDoneCound = 0
		if eventTierCount < 1:
			errText.append('Keine Event Tier zu Informant mit ID "' + str(aElement.id) + '" vorhanden!')
		else:
			aAIdList = {}
			with open(os.path.join(getattr(settings, 'BASE_DIR', None), 'AnnotationsDB', 'fx', 'pp04_texttags_tagid_tagebene.csv'), 'r', encoding="utf-8") as file:
				dg = 0
				for aLine in file:
					if dg > 0:
						[tName, tId, tEId] = aLine.strip().split(';')
						aAIdList[tName] = [int(tId), int(tEId.split(',')[0])]
					dg += 1
			eventTierImportedCount = AnnotationsDB.tbl_event_tier.objects.filter(ID_Inf_id=aElement.id, imported=True).count()
			for aEventTier in AnnotationsDB.tbl_event_tier.objects.filter(ID_Inf_id=aElement.id):
				aTest += '<div style="margin-bottom:15px;padding-bottom:15px;border-bottom:1px solid #000">'
				aTest += '<b>' + str(aEventTier.id) + '</b> - ' + str(aEventTier.tier_id) + '<br>'
				aTest += str(aEventTier.text) + '<br>'
				stichworte = ['diskursmarker', 'phraseologisch', 'phraseologismus', 'diekursmarker', 'diskrusmarker']
				stichworte_re = re.compile("|".join(stichworte))
				if aEventTier.text and stichworte_re.search(aEventTier.text.lower()):
					aTest += '<b style="color:#00a">Zeile wird wegen Stichwort nicht importier. (z.B. "Diskursmarker")</b><br>'
				else:
					if aEventTier.text and len(aEventTier.text) > 3:
						aTagLines = []
						aTagLinesR = re.findall(r'\[([^\]]+)\]', aEventTier.text)
						if len(aTagLinesR) > 0:
							for aTagLineR in aTagLinesR:
								aTagsInLine = []
								aTagsInLineR = aTagLineR.split(',')
								for aTagInLineR in aTagsInLineR:
									aTagInLine = aTagInLineR.strip()
									if len(aTagInLine) > 0:
										aTagsInLine.append(aTagInLine)
								if len(aTagInLine) > 0:
									aTagLines.append(aTagsInLine)
							if len(aTagLines) > 0:
								aErrTxt = ''
								aTest += '<ul style="margin:5px 0;">'
								for aTagLine in aTagLines:
									aTest += '<li>'
									aTestTemp = []
									aTestTempE = []
									for aTag in aTagLine:
										if aTag in aAIdList:
											aTestTemp.append('<b style="color:#0a0;" title="' + str(aAIdList[aTag][0]) + '"><u>' + aTag + '</u></b>')
											aTestTempE.append(aAIdList[aTag][1])
										else:
											if aTag not in tagCache:
												tagCache[aTag] = KorpusDB.tbl_tags.objects.filter(Tag=aTag).count()
											aTagCount = tagCache[aTag]
											if aTagCount == 1:
												aTestTemp.append('<b style="color:#0a0;">' + aTag + '</b>')
											else:
												aTestTemp.append('<b style="color:#a00;">' + aTag + '</b> (' + str(aTagCount) + ')')
												if aEventTier.imported == 0:
													aErrTxt = '"' + aTag + '" wurde ' + str(aTagCount) + ' mal gefunden!'
													if aTagCount == 0:
														aErrTxt = '"' + aTag + '" wurde nicht gefunden!'
													if aErrTxt not in errText:
														errText.append(aErrTxt)
									aTest += str(aTestTemp)
									aTest += '<br>Ebenen: ' + str(aTestTempE)
									aTest += '</li>'
								aTest += '</ul>'
								if aEventTier.imported != 0:
									aTest += '<b style="color:#aa0;">Wurde bereits importiert</b>'
									eventTierImportDoneCound += 1
								else:
									if len(aErrTxt) > 0:
										aTest += '<b style="color:#a00">Wegen Fehler nicht importieren</b><br>'
									else:
										aTest += '<b style="color:#0a0">Importieren</b><br>'
										eventTierImportCound += 1
							else:
								aTest += '<b style="color:#a00">Keine Tags</b><br>'
						else:
							aTest += '<b style="color:#a00">Keine Tags</b><br>'
					else:
						aTest += '<b style="color:#a00">Keine Tags</b><br>'
				aTest += '</div>'
		aView_html = loader.render_to_string(
			'eventtier/tagimportfxfunction0.html',
			RequestContext(request, {'blub': 'blub', 'eventTierCount': eventTierCount, 'eventTierImportedCount': eventTierImportedCount, 'eventTierImportCound': eventTierImportCound + eventTierImportDoneCound, 'eventTierImportDoneCound': eventTierImportDoneCound, 'errText': errText, 'warningText': warningText, 'aTest': aTest}),)
		aval['feldoptionen'] = {
			'view_html': aView_html,
			'edit_html': '<div></div>'}
		return aval

	aufgabenform = [{
		'titel': 'Informant', 'app': 'PersonenDB', 'tabelle': 'tbl_informanten', 'id': 'informant', 'optionen': ['einzeln', 'noEditBtn'],
		'felder':['+id', 'inf_sigle', 'inf_gruppe', 'kommentar', '!tagImportFx'],
		'feldoptionen':{
			'tagImportFx': {'fxtype': {'fxfunction': tagImportFxFunction}, 'view_html': '<div></div>', 'edit_html': '<div></div>', 'nl': True}
		},
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
