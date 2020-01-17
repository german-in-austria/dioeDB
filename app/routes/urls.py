from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^transcripts/{0,1}$', views.transcripts, name='transcripts'),
	url(r'^transcript/(?P<aPk>[0-9]+)/(?P<aNr>[0-9]+)/{0,1}$', views.transcript, name='transcript'),
	url(r'^transcript/save/(?P<aPk>[0-9]+)/{0,1}$', views.transcriptSave, name='transcriptSave'),
	url(r'^transcript/create/{0,1}$', views.transcriptCreate, name='transcriptCreate'),
	url(r'^einzelerhebungen/{0,1}$', views.einzelerhebungen, name='einzelerhebungen'),
	url(r'^files/{0,1}$', views.files, name='files'),
	url(r'^auth/{0,1}$', views.auth, name='auth'),
]
