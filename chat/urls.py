from django.conf.urls import url

from chat import views

urlpatterns = [
    url(r'^$', views.index, name='chat_index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]