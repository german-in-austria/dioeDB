from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^orte/{0,1}$', views.orte, name='orte'),
	url(r'^wb/{0,1}$', views.wb, name='wb'),
	url(r'^vz/{0,1}$', views.vz, name='vz'),
	url(r'^varietaet/{0,1}$', views.varietaet, name='varietaet'),
]
