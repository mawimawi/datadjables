import operator
from .column import BaseDTColumn

class _DTMeta(object):
    pass


class MetaDataDjable(type):
    """A meta class for easier definition of DataDjable classes.
    Works similarily to Django's model meta classes."""
    def __init__(cls, name, bases, ns):
        cls._meta = _DTMeta()
        cls._meta.columns = []
        m = ns.get('Meta', object())

        # use only specific columns in the datadjable?
        if getattr(m, 'columns', None):
            for colname in m.columns:
                cls._meta.columns.append(ns[colname])
                cls._meta.columns[-1]._set_colname(colname)

        # use all columns in the order they were defined
        else:
            for colname in dir(cls):
                column = getattr(cls, colname)
                if isinstance(column, BaseDTColumn):
                    column._set_colname(colname)
                    cls._meta.columns.append(column)
            cls._meta.columns.sort(key=operator.attrgetter('_count'))

        # create index numbers for all our columns
        for idx, col in enumerate(cls._meta.columns):
            col.column_index = idx

        standard_ordering = cls._meta.columns and \
            [cls._meta.columns[0].colname, ] or []
        cls.ordering = getattr(m, 'ordering', standard_ordering)
        cls.html_id = getattr(m, 'html_id', 'datadjable')

        cls._meta.fulltext_search_columns = []

        # get the columns to search for. if not given, use all columns
        all_columns = getattr(cls._meta, 'columns', [])
        search_columnnames = getattr(
            m, 'fulltext_search_columns',
            [x.colname for x in cls._meta.columns])

        for f in search_columnnames:
            cls._meta.fulltext_search_columns.append(
                [x for x in all_columns if x.colname == f][0])

