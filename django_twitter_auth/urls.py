



from django.urls import path
from django_twitter_auth import views

urlpatterns = [
    path('', views.oauth_dance),
]