from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()


urlpatterns = [

    # Admin Url
    url(r'^admin/', include(admin.site.urls)),

    # # Auth API
    url(r'^api/1/', include('administration.urls')),

    # API
    url(r'^api/1/', include('everything.urls', namespace='everything-api')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)