from django.conf.urls import patterns, url, include
from everything import views

urlpatterns = [
    url(r'^$', views.api_root),
    # /photos/
    url(r'^create/$', views.CreateLog.as_view(), name='create-log'),
    url(r'^list/$', views.ListLog.as_view(), name='list-log'),
    url(r'^image/$', views.ListCreateImage.as_view(), name='image'),
]