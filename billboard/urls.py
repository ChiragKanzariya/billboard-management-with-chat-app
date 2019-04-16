from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include 

from billboard.views import welcome


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^advertiser/', include('advertiser.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^welcome/$', welcome, name='billboard_welcome'),
]