"""MioeDB Auswertung."""
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db import connection
from .models import tbl_mioe_orte, tbl_art_daten


def views_mioeAuswertung(request):
	"""Anzeige für MioeDB Auswertung."""
	print(request.POST)
	hideFilteredData = True if 'hidefiltereddata' in request.POST else False
	sHatErgebniss = int(request.POST.get('hatergebniss')) if 'hatergebniss' in request.POST else 1  # 1 = Nur mit Ergebniss, 2 = Nur ohne Ergebniss
	aHatErgebnisse = [
		{'v': 1, 'txt': 'Nur mit Ergebniss'},
		{'v': 2, 'txt': 'Nur ohne Ergebniss'}
	]
	sAdmLvl = request.POST.get('admlvl') if 'admlvl' in request.POST else '0'
	aAdmLvl = []
	with connection.cursor() as c:
		c.execute(query_admlvl())
		aAdmLvl = [{'id': str(x[0]), 'txt': x[1]} for x in c.fetchall()]
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
		c.execute(query_verfuegbareJahreArten(sJahr, sArt, hideFilteredData))
		for x in c.fetchall():
			if x:
				verfuegbareJahreArten.append({'id': str(int(x[0])) + '_' + str(x[1]), 'txt': str(int(x[0])) + '_' + x[2]})
	# test = query_mioe_ort(False, start, maxPerPage, sHatErgebniss, sJahr, sArt, sAdmLvl, hideFilteredData)
	aCount = 0
	with connection.cursor() as c:
		c.execute(query_mioe_ort(True, 0, 0, sHatErgebniss, sJahr, sArt, sAdmLvl, hideFilteredData))
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
		c.execute(query_mioe_ort(False, start, maxPerPage, sHatErgebniss, sJahr, sArt, sAdmLvl, hideFilteredData))
		dg = start + 1
		for x in c.fetchall():
			aAuswertung = {
				'nr': dg,
				'id': x[0],
				'id_ort': x[1],
				'ort_name': x[2],
				'adm_lvl': x[3],
				'histor_ort': x[4],
				'ortlat': x[5],
				'ortlon': x[6],
				'data': x[7],
				'xdata': {},
				'gericht_jahr': x[8],
				'xgericht_jahr': {}
			}
			if aAuswertung['data']:
				for aData in aAuswertung['data']:
					aAuswertung['xdata'][str(aData[0]['jahr']) + '_' + str(aData[0]['id_art_id'])] = aData[0]['sum_anzahl']
			if aAuswertung['gericht_jahr']:
				for aGJ in aAuswertung['gericht_jahr']:
					aAuswertung['xgericht_jahr'][str(aGJ['jahr'])] = aGJ['ort'] + ' (' + str(aGJ['moid']) + ')'
			aAuswertungen.append(aAuswertung)
			dg += 1
	if 'xls' in request.POST:
		import xlwt
		response = HttpResponse(content_type='text/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="mioeDB.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('mioeDB')
		row_num = 0
		columns = [
			('#', 2000),
			('id', 2000),
			('id_ort', 2000),
			('ort_name', 2000),
			('adm_lvl', 2000),
			('histor_ort', 2000),
			('ortlat', 2000),
			('ortlon', 2000)
		]
		columns += [('gb_' + aja, 2000) for aja in aJahre]
		columns += [(avja['txt'], 2000) for avja in verfuegbareJahreArten]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
		font_style = xlwt.XFStyle()
		aAuswertungsDaten = []
		for auswertung in aAuswertungen:
			aAuswertungZeile = [
				auswertung['nr'],
				auswertung['id'],
				auswertung['id_ort'],
				auswertung['ort_name'],
				auswertung['adm_lvl'],
				auswertung['histor_ort'],
				auswertung['ortlat'],
				auswertung['ortlon'],
			]
			aAuswertungZeile += [(auswertung['xgericht_jahr'][aja] if aja in auswertung['xgericht_jahr'] else None) for aja in aJahre]
			aAuswertungZeile += [(auswertung['xdata'][avja['id']] if 'xdata' in auswertung and avja['id'] in auswertung['xdata'] else None) for avja in verfuegbareJahreArten]
			aAuswertungsDaten.append(aAuswertungZeile)
		for obj in aAuswertungsDaten:
			row_num += 1
			row = obj
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		wb.save(response)
		return response
	return render_to_response(
		'mioedbvzmaske/mioeauswertungstart.html',
		RequestContext(request, {
			'prev': prev, 'next': next, 'aSeite': aSeite, 'aSeiteP': (aSeite + 1), 'mSeiten': (int(aCount / maxPerPage) + 1),
			'sHatErgebniss': sHatErgebniss, 'aHatErgebnisse': aHatErgebnisse,
			'sAdmLvl': sAdmLvl, 'aAdmLvl': aAdmLvl,
			'sJahr': sJahr, 'aJahre': aJahre,
			'sArt': sArt, 'aArten': aArten,
			'hideFilteredData': hideFilteredData,
			'aMax': tbl_mioe_orte.objects.all().count(),
			'aCount': aCount,
			'verfuegbareJahreArten': verfuegbareJahreArten,
			'aAuswertungen': aAuswertungen
		}))


def query_mioe_ort(count, start, max, sHatErgebniss, sJahr, sArt, sAdmLvl, hideFilteredData):
	"""Querystring für MiÖ Orte erstellen."""
	aQuery = """
WITH jahre AS (
	SELECT EXTRACT(YEAR FROM erheb_datum) AS year
	FROM "MioeDB_tbl_volkszaehlung"
	GROUP BY EXTRACT(YEAR FROM erheb_datum)
	ORDER BY year ASC
)
SELECT\n
	"""
	if count:
		aQuery += "	COUNT(m_orte.id)\n"
	else:
		aQuery += """	m_orte.id as id,
	m_orte.id_orte_id as id_orte,
	(CASE WHEN length(ort.ort_namelang) > 0 THEN ort.ort_namelang ELSE ort.ort_namekurz END) as ort_name,
	m_orte.adm_lvl_id as adm_lvl,
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
		if hideFilteredData and sJahr != '0':
			aQuery += "				AND EXTRACT(YEAR FROM vz.erheb_datum) = " + str(int(sJahr)) + "\n"
		if hideFilteredData and sArt != '0':
			aQuery += "				AND vzData.id_art_id = " + str(int(sArt)) + "\n"
		aQuery += """			GROUP BY jahr, vzData.id_art_id
			ORDER BY jahr ASC, vzData.id_art_id ASC
		) as zahlen
	),
	ozby.jahrarray as jahrarray\n"""
	aQuery += "FROM \"MioeDB_tbl_mioe_orte\" as m_orte\n"
	if not count:
		aQuery += """CROSS JOIN LATERAL (
		SELECT jsonb_agg(row_to_json(ozad.*)) as jahrarray
		FROM (
			SELECT jahre.year as jahr, oz.id as moid, (CASE WHEN length(oz.ort_name) > 0 THEN oz.ort_name ELSE oz.histor END) as ort
			FROM jahre,
				LATERAL (
					WITH RECURSIVE ortzuordnungen AS (
						SELECT
							adm.id,
							id_ort1_id,
							orta.histor,
							(CASE WHEN length(orta.namelang) > 0 THEN orta.namelang ELSE orta.namekurz END) as ort_name,
							id_ort2_id,
							"vonDat_start" as von_datum,
							id_quelle_id,
							orta.adm_lvl_id
						FROM "MioeDB_tbl_adm_zuordnung" adm
						LEFT JOIN (
							SELECT ma.id as id, ma.histor_ort as histor, ma.adm_lvl_id as adm_lvl_id, oa.ort_namekurz as namekurz, oa.ort_namelang as namelang
							FROM "MioeDB_tbl_mioe_orte" ma
							LEFT JOIN "OrteDB_tbl_orte" oa ON ma.id_orte_id = oa.id
						) as orta on adm.id_ort1_id = orta.id
						WHERE
							id_ort1_id = m_orte.id  -- GESUCHTE ORTSID
							AND (
								date_part('year', "bisDat_start") >= jahre.year
								OR date_part('year', "bisDat_end") >= jahre.year
								OR ("bisDat_start" IS NULL AND "bisDat_end" IS NULL)
							)
							AND (
								date_part('year', "vonDat_start") <= jahre.year
								OR date_part('year', "vonDat_end") <= jahre.year
								OR ("vonDat_start" IS NULL AND "vonDat_end" IS NULL)
							)
					UNION
						SELECT
							z.id,
							z.id_ort1_id,
							ortb.histor,
							(CASE WHEN length(ortb.namelang) > 0 THEN ortb.namelang ELSE ortb.namekurz END) as ort_name,
							z.id_ort2_id,
							z."vonDat_start" as von_datum,
							z.id_quelle_id,
							ortb.adm_lvl_id
						FROM "MioeDB_tbl_adm_zuordnung" z
						LEFT JOIN (
							SELECT mb.id as id, mb.histor_ort as histor, mb.adm_lvl_id as adm_lvl_id, ob.ort_namekurz as namekurz, ob.ort_namelang as namelang
							FROM "MioeDB_tbl_mioe_orte" mb
							LEFT JOIN "OrteDB_tbl_orte" ob ON mb.id_orte_id = ob.id
						) as ortb on z.id_ort1_id = ortb.id
						INNER JOIN ortzuordnungen o ON o.id_ort2_id = z.id_ort1_id
						WHERE
							ortb.adm_lvl_id < 4
							AND (
								date_part('year', z."bisDat_start") >= jahre.year
								OR date_part('year', z."bisDat_end") >= jahre.year
								OR (z."bisDat_start" IS NULL AND z."bisDat_end" IS NULL)
							)
							AND (
								date_part('year', z."vonDat_start") <= jahre.year
								OR date_part('year', z."vonDat_end") <= jahre.year
								OR (z."vonDat_start" IS NULL AND z."vonDat_end" IS NULL)
							)
					), ortzuordnungjahr AS (
						SELECT *
						FROM ortzuordnungen
						WHERE adm_lvl_id = 3
						ORDER BY von_datum DESC
						LIMIT 1
					)
					SELECT * FROM ortzuordnungjahr
				) AS oz
		) AS ozad
	) as ozby\n"""
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
	if sAdmLvl != '0':
		aQuery += "			AND m_orte.adm_lvl_id = " + str(int(sAdmLvl)) + "\n"
	if not count:
		# ToDo: Order by Gerichtsbezirk im Jaht
		aQuery += "ORDER BY ort_name ASC\n"
		if start > 0:
			aQuery += "OFFSET " + str(int(start)) + "\n"
		if max > 0:
			aQuery += "LIMIT " + str(int(max)) + "\n"
	# print(aQuery)
	return aQuery


def query_admlvl():
	"""Querystring für Administrative Einheiten."""
	return '''SELECT id, name
FROM "MioeDB_tbl_adm_lvl"
ORDER BY name ASC'''


def query_jahre():
	"""Querystring für Jahre."""
	return '''SELECT EXTRACT(YEAR FROM erheb_datum) AS year
FROM "MioeDB_tbl_volkszaehlung"
GROUP BY EXTRACT(YEAR FROM erheb_datum)
ORDER BY year ASC'''


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


def query_verfuegbareJahreArten(sJahr, sArt, hideFilteredData):
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
	if hideFilteredData and sJahr != '0':
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
