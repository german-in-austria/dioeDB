"""MioeDB Auswertung."""
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db import connection
from .models import tbl_mioe_orte, tbl_art_daten


def views_mioeAuswertung(request):
	"""Anzeige für MioeDB Auswertung."""
	print(request.POST)
	sHatErgebniss = int(request.POST.get('hatergebniss')) if 'hatergebniss' in request.POST else 1  # 1 = Nur mit Ergebniss, 2 = Nur ohne Ergebniss
	aHatErgebnisse = [
		{'v': 1, 'txt': 'Nur mit Ergebniss'},
		{'v': 2, 'txt': 'Nur ohne Ergebniss'}
	]
	sJahr = request.POST.get('jahr') if 'jahr' in request.POST else '0'
	aJahre = []
	with connection.cursor() as c:
		c.execute(query_jahre())
		aJahre = [str(int(x[0])) for x in c.fetchall()]
	sArt = request.POST.get('art') if 'art' in request.POST else '0'
	aArten = []
	if sJahr != '0':
		with connection.cursor() as c:
			c.execute(query_arten_fuer_jahr(sJahr))
			aArten = []
			aOk = False
			for x in c.fetchall():
				if str(x[0]) == sArt:
					aOk = True
				aArten.append({'id': str(x[0]), 'txt': x[1]})
			if not aOk:
				sArt = '0'
	else:
		sArt = '0'
	verfuegbareJahreArten = []
	with connection.cursor() as c:
		c.execute(query_verfuegbareJahreArten(sJahr, sArt))
		for x in c.fetchall():
			if x:
				verfuegbareJahreArten.append({'id': str(int(x[0])) + '_' + str(x[1]), 'txt': str(int(x[0])) + '_' + x[2]})
	# test = query_mioe_ort(False, start, maxPerPage, sHatErgebniss, sJahr, sArt)
	aCount = 0
	with connection.cursor() as c:
		c.execute(query_mioe_ort(True, 0, 0, sHatErgebniss, sJahr, sArt))
		aCount = c.fetchone()[0]
	aSeite = int(request.POST.get('seite')) if 'seite' in request.POST else 0
	start = 0
	maxPerPage = 15
	prev = -1
	next = -1
	if aSeite > 0:
		prev = aSeite - 1
		start = aSeite * maxPerPage
	if aCount > (aSeite + 1) * maxPerPage:
		next = aSeite + 1
	if 'xls' in request.POST:
		start = 0
		maxPerPage = 0
	aAuswertungen = []
	with connection.cursor() as c:
		c.execute(query_mioe_ort(False, start, maxPerPage, sHatErgebniss, sJahr, sArt))
		dg = start + 1
		for x in c.fetchall():
			aAuswertung = {
				'nr': dg,
				'id': x[0],
				'id_ort': x[1],
				'ort_name': x[2],
				'histor_ort': x[3],
				'ortlat': x[4],
				'ortlon': x[5],
				'data': x[6],
				'xdata': {}
			}
			for aData in aAuswertung['data']:
				aAuswertung['xdata'][str(aData[0]['jahr']) + '_' + str(aData[0]['id_art_id'])] = aData[0]['sum_anzahl']
			aAuswertungen.append(aAuswertung)
			dg += 1
	if 'xls' in request.POST:
		pass
	return render_to_response(
		'mioedbvzmaske/mioeauswertungstart.html',
		RequestContext(request, {
			'prev': prev, 'next': next, 'aSeite': aSeite,
			'sHatErgebniss': sHatErgebniss, 'aHatErgebnisse': aHatErgebnisse,
			'sJahr': sJahr, 'aJahre': aJahre,
			'sArt': sArt, 'aArten': aArten,
			'aMax': tbl_mioe_orte.objects.all().count(),
			'aCount': aCount,
			'verfuegbareJahreArten': verfuegbareJahreArten,
			'aAuswertungen': aAuswertungen
		}))


def query_mioe_ort(count, start, max, sHatErgebniss, sJahr, sArt):
	"""Querystring für MiÖ Orte erstellen."""
	aQuery = "SELECT\n"
	if count:
		aQuery += "	COUNT(m_orte.id)\n"
	else:
		aQuery += """	m_orte.id as id,
	m_orte.id_orte_id as id_orte,
	(CASE WHEN length(ort.ort_namekurz) > 0 THEN ort.ort_namekurz ELSE ort.ort_namelang END) as ort_name,
	m_orte.histor_ort as histor_ort,
	ort.lat as ortLat,
	ort.lon as ortLon,
	(
		SELECT ARRAY_AGG(json_build_array(zahlen.*))
		FROM (
			SELECT
				EXTRACT(YEAR FROM vz.erheb_datum) as jahr,
				vzData.id_art_id,
				SUM(vzData.anzahl) as sum_anzahl
			FROM "MioeDB_tbl_vz_daten" as vzData
			INNER JOIN "MioeDB_tbl_volkszaehlung" vz ON ( vzData.id_vz_id = vz.id )
			WHERE
				vzData.id_mioe_ort_id = m_orte.id\n"""
		if sJahr != '0':
			aQuery += "				AND EXTRACT(YEAR FROM vz.erheb_datum) = " + str(int(sJahr)) + "\n"
		if sArt != '0':
			aQuery += "				AND vzData.id_art_id = " + str(int(sArt)) + "\n"
		aQuery += """			GROUP BY jahr, vzData.id_art_id
			ORDER BY jahr ASC, vzData.id_art_id ASC
		) as zahlen
	)\n"""
	aQuery += "FROM \"MioeDB_tbl_mioe_orte\" as m_orte\n"
	if not count:
		aQuery += "LEFT JOIN \"OrteDB_tbl_orte\" ort ON m_orte.id_orte_id = ort.id\n"
	aQuery += "WHERE\n"
	aQuery += """	(
		SELECT COUNT(vz_data.id)
		FROM \"MioeDB_tbl_vz_daten\" vz_data
		INNER JOIN \"MioeDB_tbl_volkszaehlung\" vz ON ( vz_data.id_vz_id = vz.id )
		WHERE
			vz_data.id_mioe_ort_id = m_orte.id\n"""
	if sJahr != '0':
		aQuery += "			AND EXTRACT(YEAR FROM vz.erheb_datum) = " + str(int(sJahr)) + "\n"
	if sArt != '0':
		aQuery += "			AND vz_data.id_art_id = " + str(int(sArt)) + "\n"
	aQuery += "	) " + (">" if sHatErgebniss == 1 else "=") + " 0\n"
	if not count:
		aQuery += "ORDER BY ort_name ASC\n"
		if start > 0:
			aQuery += "OFFSET " + str(int(start)) + "\n"
		if max > 0:
			aQuery += "LIMIT " + str(int(max)) + "\n"
	return aQuery


def query_jahre():
	"""Querystring für Jahre."""
	return '''SELECT EXTRACT(YEAR FROM erheb_datum) AS "year"
FROM "MioeDB_tbl_volkszaehlung"
GROUP BY EXTRACT(YEAR FROM erheb_datum)
ORDER BY "year" ASC'''


def query_arten_fuer_jahr(sJahr):
	"""Querystring für Arten für ausgewähltes Jahr."""
	return '''SELECT arten.id_art_id, arten.art_name
	FROM (
		SELECT DISTINCT
			"MioeDB_tbl_art_in_vz".id,
			"MioeDB_tbl_art_in_vz".id_art_id,
			"MioeDB_tbl_art_daten".art_name,
			"MioeDB_tbl_art_in_vz".reihung
		FROM "MioeDB_tbl_art_in_vz"
		INNER JOIN "MioeDB_tbl_volkszaehlung" ON ( "MioeDB_tbl_art_in_vz".id_vz_id = "MioeDB_tbl_volkszaehlung".id )
		INNER JOIN "MioeDB_tbl_art_daten" ON ( "MioeDB_tbl_art_in_vz".id_art_id = "MioeDB_tbl_art_daten".id )
		WHERE EXTRACT(YEAR FROM "MioeDB_tbl_volkszaehlung".erheb_datum) = ''' + str(int(sJahr)) + '''
		ORDER BY "MioeDB_tbl_art_in_vz".reihung ASC, "MioeDB_tbl_art_daten".art_name ASC
	) as arten
	GROUP BY arten.id_art_id, arten.art_name'''


def query_verfuegbareJahreArten(sJahr, sArt):
	"""Querystring für verfügbare Kombination aus Jahren und Arten."""
	aQuery = """WITH aJahrArt AS (
	SELECT DISTINCT
		\"MioeDB_tbl_art_in_vz\".id,
		\"MioeDB_tbl_art_in_vz\".id_art_id,
		\"MioeDB_tbl_art_daten\".art_name,
		\"MioeDB_tbl_art_in_vz\".reihung,
		EXTRACT(YEAR FROM \"MioeDB_tbl_volkszaehlung\".erheb_datum) as jahr,
		ROW_NUMBER() OVER (
			PARTITION BY
				\"MioeDB_tbl_art_in_vz\".id_art_id,
				EXTRACT(YEAR FROM \"MioeDB_tbl_volkszaehlung\".erheb_datum)
			ORDER BY
				EXTRACT(YEAR FROM \"MioeDB_tbl_volkszaehlung\".erheb_datum) ASC,
				\"MioeDB_tbl_art_in_vz\".reihung ASC,
				\"MioeDB_tbl_art_daten\".art_name ASC
		) as rk
	FROM \"MioeDB_tbl_art_in_vz\"
	INNER JOIN \"MioeDB_tbl_volkszaehlung\" ON (\"MioeDB_tbl_art_in_vz\".id_vz_id = \"MioeDB_tbl_volkszaehlung\".id)
	INNER JOIN \"MioeDB_tbl_art_daten\" ON (\"MioeDB_tbl_art_in_vz\".id_art_id = \"MioeDB_tbl_art_daten\".id)\n"""
	if sJahr != '0':
		aQuery += "		WHERE EXTRACT(YEAR FROM \"MioeDB_tbl_volkszaehlung\".erheb_datum) = " + str(int(sJahr)) + "\n"
		if sArt != '0':
			aQuery += "				AND \"MioeDB_tbl_art_in_vz\".id_art_id = " + str(int(sArt)) + "\n"
	aQuery += """ORDER BY jahr ASC, "MioeDB_tbl_art_in_vz"."reihung" ASC, "MioeDB_tbl_art_daten"."art_name" ASC
	), xJahrArt AS (
	SELECT
		jahrArt.jahr,
		jahrArt.id_art_id,
		jahrArt.art_name,
		jahrArt.reihung
	FROM aJahrArt jahrArt
	WHERE jahrArt.rk = 1
	)
	SELECT
	jahrArt.jahr,
	jahrArt.id_art_id,
	jahrArt.art_name
	FROM xJahrArt jahrArt"""
	return aQuery
