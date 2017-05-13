
Example Usage for Series
========================

.. code:: python

    # remove comment to use latest development version
    import sys; sys.path.insert(0, '../')

.. code:: python

    # import libraries
    import raccoon as rc

Initialize
----------

.. code:: python

    # empty DataFrame
    srs = rc.Series()
    srs




.. parsed-literal::

    object id: 1891392163736
    data:
    []
    index:
    []



.. code:: python

    # with indexes but no data
    srs = rc.Series(index=[1, 2, 3])
    srs




.. parsed-literal::

    object id: 1891392163568
    data:
    [None, None, None]
    index:
    [1, 2, 3]



.. code:: python

    # with data
    srs = rc.Series(data=[4, 5, 6], index=[10, 11, 12])
    srs




.. parsed-literal::

    object id: 1891392217440
    data:
    [4, 5, 6]
    index:
    [10, 11, 12]



Print
-----

.. code:: python

    srs.show()


.. parsed-literal::

      index    value
    -------  -------
         10        4
         11        5
         12        6
    

.. code:: python

    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         10        4
         11        5
         12        6
    

Setters and Getters
-------------------

.. code:: python

    # data_name
    srs.data_name




.. parsed-literal::

    'value'



.. code:: python

    srs.data_name = 'new_data'
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           4
         11           5
         12           6
    

.. code:: python

    # index
    srs.index




.. parsed-literal::

    [10, 11, 12]



.. code:: python

    #indexes can be any non-repeating unique values
    srs.index = ['apple', 'pear', 7.7]
    srs.show()


.. parsed-literal::

    index      new_data
    -------  ----------
    apple             4
    pear              5
    7.7               6
    

.. code:: python

    srs.index = [10, 11, 12]
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           4
         11           5
         12           6
    

.. code:: python

    # the index can also have a name, befault it is "index"
    srs.index_name




.. parsed-literal::

    'index'



.. code:: python

    srs.index_name = 'units'
    srs.index_name




.. parsed-literal::

    'units'



.. code:: python

    # data is a shallow copy, be careful on how this is used
    srs.index_name = 'index'
    srs.data




.. parsed-literal::

    [4, 5, 6]



Select Index
------------

.. code:: python

    srs.select_index(11)




.. parsed-literal::

    [False, True, False]



Set Values
----------

.. code:: python

    # set a single cell
    srs.set(10, 100)
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10         100
         11           5
         12           6
    

.. code:: python

    # set a value outside current range creates a new row. Can also use [] for setting
    srs[13] = 9
    srs.show()


.. parsed-literal::

      index    new_data
    -------  ----------
         10         100
         11           5
         12           6
         13           9
    

.. code:: python

    # set a subset of rows
    srs[[10, 12]] = 66
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          66
         11           5
         12          66
         13           9
    

.. code:: python

    # using boolean list
    srs.set([True, False, True, False], [88, 99])
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          88
         11           5
         12          99
         13           9
    

.. code:: python

    # setting with slices
    srs[12:13] = 33
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          88
         11           5
         12          33
         13          33
    

.. code:: python

    srs[10:12] = [1, 2, 3]
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           1
         11           2
         12           3
         13          33
    

.. code:: python

    # set a location
    srs.set_location(1, 22)
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           1
         11          22
         12           3
         13          33
    

.. code:: python

    # set multiple locations
    srs.set_locations([0, 2], [11, 27])
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
         12          27
         13          33
    

.. code:: python

    # append a row, DANGEROUS as there is not validation checking, but can be used for speed
    srs.append_row(14, 99)
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
         12          27
         13          33
         14          99
    

.. code:: python

    # append multiple rows, again no sort check
    srs.append_rows([15, 16], [100, 110])
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
         12          27
         13          33
         14          99
         15         100
         16         110
    

Get Values
----------

.. code:: python

    # get a single cell
    srs[10]




.. parsed-literal::

    11



.. code:: python

    # get subset of the index
    srs[[11, 12, 13]].show()


.. parsed-literal::

      index    new_data
    -------  ----------
         11          22
         12          27
         13          33
    

.. code:: python

    # get using slices
    srs[11:13].show()


.. parsed-literal::

      index    new_data
    -------  ----------
         11          22
         12          27
         13          33
    

.. code:: python

    # return as a list
    srs.get([11, 12, 13], as_list=True)




.. parsed-literal::

    [22, 27, 33]



Set and Get by Location
-----------------------

Locations are the index of the index, in other words the index locations
from 0...len(index)

.. code:: python

    print(srs.get_location(2))


.. parsed-literal::

    {'index': 12, 'new_data': 27}
    

.. code:: python

    srs.get_location(-1)




.. parsed-literal::

    {'index': 16, 'new_data': 110}



.. code:: python

    srs.get_locations(locations=[0, 2]).show()


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         12          27
    

.. code:: python

    srs.get_locations(locations=[0, 2], as_list=True)




.. parsed-literal::

    [11, 27]



.. code:: python

    srs.set_locations([-1, -2], values=[10, 9])
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
         12          27
         13          33
         14          99
         15           9
         16          10
    

Head and Tail
-------------

.. code:: python

    srs.head(2).show()


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
    

.. code:: python

    srs.tail(2).show()


.. parsed-literal::

      index    new_data
    -------  ----------
         15           9
         16          10
    

Delete rows
-----------

.. code:: python

    srs.delete([10, 13])
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         11          22
         12          27
         14          99
         15           9
         16          10
    

Convert
-------

.. code:: python

    # return a dict
    srs.to_dict()




.. parsed-literal::

    {'index': [11, 12, 14, 15, 16], 'new_data': [22, 27, 99, 9, 10]}



.. code:: python

    # exclude the index
    srs.to_dict(index=False)




.. parsed-literal::

    {'new_data': [22, 27, 99, 9, 10]}



.. code:: python

    # return an OrderedDict()
    srs.to_dict(ordered=True)




.. parsed-literal::

    OrderedDict([('index', [11, 12, 14, 15, 16]),
                 ('new_data', [22, 27, 99, 9, 10])])



Sort by Index
-------------

.. code:: python

    srs = rc.Series([6, 7, 8, 9], index=[25, 24, 23, 22])
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         25        6
         24        7
         23        8
         22        9
    

.. code:: python

    # sort by index. Sorts are inplace
    srs.sort_index()
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         22        9
         23        8
         24        7
         25        6
    

Math Methods
------------

.. code:: python

    srs = rc.Series([1, 2, 3])

.. code:: python

    # test for equality
    srs.equality(value=3)




.. parsed-literal::

    [False, False, True]



.. code:: python

    # all math methods can operate on a subset of the index
    srs.equality(indexes=[1, 2], value=2)




.. parsed-literal::

    [True, False]



Multi-Index
-----------

Raccoon does not have true hierarchical mulit-index capabilities like
Pandas, but attempts to mimic some of the capabilities with the use of
tuples as the index. Raccoon does not provide any checking to make sure
the indexes are all the same length or any other integrity checking.

.. code:: python

    tuples = [('a', 1, 3), ('a', 1, 4), ('a', 2, 3), ('b', 1, 4), ('b', 2, 1), ('b', 3, 3)]
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=tuples)
    print(srs)


.. parsed-literal::

    index          value
    -----------  -------
    ('a', 1, 3)        1
    ('a', 1, 4)        2
    ('a', 2, 3)        3
    ('b', 1, 4)        4
    ('b', 2, 1)        5
    ('b', 3, 3)        6
    

The select\_index method works with tuples by allowing the \* to act as
a wild card for matching.

.. code:: python

    compare = ('a', None, None)
    srs.select_index(compare)




.. parsed-literal::

    [True, True, True, False, False, False]



.. code:: python

    compare = ('a', None, 3)
    srs.select_index(compare, 'boolean')




.. parsed-literal::

    [True, False, True, False, False, False]



.. code:: python

    compare = (None, 2, None)
    srs.select_index(compare, 'value')




.. parsed-literal::

    [('a', 2, 3), ('b', 2, 1)]



.. code:: python

    compare = (None, None, 3)
    srs.select_index(compare, 'value')




.. parsed-literal::

    [('a', 1, 3), ('a', 2, 3), ('b', 3, 3)]



.. code:: python

    compare = (None, None, None)
    srs.select_index(compare)




.. parsed-literal::

    [True, True, True, True, True, True]



Reset Index
-----------

.. code:: python

    srs = rc.Series([1, 2, 3], index=[9, 10, 11])
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
          9        1
         10        2
         11        3
    

.. code:: python

    srs.reset_index()
    srs




.. parsed-literal::

    object id: 1891392288752
    data:
    [1, 2, 3]
    index:
    [0, 1, 2]



.. code:: python

    srs = rc.Series([1, 2, 3], index=[9, 10, 11], index_name='new name')
    print(srs)


.. parsed-literal::

      new name    value
    ----------  -------
             9        1
            10        2
            11        3
    

.. code:: python

    srs.reset_index()
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
          0        1
          1        2
          2        3
    

Sorted Series
-------------

Series will be set to sorted by default if no index is given at
initialization. If an index is given at initialization then the
parameter sorted must be set to True

.. code:: python

    srs = rc.Series([3, 5, 4], index=[12, 15, 14], sort=True)

When sorted=True on initialization the data will be sorted by index to
start

.. code:: python

    srs.show()


.. parsed-literal::

      index    value
    -------  -------
         12        3
         14        4
         15        5
    

.. code:: python

    srs[16] = 9
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         12        3
         14        4
         15        5
         16        9
    

.. code:: python

    srs.set(indexes=13, values=3.5)
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         12      3
         13      3.5
         14      4
         15      5
         16      9
    

List or BList
-------------

The underlying data structure can be either blist (default) or list

.. code:: python

    # Construct with blist=True, the default
    srs_blist = rc.Series([1, 2, 3], index=[5, 6, 7], use_blist=True)

.. code:: python

    # see that the data structures are all blists
    srs_blist.data




.. parsed-literal::

    blist([1, 2, 3])



.. code:: python

    srs_blist.index




.. parsed-literal::

    blist([5, 6, 7])



.. code:: python

    # now construct as blist = False and they are all lists
    srs_list = rc.Series([1, 2, 3], index=[5, 6, 7], use_blist=False)

.. code:: python

    srs_list.data




.. parsed-literal::

    [1, 2, 3]



.. code:: python

    srs_list.index




.. parsed-literal::

    [5, 6, 7]


