from django.shortcuts import render

from django.shortcuts import redirect, render_to_response, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login as django_login
from django.conf import settings

import json
import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

from .config import *
from .models import TwitterUser

# Create your views here.

def oauth_dance(request):

    _twitter = twitter.Twitter(
    auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET),
    format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
            _twitter.oauth.request_token(oauth_callback=OAUTH_CALLBACK))

    print(oauth_token, oauth_token_secret, "token and secret from twitter")
    # Need to write these interim values out to a file to pick up on the callback 
    # from Twitter that is handled by the web server in /oauth_helper
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)

    oauth_url = (OAUTH_URL + oauth_token)

    # Redirect to twitter URL for user authorization.
    return HttpResponseRedirect(oauth_url)


def oauth_helper(request):

    oauth_verifier = request.GET.get('oauth_verifier')

    # Pick back up credentials from ipynb_oauth_dance
    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)

    _twitter = twitter.Twitter(
        auth=twitter.OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
        _twitter.oauth.access_token(oauth_verifier=oauth_verifier,
                                    oauth_token=oauth_token,
                                    oauth_consumer_key=CONSUMER_KEY))

    # Save tokens to TwitterUser model
    tuser, created = TwitterUser.objects.get_or_create(
            OAUTH_TOKEN = oauth_token,
            OAUTH_TOKEN_SECRET = oauth_token_secret
    )
    
    django_login(request, tuser.user)

    return HttpResponseRedirect(request.build_absolute_uri(REDIRECT_URL_AFTER_AUTH))




def confirm(request):
    
    tokens = TwitterUser.objects.filter(
        username=request.user).values_list('OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET')
    oauth_token, oauth_token_secret = tokens[0][0], tokens[0][1]

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   CONSUMER_KEY, CONSUMER_SECRET)
  
    twitter_api = twitter.Twitter(auth=auth)
    try:
        screen_name = twitter_api.account.verify_credentials()['screen_name']
        return redirect(settings.POST_TWAUTH_URL)
    except twitter.api.TwitterHTTPError:
        return HttpResponse("Twitter returned error. Something went wrong with authorization.") 

# TODO: git clone https://github.com/twbs/bootstrap.git
