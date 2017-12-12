from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^test/{0,1}$', views.test, name='test'),
	url(r'^getTags/{0,1}$', views.getTags, name='getTags'),
]
