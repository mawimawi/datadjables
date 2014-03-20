Creating and Customizing a DataDjable
=====================================

Creating a DataDjable is very similar to creating a Django form or a Django model::

  from datadjables import DataDjable, StringColumn, DateColumn

  class MyDataTable(DataTable):
      myfirstcolumn = StringColumn(...)
      mysecondcolumn = DateColumn(...)

      class Meta:
          html_id = 'mydatatable'
          fulltext_search_columns = ('myfirstcolumn',)
          columns = ('myfirstcolumn',)
          show_tablefooter = False

The ``Meta`` class can contain these attributes:

* html_id (optional, default value: ``datadjable``): This string will be used in the html page to identify this specific datatable. Make sure that this string is unique in all datatables displayed on this page. (Usually you might create only one datatable per html page)

* fulltext_search_columns (optional): A tuple indicating all columns that shall be searched when a user enters text into the search field on the top right of the jQuery DataTable. If empty or not given, then all columns will be searched.

* columns (optional, default is to display all defined columns): If you would like to only display some columns, or in a different order than defined, use this tuple with all column names that should be displayed, in this order.

* ordering: A tuple in the form ``('-mylastcolumn', 'myfirstcolumn')``. This is the same syntax as for Django models, and is being used as ordering when initially showing the DataTable in the browser.

* show_tablefooter (default: True): a boolean whether to show the footer of the table. You might want not to display the footer if you use a ``tag_selector`` for your columns, or if you do not need the columnfilter at all.
