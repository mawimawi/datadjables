Creating and Customizing a DataDjable
=====================================

THIS SECITON IS OUTDATED! 

Creating a DataDjable is very similar to creating a Django form or a Django model::

  from datadjables import DataDjable

  class MyDataTable(DataTable):
      myfirstcolumn = StringColumn(...)
      mysecondcolumn = DateColumn(...)

      class Meta:
          ajax_urlname = 'mydatatable_ajax'
          base_query = MyModel.objects.all()  # must return the columns defined above
          html_id = 'mydatatable'
          fulltext_search_columns = ('myfirstcolumn',)

The ``Meta`` class can contain these attributes:

* ajax_urlname (required): The named url for returning the json code of your data. This string must be usable with the ``{% url %}`` template tag.

* base_query (required): A Queryset instance for retrieving all data that you'd like to return.

* html_id (required): This string will be used in the html page to identify this specific datatable. Make sure that this string is unique in all datatables displayed on this page. (Usually you might create only one datatable per html page)

* fulltext_search_columns (optional): A tuple indicating all columns that shall be searched when a user enters text into the search field on the top right of the jQuery DataTable. If empty or not given, then all columns will be searched.

* columns (optional): If you would like to only display some fields, or in a different order than defined, use this tuple with all column names that should be displayed, in this order.

* ordering: A tuple in the form ``('-mylastcolumn', 'myfirstcolumn')``. This is the same syntax as for Django models, and is being used as ordering when initially showing the DataTable in the browser.
