Example Usage for Series
========================

.. code:: ipython3

    # remove comment to use latest development version
    import sys; sys.path.insert(0, '../')

.. code:: ipython3

    # import libraries
    import raccoon as rc

Initialize
----------

.. code:: ipython3

    # empty DataFrame
    srs = rc.Series()
    srs




.. parsed-literal::

    object id: 1875881342160
    data:
    []
    index:
    []



.. code:: ipython3

    # with indexes but no data
    srs = rc.Series(index=[1, 2, 3])
    srs




.. parsed-literal::

    object id: 1875880829648
    data:
    [None, None, None]
    index:
    [1, 2, 3]



.. code:: ipython3

    # with data
    srs = rc.Series(data=[4, 5, 6], index=[10, 11, 12])
    srs




.. parsed-literal::

    object id: 1875880829840
    data:
    [4, 5, 6]
    index:
    [10, 11, 12]



Print
-----

.. code:: ipython3

    srs.print()


.. parsed-literal::

      index    value
    -------  -------
         10        4
         11        5
         12        6
    

.. code:: ipython3

    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         10        4
         11        5
         12        6
    

Setters and Getters
-------------------

.. code:: ipython3

    # data_name
    srs.data_name




.. parsed-literal::

    'value'



.. code:: ipython3

    srs.data_name = 'new_data'
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           4
         11           5
         12           6
    

.. code:: ipython3

    # index
    srs.index




.. parsed-literal::

    [10, 11, 12]



.. code:: ipython3

    #indexes can be any non-repeating unique values
    srs.index = ['apple', 'pear', 7.7]
    srs.print()


.. parsed-literal::

    index      new_data
    -------  ----------
    apple             4
    pear              5
    7.7               6
    

.. code:: ipython3

    srs.index = [10, 11, 12]
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           4
         11           5
         12           6
    

.. code:: ipython3

    # the index can also have a name, befault it is "index"
    srs.index_name




.. parsed-literal::

    'index'



.. code:: ipython3

    srs.index_name = 'units'
    srs.index_name




.. parsed-literal::

    'units'



.. code:: ipython3

    # data is a shallow copy, be careful on how this is used
    srs.index_name = 'index'
    srs.data




.. parsed-literal::

    [4, 5, 6]



Select Index
------------

.. code:: ipython3

    srs.select_index(11)




.. parsed-literal::

    [False, True, False]



Set Values
----------

.. code:: ipython3

    # set a single cell
    srs.set(10, 100)
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10         100
         11           5
         12           6
    

.. code:: ipython3

    # set a value outside current range creates a new row. Can also use [] for setting
    srs[13] = 9
    srs.print()


.. parsed-literal::

      index    new_data
    -------  ----------
         10         100
         11           5
         12           6
         13           9
    

.. code:: ipython3

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
    

.. code:: ipython3

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
    

.. code:: ipython3

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
    

.. code:: ipython3

    srs[10:12] = [1, 2, 3]
    print(srs)


.. parsed-literal::

      index    new_data
    -------  ----------
         10           1
         11           2
         12           3
         13          33
    

.. code:: ipython3

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
    

.. code:: ipython3

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
    

.. code:: ipython3

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
    

.. code:: ipython3

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

.. code:: ipython3

    # get a single cell
    srs[10]




.. parsed-literal::

    11



.. code:: ipython3

    # get subset of the index
    srs[[11, 12, 13]].print()


.. parsed-literal::

      index    new_data
    -------  ----------
         11          22
         12          27
         13          33
    

.. code:: ipython3

    # get using slices
    srs[11:13].print()


.. parsed-literal::

      index    new_data
    -------  ----------
         11          22
         12          27
         13          33
    

.. code:: ipython3

    # return as a list
    srs.get([11, 12, 13], as_list=True)




.. parsed-literal::

    [22, 27, 33]



Set and Get by Location
-----------------------

Locations are the index of the index, in other words the index locations
from 0…len(index)

.. code:: ipython3

    print(srs.get_location(2))


.. parsed-literal::

    {'index': 12, 'new_data': 27}
    

.. code:: ipython3

    srs.get_location(-1)




.. parsed-literal::

    {'index': 16, 'new_data': 110}



.. code:: ipython3

    srs.get_locations(locations=[0, 2]).print()


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         12          27
    

.. code:: ipython3

    srs.get_locations(locations=[0, 2], as_list=True)




.. parsed-literal::

    [11, 27]



.. code:: ipython3

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

.. code:: ipython3

    srs.head(2).print()


.. parsed-literal::

      index    new_data
    -------  ----------
         10          11
         11          22
    

.. code:: ipython3

    srs.tail(2).print()


.. parsed-literal::

      index    new_data
    -------  ----------
         15           9
         16          10
    

Delete rows
-----------

.. code:: ipython3

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

.. code:: ipython3

    # return a dict
    srs.to_dict()




.. parsed-literal::

    {'index': [11, 12, 14, 15, 16], 'new_data': [22, 27, 99, 9, 10]}



.. code:: ipython3

    # exclude the index
    srs.to_dict(index=False)




.. parsed-literal::

    {'new_data': [22, 27, 99, 9, 10]}



.. code:: ipython3

    # return an OrderedDict()
    srs.to_dict(ordered=True)




.. parsed-literal::

    OrderedDict([('index', [11, 12, 14, 15, 16]),
                 ('new_data', [22, 27, 99, 9, 10])])



Sort by Index
-------------

.. code:: ipython3

    srs = rc.Series([6, 7, 8, 9], index=[25, 24, 23, 22])
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         25        6
         24        7
         23        8
         22        9
    

.. code:: ipython3

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

.. code:: ipython3

    srs = rc.Series([1, 2, 3])

.. code:: ipython3

    # test for equality
    srs.equality(value=3)




.. parsed-literal::

    [False, False, True]



.. code:: ipython3

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

.. code:: ipython3

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
    

The select_index method works with tuples by allowing the \* to act as a
wild card for matching.

.. code:: ipython3

    compare = ('a', None, None)
    srs.select_index(compare)




.. parsed-literal::

    [True, True, True, False, False, False]



.. code:: ipython3

    compare = ('a', None, 3)
    srs.select_index(compare, 'boolean')




.. parsed-literal::

    [True, False, True, False, False, False]



.. code:: ipython3

    compare = (None, 2, None)
    srs.select_index(compare, 'value')




.. parsed-literal::

    [('a', 2, 3), ('b', 2, 1)]



.. code:: ipython3

    compare = (None, None, 3)
    srs.select_index(compare, 'value')




.. parsed-literal::

    [('a', 1, 3), ('a', 2, 3), ('b', 3, 3)]



.. code:: ipython3

    compare = (None, None, None)
    srs.select_index(compare)




.. parsed-literal::

    [True, True, True, True, True, True]



Reset Index
-----------

.. code:: ipython3

    srs = rc.Series([1, 2, 3], index=[9, 10, 11])
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
          9        1
         10        2
         11        3
    

.. code:: ipython3

    srs.reset_index()
    srs




.. parsed-literal::

    object id: 1875881741104
    data:
    [1, 2, 3]
    index:
    [0, 1, 2]



.. code:: ipython3

    srs = rc.Series([1, 2, 3], index=[9, 10, 11], index_name='new name')
    print(srs)


.. parsed-literal::

      new name    value
    ----------  -------
             9        1
            10        2
            11        3
    

.. code:: ipython3

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

.. code:: ipython3

    srs = rc.Series([3, 5, 4], index=[12, 15, 14], sort=True)

When sorted=True on initialization the data will be sorted by index to
start

.. code:: ipython3

    srs.print()


.. parsed-literal::

      index    value
    -------  -------
         12        3
         14        4
         15        5
    

.. code:: ipython3

    srs[16] = 9
    print(srs)


.. parsed-literal::

      index    value
    -------  -------
         12        3
         14        4
         15        5
         16        9
    

.. code:: ipython3

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
    
