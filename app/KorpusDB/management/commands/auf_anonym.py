from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sys
import locale
import os
import json
import time
import datetime
import KorpusDB.models as KorpusDB
from django.db.models import Q


class Command(BaseCommand):
	help = 'CSV Dateien für die Anonymisierung der Aufgaben erstellen.'

	def handle(self, *args, **options):
		verzeichnis = os.path.join(settings.PRIVATE_STORAGE_ROOT, 'anonym_a')
		if not os.path.isdir(verzeichnis):
			os.mkdir(verzeichnis)

		for aInfErh in KorpusDB.tbl_inferhebung.objects.filter(id_Transcript=None):
			aErhInfAufgaben = aInfErh.tbl_erhinfaufgaben_set.all()
			csv = os.path.join(aInfErh.Dateipfad, aInfErh.Audiofile) + '\nErhInfAufgabeId;beep;sync;start;end\n'
			hasData = False
			if aErhInfAufgaben.count() > 0:
				print(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
				# print(aInfErh, datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
				# print('  ', aInfErh.Audiofile, aInfErh.time_beep, aInfErh.sync_time)
				# print('   -', aErhInfAufgaben.count(), 'Aufgaben')
				keep = True
				for aErhInfAufgabe in aErhInfAufgaben:
					syncDiff = (aErhInfAufgabe.time_beep if aErhInfAufgabe.time_beep else datetime.timedelta(seconds=0)) - (aErhInfAufgabe.sync_time if aErhInfAufgabe.sync_time else datetime.timedelta(seconds=0))
					# print('     ', syncDiff, aErhInfAufgabe.start_Aufgabe - syncDiff, aErhInfAufgabe.stop_Aufgabe - syncDiff)
					for aAntwort in aErhInfAufgabe.id_Aufgabe.tbl_antworten_set.all():
						if aAntwort.ist_Satz and ((aAntwort.ist_Satz.Transkript and ('[' in aAntwort.ist_Satz.Transkript or ']' in aAntwort.ist_Satz.Transkript)) or (aAntwort.ist_Satz.Standardorth and ('[' in aAntwort.ist_Satz.Standardorth or ']' in aAntwort.ist_Satz.Standardorth)) or (aAntwort.ist_Satz.ipa and ('[' in aAntwort.ist_Satz.ipa or ']' in aAntwort.ist_Satz.ipa))):
							# print('         ', aAntwort.ist_Satz.Transkript, aAntwort.ist_Satz.Standardorth, aAntwort.ist_Satz.ipa)
							keep = False
					if keep:
						# print('       ', aErhInfAufgabe.id_Aufgabe_id, aErhInfAufgabe.id_Aufgabe.tbl_antworten_set.all().count())
						csv += str(aErhInfAufgabe.pk) + ';' + str(aInfErh.time_beep) + ';' + str(aInfErh.sync_time) + ';' + str(aErhInfAufgabe.start_Aufgabe - syncDiff) + ';' + str(aErhInfAufgabe.stop_Aufgabe - syncDiff) + '\n'
						hasData = True
			dateiname = '.'.join(aInfErh.Audiofile.split('.')[:-1]) + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
			if hasData:
				with open(os.path.join(verzeichnis, dateiname), 'a') as file:
					file.write(csv)
			# print('   ->', dateiname)
		print('Fertig!', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
