# coding: utf-8
from json import dumps

from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from .internals import MetaDataDjable

class DataDjable(TemplateView):
    __metaclass__ = MetaDataDjable

    def __init__(self, max_rows_per_batch=500):
        self.max_rows_per_batch = max_rows_per_batch

    def thead(self):
        """Renders the table header as HTML"""
        return mark_safe('<th>' + '</th><th>'.join(
            [obj.coltitle for obj in self._meta.columns]) + '</th>')

    def js_get_ordering(self):
        """Returns the default ordering of the DataDjable in a format
        that jQuery-DataTables understands."""
        orderarray = []
        for idx, strg in enumerate(self.ordering):
            if strg.startswith('-'):
                order = 'desc'
            else:
                order = 'asc'
            # cleanup strg
            strg = strg.split('-')[-1]
            strg = strg.split('+')[-1]

            orderarray.append((self._meta.colnames.index(strg), order))

        return dumps(orderarray)

    def js_data_columns(self):
        """Creates the javascript list of objects for initialization of 
        the jQuery-DataTable"""
        return mark_safe('[' +
                         ','.join([obj.js_data_column() for obj in self._meta.columns]) +
                         ']')

    def result_data(self, queryset):
        """Returns a list of rows to be shown in the jQuery-DataTable tbody"""
        return [self.get_row(obj) for obj in queryset]

    def get_row(self, queryset_row):
        """Returns one row to be shown in the jQuery-DataTable tbody"""
        return [x.dt_cell_content(queryset_row) for x in self._meta.columns]

    def js_columnfilter_init(self):
        """Returns the initialization JavaScript list for the
        jQuery-DataTable.columnfilter plugin"""
        result = [x.js_columnfilter_init() for x in self._meta.columns]
        return mark_safe(dumps(result))

    def sort_queryset(self, queryset, request):
        ordering = []
        for sortcol in range(len(self._meta.columns)):
            colnum = int(request.GET.get('iSortCol_%s' % sortcol, -1))
            if colnum > -1 and self._meta.columns[colnum].sortable:
                prefix = ''
                if request.GET.get('sSortDir_%s' % sortcol) == 'desc':
                    prefix = '-'
                ordering.append(
                    '%s%s' % (
                        prefix,
                        self._meta.columns[colnum].colname
                    ))
        return queryset.order_by(*ordering)

    def filter_by_columns(self, queryset, request):
        for colnum in range(len(self._meta.columns)):
            expr = request.GET.get('sSearch_%s' % colnum, '').encode('utf-8')
            column = self._meta.columns[colnum]
            if expr and column.searchable:
                queryset = column.filter(expr, queryset=queryset)
        return queryset

    def filter_fulltext(self, queryset, request):
        """global search over all "fulltext_search_columns" """
        expr = request.GET.get('sSearch', '').encode('utf-8')
        if expr:
            q = None
            for column in self._meta.fulltext_search_columns:
                q = q | column.filter(expr) if q else column.filter(expr)
            return queryset.filter(q)
        return queryset

    def base_query(self, *args, **kwargs):
        raise NotImplementedError(
            "You need to define a base_query method which returns a QuerySet")

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax_response(request, *args, **kwargs)
        else:
            return super(DataDjable, self).get(request, dtobj=self, *args, **kwargs)
    
    def ajax_response(self, request, *args, **kwargs):
        # check for weird input
        queryset = self.base_query(request=request, *args, **kwargs)
        echo = request.GET.get('sEcho', '0')  # needed by datatables.js

        # return max. 'self.max_rows_per_batch' rows
        length = min(int(request.GET.get('iDisplayLength', 50)),
                self.max_rows_per_batch)

        start = int(request.GET.get('iDisplayStart', 0))
        end = start + length

        # filter by all fulltext_search_columns
        queryset = self.filter_fulltext(queryset, request)

        # filter by individual columns
        queryset = self.filter_by_columns(queryset, request)

        # do the sorting
        queryset = self.sort_queryset(queryset, request)

        # how many records are there?
        total_records = total_display_records = queryset.count()

        # slice it
        queryset = queryset[start:end]

        # return the finished queryset
        jsonString = dumps({'sEcho': echo,
                            'iTotalRecords': total_records,
                            'iTotalDisplayRecords': total_display_records,
                            'aaData': self.result_data(queryset)}
                           )
        response = HttpResponse(jsonString, mimetype="application/javascript")

        add_never_cache_headers(response)
        return response
