DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'foo bar baz qux quu2x qUUU3x'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'datadjables.sqlite.db',
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'datadjables',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'datadjables',
    'datadjables.datadjable_testing',
)

STATIC_URL = '/static/'
STATIC_ROOT = './static/'
ROOT_URLCONF = 'datadjables.datadjable_testing.urls'

