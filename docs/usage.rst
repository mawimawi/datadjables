Usage overview
==============

THIS SECTION IS OUTDATED


Suppose we have three models: ``Person``, ``Product`` and ``Purchase``. A person buys some product for a price that may be different from the ``standard_price`` stored in the ``Product`` model. This price is stored in a ``Purchase`` object which also contains the timestamp of the sale. This setup is identical to the ``datadjable_testing`` app inside the ``datatables`` django app.

The heart of every DataDjable is a queryset like ``Product.objects.all()``. Of course this base_query can be something more complicated like ``Product.objects.all().select_related().annotate(avg_price=Avg('purchase__price'))``.

The data being displayed in your browser can hold any information that your queryset offers. An example would be::

  class DtProducts(DataDjable):
      template_name = 'datadjable_testing/product_list.html'

      standard_price = DecimalColumn(
          coltitle=_('Std. price'),
          renderer=Template('{{ obj.standard_price|floatformat:2 }}'),)
      name = StringColumn(coltitle=_('Name'))
      avg_price = DecimalColumn(
          coltitle=_('Avg. price'),
          renderer=Template('{{ obj.avg_price|floatformat:2 }}'),
          sortable=True,
          searchable=True)

      class Meta:
          base_query = Product.objects.all().annotate(avg_price=Avg('purchase__price'))

This specific datadjable consists of three columns ``standard_price``, ``name`` and ``avg_price`` (which the queryset creates using the ``annotate`` method).

This is a view that shows a html page with the required JavaScript code and a <table> which contains information to render the datadjable in the browser::

  {% load datatables %}<html>
      <head>
        <script type="text/javascript" src="/static/datadjables/js/jquery.js"></script>
        <script type="text/javascript" src="/static/datadjables/js/jquery-ui-1.10.3.custom.min.js"></script>
        <script type="text/javascript" src="/static/datadjables/js/jquery.dataTables.js"></script>
        <script type="text/javascript" src="/static/datadjables/js/jquery.dataTables.columnFilter.js"></script>
        <script type="text/javascript" src="/static/datadjables/js/datadjables.js"></script>
        <link rel="stylesheet" href="/static/datadjables/css/jquery.dataTables.css">
        <link rel="stylesheet" href="/static/datadjables/css/ui-lightness/jquery-ui-1.10.3.custom.css" >
        <link rel="stylesheet" href="/static/datadjables/css/datadjables.css">
      </head>
      <body>
          <h1>Products</h1>
          {% table_init dtobj %}
      </body>
  </html>

The template tag ``table_init`` renders something like::

  <table class="django-datatable" id="productstable" data-id="productstable"
   data-columns='[{"bSearchable": false, "bSortable": true, "sType": "string"},
                  {"bSearchable": false, "bSortable": true, "sType": "string"},
                  {"bSearchable": true, "bSortable": true, "sType": "string"}]'
   data-sorting='[[0, &quot;asc&quot;]]'
   data-source='/datadjable_testing/products/data/'>
   <thead>
       <tr><th>Name</th><th>Std. price</th><th>Avg. price</th></tr>
   </thead>
   <tbody></tbody>
   <tfoot><tr>
     <th><input style="display:none">&nbsp;</th>
     <th><input style="display:none">&nbsp;</th>
     <th><input class="search_init" type="text" value="Search Avg. prices" name="search_avg_price"></th>
   </tr></tfoot>
  </table>

This view sends the first batch of records as json data to the browser, where jQuery DataTables renders it nicely into your table. Whenever the user scrolls further down, jQuery DataTables fetches the next batch.
