"""Anzeige eines Diagramms der Models."""
from django.shortcuts import render_to_response
from django.template import RequestContext
import AnnotationsDB.models as adbmodels


def view_statistik(request):
	"""Standard Anzeige für Statistik."""
	info = ''
	error = ''
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
		'DB/statistik.html',
		RequestContext(request, {'statistik': statistik, 'error': error, 'info': info}),
	)
