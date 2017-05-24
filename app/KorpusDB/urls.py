from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^aufgabensets/{0,1}$', views.aufgabensets, name='aufgabensets'),
	url(r'^tagsedit/{0,1}$', views.tagsedit, name='tagsedit'),
	url(r'^presettagsedit/{0,1}$', views.presettagsedit, name='presettagsedit'),
	url(r'^maske/(?P<ipk>[A-ZÄÖÜa-zäöü0-9_]+)/(?P<apk>[A-ZÄÖÜa-zäöü0-9_]+)/{0,1}$', views.maske, name='maske'),
	url(r'^inferhebung/{0,1}$', views.inferhebung, name='inferhebung'),
]
