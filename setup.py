# -*- coding: utf-8 -*-
#from distutils.core import setup
from setuptools import setup, find_packages

version = '1.0.37'

setup(
    name='datadjables',
    version=version,
    description='A Django app for jQuery DataTables integration using AJAX, endless scrolling, individual column filtering etc.',
    author=u'Martin Winkler',
    author_email='mw@martinwinkler.com',
    url='https://https://github.com/mawimawi/datadjables',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.5', ]
)


# import os
# os.chdir('build/lib/')
# os.system('tar czf datadjables.tar.gz datadjables')
# print "tarfile is now in build/lib/datadjables.tar.gz"
