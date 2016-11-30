from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^maske/{0,1}$', views.maske, name='maske'),
]
