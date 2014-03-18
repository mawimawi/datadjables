# encoding: utf-8
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext as _
from datadjables.datadjable_testing.views import DPersons
from datadjables import DataDjable
from datadjables.datadjable_testing.models import Person


class HtmlTest(TestCase):
    persons = DPersons()

    def get_json(self, url, dct={}, method="get"):
        getpost = getattr(self.client, method)
        resp = getpost(url, dct)
        return json.loads(resp.content)

    def test_missing_base_query(self):
        class DT(DataDjable):
            pass
        self.assertRaises(NotImplementedError, DT().base_query )

    def test_colnames(self):
        self.assertEqual(
            ' '.join([obj.colname for obj in self.persons._meta.columns]),
            'last_name first_name birthdate age zip')

    def test_ordering(self):
        self.assertEqual(self.persons.js_initial_ordering(), '[[0, "asc"]]')
        multipers = DPersons()
        multipers.ordering = ['-birthdate', '+first_name', 'last_name']
        self.assertEqual(multipers.js_initial_ordering(),
                         '[[2, "desc"], [1, "asc"], [0, "asc"]]')

    def test_js_data_columns(self):
        self.assertEqual(self.persons.js_data_columns(), u'[{"bSearchable": true, "bSortable": true, "sType": "string"},{"bSearchable": false, "bSortable": true, "sType": "string"},{"bSearchable": true, "bSortable": true, "sType": "date-range"},{"bSearchable": false, "bSortable": false, "sType": "numeric"},{"bSearchable": true, "bSortable": true, "sType": "number-range"}]')

    def test_thead(self):
        response = self.client.get(reverse('datadjable_testing_person_list'))
        strippedresponse = ''.join([x.strip() for x in response.content.decode('utf8').splitlines()])

        self.assertIn(u'<thead><tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr></thead>'.format(
            _('Name'), _('First name'), _('Date of birth'), _('Age'), _('Zip code')
            ), strippedresponse)

    def test_get_first_two_records(self):
        resp = self.get_json(reverse('datadjable_testing_person_list'),
                             {'iDisplayLength': 2, 'sEcho': '33'})
        self.assertEqual(len(resp['aaData']), 2)
        self.assertEqual(resp['iTotalRecords'], 500)
        self.assertEqual(resp['iTotalDisplayRecords'], 500)
        self.assertEqual(resp['sEcho'], '33')

    def test_sort_by_lastname_then_firstname(self):
        resp = self.get_json(reverse('datadjable_testing_person_list'),
                {'sEcho':'x', 'iDisplayLength': 7, 'iSortCol_0': 0,
                    'iSortCol_1': 1, 'iDisplayStart': 5, 'sSortDir_0': 'asc', 'sSortDir_1': 'desc', })
        self.assertEqual(resp['sEcho'], 'x')

        # we expect these records to receive:
        # Sushant|Alsheimer|570
        # Richard|Alsheimer|575
        # Mihaela|Altringer|291
        # Adamat|Altringer|371
        # Avşar|Arbegans|833
        # Auður-Borasha|Arbegans|857
        # Aloysius|Arbegans|172
        zipcodes = [u'570', u'575', u'291', u'371', u'833', u'857', u'172']
        respzipcodes = [x[4] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

    def test_filter(self):
        resp = self.get_json(reverse('datadjable_testing_person_list'),
                {'sEcho':'0', 'iDisplayLength': 10,
                    'iSortCol_0': 1,  # order by first_name
                    'cSortDir_0': 'asc', 'sSearch_1': '',
                    'sSearch_0': 'Arbegans', 'sSearch_2': '',
                    }
                )
        # we expect these records to receive:
        # Aloysius|Arbegans|172
        # Auður-Borasha|Arbegans|857
        # Avşar|Arbegans|833
        zipcodes = [u'172', u'857', u'833']
        respzipcodes = [x[4] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

        resp = self.get_json(reverse('datadjable_testing_person_list'),
                             {'sEcho':'0', 'iDisplayLength': 10,
                              'iSortCol_0': '0',  # order by first_name
                              'iSortingCols': '1',
                              'sSortDir_0': 'asc',
                              'sSearch_0': 'ar',
                              'sSearch_4': '1000~1015',
                              'sRangeSeparator': '~',
                              })
        # we expect these records to receive:
        # Barth Karine
        self.assertEqual(u'Karine', resp['aaData'][0][1])


    def test_full_search(self):
        resp = self.get_json(reverse('datadjable_testing_person_list'),
                             {'iDisplayLength': 10, 'sEcho':'0',
                              'iSortCol_0': 1,  # order by first_name
                              'cSortDir_0': 'asc',
                              'sSearch': 'osto',
                              })
        # we expect these records to receive:
        # Aliza|Jostock|545
        # Astolfo|Jostok|995
        # Hugues-Liana|Jostock|50
        # Ostoja|Weiland|649
        # Ruth|Jostock|391
        zipcodes = u'545 995 50 649 391'.split()
        respzipcodes = [x[4] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

    def test_date_range(self):
        resp = self.get_json(reverse('datadjable_testing_personfiltertop_list'),
                {'sSearch_0': 'b',
                 'sSearch_2': '1990-06-01~1990-08-04',
                 'sEcho':'0',
                 'iDisplayLength': 10,
                 })
        self.assertEqual(u'Biwer', resp['aaData'][0][0])
        assert resp[u'iTotalRecords'] == 1

    def test_date_invalid_date_range(self):
        resp = self.get_json(reverse('datadjable_testing_personfiltertop_list'),
                {'sSearch_2': '1990-06-01',
                 'sEcho':'0',
                 })
        assert resp[u'iTotalRecords'] == 500

    def test_date_invalid_number_range(self):
        resp = self.get_json(reverse('datadjable_testing_personfiltertop_list'),
                {'sSearch_3': '1',
                 'sEcho':'0',
                 })
        assert resp[u'iTotalRecords'] == 500

    def test_colwidth(self):
        resp = self.client.get(reverse('datadjable_testing_simpleperson_list'))
        dtobj = resp.context.get('dtobj')
        sWidth = json.loads(dtobj.js_data_columns())[0]['sWidth']
        assert sWidth == '90%'

