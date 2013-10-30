# coding: utf-8
import itertools

from django.db.models import Q
from django.template import Template, Context

from .renderers import simple


class _OrQ(Q):
    """A Q object which uses OR instead of AND for combining multiple 
    lookup model fields in a datadjable column"""
    default = Q.OR


def _jsbool(prop):
    """quick and dirty conversion of a value into a javascript boolean"""
    return prop and 'true' or 'false'


class BaseDTColumn(object):
    """Superclass for all kinds of columns like StringColum, DateColumn etc."""
    _counter = itertools.count()
    coltype = None

    def __init__(self, colname=None, coltitle=u'',
                 searchable=False, sortable=True,
                 renderer=None, lookup_fields=(), lookup_op='icontains',
                 colwidth="", selector=None):
        self.colname = colname
        self.coltitle = coltitle
        self.searchable = searchable
        self.sortable = sortable
        self.renderer = renderer
        self.lookup_fields = lookup_fields
        self.colwidth = colwidth
        self._count = BaseDTColumn._counter.next()
        self.lookup_op = lookup_op and '__%s' % lookup_op or ''
        self.selector = selector or None

    def _set_colname(self, colname):
        """Set the column name and - if necessary - renderer. This method
        is being used by MetaDataDjable when creating a new DataDjable class"""
        self.colname = colname
        self.renderer = self.renderer or simple(colname=colname)

    def js_data_column(self):
        result = []
        if self.colwidth:
            result.append('"sWidth": "%s"' % self.colwidth)
        result.append('"bSearchable": %s, "bSortable": %s, "sType": "%s"' % (
            _jsbool(self.searchable),
            _jsbool(self.sortable),
            self.coltype,))
        return '{' + ', '.join(result) + '}'

    def dt_cell_content(self, obj):
        """Returns the html content for current column of the current object"""
        if isinstance(self.renderer, Template):
            return self.renderer.render(Context({'obj': obj}))
        return self.renderer.format(obj=obj)  # must be a string or unicode

    def filter(self, strg, queryset=None):
        if self.selector:
            return queryset.extra(where=[self.selector + '=%s'],
                    params=[strg])
        kwargs = dict([
            ('%s%s' % (lookup_field, self.lookup_op), strg)
            for lookup_field in self.lookup_fields or [self.colname, ]
        ])
        return queryset.filter(_OrQ(**kwargs))

    def js_columnfilter_init(self):
        if self.searchable:
            return {'type': self.coltype}
        else:
            return None


class NumberRangeColumn(BaseDTColumn):
    coltype = 'number-range'

    def js_columnfilter_init(self):
        return {'type': self.coltype}

    def filter(self, strg, queryset=None):
        if '~' not in strg:
            return None
        parts = strg.split('~')
        kwargs = {}
        if parts[0]:
            kwargs.update(dict([
                ('%s__gte' % lookup_field, parts[0])
                for lookup_field in self.lookup_fields or [self.colname, ]
            ]))
        if parts[1]:
            kwargs.update(dict([
                ('%s__lte' % lookup_field, parts[1])
                for lookup_field in self.lookup_fields or [self.colname, ]
            ]))
        return queryset.filter(Q(**kwargs))



class StringColumn(BaseDTColumn):
    coltype = 'string'


class IntegerColumn(BaseDTColumn):
    coltype = 'numeric'


class DecimalColumn(BaseDTColumn):
    coltype = 'numeric'


class DateColumn(BaseDTColumn):
    coltype = 'date'


class DateRangeColumn(BaseDTColumn):
    coltype = 'date-range'

    def js_columnfilter_init(self):
        return {'type': self.coltype}

    def filter(self, strg, queryset=None):
        if '~' not in strg:
            return None
        parts = strg.split('~')
        kwargs = {}
        if parts[0]:
            kwargs.update(dict([
                ('%s__gte' % lookup_field, parts[0])
                for lookup_field in self.lookup_fields or [self.colname, ]
            ]))
        if parts[1]:
            kwargs.update(dict([
                ('%s__lte' % lookup_field, parts[1])
                for lookup_field in self.lookup_fields or [self.colname, ]
            ]))
        return queryset.filter(Q(**kwargs))

class ChoiceColumn(BaseDTColumn):
    coltype = 'select'

    def __init__(self, choices=(), lookup_op=None, *a, **k):
        super(ChoiceColumn, self).__init__(lookup_op='', *a, **k)
        self.choices = choices

    def js_columnfilter_init(self):
        values = list(self.choices)
        return {'type': 'select', 'values':values}


