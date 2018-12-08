



from django.urls import path
from django_twitter_auth import views
from django.conf.urls import url

urlpatterns = [
    path('dance', views.oauth_dance),
    path('helper', views.oauth_helper),
    path('confirm', views.confirm)
]
