



from django.urls import path
from django_twitter_auth import views

urlpatterns = [
    path('dance', views.oauth_dance),
    path('helper', views.oauth_helper)
]
