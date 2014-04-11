DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'foo bar baz qux quu2x qUUU3x'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datadjables_testing',
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

LANGUAGE_CODE = 'de'
LANGUAGES = (
    ('de', 'Deutsch'),
    ('en', 'English'),
)

USE_I18N = True
USE_L10N = True
