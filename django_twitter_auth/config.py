# Twitter specific auth keys and URLs
# Never add this file to git 

# Twitter key and secret
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# This is where user's authorized token will be saved. Never add this file to git.
OAUTH_FILE = ''
# Twitter URL used to authorize the app.
OAUTH_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
# Callback URL, must be same as app settings in twitter developer portal.
OAUTH_CALLBACK = 'http://127.0.0.1:8000/twitter_oauth/helper'
# Where to go after authorization.
REDIRECT_URL_AFTER_AUTH = '/twitter_oauth/confirm'
