from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base  import TemplateView

from advertiser import views

urlpatterns = [
    url(r'^$', views.home, name='advertiser_home'),
    url(r'^owner/$', views.billboard_owner, name='advertiser_owner_home'),
    url(r'^login$', LoginView.as_view(template_name="advertiser/login_form.html"), name='advertiser_login'),
    url(r'logout$', LogoutView.as_view(), name='advertiser_logout'),
    url(r'^video/$', views.post_new, name='add_video'),
    url(r'^signup$', views.signup, name='advertiser_signup'),
    url(r'invitation$', views.new_invitation, name='advertiser_new_invitation'),
    url(r'accept_invitation/(?P<id>\d+)/$', views.accept_invitation, name="advertiser_accept_invitation"),
]
