from django.conf.urls import patterns, url, include
from administration import urls as auth_urls
from paparazzi import views

urlpatterns = patterns(
    # /auth/
    url(r'^auth/', include(auth_urls)),

    url(r'^$', views.api_root, name='paparazzi-api'),
    url(r'^$', views.index, name='index'),
)