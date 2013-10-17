Customizing Columns
===================

THIS SECTION IS OUTDATED

There are three types of columns (derived from the jQuery plugin): StringColumn, DateColumn and DecimalColumn. Right now they don't really differ from each other, but maybe in a next version.

When initializing a Column object, you can specify these parameters::


  myCol = StringColumn(coltitle=u'', coltitle_plural=None, searchable=False,
                sortable=True, renderer=None,
                lookup_fields=(), lookup_op='icontains'):

* coltitle: The title in the column header
* coltitle_plural: used for searchable columns to display "Search in XXX" inside the input widget.
* searchable: if True, then the input widget in the footer will be displayed to make this column searchable.
* sortable: if True, then the column can be sorted in ascending and descending order.
* lookup_fields: if not empty, then the fields in the queryset will be searched with the specified lookup_op operator.
  Useful if you have a "fullname" column for looking up the search string in firstname and lastname fields.
* lookup_op: operator to do lookups. Can be e.g. ``lte``, ``startswith`` etc. See the field lookups in Djangos QuerySet reference.
