from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.start, name='start'),
	url(r'^view/(?P<app_name>[A-Zaeoeuea-zaeoeuess0-9_]+)/(?P<tabelle_name>[a-zaeoeue0-9_]+)/{0,1}$', views.view, name='view'),
]
