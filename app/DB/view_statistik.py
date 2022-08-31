"""Anzeige eines Diagramms der Models."""
from django.shortcuts import render_to_response
from django.template import RequestContext
import os
import datetime
import json
from django.conf import settings
import AnnotationsDB.models as adbmodels


def view_statistik(request):
	"""Standard Anzeige für Statistik."""
	info = ''
	error = ''

	if 'type' in request.POST and request.POST.get('type') == 'now':
		statistik = {
			'counts': {
				'transcripts': adbmodels.transcript.objects.all().count(),
				'events': adbmodels.event.objects.all().count(),
				'tokens': adbmodels.token.objects.all().count(),
				'transcriptlessEvents': adbmodels.event.objects.filter(transcript_id__isnull=True).count(),
				'transcriptlessTokens': adbmodels.token.objects.filter(transcript_id__isnull=True).count()
			},
			'transcripts': []
		}

		for aTrans in adbmodels.transcript.objects.all():
			statistik['transcripts'].append(
				{
					'id': aTrans.id,
					'name': aTrans.name,
					'update_time': aTrans.update_time,
					'updated': aTrans.updated,
					'events': {
						'count': adbmodels.event.objects.filter(transcript_id=aTrans.id).count(),
						'oldest': adbmodels.event.objects.filter(transcript_id=aTrans.id).order_by('updated').first(),
						'newest': adbmodels.event.objects.filter(transcript_id=aTrans.id).order_by('updated').last(),
					},
					'tokens': {
						'count': adbmodels.token.objects.filter(transcript_id=aTrans.id).count(),
						'oldest': adbmodels.token.objects.filter(transcript_id=aTrans.id).order_by('updated').first(),
						'newest': adbmodels.token.objects.filter(transcript_id=aTrans.id).order_by('updated').last(),
					},
				}
			)

		# Ausgabe der Seite
		return render_to_response(
			'DB/statistik_now.html',
			RequestContext(request, {'statistik': statistik, 'error': error, 'info': info}),
		)
	else:
		transcripte = {}
		for tr in adbmodels.transcript.objects.all():
			transcripte[tr.id] = tr.name
		statistikListe = []
		tagBreite = 15
		aDir = settings.AUDIO_ROOT
		aFile = os.path.join(aDir, 'statistic_' + datetime.datetime.now().strftime('%Y') + '.log')
		with open(aFile, "rb") as f:
			for line in tail(f, 90):
				statistikListe.append(line.decode("utf-8"))
		statistikData = '[' + ','.join(statistikListe) + ']'
		statistikListe = json.loads(statistikData)
		statistikListeClean = []
		statistikGrafik = {
			'kc': {},
			'kcs': {},
			'ac': {},
			'acs': {},
			'c': len(statistikListe),
			'cw': (len(statistikListe) - 1) * tagBreite + 2,
			'tr': {}
		}
		min = {}
		max = {}
		min2 = {}
		max2 = {}
		for line in statistikListe:
			for p in line:
				cleanLine = line[p]
				cleanLine['lt'] = p[0:10] + '_' + p[10:]
			for p2 in cleanLine['kc']:
				if p2 not in max or max[p2] < cleanLine['kc'][p2]:
					max[p2] = cleanLine['kc'][p2]
				if p2 not in min or min[p2] > cleanLine['kc'][p2]:
					min[p2] = cleanLine['kc'][p2]
			for p2 in cleanLine['ac']:
				if p2 not in max2 or max2[p2] < cleanLine['ac'][p2]:
					max2[p2] = cleanLine['ac'][p2]
				if p2 not in min2 or min2[p2] > cleanLine['ac'][p2]:
					min2[p2] = cleanLine['ac'][p2]
			statistikListeClean.append(cleanLine)
		dg = 0
		for line in statistikListeClean:
			for c in line['kc']:
				if c not in statistikGrafik['kc']:
					statistikGrafik['kc'][c] = []
					statistikGrafik['kcs'][c] = ''
				av = ((line['kc'][c] - min[c]) / (max[c] - min[c])) if max[c] > min[c] else 0.5
				statistikGrafik['kc'][c].append(av)
				statistikGrafik['kcs'][c] += str(dg * tagBreite) + ',' + str((1 - av) * 100) + ' '
			for c in line['ac']:
				if c not in statistikGrafik['ac']:
					statistikGrafik['ac'][c] = []
					statistikGrafik['acs'][c] = ''
				av = ((line['ac'][c] - min2[c]) / (max2[c] - min2[c])) if max2[c] > min2[c] else 0.5
				statistikGrafik['ac'][c].append(av)
				statistikGrafik['acs'][c] += str(dg * tagBreite) + ',' + str((1 - av) * 100) + ' '
			for tr in line['tr']:
				if tr['i'] not in statistikGrafik['tr']:
					statistikGrafik['tr'][tr['i']] = {
						'n': transcripte[tr['i']] if tr['i'] in transcripte else 'None',
						'i': tr['i'],
						'fu': tr['u'],
						'lu': tr['u'],
						'p': '',
						'fec': tr['e'],
						'lec': tr['e'],
						'dec': [tr['e']],
						'minec': tr['e'],
						'maxec': tr['e'],
						'svgec': '',
						'ftc': tr['t'],
						'ltc': tr['t'],
						'dtc': [tr['t']],
						'mintc': tr['t'],
						'maxtc': tr['t'],
						'svgtc': ''
					}
				else:
					statistikGrafik['tr'][tr['i']]['lu'] = tr['u']
					statistikGrafik['tr'][tr['i']]['lec'] = tr['e']
					statistikGrafik['tr'][tr['i']]['ltc'] = tr['t']
					statistikGrafik['tr'][tr['i']]['dec'].append(tr['e'])
					statistikGrafik['tr'][tr['i']]['dtc'].append(tr['t'])
					if statistikGrafik['tr'][tr['i']]['minec'] > tr['e']:
						statistikGrafik['tr'][tr['i']]['minec'] = tr['e']
					if statistikGrafik['tr'][tr['i']]['maxec'] < tr['e']:
						statistikGrafik['tr'][tr['i']]['maxec'] = tr['e']
					if statistikGrafik['tr'][tr['i']]['mintc'] > tr['t']:
						statistikGrafik['tr'][tr['i']]['mintc'] = tr['t']
					if statistikGrafik['tr'][tr['i']]['maxtc'] < tr['t']:
						statistikGrafik['tr'][tr['i']]['maxtc'] = tr['t']
			dg = dg + 1
		for k, gtr in statistikGrafik['tr'].items():
			dge = dg - len(gtr['dec'])
			for e in gtr['dec']:
				av = ((e - gtr['minec']) / (gtr['maxec'] - gtr['minec'])) if gtr['maxec'] > gtr['minec'] else 0.5
				gtr['svgec'] += str(dge * tagBreite) + ',' + str((1 - av) * 74 + 1) + ' '
				dge = dge + 1
			dgt = dg - len(gtr['dtc'])
			for t in gtr['dtc']:
				av = ((t - gtr['mintc']) / (gtr['maxtc'] - gtr['mintc'])) if gtr['maxtc'] > gtr['mintc'] else 0.5
				gtr['svgtc'] += str(dgt * tagBreite) + ',' + str((1 - av) * 74 + 1) + ' '
				dgt = dgt + 1
		return render_to_response(
			'DB/statistik_overview.html',
			RequestContext(request, {'statistikData': statistikData, 'statistikListe': statistikListeClean, 'statistikLastLine': statistikListeClean[-1], 'statistikFirstLine': statistikListeClean[0], 'statistikGrafik': statistikGrafik, 'error': error, 'info': info}),
		)


def tail(f, lines=20):
    total_lines_wanted = lines
    BLOCK_SIZE = 102400
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0,0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return all_read_text.splitlines()[-total_lines_wanted:]
