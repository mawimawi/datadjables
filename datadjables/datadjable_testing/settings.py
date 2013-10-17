DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'foo bar baz qux quu2x qUUU3x'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'datadjables.sqlite.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'datadjables',
    'datadjables.datadjable_testing',
)

STATIC_URL = '/static/'
STATIC_ROOT = './static/'
ROOT_URLCONF = 'datadjables.datadjable_testing.urls'

