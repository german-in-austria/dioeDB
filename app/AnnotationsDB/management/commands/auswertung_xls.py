from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sys, locale, os
import json
import time
import datetime
from AnnotationsDB.views_auswertung import views_auswertung_func


class Command(BaseCommand):
	help = 'Auswertung XLS erstellen.'

	def add_arguments(self, parser):
		parser.add_argument('aTagEbene', nargs='+', type=int)

	def handle(self, *args, **options):
		aTagEbene = options['aTagEbene'][0]
		print('auswertung_xls.py aufgerufen', aTagEbene)
		[art, wb] = views_auswertung_func(aTagEbene, 0, 1, None, None)
		dateiname = 'tagebene_' + str(aTagEbene) + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.xls'
		verzeichnis = settings.PRIVATE_STORAGE_ROOT
		for subdir in ['annotationsdb', 'auswertung']:
			verzeichnis = os.path.join(verzeichnis, subdir)
			if not os.path.isdir(verzeichnis):
				os.mkdir(verzeichnis)
		wb.save(os.path.join(verzeichnis, dateiname))
		print('auswertung_xls.py fertig', aTagEbene, ' -> ', os.path.join(verzeichnis, dateiname), art, wb)
