from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^test/{0,1}$', views.test, name='test'),
	url(r'^getTags/{0,1}$', views.getTags, name='getTags'),
	url(r'^getZitatUrl/{0,1}$', views.getZitatUrl, name='getZitatUrl'),
	url(r'^getAntworten/{0,1}$', views.getAntworten, name='getAntworten'),
	url(r'^getErhebungsorte/{0,1}$', views.getErhebungsorte, name='getErhebungsorte'),
	url(r'^getBerufe/{0,1}$', views.getBerufe, name='getBerufe'),
]
