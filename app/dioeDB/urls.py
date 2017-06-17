from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from Startseite import views as Startseite_views
import private_storage.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('Startseite.urls', namespace='Startseite')),
    url(r'^db/', include('DB.urls', namespace='DB')),
    url(r'^korpusdb/', include('KorpusDB.urls', namespace='KorpusDB')),
    url(r'^personendb/', include('PersonenDB.urls', namespace='PersonenDB')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='dioedb_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('Startseite:start')}, name='dioedb_logout'),
    url(r'^change-password/$', 'django.contrib.auth.views.password_change', {'template_name': 'main/change-password.html'}, name='password_change'),
    url(r'^change-password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'main/change-password-done.html'}, name='password_change_done'),
   	url(r'^sysstatus/{0,1}$', Startseite_views.sysStatusView, name='sysstatus'),
    url(r'^private-media/', include(private_storage.urls)),
]
