# encoding: utf-8
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from datadjables.datadjable_testing.views import DPersons
from datadjables import DataDjable
from datadjables.datadjable_testing.models import Person


class HtmlTest(TestCase):
    persons = DPersons()
#    products = DtProducts()

    def get_json(self, url, dct={}, method="get"):
        getpost = getattr(self.client, method)
        resp = getpost(url, dct)
        return json.loads(resp.content)

    def test_00_missing_base_query(self):
        class DT(DataDjable):
            pass
        self.assertRaises(NotImplementedError, DT().base_query )

    def test_01_colnames(self):
        self.assertEqual(
            ' '.join([obj.colname for obj in self.persons._meta.columns]),
            'last_name first_name birthdate age zip')

    def test_01a_ordering(self):
        self.assertEqual(self.persons.js_initial_ordering(), '[[0, "asc"]]')
        multipers = DPersons()
        multipers.ordering = ['-birthdate', '+first_name', 'last_name']
        self.assertEqual(multipers.js_initial_ordering(),
                         '[[2, "desc"], [1, "asc"], [0, "asc"]]')

    def test_02_js_data_columns(self):
        self.assertEqual(self.persons.js_data_columns(), u'[{"bSearchable": true, "bSortable": true, "sType": "string"},{"bSearchable": false, "bSortable": true, "sType": "string"},{"bSearchable": true, "bSortable": true, "sType": "date-range"},{"bSearchable": false, "bSortable": false, "sType": "numeric"},{"bSearchable": true, "bSortable": true, "sType": "number-range"}]')

    def test_03_thead(self):
        response = self.client.get(reverse('datadjable_testing_person_list'))
        strippedresponse = ''.join([x.strip() for x in response.content.decode('utf8').splitlines()])

        self.assertIn(u'<thead><tr><th>Name</th><th>First name</th><th>Date of birth</th><th>Age</th><th>Zip code</th></tr></thead>',
                      strippedresponse)

    def test_04_get_first_two_records(self):
        resp = self.get_json(reverse('datadjable_testing_person_list'),
                             {'iDisplayLength': 2, 'sEcho': '33'})
        self.assertEqual(len(resp['aaData']), 2)
        self.assertEqual(resp['iTotalRecords'], 500)
        self.assertEqual(resp['iTotalDisplayRecords'], 500)
        self.assertEqual(resp['sEcho'], '33')

    def test_05_sort_by_lastname_then_firstname(self):
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

    def test_06_filter(self):
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


    def test_06_full_search(self):
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

