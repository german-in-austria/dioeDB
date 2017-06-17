from django.core.urlresolvers import reverse

def navbar(request):
    anav = []
    if request.user.is_authenticated():
        anav.append({'sort':0,'titel':'Startseite','url':reverse('Startseite:start'),'class':''})
        asub = []
        if request.user.is_superuser:
            asub.append({'sort':50,'titel':'Admin','url':reverse('admin:index'),'target':'_blank'})
        asub.append({'sort':60,'titel':'Passwort ändern','url':reverse('password_change')})
        asub.append({'sort':99,'titel':'Abmelden','url':reverse('dioedb_logout')})
        anav.append({'sort':99,'titel':request.user.username,'url':'#','aclass':'text-uppercase','sub':asub})
    return anav
