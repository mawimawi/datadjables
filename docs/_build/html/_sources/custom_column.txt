Customizing Columns
===================

There are a couple of types of columns (derived from the jQuery plugin):
StringColumn, DateColumn and DecimalColumn. Furthermore we have the following special columns, thanks to the Datatables-Column Plugin: NumberRangeColumn, DateRangeColumn and ChoiceColumn.

When initializing a Column object, you can specify these parameters::

  myCol = StringColumn(self, colname=None, coltitle=u'',
                 searchable=False, sortable=True,
                 renderer=None, lookup_fields=(), lookup_op='icontains',
                 colwidth='', selector=None, tag_selector=None):

* colname: The internal name of the column according to model's fieldname. Usually you might not want to set this parameter, but instead name the property `myCol` itself to match the model's fieldname.

* coltitle: The title in the column header

* searchable: if True, then the input widget in the footer will be displayed to make this column searchable.

* sortable: if True, then the column can be sorted in ascending and descending order by clicking on the little arrows in the column's header.

* renderer: when set to `None`, the value of the model's field will be used as-is. Otherwise you can specify a Django template string which will be rendered.

* lookup_fields: if not empty, then the specified model fields will be searched with the specified lookup_op operator. A good example might be to use a column `fullname` which looks up the database fields `first_name` and `last_name`.

* lookup_op: operator to do lookups. Can be e.g. ``lte``, ``startswith`` etc. See the field lookups in Djangos QuerySet reference.
* colwidth: A CSS value for specifying the width of the column. e.g. `90px` or `10em`.

* selector: useful for a computed field like the number of comments for an article. In this case `selector` might be something like ``(SELECT COUNT(*) from article_comments ac WHERE articles_article.id = ac.article_id)``

* tag_selector: If you want to position the column's filter not in the table's footer, but somewhere else, this can be the html-id of the tag where the input field should be placed. Example: `#filter_mycol`.

Columns with choices
--------------------

A ``ChoiceColumn`` has an additional parameter when instantiating:

* choices: per default an empty tuple, but it should be popuplated with some iterable consisting of tuples. E.g. ``[('g', 'Girl'), ('b', 'Boy')]``. Of course this can also be something like ``SomeModel.objects.all().values_list('id', 'name')``.
