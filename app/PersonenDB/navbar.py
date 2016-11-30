from django.core.urlresolvers import reverse

def navbar(request):
    anav = []
    if request.user.is_authenticated():
        asub = []
        if request.user.has_perm('PersonenDB.personen_maskView'):
            asub.append({'sort':0,'titel':'Eingabemaske','url':reverse('PersonenDB:maske')})
        if asub:
            anav.append({'sort':5,'titel':'PersonenDB','url':'#','sub':asub})
    return anav
