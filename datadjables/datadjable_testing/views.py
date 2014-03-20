from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.template import Template
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views import generic

from datadjables.datadjable_testing.models import Person, Purchase, Product
from datadjables.views import DataDjable, ModelDataDjable
from datadjables.column import StringColumn, DateColumn, IntegerColumn, \
        DecimalColumn, NumberRangeColumn, ChoiceColumn, DateRangeColumn

class DPersons(ModelDataDjable):
    template_name = 'datadjable_testing/person_list.html'
    model = Person

    # "last_name" is being used for the lookup field
    last_name = StringColumn(coltitle=_('Name'),
        searchable=True, sortable=True,
        lookup_op='icontains',
        renderer=u'<b>{obj.last_name} {obj.first_name}</b>')
    first_name = StringColumn(coltitle=_('First name'),
            )

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), sortable=True, searchable=True)

    age = IntegerColumn(coltitle=_('Age'), sortable=False, searchable=False)

    zip = NumberRangeColumn(coltitle=_('Zip code'),
            searchable=True, sortable=True)

    class Meta:
        html_id = "personstable"
        fulltext_search_columns = ['last_name','first_name']


class DPersonsFilterTop(ModelDataDjable):
    template_name = 'datadjable_testing/personfiltertop_list.html'
    model = Person

    last_name = StringColumn(coltitle=_('Last name'),
        searchable=True, sortable=True, lookup_op='icontains',
        tag_selector = '#f_last_name')
    first_name = StringColumn(coltitle=_('First name'),)

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), sortable=True, searchable=True,
        tag_selector='#f_birthdate')

    zip = NumberRangeColumn(coltitle=_('Zip code'),
            searchable=True, sortable=True, tag_selector='#f_zip')

    class Meta:
        html_id = "personsfiltertoptable"
        fulltext_search_columns = ['last_name','first_name']
        show_tablefooter = True

class DSimplePersons(ModelDataDjable):
    template_name = 'datadjable_testing/person_list.html'
    model = Person

    last_name = StringColumn(coltitle=_('Name'),
        searchable=True, sortable=True,
        lookup_op='icontains',
        renderer=u'<b>{obj.last_name} {obj.first_name}</b>',
        colwidth='90%')
    first_name = StringColumn(coltitle=_('First name'),
            )

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), sortable=True, searchable=True,
        colwidth='10%')

    age = IntegerColumn(coltitle=_('Age'), sortable=False, searchable=False)

    zip = NumberRangeColumn(coltitle=_('Zip code'),
            searchable=True, sortable=True)


    class Meta:
        columns = ('last_name', 'birthdate')

##### class DProducts(DataDjable):
#####     name = StringColumn(searchable=True, coltitle=_('Name'),
#####         renderer=Template('{{ obj }}'))
#####     standard_price = DecimalColumn(searchable=True,
#####         coltitle=_('Std. price'),
#####         renderer=Template('{{ obj.standard_price|floatformat:2 }}'),)
#####     avg_price = DecimalColumn(
#####         coltitle=_('Avg. price'),
#####         renderer=Template('{{ obj.avg_price|floatformat:2 }}'),
#####         sortable=True,
#####         searchable=True)
##### 
#####     class Meta:
#####         html_id = 'productstable'
#####         columns = ('name', 'standard_price', 'avg_price')
#####         fulltext_search_columns = ('name',)
##### 
#####     def base_query(self, *a, **k):
#####         return Product.objects.all().annotate(avg_price=Avg('purchase__price'))
##### 
##### 
##### class DPurchases(DataDjable):
#####     buyer__last_name = StringColumn(
#####         coltitle=_('Buyer'),
#####         lookup_fields=('buyer__first_name',
#####                        'buyer__last_name'),
#####         renderer=get_template('datadjable_testing/person_table_cell.html'),
#####         searchable=True, sortable=True,)
#####     product__name = StringColumn(coltitle=_('Product'),
#####                                  searchable=True,
#####                                  sortable=True,
#####                                  renderer=u"{obj.product.name}",
#####                                  )
#####     purchase_timestamp = DateColumn(coltitle=_('Purchase date'))
#####     price = DecimalColumn(coltitle=_('Price'))
##### 
#####     # be careful! fields in a "extra" clause cannot be searched easily
#####     # due to Djangos ORM limitations
#####     price_wo_tax = DecimalColumn(
#####         coltitle=_('Price minux 20% tax'),
#####         searchable=False,
#####         renderer=Template('{{ obj.price_wo_tax|floatformat:2 }}'))
##### 
#####     class Meta:
#####         html_id = "purchasestable"
#####         fulltext_search_columns = ('buyer__last_name', 'product__name',
#####                                    'purchase_timestamp', 'price')
##### 
#####     def base_query(self, person_pk=None, *a, **k):
#####         # we can use this base_query also for a specific person!
#####         query = Purchase.objects.all().select_related()
##### 
#####         if person_pk:
#####             pers = get_object_or_404(Person, pk=person_pk)
#####             query = query.filter(buyer=pers)
##### 
#####         return query.extra(select={'price_wo_tax': 'price / 120 * 100'})
##### 
##### 
##### class DPersonPurchases(DPurchases):
#####     product__name = StringColumn(coltitle=_('Product'),
#####                                  searchable=True,
#####                                  sortable=True,
#####                                  renderer=u"{obj.product.name}",
#####                                  )
#####     purchase_timestamp = DateColumn(coltitle=_('Purchase date'))
#####     price = DecimalColumn(coltitle=_('Price'))
##### 
#####     class Meta:
#####         ordering = ('-product__name',)
#####         html_id = "perspurchtable"
#####         fulltext_search_columns = ('product__name',
#####                                    'purchase_timestamp', 'price')
