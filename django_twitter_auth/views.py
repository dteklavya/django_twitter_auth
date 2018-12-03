from django.shortcuts import render
from django.shortcuts import redirect, render_to_response, HttpResponse

# Create your views here.

def oauth_dance(request):

    print("OAuth Dancing")
    return HttpResponse("OAuth Dancing")
