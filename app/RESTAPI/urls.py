from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^test/{0,1}$", views.test, name="test"),
    url(r"^auth/{0,1}$", views.auth, name="auth"),
    url(r"^getTags/{0,1}$", views.getTags, name="getTags"),
    url(r"^getZitatUrl/{0,1}$", views.getZitatUrl, name="getZitatUrl"),
    url(r"^setZitatUrl/{0,1}$", views.setZitatUrl, name="setZitatUrl"),
    url(
        r"^setZitatUrl/(?P<aPk>[0-9]+)/{0,1}$", views.setZitatUrl, name="setZitatUrlId"
    ),
    url(r"^getAntworten/{0,1}$", views.getAntworten, name="getAntworten"),
    url(r"^getErhebungsorte/{0,1}$", views.getErhebungsorte, name="getErhebungsorte"),
    url(r"^getBerufe/{0,1}$", views.getBerufe, name="getBerufe"),
    url(r"^docs/", include("rest_framework_swagger.urls")),
]
