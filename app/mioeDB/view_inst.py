"""Formular für Vokszählungen."""
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from DB.funktionenDB import httpOutput
import mioeDB.models as mioeDB
import json


def view_inst(request):
	"""Anzeige für mioe Volkszählungs Maske."""
	aUrl = '/mioedb/inst/'
	aDUrl = 'mioeDB:varietaet'
	test = ''
	error = ''
	if 'getmask' in request.POST:
		aStatus = 'success'
		aInstId = int(request.POST.get('aInstId'))
		instDaten = []
		aArtenInInst = []
		aInst = False
		if aInstId > 0:
			aInst = mioeDB.tbl_institutionen.objects.get(pk=aInstId)
		if aInstId > 0:
			if 'save' in request.POST:
				for aDataSet in json.loads(request.POST.get('sInstData')):
					aDataSet['datenPk'] = int(aDataSet['datenPk'].strip()) if len(aDataSet['datenPk'].strip()) >= 0 else 0
					aDataSet['artId'] = int(aDataSet['artId'].strip()) if len(aDataSet['artId'].strip()) > 0 else None
					aDataSet['artAnzahl'] = int(aDataSet['artAnzahl'].strip()) if len(aDataSet['artAnzahl'].strip()) > 0 else None
					aDataSet['artKommentar'] = aDataSet['artKommentar'].strip()
					if not aDataSet['artId']:
						aStatus = 'error'
						error = '"artId" nicht vorhanden!'
					else:
						if mioeDB.tbl_institut_daten.objects.filter(id_institution_id=aInstId, id_art_id=aDataSet['artId']).count() != (1 if aDataSet['datenPk'] and aDataSet['datenPk'] > 0 else 0):
							aStatus = 'error'
							error = '"vz_daten" Anzahl stimmt nicht!'
						else:
							if aDataSet['datenPk'] and aDataSet['datenPk'] > 0:
								aInstDatenModel = mioeDB.tbl_institut_daten.objects.get(pk=aDataSet['datenPk'], id_institution_id=aInstId, id_art_id=aDataSet['artId'])
							else:
								aInstDatenModel = mioeDB.tbl_institut_daten()
							aInstDatenModel.id_institution_id = aInstId
							aInstDatenModel.id_art_id = aDataSet['artId']
							aInstDatenModel.kommentar = aDataSet['artKommentar']
							aInstDatenModel.anzahl = aDataSet['artAnzahl']
							aInstDatenModel.save()
							test = 'Gespeichert ...'
			for aArtInINST in mioeDB.tbl_art_in_institution.objects.filter(id_institution_id=aInstId):
				aArtInInstMitDaten = {'model': aArtInINST, 'daten': {'models': mioeDB.tbl_institut_daten.objects.filter(id_institution_id=aInstId, id_art_id=aArtInINST.id_art.pk)}}
				aArtenInInst.append(aArtInInstMitDaten)
		return httpOutput(json.dumps({
			'status': aStatus,
			'error': error,
			'html': loader.render_to_string(
				'mioedbinstmaske/inst_daten_formular.html',
				RequestContext(request, {'aInst': aInst, 'aArtenInInst': aArtenInInst, 'instDaten': instDaten, 'test': test}),)}))
	# Ausgabe der Seite
	return render_to_response(
		'mioedbinstmaske/start.html',
		RequestContext(request, {'aUrl': aUrl, 'aDUrl': aDUrl, 'test': test}),)
