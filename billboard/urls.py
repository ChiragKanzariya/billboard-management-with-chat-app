from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include 
from django.views.generic.base  import TemplateView

from billboard.views import welcome, send_push, notification


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^advertiser/', include('advertiser.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^welcome/$', welcome, name='billboard_welcome'),
    path('', notification),
    path('send_push', send_push),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='advertiser/sw.js', content_type='application/x-javascript')),
] 