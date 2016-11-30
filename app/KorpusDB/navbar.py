from django.core.urlresolvers import reverse

def navbar(request):
    anav = []
    if request.user.is_authenticated():
        asub = []
        if request.user.has_perm('KorpusDB.antworten_maskView'):
            asub.append({'sort':0,'titel':'Eingabemaske','url':'#'})
        if request.user.has_perm('KorpusDB.aufgabensets_maskView'):
            asub.append({'sort':2,'titel':'Aufgabensets','url':reverse('KorpusDB:aufgabensets'),'class':''})
        if asub:
            anav.append({'sort':10,'titel':'KorpusDB','url':'#','sub':asub})
    return anav
