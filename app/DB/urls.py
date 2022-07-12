from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.start, name='start'),
	url(r'^resetidseq/(?P<app_name>[A-ZÄÖÜa-zäöüß0-9_]+)/(?P<tabelle_name>[A-ZÄÖÜa-zäöüß0-9_]+)/{0,1}$', views.resetidseq, name='resetidseq'),
	url(r'^getDuration/(?P<app_name>[A-ZÄÖÜa-zäöüß0-9_]+)/(?P<tabelle_name>[A-ZÄÖÜa-zäöüß0-9_]+)/{0,1}$', views.getDuration, name='getDuration'),
	url(r'^view/(?P<app_name>[A-ZÄÖÜa-zäöüß0-9_]+)/(?P<tabelle_name>[A-ZÄÖÜa-zäöüß0-9_]+)/{0,1}$', views.view, name='view'),
	url(r'^diagramm/{0,1}$', views.diagramm, name='diagramm'),
	url(r'^search/{0,1}$', views.search, name='search'),
	url(r'^tagsystemvue/{0,1}$', views.tagsystemvue, name='tagsystemvue'),
	url(r'^dateien/{0,1}$', views.dateien, name='dateien'),
	url(r'^statistik/{0,1}$', views.statistik, name='statistik'),
]
