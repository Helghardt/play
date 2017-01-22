from django.conf.urls import patterns, url, include
from administration import urls as auth_urls
from starter_app import views

urlpatterns = patterns(
    '',
    url(r'^auth/', include(auth_urls)),
    url(r'^$', views.api_root),
    url(r'^$', views.index, name='index'),
)