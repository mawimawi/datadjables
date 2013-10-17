from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.template import Template
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views import generic

from datadjables.datadjable_testing.models import Person, Purchase, Product
from datadjables.views import DataDjable
from datadjables.column import StringColumn, DateColumn, IntegerColumn, \
        DecimalColumn, NumberRangeColumn, ChoiceColumn, DateRangeColumn

class DPersons(DataDjable):
    template_name = 'datadjable_testing/person_list.html'
    first_name = StringColumn(
        coltitle=_('First name'), coltitle_plural=_('First names'),
        searchable=True, sortable=True)
    last_name = ChoiceColumn(
        coltitle=_('Last name'), coltitle_plural=_('Last names'),
        searchable=True, sortable=True,
        choices=Person.objects.all().values_list(
            'last_name', flat=True).distinct().order_by('last_name')
        )
    zip = NumberRangeColumn(
        coltitle=_('Zip code'), coltitle_plural=_('Zip codes'),
        searchable=True, sortable=True)
    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), coltitle_plural=_('Dates of birth'),
        sortable=True, searchable=True)
    age = IntegerColumn(coltitle=_('Age'), coltitle_plural=_('Ages'),
                        sortable=False, searchable=False,
                        )
    full_name = StringColumn(
        coltitle=_('Full name'), coltitle_plural=_('Full names'),
        searchable=False, sortable=False,
        lookup_fields=('first_name', 'last_name'),
        lookup_op='endswith',
        renderer=u'<b>{obj.last_name} {obj.first_name}</b>',
    )

    class Meta:
        html_id = "personstable"
        fulltext_search_columns = 'first_name last_name'.split()

    def base_query(self, *a, **k):
        return Person.objects.all()


class DProducts(DataDjable):
    standard_price = DecimalColumn(searchable=True,
        coltitle=_('Std. price'),
        coltitle_plural=_("Std. prices"),
        renderer=Template('{{ obj.standard_price|floatformat:2 }}'),)
    name = StringColumn(searchable=True, coltitle=_('Name'),
        coltitle_plural=_("Names"), renderer=Template('{{ obj }}'))
    avg_price = DecimalColumn(
        coltitle=_('Avg. price'),
        coltitle_plural=_('Avg. prices'),
        renderer=Template('{{ obj.avg_price|floatformat:2 }}'),
        sortable=True,
        searchable=True)

    class Meta:
        html_id = 'productstable'
        columns = ('name', 'standard_price', 'avg_price')
        fulltext_search_columns = ('name',)

    def base_query(self, *a, **k):
        return Product.objects.all().annotate(avg_price=Avg('purchase__price'))


class DPurchases(DataDjable):
    buyer__last_name = StringColumn(
        coltitle=_('Buyer'), coltitle_plural=_("Buyers"),
        lookup_fields=('buyer__first_name',
                       'buyer__last_name'),
        renderer=get_template('datadjable_testing/person_table_cell.html'),
        searchable=True, sortable=True,)
    product__name = StringColumn(coltitle=_('Product'),
                                 coltitle_plural=_("Products"),
                                 searchable=True,
                                 sortable=True,
                                 renderer=u"{obj.product.name}",
                                 )
    purchase_timestamp = DateColumn(coltitle=_('Purchase date'),
                                    coltitle_plural=_('Purchase dates'))
    price = DecimalColumn(coltitle=_('Price'))

    # be careful! fields in a "extra" clause cannot be searched easily
    # due to Djangos ORM limitations
    price_wo_tax = DecimalColumn(
        coltitle=_('Price minux 20% tax'),
        searchable=False,
        renderer=Template('{{ obj.price_wo_tax|floatformat:2 }}'))

    class Meta:
        html_id = "purchasestable"
        fulltext_search_columns = ('buyer__last_name', 'product__name',
                                   'purchase_timestamp', 'price')

    def base_query(self, person_pk=None, *a, **k):
        # we can use this base_query also for a specific person!
        query = Purchase.objects.all().select_related()

        if person_pk:
            pers = get_object_or_404(Person, pk=person_pk)
            query = query.filter(buyer=pers)

        return query.extra(select={'price_wo_tax': 'price / 120 * 100'})


class DPersonPurchases(DPurchases):
    product__name = StringColumn(coltitle=_('Product'),
                                 coltitle_plural=_("Products"),
                                 searchable=True,
                                 sortable=True,
                                 renderer=u"{obj.product.name}",
                                 )
    purchase_timestamp = DateColumn(coltitle=_('Purchase date'),
                                    coltitle_plural=_('Purchase dates'))
    price = DecimalColumn(coltitle=_('Price'))

    class Meta:
        ordering = ('-product__name',)
        html_id = "perspurchtable"
        fulltext_search_columns = ('product__name',
                                   'purchase_timestamp', 'price')
