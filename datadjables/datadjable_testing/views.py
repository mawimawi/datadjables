import datetime
from django.utils.translation import ugettext as _

from datadjables.datadjable_testing.models import Person, Purchase, Product
from datadjables.views import DataDjable, ModelDataDjable
from datadjables.column import StringColumn, IntegerColumn, \
    DecimalColumn, NumberRangeColumn, ChoiceColumn, DateRangeColumn


class DPersons(ModelDataDjable):
    template_name = 'datadjable_testing/person_list.html'
    model = Person

    # "last_name" is being used for the lookup field
    last_name = StringColumn(
        coltitle=_('Name'),
        searchable=True, sortable=True,
        lookup_op='icontains',
        renderer=u'<b>{obj.last_name} {obj.first_name}</b>')
    first_name = StringColumn(coltitle=_('First name'))

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'),
        sortable=True, searchable=True)

    age = IntegerColumn(coltitle=_('Age'), sortable=False, searchable=False)

    zip = NumberRangeColumn(
        coltitle=_('Zip code'),
        searchable=True, sortable=True)

    class Meta:
        html_id = "personstable"
        show_tablefooter = True
        fulltext_search_columns = ['last_name', 'first_name']
        adjust_bottom_px = 90

    def render_to_response(self, *args, **kwargs):
        # generate the range for the datetime jqueryui popup
        # (can't be made in the colum definitions above, since "now" would
        # be evaluated in advance...

        this_year = datetime.date.today().year
        self._meta.columns[2].year_range = [this_year - 128, this_year]
        return super(DPersons, self).render_to_response(*args, **kwargs)


class DPersonsFilterTop(ModelDataDjable):
    template_name = 'datadjable_testing/personfiltertop_list.html'
    model = Person

    last_name = StringColumn(
        coltitle=_('Last name'),
        searchable=True, sortable=True, lookup_op='icontains',
        tag_selector='#f_last_name')
    first_name = StringColumn(coltitle=_('First name'),)

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), sortable=True, searchable=True,
        tag_selector='#f_birthdate')

    zip = NumberRangeColumn(
        coltitle=_('Zip code'),
        searchable=True, sortable=True, tag_selector='#f_zip')

    class Meta:
        html_id = "personsfiltertoptable"
        fulltext_search_columns = ['last_name', 'first_name']
        show_tablefooter = False


class DSimplePersons(ModelDataDjable):
    template_name = 'datadjable_testing/person_list.html'
    model = Person

    last_name = StringColumn(
        coltitle=_('Name'), searchable=True, sortable=True,
        lookup_op='icontains',
        renderer=u'<b>{obj.last_name} {obj.first_name}</b>',
        colwidth='90%')
    first_name = StringColumn(coltitle=_('First name'))

    birthdate = DateRangeColumn(
        coltitle=_('Date of birth'), sortable=True, searchable=True,
        colwidth='10%')

    age = IntegerColumn(coltitle=_('Age'), sortable=False, searchable=False)

    zip = NumberRangeColumn(
        coltitle=_('Zip code'), searchable=True, sortable=True)

    class Meta:
        columns = ('last_name', 'birthdate')


class DPurchases(DataDjable):
    template_name = 'datadjable_testing/purchase_list.html'

    buyer__last_name = StringColumn(
        coltitle=_('Buyer'),
        filter_label=_('Filter first/last name'),
        colwidth="30em",
        lookup_fields=('buyer__first_name',
                       'buyer__last_name'),
        searchable=True, sortable=True,
        renderer=u"{obj.buyer.last_name}")
    product__pk = ChoiceColumn(
        coltitle=_('Product'),
        filter_label=_('All products'),
        colwidth="*",
        choices=(),  # will be filled in render_to_response
        searchable=True, sortable=True,
        renderer=u"{obj.product.name}, {obj.product.pk}")
    purchase_year = ChoiceColumn(
        coltitle=_('Purchase year',),
        filter_label=_('All years'),
        colwidth="20em",
        selector="date_part('year', purchase_timestamp)::integer",
        choices=(),  # will be filled in render_to_response
        searchable=True, sortable=True)
    price = DecimalColumn(
        coltitle=_('Price'),
        colwidth="10em")

    class Meta:
        html_id = "purchasestable"

    def base_query(self, person_pk=None, *a, **k):
        query = Purchase.objects.all().select_related('buyer', 'product')

        return query

    def render_to_response(self, *args, **kwargs):
        # choices for product popup
        product_choices = Product.objects.distinct('pk', 'name')\
            .order_by('name', 'pk')
        choices = [[x.pk, x.short_name] for x in product_choices]
        self._meta.columns[1].choices = choices

        # choices for purchase year
        year_choices = Purchase.objects.values_list('purchase_timestamp',
                                                    flat=True)
        choices = list(set(x.year for x in year_choices))
        self._meta.columns[2].choices = choices

        return super(DPurchases, self).render_to_response(*args, **kwargs)
