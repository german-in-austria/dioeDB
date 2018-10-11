from django.core.urlresolvers import reverse


def navbar(request):
	anav = []
	if request.user.is_authenticated():
		asub = []
		if request.user.has_perm('KorpusDB.antworten_maskView'):
			asub.append({'sort': 0, 'titel': 'EingabeSPT', 'url': reverse('KorpusDB:maske', args=[0, 0])})
		if request.user.has_perm('KorpusDB.antworten_maskView'):
			asub.append({'sort': 5, 'titel': 'EingabeFB', 'url': reverse('KorpusDB:maske2', args=[0, 0])})
		if request.user.has_perm('KorpusDB.antworten_maskView'):
			asub.append({'sort': 5, 'titel': 'Aufgabenmöglichkeiten Tags', 'url': reverse('KorpusDB:aufmoegtags', args=[0, 0])})
		# if request.user.has_perm('KorpusDB.aufgabensets_maskView'):
		# 	asub.append({'sort': 10, 'titel': 'Aufgabensets', 'url': reverse('KorpusDB:aufgabensets'), 'class': ''})
		if request.user.has_perm('KorpusDB.tags_maskView'):
			asub.append({'sort': 20, 'titel': 'Tageditor', 'url': reverse('KorpusDB:tagsedit'), 'class': ''})
		if request.user.has_perm('KorpusDB.presettags_maskView'):
			asub.append({'sort': 21, 'titel': 'Preset Tags Editor', 'url': reverse('KorpusDB:presettagsedit'), 'class': ''})
		if request.user.has_perm('KorpusDB.aufgabensets_maskView'):
			asub.append({'sort': 30, 'titel': 'InfErhebungen', 'url': reverse('KorpusDB:inferhebung'), 'class': ''})
		if request.user.has_perm('KorpusDB.auswertung'):
			asub.append({'sort': 40, 'titel': 'Auswertung', 'url': reverse('KorpusDB:auswertung'), 'class': ''})
		if asub:
			anav.append({'sort': 10, 'titel': 'KorpusDB', 'url': '#', 'sub': asub})
	return anav
