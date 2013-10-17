Usage overview
==============

THIS SECTION IS OUTDATED


Suppose we have three models: ``Person``, ``Product`` and ``Purchase``. A person buys some product for a price that may be different from the ``standard_price`` stored in the ``Product`` model. This price is stored in a ``Purchase`` object which also contains the timestamp of the sale. This setup is identical to the ``dt_testing`` app inside the ``datatables`` django app.

The heart of every DataTable is a queryset like ``Product.objects.all()``. Of course this base_query can be something more complicated like ``Product.objects.all().select_related().annotate(avg_price=Avg('purchase__price'))``.

The data being displayed in your browser can hold any information that your queryset offers. An example would be::

  class DtProducts(DataTable):
      standard_price = DecimalColumn(
          coltitle=_('Std. price'),
          coltitle_plural=_("Std. prices"),
          renderer=Template('{{ obj.standard_price|floatformat:2 }}'),)
      name = StringColumn(coltitle=_('Name'), coltitle_plural=_("Names"))
      avg_price = DecimalColumn(
          coltitle=_('Avg. price'),
          coltitle_plural=_('Avg. prices'),
          renderer=Template('{{ obj.avg_price|floatformat:2 }}'),
          sortable=True,
          searchable=True)

      class Meta:
          base_query = Product.objects.all().annotate(avg_price=Avg('purchase__price'))

This specific datatable consists of three columns ``standard_price``, ``name`` and ``avg_price`` (which the queryset creates using the ``annotate`` method).

For viewing your datatable in a browser you first two views::


  def product_list(request):
      return TemplateResponse(request, 'dt_testing/product_list.html',
                              {'dtobj': DtProducts()})

This is a view that shows a html page with the required JavaScript code and a <table> which contains information to render the datatable in the browser::

  {% load datatables %}<html>
      <head>
          <script type="text/javascript" src="/static/datatables/js/jquery.js"></script>
          <script type="text/javascript" src="/static/datatables/js/jquery.dataTables.js"></script>
          <script type="text/javascript" src="/static/datatables/js/django_datatables.js"></script>
          <link rel="stylesheet" href="/static/datatables/css/jquery.dataTables.css">
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
   data-source='/dt_testing/products/data/'>
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

You also need a second view which returns the data itself which will be inserted between ``<tbody>`` and ``</tbody>``::

  def product_list_ajax(request):
      return DtProducts().json(request)

This view sends the first batch of records as json data to the browser, where jQuery DataTables renders it nicely into your table. Whenever the user scrolls further down, jQuery DataTables fetches the next batch.
