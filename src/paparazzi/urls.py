from django.conf.urls import patterns, url

from paparazzi import views

urlpatterns = patterns(
    '',
    url(r'^$', views.api_root),
    url(r'^$', views.index, name='index'),
)