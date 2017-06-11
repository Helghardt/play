from django.conf.urls import patterns, url, include
from everything import views
from config.views import *

urlpatterns = [
    url(r'^$', api_root),
    # /photos/
    url(r'^create/$', views.CreateLog.as_view(), name='create-log'),
    url(r'^list/$', views.ListLog.as_view(), name='list-log'),
    url(r'^image/$', views.ListCreateImage.as_view(), name='image'),
]