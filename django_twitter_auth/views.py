from django.shortcuts import render

from django.shortcuts import redirect, render_to_response, HttpResponse
from django.shortcuts import HttpResponseRedirect

import json
import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

from .config import *

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

    # Write out the final credentials that can be picked up after the following
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
#     return HttpResponse("%s %s written to %s" % (oauth_token, oauth_token_secret, OAUTH_FILE))
    return HttpResponseRedirect(request.build_absolute_uri(REDIRECT_URL_AFTER_AUTH))




def trends(request, woe_id):

    print("WOE ID", woe_id)
    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    trends = twitter_api.trends.place(_id=woe_id)
#     print(json.dumps(trends, indent=1))

    # Some basic filters for trending topics
    my_trends = []
    for trend in trends[0]['trends']:
        if trend['tweet_volume'] != None:
            my_trends.append({
                'name': trend['name'],
                'tweet_volume': trend['tweet_volume'],
                'url': trend['url']})

    print(my_trends)
    return HttpResponse(json.dumps(my_trends, indent=1))


def confirm(request):
    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    print(oauth_token, twitter_api)
    try:
        twitter_api.statuses.home_timeline()
        return HttpResponse("Twitter OAuth Dance Completed Successfully")        
    except twitter.api.TwitterHTTPError:
        return HttpResponse("Twitter returned error. Something went wrong with authorization.") 

