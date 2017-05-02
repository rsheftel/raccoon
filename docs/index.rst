.. Raccoon documentation master file, created by
   sphinx-quickstart on Fri Jul 29 08:26:04 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Raccoon documentation
=====================
Overview
--------
Raccoon is a lightweight DataFrame and Series implementation inspired by the phenomenal Pandas package for the one use
case where Pandas is known to be sub-optimal: DataFrames and Series that grow in size by rows frequently in the code.
A simple speed comparison is below in the contents.

Source location
~~~~~~~~~~~~~~~
Hosted on GitHub: https://github.com/rsheftel/raccoon

Inspiration
~~~~~~~~~~~
Pandas DataFrames and Series are excellent multi-purpose data structures for data management and analysis. One of the
use cases I had was to use DataFrames as a type of in-memory database table. The issue was that this required lots of
growing the rows of the DataFrame, something that is known to be slow in Pandas. The reason it is slow in Pandas is
that the underlying data structure is numpy which does a complete copy of the data when the size of the array grows.

Functionality
~~~~~~~~~~~~~
Raccoon implements what is needed to use the DataFrame as an in memory store of index and column data structure
supporting simple and tuple indexes to mimic the hierarchical indexes of Pandas. The methods included are primarily
about setting values of the data frame, growing and appending the data frame and getting values from the data frame.
The raccoon DataFrame is not intended for math operations like pandas and only limited basic math methods are included.

Underlying Data Structure
~~~~~~~~~~~~~~~~~~~~~~~~~
Raccoon uses the standard built in lists. There is an option on object construction to use fast blist
http://stutzbachenterprises.com/blist/ list replacement for the underlying data structure.

Why Raccoon?
~~~~~~~~~~~~
According to wikipedia some scientists believe the panda is related to the raccoon

Future
~~~~~~
This package serves the needs it was originally created for. Any future additions by myself will be driven by my own
needs, but it is completely open source to I encourage anyone to add on and expand.

My hope is that one day Pandas solves the speed problem with growing DataFrames and this package becomes obsolete.

Python Version
~~~~~~~~~~~~~~
Raccoon required Python 2.7 or 3.3 or greater to run because it utilizes "yield from" which was introduced in 3.3

Helper scripts
~~~~~~~~~~~~~~
There is helper function to generate these docs from the source code. On windows cd into the docs directory and
execute make_docs.bat from the command line. To run the test coverage report run the coverage.sh script.

Updates
-------
.. toctree::
   :maxdepth: 1

   change_log.rst

Contents
--------
.. toctree::
   :maxdepth: 2

   modules.rst
   raccoon.rst
   usage_dataframe.rst
   usage_series.rst
   convert_pandas.rst
   speed_test.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
