from django.core.urlresolvers import reverse

def navbar(request):
	anav = []
	if request.user.is_authenticated():
		asub = []
		if request.user.has_perm('KorpusDB.edit') or request.user.has_perm('PersonenDB.edit'):
			asub.append({'sort':0,'titel':'Verwaltung','url':reverse('DB:start')})
		if request.user.has_perm('DB.dateien'):
			asub.append({'sort':50,'titel':'Dateien','url':reverse('DB:dateien'),'class':''})
		if asub:
			anav.append({'sort':98,'titel':'DB','url':'#','sub':asub})
	return anav
