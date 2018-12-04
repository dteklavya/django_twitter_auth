



from django.urls import path
from django_twitter_auth import views
from django.conf.urls import url

urlpatterns = [
    path('dance', views.oauth_dance),
    path('helper', views.oauth_helper),
    url(r'^trends/(?P<woe_id>[0-9]+)/$', views.trends),
]
