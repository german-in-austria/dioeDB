from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^maske/{0,1}$', views.maske, name='maske'),
	url(r'^termine/{0,1}$', views.termine, name='termine'),
	url(r'^berufe/{0,1}$', views.berufe, name='berufe'),
	url(r'^test/{0,1}$', views.test, name='test'),
]
