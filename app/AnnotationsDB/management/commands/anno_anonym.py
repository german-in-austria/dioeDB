from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sys
import locale
import os
import json
import time
import datetime
import AnnotationsDB.models as adbmodels
from django.db.models import Q


class Command(BaseCommand):
	help = 'CSV Dateien für die Anonymisierung der Transkripte erstellen.'

	def handle(self, *args, **options):
		verzeichnis = os.path.join(settings.PRIVATE_STORAGE_ROOT, 'anonym')
		if not os.path.isdir(verzeichnis):
			os.mkdir(verzeichnis)
		for aTrans in adbmodels.transcript.objects.all():
			print('...', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
			# print('\n' + aTrans.name, datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
			for aInfErh in aTrans.tbl_inferhebung_set.all():
				# print('  -', aInfErh.Audiofile, aInfErh.time_beep, aInfErh.sync_time)
				if aInfErh.Audiofile and '.' in aInfErh.Audiofile:
					aEvents = []
					csv = os.path.join(aInfErh.Dateipfad, aInfErh.Audiofile) + '\neventId;beep;sync;start;end\n'
					hasData = False
					for aToken in adbmodels.token.objects.filter(Q(text__contains='[') | Q(text__contains=']') | Q(ortho__contains='[') | Q(ortho__contains=']'), transcript_id=aTrans.pk):
						if aToken.event_id_id not in aEvents:
							aEvents.append(aToken.event_id_id)
					aEvents.sort()
					for aEvent in aEvents:
						aEventObj = adbmodels.event.objects.get(pk=aEvent)
						csv += str(aEvent) + ';' + str(aInfErh.time_beep) + ';' + str(aInfErh.sync_time) + ';' + str(aEventObj.start_time) + ';' + str(aEventObj.end_time) + '\n'
						hasData = True
						# print('     ', aEvent, aEventObj.start_time, '-', aEventObj.end_time)
					dateiname = '.'.join(aInfErh.Audiofile.split('.')[:-1]) + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
					if hasData:
						with open(os.path.join(verzeichnis, dateiname), 'a') as file:
							file.write(csv)
					# print('   ->', dateiname)
		print('Fertig!', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
