=====
Django Twitter Auth
=====

Django Twitter Auth is a simple Django plugin/app to add Twitter authentication and authorization.


Twitter setup
-------------

1. Got to https://developer.twitter.com/ and create a new app if you don't already have one.

2. Generate the keys and tokens and save them in config.py. CAUTION: Never add config.py to git.

3. Setup the callback URL in twitter app settings and save the same in config.py.


Quick Start
-----------

1. Add "django_twitter_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_twitter_auth',
    ]

2. Include the django_twitter_auth URLconf in your project urls.py like this::

    url('twitter_oauth/', include('django_twitter_auth.urls')),
    
3. Start the development server and visit http://127.0.0.1:8000/twitter_oauth/dance
   to get user's authorization.

5. Once the OAuth Dance is complete, page redirects to http://127.0.0.1:8000/twitter_oauth/confirm.
