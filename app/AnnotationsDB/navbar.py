from django.core.urlresolvers import reverse


def navbar(request):
	anav = []
	if request.user.is_authenticated():
		asub = []
		if request.user.has_perm('AnnotationsDB.transcript_maskView'):
			asub.append({'sort': 0, 'titel': 'Annotations Tool (dev)', 'url': reverse('AnnotationsDB:tool')})
		if request.user.has_perm('AnnotationsDB.transcript_maskView'):
			asub.append({'sort': 5, 'titel': 'Anno-sent', 'url': reverse('AnnotationsDB:annosent')})
		if request.user.has_perm('AnnotationsDB.transcript_maskView'):
			asub.append({'sort': 10, 'titel': 'Anno-check', 'url': reverse('AnnotationsDB:annocheck')})
		if request.user.has_perm('AnnotationsDB.transcript_maskView'):
			asub.append({'sort': 15, 'titel': 'Auswertung', 'url': reverse('AnnotationsDB:auswertung', args=[0, 0])})
		if asub:
			anav.append({'sort': 98, 'titel': 'AnnotationsDB', 'url': '#', 'sub': asub})
	return anav
