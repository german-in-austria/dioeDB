from django.core.urlresolvers import reverse


def navbar(request):
    anav = []
    # if request.user.is_authenticated():
    #     asub = []
    #     if request.user.has_perm('mioeDB.personen_maskView'):
    #         asub.append({
    #             'sort': 0,
    #             'titel': 'MiÖ-Orte',
    #             'url': reverse('mioeDB:orte')
    #             })
    #         asub.append({
    #             'sort': 1,
    #             'titel': 'VZ',
    #             'url': reverse('mioeDB:vz')
    #             })
    #         asub.append({
    #             'sort': 2,
    #             'titel': 'Wenkerbogen',
    #             'url': reverse('mioeDB:wb')
    #             })
    #     if asub:
    #         anav.append({'sort': 15, 'titel': 'MioeDB', 'url': '#', 'sub': asub})
    return anav
