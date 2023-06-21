from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^tool/{0,1}$', views.tool, name='tool'),
	url(r'^annotool/{0,1}$', views.annotool, name='annotool'),
	url(r'^annotool/(?P<ipk>[A-ZÄÖÜa-zäöü0-9_]+)/(?P<tpk>[A-ZÄÖÜa-zäöü0-9_]+)/{0,1}$', views.annotool, name='annotool'),
	url(r'^auswertung/(?P<aErhebung>[A-ZÄÖÜa-zäöü0-9_]+)/(?P<aTagEbene>[A-ZÄÖÜa-zäöü0-9_]+)/(?P<aSeite>[A-ZÄÖÜa-zäöü0-9_]+)/{0,1}$', views.auswertung, name='auswertung'),
	url(r'^annosent/{0,1}$', views.annosent, name='annosent'),
	url(r'^annocheck/{0,1}$', views.annocheck, name='annocheck'),
	url(r'^eventtier/{0,1}$', views.eventtier, name='eventtier'),
]
