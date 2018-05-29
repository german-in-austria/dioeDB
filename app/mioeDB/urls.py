from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^orte/{0,1}$', views.mioe, name='orte'),
	url(r'^wb/{0,1}$', views.wb, name='wb'),
	url(r'^vz/{0,1}$', views.vz, name='vz'),
	url(r'^admzuord/{0,1}$', views.admzuord, name='admzuord'),
]
