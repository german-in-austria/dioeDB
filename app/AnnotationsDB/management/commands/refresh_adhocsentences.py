from django.core.management.base import BaseCommand, CommandError
import datetime
import AnnotationsDB.models as adbmodels


class Command(BaseCommand):
	help = 'Materialized View für Annosent aktuallisieren.'

	def handle(self, *args, **options):
		print('refresh_adhocsentences.py aufgerufen', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
		adbmodels.tbl_refreshlog_mat_adhocsentences.refresh()
		print('refresh_adhocsentences.py fertig', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
