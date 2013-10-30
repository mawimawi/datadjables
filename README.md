datadjables
===========

jQuery Datatables for Django (ajaxy, no pagination necessary, nice filter columns)
Filtering by columns is made possible by the great ColumnFilter plugin
http://code.google.com/p/jquery-datatables-column-filter/wiki/ColumnFilter

It's under quite heavy development, and I plan to make available custom columns
which are searchable and sortable. An example for this is a model like this:

    class Person(models.Model):
        birthdate = models.DateField()


    class PersonTable(DateDjable):
        age = DateColumn(searchable=True, sortable=True,
            selector='CURRENT_DATE - birthdate')

Stay tuned, hopefully you'll like this.


Some documentation:
-------------------

$ cd docs
$ make html

Then open your browser and go to ./_build/index.html


Internal use:
-------------

Howto create a new tar.gz file for (my internally used) piprepos:

# IMPORTANT: first update the version number in setup.py
python setup.py sdist
svn add dist/* 2>/dev/null ; svn ci -m "version bump" dist
