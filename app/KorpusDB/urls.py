from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^aufgabensets/{0,1}$', views.aufgabensets, name='aufgabensets'),
	url(r'^tagsedit/{0,1}$', views.tagsedit, name='tagsedit'),
]
