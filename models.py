from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import login

import string
from random import randint, choice

import twitter
from .config import *

# Create your models here.


class TwitterUser(models.Model):
    '''
    Holds minimal data from user's twitter profile.
    '''

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Adding a new user.
        # RefCode: https://docs.djangoproject.com/en/1.9/ref/models/instances/#customizing-model-loading
        if self._state.adding:

            oauth_token = self.OAUTH_TOKEN
            oauth_token_secret = self.OAUTH_TOKEN_SECRET

            auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                              CONSUMER_KEY, CONSUMER_SECRET)
            twitter_api = twitter.Twitter(auth=auth)
            response = twitter_api.account.verify_credentials()
            screen_name = response['screen_name']
            self.username = screen_name

            User = get_user_model()

            # Check if this is a pre-existing user
            returning_user = User.objects.filter(username=self.username)

            if returning_user:
                user = returning_user[0]
                tuser = user.twitteruser
                tuser.OAUTH_TOKEN = self.OAUTH_TOKEN
                tuser.OAUTH_TOKEN_SECRET = self.OAUTH_TOKEN_SECRET
                tuser.save()
                return

            # New user.
            # Setup a random password

            chars = string.ascii_letters + string.punctuation + string.digits + string.ascii_uppercase
            password = "".join(choice(chars) for x in range(randint(16, 26)))

            user = User.objects.create_user(
                    username=self.username,
                    password=password
                )
            self.user = user
        super(TwitterUser, self).save(*args, **kwargs)

    OAUTH_TOKEN = models.CharField(max_length=250, null=True, blank=True)
    OAUTH_TOKEN_SECRET = models.CharField(max_length=250, null=True, blank=True)

    username = models.CharField(max_length=250, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='cascade')


def oauth_twitter_login(request, user):
    """

    :param request:
    :param user:

    Gets user's tokens if available or redirects to Twitter API for complete -
    OAuth dance.

    If successful, returns authorized handle from Twitter.

    :return:
    """

    tokens = TwitterUser.objects.filter(
        username=user).values_list('OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET')
    oauth_token, oauth_token_secret = tokens[0][0], tokens[0][1]

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   CONSUMER_KEY, CONSUMER_SECRET)

    # Make sure user logs in to the dJango ecosystem as well.
    login(request, user)
    return twitter.Twitter(auth=auth)


# Get Twitter Streaming OAuth API
def oauth_twitter_streaming(user):
    tokens = TwitterUser.objects.filter(
        username=user).values_list('OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET')
    oauth_token, oauth_token_secret = tokens[0][0], tokens[0][1]

    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                   CONSUMER_KEY, CONSUMER_SECRET)

    return twitter.TwitterStream(auth=auth)
