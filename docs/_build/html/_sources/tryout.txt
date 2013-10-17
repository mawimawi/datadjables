Give it a try!
==============

THIS SECTION IS OUTDATED

DataDjables has a ready-to-use demo application built in. For a quick try do the following:

Create a new Django project::

  django-admin startproject mydatatables

copy the datatables directory into the project directory

Make sure that your settings file has the following configured::

  USE_TZ = False  # Only important for this demo project and for running the unit tests

Use a database backend which you like or just sqlite3::
  
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': 'datatabletest.db',
          'USER': '',
          'PASSWORD': '',
          'HOST': '',
          'PORT': '',
      }
  }

Add these apps to your INSTALLED_APPS::

  INSTALLED_APPS = (
      [...]
      'datatables',
      'datatables.dt_testing',
  )

Include the datatables.dt_testing urls into your urls.py::

  from django.conf.urls import patterns, url, include
  
  urlpatterns = patterns( '',
      url(r'^dt_testing/', include('datatables.dt_testing.urls')),
  )

Run a ``manage.py syncdb`` to create some pre-filled testing tables, then start your development server with ``manage.py runserver``.

Finally go to http://localhost:8000/dt_testing/ and try the three different datatables in your browser.
