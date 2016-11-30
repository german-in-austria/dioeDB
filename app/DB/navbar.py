from django.core.urlresolvers import reverse

def navbar(request):
    anav = []
    if request.user.is_authenticated():
        asub = []
        if request.user.has_perm('KorpusDB.edit') or request.user.has_perm('PersonenDB.edit'):
            asub.append({'sort':0,'titel':'Verwaltung','url':reverse('DB:start')})
            anav.append({'sort':98,'titel':'DB','url':'#','sub':asub})
    return anav
