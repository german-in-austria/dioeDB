from django.apps import apps
from DB.funktionenDB import httpOutput
import json


def view_search(request):
	"""Suche (OSM)."""
	# Nach OpenStreetMap Orten in der tbl_orte suchen ...
	if 'sucheorte' in request.POST:
		suchorte = json.loads(request.POST.get('suchorte'))
		ortModel = apps.get_model('PersonenDB', 'tbl_orte')
		for suchort in suchorte:
			# print(suchort['osm_id'], suchort['osm_type'])
			try:
				ortObjekt = ortModel.objects.filter(osm_id=suchort['osm_id'], osm_type=suchort['osm_type']).order_by('pk').first()
				suchort['ort_pk'] = ortObjekt.pk
			except:
				pass
		return httpOutput('OK' + json.dumps(suchorte))

	# Nach Ort in der tbl_orte suchen und als Json ausgeben
	if 'getort' in request.POST:
		ortData = {}
		ortModel = apps.get_model('PersonenDB', 'tbl_orte')
		try:
			ortObjekt = ortModel.objects.get(pk=request.POST.get('getort'))
			ortData['pk'] = ortObjekt.pk
			ortData['ort_namelang'] = ortObjekt.ort_namelang
			ortData['lat'] = ortObjekt.lat
			ortData['lon'] = ortObjekt.lon
			ortData['osm_id'] = ortObjekt.osm_id
			ortData['osm_type'] = ortObjekt.osm_type
		except:
			pass
		return httpOutput('OK' + json.dumps(ortData))

	return httpOutput('Error: Keine kompatible Suche!')
