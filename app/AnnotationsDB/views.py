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
		import datetime
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
								aNoImport = False
								aTestTemp2 = ''
								aTest += '<ul style="margin:5px 0;">'
								aTagIds = []
								for aTagLine in aTagLines:
									aTest += '<li>'
									aTestTemp = []
									aTestTempE = []
									aTestTempEId = 0
									for aTag in aTagLine:
										if aTag in aAIdList:
											aTestTemp.append('<b style="color:#0a0;" title="' + str(aAIdList[aTag][0]) + '"><u>' + aTag + '</u></b>')
											if len(aTestTempE) == 0:
												aTestTempEId = aAIdList[aTag][1]
												aTestTempE.append('<b style="color:#0a0;"><u>' + str(aAIdList[aTag][1]) + '</u></b>')
											else:
												aTestTempE.append(str(aAIdList[aTag][1]))
											aTagIds.append([aTestTempEId, aAIdList[aTag][0]])
										else:
											if aTag not in tagCache:
												tagCache[aTag] = KorpusDB.tbl_tags.objects.filter(Tag=aTag)
											aTagCount = tagCache[aTag].count()
											if aTagCount == 1:
												aTagId = list(tagCache[aTag])[0].pk
												aTestTemp.append('<b style="color:#0a0;" title="' + str(aTagId) + '">' + aTag + '</b>')
												aTagIds.append([0, aTagId])
											else:
												aTestTemp.append('<b style="color:#a00;">' + aTag + '</b> (' + str(aTagCount) + ')')
												if aEventTier.imported == 0:
													if aTagCount == 0:
														aTestTemp2 += '<b style="color:#00a">Nicht importieren da "' + aTag + '" nicht gefunden wurde!</b><br>'
														aNoImport = True
													else:
														aErrTxt = '"' + aTag + '" wurde ' + str(aTagCount) + ' mal gefunden!'
														if aErrTxt not in errText:
															errText.append(aErrTxt)
									aTest += str(aTestTemp)
									aTest += '<br>Ebenen: ' + str(aTestTempE)
									aTest += '</li>'
								aTest += '</ul>'
								aTest += aTestTemp2
								if aEventTier.imported != 0:
									aTest += '<b style="color:#aa0;">Wurde bereits importiert</b>'
									eventTierImportDoneCound += 1
								else:
									if len(aErrTxt) > 0:
										aTest += '<b style="color:#a00">Wegen Fehler nicht importieren</b><br>'
									elif not aNoImport:
										eventTierImportCound += 1
										if 'stxsmfxfunction' in request.POST and int(request.POST.get('stxsmfxfunction')) == 1:
											# ToDo: Importieren
											newTokenSetTokens = list(AnnotationsDB.token.objects.filter(ID_Inf_id=aElement.id, event_id=aEventTier.event_id_id))
											if len(newTokenSetTokens) < 1:
												aErrTxt = 'Event mit der id: "' + str(aEventTier.event_id_id) + '" hat keine Tokens!'
												if aErrTxt not in errText:
													errText.append(aErrTxt)
												aTest += '<b style="color:#a00;">' + aErrTxt + '</b><br>'
											else:
												newTokenSet = AnnotationsDB.tbl_tokenset()
												# print('Importieren ...', newTokenSet, newTokenSetTokens[0], newTokenSetTokens[-1])
												newTokenSet.id_von_token = newTokenSetTokens[0]
												newTokenSet.id_bis_token = newTokenSetTokens[-1]
												newTokenSet.save()
												newAntwort = KorpusDB.tbl_antworten()
												newAntwort.von_Inf = aElement
												newAntwort.ist_tokenset = newTokenSet
												newAntwort.start_Antwort = datetime.timedelta(microseconds=0)
												newAntwort.stop_Antwort = datetime.timedelta(microseconds=0)
												newAntwort.save()
												dg = 0
												for aTagId in aTagIds:
													newTag = KorpusDB.tbl_antwortentags()
													newTag.id_Antwort = newAntwort
													newTag.id_Tag_id = aTagId[1]
													if aTagId[0] > 0:
														newTag.id_TagEbene_id = aTagId[0]
													newTag.Reihung = dg
													newTag.save()
													dg += 1
												aEventTier.imported = True
												aEventTier.save()
												eventTierImportDoneCound += 1
												eventTierImportCound -= 1
												aTest += '<b style="color:#0a0"><u>Importiert</u></b><br>'
										else:
											aTest += '<b style="color:#0a0">Importieren</b><br>'
							else:
								aTest += '<b style="color:#00a">Keine Tags</b> (1)<br>'
						else:
							aTest += '<b style="color:#00a">Keine Tags</b> (2)<br>'
					else:
						aTest += '<b style="color:#00a">Keine Tags</b> (3)<br>'
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
		'addJS': [{'static': 'korpusdbfx/js/fxaudioplayer.js'}, {'static': 'korpusdbfx/js/fxerhinfaufgabe.js'}],
	}]
	return formularView(app_name, tabelle_name, permName, primaerId, aktueberschrift, asurl, aufgabenform, request, info, error)
