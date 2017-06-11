from django.conf.urls import patterns, url, include
from escrow import views
from config.views import *

urlpatterns = [
    url(r'^escrow/create/$', views.CreateEscrow.as_view(), name='create-escrow'),
    url(r'^escrow/(?P<transfer_id>.*)/$', views.UpdateEscrow.as_view(), name='update-escrow'),
]