from django.conf.urls import patterns, url
from django.views.generic import TemplateView, DetailView
from .models import Person
from django.conf import settings
from datadjables.datadjable_testing.views import DPersons, DPersonsFilterTop, \
    DSimplePersons, DPurchases

urlpatterns = patterns(
    '',
    url(r'^$',
        TemplateView.as_view(template_name='datadjable_testing/index.html'),
        name='datadjable_testing_index'),

    url(r'^persons/$',
        DPersons.as_view(),
        name='datadjable_testing_person_list'),
    url(r'^persons/(?P<pk>\d+)/$', DetailView.as_view(
        model=Person, template_name='datadjable_testing/person_detail.html'),
        name='datadjable_testing_person_detail'),

    url(r'^personsfiltertop/$', DPersonsFilterTop.as_view(),
        name='datadjable_testing_personfiltertop_list'),

    url(r'^simplepersons/$', DSimplePersons.as_view(),
        name='datadjable_testing_simpleperson_list'),

    url(r'^purchases/$', DPurchases.as_view(),
        name='datadjable_testing_purchases_list'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT}),
)
