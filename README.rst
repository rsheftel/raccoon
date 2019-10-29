raccoon
=======
Python DataFrame with fast insert and appends

.. image:: https://badge.fury.io/py/raccoon.svg
    :target: https://badge.fury.io/py/raccoon

.. image:: https://travis-ci.org/rsheftel/raccoon.svg?branch=master
    :target: https://travis-ci.org/rsheftel/raccoon

.. image:: https://coveralls.io/repos/github/rsheftel/raccoon/badge.svg?branch=master
    :target: https://coveralls.io/github/rsheftel/raccoon?branch=master
    
.. image:: https://readthedocs.org/projects/raccoon/badge/?version=latest
   :target: http://raccoon.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Documentation
-------------
http://raccoon.readthedocs.io/en/latest/

Source location
~~~~~~~~~~~~~~~
Hosted on GitHub: https://github.com/rsheftel/raccoon

Overview
--------
Raccoon is a lightweight DataFrame and Series implementation inspired by the phenomenal Pandas package for the one use
case where Pandas is known to be sub-optimal: DataFrames and Series that grow in size by rows frequently in the code.
Additionally Raccoon DataFrames and Series can be parametrized to be sorted so that additions to the DataFrame keep the
index in sorted order to speed inserts and retrievals.

A simple speed comparison of Raccoon vs Pandas for typical functionality is located in the documentation.

Inspiration
~~~~~~~~~~~
Pandas DataFrames and Series are excellent multi-purpose data structures for data management and analysis. One of the
use cases I had was to use DataFrames as a type of in-memory database table. The issue was that this required lots of
growing the rows of the DataFrame, something that is known to be slow in Pandas. The reason it is slow in Pandas is that
the underlying data structure is numpy which does a complete copy of the data when the size of the array grows.

Functionality
~~~~~~~~~~~~~
Raccoon implements what is needed to use the DataFrame as an in memory store of index and column data structure
supporting simple and tuple indexes to mimic the hierarchical indexes of Pandas. The methods included are primarily
about setting values of the data frame, growing and appending the data frame and getting values from the data frame.
The raccoon DataFrame is not intended for math operations like pandas and only limited basic math methods are included.

Underlying Data Structure
~~~~~~~~~~~~~~~~~~~~~~~~~
Raccoon uses the standard built in lists as its default underlying data structure. There is an option on object
construction to use any other drop-in replacement for lists. For example the fast blist package
http://stutzbachenterprises.com/blist/ could be used as a list replacement for the underlying data structure.

Why Raccoon?
~~~~~~~~~~~~
According to wikipedia some scientists believe the panda is related to the raccoon

Contributing
~~~~~~~~~~~~
Contribution in the form of pull requests are welcome. Use pytest to run the test suite. Be sure any new additions
come with accompanying tests.

Future
~~~~~~
This package serves the needs it was originally created for. Any future additions by myself will be driven by my own
needs, but it is completely open source to I encourage anyone to add on and expand.

My hope is that one day Pandas solves the speed problem with growing DataFrames and this package becomes obsolete.

Python Version
~~~~~~~~~~~~~~
Raccoon requires Python 3.4 or greater. Python 2.7 support was eliminated as of version 3.0. If you need to use raccoon
with Python 2.7 use any version less than 3.0

Helper scripts
~~~~~~~~~~~~~~
There is helper function to generate these docs from the source code. On windows cd into the docs directory and
execute make_docs.bat from the command line. To run the test coverage report run the coverage.sh script.
