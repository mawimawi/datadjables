# encoding: utf-8
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from datatables.dt_testing.views import DtPersons, DtProducts
from datatables import DataTable
from datatables.dt_testing.models import Person


class HtmlTest(TestCase):
    persons = DtPersons()
    products = DtProducts()

    def get_json(self, url, dct={}, method="get"):
        getpost = getattr(self.client, method)
        resp = getpost(url, dct)
        return json.loads(resp.content)

    def test_00_missing_base_query(self):
        class DT(DataTable):
            pass
        self.assertRaises(NotImplementedError, DT().view, [{}])

    def test_01_colnames(self):
        self.assertEqual(
            ' '.join([obj.colname for obj in self.persons._meta.columns]),
            'first_name last_name zip birthdate age full_name')
        self.assertEqual(
            ' '.join([obj.colname for obj in self.products._meta.columns]),
            'name standard_price avg_price')

    def test_01a_ordering(self):
        self.assertEqual(self.persons.get_ordering(), '[[0, "asc"]]')
        self.assertEqual(self.products.get_ordering(), '[[0, "asc"]]')
        multipers = DtPersons()
        multipers.ordering = ['-zip', '+last_name', 'first_name']
        self.assertEqual(multipers.get_ordering(),
                         '[[2, "desc"], [1, "asc"], [0, "asc"]]')

    def test_02_jscode(self):
        self.assertEqual(self.persons.js(), u'[{"bSearchable": true, "bSortable": true, "sType": "string"},{"bSearchable": true, "bSortable": true, "sType": "string"},{"bSearchable": true, "bSortable": true, "sType": "string"},{"bSearchable": false, "bSortable": true, "sType": "string"},{"bSearchable": false, "bSortable": false, "sType": "string"},{"bSearchable": true, "bSortable": false, "sType": "string"}]')
        self.assertEqual(self.products.js(), u'[{"bSearchable": false, "bSortable": true, "sType": "string"},{"bSearchable": false, "bSortable": true, "sType": "string"},{"bSearchable": true, "bSortable": true, "sType": "string"}]')

    def test_03_thead_tfoot(self):
        response = self.client.get(reverse('dt_testing_person_list'))
        self.assertIn(u'<th>First name</th><th>Last name</th><th>Zip code</th><th>Date of birth</th><th>Age</th><th>Full name</th>',
                      response.content.decode('utf8'))
        self.assertIn(u'<th><input type="text" value="" style="width:15em" name="search_first_name"></th><th><input type="text" value="" style="width:15em" name="search_last_name"></th><th><input type="text" value="" style="width:15em" name="search_zip"></th><th><input style="display:none">&nbsp;</th><th><input style="display:none">&nbsp;</th><th><input type="text" value="" style="width:15em" name="search_full_name"></th>',
                response.content.decode('utf8'))

        response = self.client.get(reverse('dt_testing_product_list'))
        self.assertIn(u'<th>Name</th>',
                      response.content.decode('utf8'))
        self.assertIn(u'<th><input style="display:none">&nbsp;</th>',
                      response.content.decode('utf8'))

        response = self.client.get(reverse('dt_testing_purchase_list'))
        self.assertIn(u'<th>Buyer</th><th>Product</th><th>Purchase date</th><th>Price</th><th>Price minux 20% tax</th>',
                      response.content.decode('utf8'))
        self.assertIn(u'<tr><th><input type="text" value="" style="width:15em" name="search_buyer__last_name"></th><th><input type="text" value="" style="width:15em" name="search_product__name"></th><th><input style="display:none">&nbsp;</th><th><input style="display:none">&nbsp;</th><th><input style="display:none">&nbsp;</th></tr>',
                response.content.decode('utf8'))

    def test_04_get_first_two_records(self):
        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 2, 'sEcho': '33'})
        self.assertEqual(len(resp['aaData']), 2)
        self.assertEqual(resp['iTotalRecords'], 500)
        self.assertEqual(resp['iTotalDisplayRecords'], 500)
        self.assertEqual(resp['sEcho'], '33')

        resp = self.get_json(reverse('dt_testing_product_list_ajax'),
                             {'iDisplayLength': 2, 'sEcho': '33'})
        self.assertEqual(len(resp['aaData']), 2)
        self.assertEqual(resp['iTotalRecords'], 40)
        self.assertEqual(resp['iTotalDisplayRecords'], 40)
        self.assertEqual(resp['sEcho'], '33')

        resp = self.get_json(reverse('dt_testing_purchase_list_ajax'),
                             {'iDisplayLength': 2, 'sEcho': '33'})
        self.assertEqual(len(resp['aaData']), 2)
        self.assertEqual(resp['iTotalRecords'], 2000)
        self.assertEqual(resp['iTotalDisplayRecords'], 2000)
        self.assertEqual(resp['sEcho'], '33')

    def test_05_sort_by_lastname_then_firstname(self):
        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 7, 'iSortCol_0': 1,
                              'iSortCol_1': 0, 'iDisplayStart': 5,
                              'sSortDir_0': 'asc', 'sSortDir_1': 'desc', })
        self.assertEqual(resp['sEcho'], '0')

        # we expect these records to receive:
        # Sushant|Alsheimer|570
        # Richard|Alsheimer|575
        # Mihaela|Altringer|291
        # Adamat|Altringer|371
        # Avşar|Arbegans|833
        # Auður-Borasha|Arbegans|857
        # Aloysius|Arbegans|172
        zipcodes = [u'570', u'575', u'291', u'371', u'833', u'857', u'172']
        respzipcodes = [x[2] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

    def test_06_filter(self):
        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 10,
                              'iSortCol_0': 0,  # order by first_name
                              'cSortDir_0': 'asc',
                              'sSearch_0': '',
                              'sSearch_1': 'Arbegans',
                              'sSearch_2': '',
                              })
        # we expect these records to receive:
        # Aloysius|Arbegans|172
        # Auður-Borasha|Arbegans|857
        # Avşar|Arbegans|833
        zipcodes = [u'172', u'857', u'833']
        respzipcodes = [x[2] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 10,
                              'iSortCol_0': 0,  # order by first_name
                              'cSortDir_0': 'asc',
                              'sSearch_0': 'alo',
                              'sSearch_1': 'a',
                              'sSearch_2': '',
                              })
        # we expect these records to receive:
        # Aloysius|Arbegans|172
        zipcodes = [u'172', ]
        respzipcodes = [x[2] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

        # search with lookup_fields and lookup_op
        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 10,
                              'iSortCol_0': 0,  # order by first_name
                              'cSortDir_0': 'asc',
                              'sSearch_5': 'ter',
                              })
        # we expect these records to receive:
        # Anas|Ritter|607
        # Arife-Kester|Herber|506
        # Bertrando-Fernand|Poppelreiter|318
        # Bukureza|Poppelreiter|849
        # Burkhardt-Lester|Otto|130
        # Olivera|Lichter|894
        zipcodes = u'607 506 318 849 130 894'.split()
        respzipcodes = [x[2] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

    def test_06_full_search(self):
        resp = self.get_json(reverse('dt_testing_person_list_ajax'),
                             {'iDisplayLength': 10,
                              'iSortCol_0': 0,  # order by first_name
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
        respzipcodes = [x[2] for x in resp['aaData']]
        self.assertListEqual(respzipcodes, zipcodes)

    def test_07_related_fields(self):
        resp = self.get_json(reverse('dt_testing_purchase_list_ajax'),
                             {'iDisplayLength': 10,
                              'iSortCol_0': 2,  # order by purchase timestamp
                              'cSortDir_0': 'asc',
                              'sSearch': 'illard',
                              })
        first_record = [u'<a href="/persons/462/">Millard Gojar</a>\n',
                        u'As the lion, we moest ons have sigilp',
                        u'Feb. 9, 1933, 11 p.m.',
                        u'2273.77',
                        u'1894.81']
        self.assertListEqual(resp['aaData'][0], first_record)

    def test_08_limited_queryset(self):
        pers = Person.objects.get(pk=429)  # Richard Alsheimer
        response = self.client.get(reverse('dt_testing_person_purchase_list', args=[pers.pk]))
        self.assertIn(u'<th>Buyer</th><th>Price minux 20% tax</th><th>Product</th><th>Purchase date</th><th>Price</th>',
                      response.content.decode('utf8'))
        self.assertIn(u'<th><input type="text" value="" style="width:15em" name="search_buyer__last_name"></th><th><input style="display:none">&nbsp;</th><th><input type="text" value="" style="width:15em" name="search_product__name"></th><th><input style="display:none">&nbsp;</th><th><input style="display:none">&nbsp;</th></tr>',
                response.content.decode('utf8'))

        resp = self.get_json(reverse('dt_testing_person_purchase_list_ajax',
                                     args=[pers.pk]))
        self.assertEqual(len(resp['aaData']), 13)
        self.assertEqual(resp['iTotalRecords'], 13)
        self.assertEqual(resp['iTotalDisplayRecords'], 13)
