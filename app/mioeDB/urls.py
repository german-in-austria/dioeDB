from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^orte/{0,1}$', views.orte, name='orte'),
	url(r'^wb/{0,1}$', views.wb, name='wb'),
	url(r'^vz/{0,1}$', views.vz, name='vz'),
	url(r'^inst/{0,1}$', views.inst, name='inst'),
	url(r'^varietaet/{0,1}$', views.varietaet, name='varietaet'),
	url(r'^literatur/{0,1}$', views.literatur, name='literatur'),
	url(r'^verlage/{0,1}$', views.verlage, name='verlage'),
	url(r'^quelle/{0,1}$', views.quelle, name='quelle'),
	url(r'^artquelle/{0,1}$', views.artInQuelle, name='artInQuelle'),
	url(r'^religion/{0,1}$', views.religion, name='religion'),
	url(r'^institutionen/{0,1}$', views.institutionen, name='institutionen'),
	url(r'^auswertung/{0,1}$', views.auswertung, name='auswertung'),
	url(r'^mioe-auswertung/{0,1}$', views.mioeAuswertung, name='mioeAuswertung'),
]
