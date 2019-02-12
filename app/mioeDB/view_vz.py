"""Formular für Vokszählungen."""
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from DB.funktionenDB import httpOutput
import mioeDB.models as mioeDB
import json


def view_vz(request):
	"""Anzeige für mioe Volkszählungs Maske."""
	aUrl = '/mioedb/vz/'
	aDUrl = 'mioeDB:varietaet'
	test = ''
	error = ''
	if 'getmask' in request.POST:
		aStatus = 'success'
		aMioeOrtId = int(request.POST.get('aMioeOrtId'))
		aVzId = int(request.POST.get('aVzId'))
		vzDaten = []
		aArtenInVZ = []
		aVz = False
		aMioeOrt = False
		if aVzId > 0:
			aVz = mioeDB.tbl_volkszaehlung.objects.get(pk=aVzId)
		if aMioeOrtId > 0:
			aMioeOrt = mioeDB.tbl_mioe_orte.objects.get(pk=aMioeOrtId)
		if aVzId > 0 and aMioeOrtId > 0:
			if 'save' in request.POST:
				for aDataSet in json.loads(request.POST.get('sVzData')):
					aDataSet['datenPk'] = int(aDataSet['datenPk'].strip()) if len(aDataSet['datenPk'].strip()) >= 0 else 0
					aDataSet['artId'] = int(aDataSet['artId'].strip()) if len(aDataSet['artId'].strip()) > 0 else None
					aDataSet['artAnzahl'] = int(aDataSet['artAnzahl'].strip()) if len(aDataSet['artAnzahl'].strip()) > 0 else None
					aDataSet['artAbwBez'] = aDataSet['artAbwBez'].strip()
					if not aDataSet['artId']:
						aStatus = 'error'
						error = '"artId" nicht vorhanden!'
					else:
						if mioeDB.tbl_vz_daten.objects.filter(id_vz_id=aVzId, id_art_id=aDataSet['artId'], id_mioe_ort_id=aMioeOrtId).count() != (1 if aDataSet['datenPk'] and aDataSet['datenPk'] > 0 else 0):
							aStatus = 'error'
							error = '"vz_daten" Anzahl stimmt nicht!'
						else:
							if aDataSet['datenPk'] and aDataSet['datenPk'] > 0:
								aVzDatenModel = mioeDB.tbl_vz_daten.objects.get(pk=aDataSet['datenPk'], id_vz_id=aVzId, id_art_id=aDataSet['artId'], id_mioe_ort_id=aMioeOrtId)
							else:
								aVzDatenModel = mioeDB.tbl_vz_daten()
							aVzDatenModel.id_vz_id = aVzId
							aVzDatenModel.id_mioe_ort_id = aMioeOrtId
							aVzDatenModel.id_art_id = aDataSet['artId']
							aVzDatenModel.abw_bez = aDataSet['artAbwBez']
							aVzDatenModel.anzahl = aDataSet['artAnzahl']
							aVzDatenModel.save()
							test = 'Gespeichert ...'
			for aArtInVZ in mioeDB.tbl_art_in_vz.objects.filter(id_vz_id=aVzId):
				aArtInVzMitDaten = {'model': aArtInVZ, 'daten': {'models': mioeDB.tbl_vz_daten.objects.filter(id_vz_id=aVzId, id_art_id=aArtInVZ.id_art.pk, id_mioe_ort_id=aMioeOrtId)}}
				aArtenInVZ.append(aArtInVzMitDaten)
		return httpOutput(json.dumps({
			'status': aStatus,
			'error': error,
			'html': loader.render_to_string(
				'mioedbvzmaske/vz_daten_formular.html',
				RequestContext(request, {'aVz': aVz, 'aMioeOrt': aMioeOrt, 'aArtenInVZ': aArtenInVZ, 'vzDaten': vzDaten, 'test': test}),)}))
	# Ausgabe der Seite
	return render_to_response(
		'mioedbvzmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
