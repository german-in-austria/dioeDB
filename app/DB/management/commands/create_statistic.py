from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sys, locale, os
import json
import time
import datetime
from django.db.models import Q
import AnnotationsDB.models as adbmodels
import KorpusDB.models as kdbmodels


class Command(BaseCommand):
	help = 'Statistische Daten erheben.'

	def handle(self, *args, **options):
		zeit = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
		print('create_statistic.py aufgerufen', zeit)
		aDir = settings.AUDIO_ROOT
		aFile = os.path.join(aDir, 'statistic_' + datetime.datetime.now().strftime('%Y') + '.log')

		statistik = {
			'kc': {
				'a': kdbmodels.tbl_antworten.objects.all().count(),
				'at': kdbmodels.tbl_antwortentags.objects.all().count(),
				't': kdbmodels.tbl_tags.objects.all().count(),
				'au': kdbmodels.tbl_aufgaben.objects.all().count(),
			},
			'ac': {
				'tr': adbmodels.transcript.objects.all().count(),
				'e': adbmodels.event.objects.all().count(),
				't': adbmodels.token.objects.all().count(),
				'at': kdbmodels.tbl_antworten.objects.filter(ist_token__gt=0).count(),
				'ats': kdbmodels.tbl_antworten.objects.filter(ist_tokenset__gt=0).count(),
				'aes': kdbmodels.tbl_antworten.objects.filter(ist_eventset__gt=0).count(),
			},
			'tr': []
		}

		for aTrans in adbmodels.transcript.objects.all():
			statistik['tr'].append(
				{
					'i': aTrans.id,
					'u': aTrans.updated.strftime('%d.%m.%Y_%H:%M:%S') if aTrans.updated else None,
					'e': adbmodels.event.objects.filter(transcript_id=aTrans.id).count(),
					't': adbmodels.token.objects.filter(transcript_id=aTrans.id).count(),
					'at': kdbmodels.tbl_antworten.objects.filter(ist_token__transcript_id_id=aTrans.id).distinct().count(),
					'ats': kdbmodels.tbl_antworten.objects.filter(Q(ist_tokenset__id_von_token__transcript_id_id=aTrans.id) | Q(ist_tokenset__tbl_tokentoset__id_token__transcript_id_id=aTrans.id)).distinct().count(),
					'aes': kdbmodels.tbl_antworten.objects.filter(ist_eventset__id_von_event__transcript_id_id=aTrans.id).distinct().count(),
				}
			)

		with open(aFile, 'a') as file:
			file.write(json.dumps({zeit: statistik}).replace(" ", "") + '\n')
		print('create_statistic.py fertig', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
