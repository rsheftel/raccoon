
Example Usage for Raccoon
=========================

.. code:: python

    # import libraries
    import raccoon as rc

Initialize
----------

.. code:: python

    # empty DataFrame
    df = rc.DataFrame()
    df




.. parsed-literal::

    object id: 2000238116424
    columns:
    []
    data:
    []
    index:
    []



.. code:: python

    # with columns and indexes but no data
    df = rc.DataFrame(columns=['a', 'b', 'c'], index=[1, 2, 3])
    df




.. parsed-literal::

    object id: 2000238363088
    columns:
    ['a', 'b', 'c']
    data:
    [[None, None, None], [None, None, None], [None, None, None]]
    index:
    [1, 2, 3]



.. code:: python

    # with data
    df = rc.DataFrame(data={'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[10, 11, 12], columns=['a', 'b'])
    df




.. parsed-literal::

    object id: 2000238363928
    columns:
    ['a', 'b']
    data:
    [[1, 2, 3], [4, 5, 6]]
    index:
    [10, 11, 12]



Print
-----

.. code:: python

    df.show()


.. parsed-literal::

      index    a    b
    -------  ---  ---
         10    1    4
         11    2    5
         12    3    6
    

.. code:: python

    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         10    1    4
         11    2    5
         12    3    6
    

Setters and Getters
-------------------

.. code:: python

    # columns
    df.columns




.. parsed-literal::

    ['a', 'b']



.. code:: python

    df.columns = ['first', 'second']
    print(df)


.. parsed-literal::

      index    first    second
    -------  -------  --------
         10        1         4
         11        2         5
         12        3         6
    

.. code:: python

    # columns can be renamed with a dict()
    df.rename_columns({'second': 'b', 'first': 'a'})
    df.columns




.. parsed-literal::

    ['a', 'b']



.. code:: python

    # index
    df.index




.. parsed-literal::

    [10, 11, 12]



.. code:: python

    #indexes can be any non-repeating unique values
    df.index = ['apple', 'pear', 7.7]
    df.show()


.. parsed-literal::

    index      a    b
    -------  ---  ---
    apple      1    4
    pear       2    5
    7.7        3    6
    

.. code:: python

    df.index = [10, 11, 12]
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         10    1    4
         11    2    5
         12    3    6
    

.. code:: python

    # the index can also have a name, befault it is "index"
    df.index_name




.. parsed-literal::

    'index'



.. code:: python

    df.index_name = 'units'
    df.index_name




.. parsed-literal::

    'units'



.. code:: python

    # data is a shallow copy, be careful on how this is used
    df.index_name = 'index'
    df.data




.. parsed-literal::

    [[1, 2, 3], [4, 5, 6]]



.. code:: python

    # get_index() is a view not a copy, be careful when using this
    df.get_index()




.. parsed-literal::

    [10, 11, 12]



Select Index
------------

.. code:: python

    df.select_index(11)




.. parsed-literal::

    [False, True, False]



Set Values
----------

.. code:: python

    # set a single cell
    df.set(10, 'a', 100)
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         10  100    4
         11    2    5
         12    3    6
    

.. code:: python

    # set a value outside current range creates a new row and/or column. Can also use [] for setting
    df[13, 'c'] = 9
    df.show()


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100    4
         11    2    5
         12    3    6
         13              9
    

.. code:: python

    # set column
    df['b'] = 55
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   55
         11    2   55
         12    3   55
         13        55    9
    

.. code:: python

    # set a subset of column
    df[[10, 12], 'b'] = 66
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   66
         11    2   55
         12    3   66
         13        55    9
    

.. code:: python

    # using boolean list
    df.set([True, False, True, False], 'b', [88, 99])
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   88
         11    2   55
         12    3   99
         13        55    9
    

.. code:: python

    # setting with slices
    df[12:13, 'a'] = 33
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   88
         11    2   55
         12   33   99
         13   33   55    9
    

.. code:: python

    df[10:12, 'c'] = [1, 2, 3]
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   88    1
         11    2   55    2
         12   33   99    3
         13   33   55    9
    

.. code:: python

    # append a row, DANGEROUS as there is not validation checking, but can be used for speed
    df.append_row(14, {'a': 44, 'c': 100, 'd': 99})
    print(df)


.. parsed-literal::

      index    a    b    c    d
    -------  ---  ---  ---  ---
         10  100   88    1
         11    2   55    2
         12   33   99    3
         13   33   55    9
         14   44       100   99
    

Get Values
----------

.. code:: python

    # get a single cell
    df[10, 'a']




.. parsed-literal::

    100



.. code:: python

    # get an entire column
    df['c'].show()


.. parsed-literal::

      index    c
    -------  ---
         10    1
         11    2
         12    3
         13    9
         14  100
    

.. code:: python

    # get list of columns
    df[['a', 'c']].show()


.. parsed-literal::

      index    a    c
    -------  ---  ---
         10  100    1
         11    2    2
         12   33    3
         13   33    9
         14   44  100
    

.. code:: python

    # get subset of the index
    df[[11, 12, 13], 'b'].show()


.. parsed-literal::

      index    b
    -------  ---
         11   55
         12   99
         13   55
    

.. code:: python

    # get using slices
    df[11:13, 'b'].show()


.. parsed-literal::

      index    b
    -------  ---
         11   55
         12   99
         13   55
    

.. code:: python

    # get a matrix
    df[10:11, ['a', 'c']].show()


.. parsed-literal::

      index    a    c
    -------  ---  ---
         10  100    1
         11    2    2
    

.. code:: python

    # get a column, return as a list
    df.get(columns='a', as_list=True)




.. parsed-literal::

    [100, 2, 33, 33, 44]



.. code:: python

    # get a row and return as a dictionary
    df.get_columns(index=13, columns=['a', 'b'], as_dict=True)




.. parsed-literal::

    {'a': 33, 'b': 55, 'index': 13}



Set and Get by Location
-----------------------

Locations are the index of the index, in other words the index locations
from 0...len(index)

.. code:: python

    print(df.get_location(2))


.. parsed-literal::

      index    a    b    c  d
    -------  ---  ---  ---  ---
         12   33   99    3
    

.. code:: python

    print(df.get_location(0, ['b', 'c'], as_dict=True))


.. parsed-literal::

    {'b': 88, 'c': 1, 'index': 10}
    

.. code:: python

    df.get_location(-1).show()


.. parsed-literal::

      index    a  b      c    d
    -------  ---  ---  ---  ---
         14   44       100   99
    

.. code:: python

    df.get_locations(locations=[0, 2]).show()


.. parsed-literal::

      index    a    b    c  d
    -------  ---  ---  ---  ---
         10  100   88    1
         12   33   99    3
    

.. code:: python

    df.set_locations(locations=[0, 2], column='a', values=-9)
    df.show()


.. parsed-literal::

      index    a    b    c    d
    -------  ---  ---  ---  ---
         10   -9   88    1
         11    2   55    2
         12   -9   99    3
         13   33   55    9
         14   44       100   99
    

Head and Tail
-------------

.. code:: python

    df.head(2).show()


.. parsed-literal::

      index    a    b    c  d
    -------  ---  ---  ---  ---
         10   -9   88    1
         11    2   55    2
    

.. code:: python

    df.tail(2).show()


.. parsed-literal::

      index    a    b    c    d
    -------  ---  ---  ---  ---
         13   33   55    9
         14   44       100   99
    

Delete colunmns and rows
------------------------

.. code:: python

    df.delete_rows([10, 13])
    print(df)


.. parsed-literal::

      index    a    b    c    d
    -------  ---  ---  ---  ---
         11    2   55    2
         12   -9   99    3
         14   44       100   99
    

.. code:: python

    df.delete_columns('b')
    print(df)


.. parsed-literal::

      index    a    c    d
    -------  ---  ---  ---
         11    2    2
         12   -9    3
         14   44  100   99
    

Convert
-------

.. code:: python

    # return a dict
    df.to_dict()




.. parsed-literal::

    {'a': [2, -9, 44],
     'c': [2, 3, 100],
     'd': [None, None, 99],
     'index': [11, 12, 14]}



.. code:: python

    # exclude the index
    df.to_dict(index=False)




.. parsed-literal::

    {'a': [2, -9, 44], 'c': [2, 3, 100], 'd': [None, None, 99]}



.. code:: python

    # return an OrderedDict()
    df.to_dict(ordered=True)




.. parsed-literal::

    OrderedDict([('index', [11, 12, 14]),
                 ('a', [2, -9, 44]),
                 ('c', [2, 3, 100]),
                 ('d', [None, None, 99])])



.. code:: python

    # return a list of just one column
    df['c'].to_list()




.. parsed-literal::

    [2, 3, 100]



.. code:: python

    # convert to JSON
    string = df.to_json()
    print(string)


.. parsed-literal::

    {"data": {"a": [2, -9, 44], "c": [2, 3, 100], "d": [null, null, 99]}, "index": [11, 12, 14], "meta_data": {"index_name": "index", "columns": ["a", "c", "d"], "sorted": false, "use_blist": false}}
    

.. code:: python

    # construct DataFrame from JSON
    df_from_json = rc.DataFrame.from_json(string)
    print(df_from_json)


.. parsed-literal::

      index    a    c    d
    -------  ---  ---  ---
         11    2    2
         12   -9    3
         14   44  100   99
    

Sort by Index and Column
------------------------

.. code:: python

    df = rc.DataFrame({'a': [4, 3, 2, 1], 'b': [6, 7, 8, 9]}, index=[25, 24, 23, 22])
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         25    4    6
         24    3    7
         23    2    8
         22    1    9
    

.. code:: python

    # sort by index. Sorts are inplace
    df.sort_index()
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         22    1    9
         23    2    8
         24    3    7
         25    4    6
    

.. code:: python

    # sort by column
    df.sort_columns('b')
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         25    4    6
         24    3    7
         23    2    8
         22    1    9
    

.. code:: python

    # sort by column in reverse order
    df.sort_columns('b', reverse=True)
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         22    1    9
         23    2    8
         24    3    7
         25    4    6
    

.. code:: python

    # sorting with a key function is avaialble, see tests for examples

Append
------

.. code:: python

    df1 = rc.DataFrame({'a': [1, 2], 'b': [5, 6]}, index=[1, 2])
    df1.show()


.. parsed-literal::

      index    a    b
    -------  ---  ---
          1    1    5
          2    2    6
    

.. code:: python

    df2 = rc.DataFrame({'b': [7, 8], 'c': [11, 12]}, index=[3, 4])
    print(df2)


.. parsed-literal::

      index    b    c
    -------  ---  ---
          3    7   11
          4    8   12
    

.. code:: python

    df1.append(df2)
    print(df1)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
          1    1    5
          2    2    6
          3         7   11
          4         8   12
    

Math Methods
------------

.. code:: python

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [2, 8, 9]})

.. code:: python

    # test for equality
    df.equality('a', value=3)




.. parsed-literal::

    [False, False, True]



.. code:: python

    # all math methods can operate on a subset of the index
    df.equality('b', indexes=[1, 2], value=2)




.. parsed-literal::

    [False, False]



.. code:: python

    # add two columns
    df.add('a', 'b')




.. parsed-literal::

    [3, 10, 12]



.. code:: python

    # subtract
    df.subtract('b', 'a')




.. parsed-literal::

    [1, 6, 6]



.. code:: python

    # multiply
    df.multiply('a', 'b', [0, 2])




.. parsed-literal::

    [2, 27]



.. code:: python

    # divide
    df.divide('b', 'a')




.. parsed-literal::

    [2.0, 4.0, 3.0]



Multi-Index
-----------

Raccoon does not have true hierarchical mulit-index capabilities like
Pandas, but attempts to mimic some of the capabilities with the use of
tuples as the index. Raccoon does not provide any checking to make sure
the indexes are all the same length or any other integrity checking.

.. code:: python

    tuples = [('a', 1, 3), ('a', 1, 4), ('a', 2, 3), ('b', 1, 4), ('b', 2, 1), ('b', 3, 3)]
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=tuples)
    print(df)


.. parsed-literal::

    index          a
    -----------  ---
    ('a', 1, 3)    1
    ('a', 1, 4)    2
    ('a', 2, 3)    3
    ('b', 1, 4)    4
    ('b', 2, 1)    5
    ('b', 3, 3)    6
    

The select\_index method works with tuples by allowing the \* to act as
a wild card for matching.

.. code:: python

    compare = ('a', None, None)
    df.select_index(compare)




.. parsed-literal::

    [True, True, True, False, False, False]



.. code:: python

    compare = ('a', None, 3)
    df.select_index(compare, 'boolean')




.. parsed-literal::

    [True, False, True, False, False, False]



.. code:: python

    compare = (None, 2, None)
    df.select_index(compare, 'value')




.. parsed-literal::

    [('a', 2, 3), ('b', 2, 1)]



.. code:: python

    compare = (None, None, 3)
    df.select_index(compare, 'value')




.. parsed-literal::

    [('a', 1, 3), ('a', 2, 3), ('b', 3, 3)]



.. code:: python

    compare = (None, None, None)
    df.select_index(compare)




.. parsed-literal::

    [True, True, True, True, True, True]



Reset Index
-----------

.. code:: python

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'])
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
          0    1    4
          1    2    5
          2    3    6
    

.. code:: python

    df.reset_index()
    df




.. parsed-literal::

    object id: 2000238549200
    columns:
    ['a', 'b', 'index_0']
    data:
    [[1, 2, 3], [4, 5, 6], [0, 1, 2]]
    index:
    [0, 1, 2]



.. code:: python

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=['x', 'y', 'z'], index_name='jelo')
    print(df)


.. parsed-literal::

    jelo      a    b
    ------  ---  ---
    x         1    4
    y         2    5
    z         3    6
    

.. code:: python

    df.reset_index()
    print(df)


.. parsed-literal::

      index    a    b  jelo
    -------  ---  ---  ------
          0    1    4  x
          1    2    5  y
          2    3    6  z
    

.. code:: python

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'],
                       index=[('a', 10, 'x'), ('b', 11, 'y'), ('c', 12, 'z')], index_name=('melo', 'helo', 'gelo'))
    print(df)


.. parsed-literal::

    ('melo', 'helo', 'gelo')      a    b
    --------------------------  ---  ---
    ('a', 10, 'x')                1    4
    ('b', 11, 'y')                2    5
    ('c', 12, 'z')                3    6
    

.. code:: python

    df.reset_index()
    print(df)


.. parsed-literal::

      index    a    b  melo      helo  gelo
    -------  ---  ---  ------  ------  ------
          0    1    4  a           10  x
          1    2    5  b           11  y
          2    3    6  c           12  z
    

.. code:: python

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=['x', 'y', 'z'], index_name='jelo')
    print(df)


.. parsed-literal::

    jelo      a    b
    ------  ---  ---
    x         1    4
    y         2    5
    z         3    6
    

.. code:: python

    df.reset_index(drop=True)
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
          0    1    4
          1    2    5
          2    3    6
    

Iterators
---------

.. code:: python

    df = rc.DataFrame({'a': [1, 2, 'c'], 'b': [5, 6, 'd']}, index=[1, 2, 3])

.. code:: python

    for row in df.iterrows():
        print(row)


.. parsed-literal::

    {'index': 1, 'a': 1, 'b': 5}
    {'index': 2, 'a': 2, 'b': 6}
    {'index': 3, 'a': 'c', 'b': 'd'}
    

.. code:: python

    for row in df.itertuples():
        print(row)


.. parsed-literal::

    Raccoon(index=1, a=1, b=5)
    Raccoon(index=2, a=2, b=6)
    Raccoon(index=3, a='c', b='d')
    

Sorted DataFrames
-----------------

DataFrames will be set to sorted by default if no index is given at
initialization. If an index is given at initialization then the
parameter sorted must be set to True

.. code:: python

    df = rc.DataFrame({'a': [3, 5, 4], 'b': [6, 8, 7]}, index=[12, 15, 14], sorted=True)

When sorted=True on initialization the data will be sorted by index to
start

.. code:: python

    df.show()


.. parsed-literal::

      index    a    b
    -------  ---  ---
         12    3    6
         14    4    7
         15    5    8
    


.. code:: python

    df[16, 'b'] = 9
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         12    3    6
         14    4    7
         15    5    8
         16         9
    

.. code:: python

    df.set(indexes=13, values={'a': 3.5, 'b': 6.5})
    print(df)


.. parsed-literal::

      index    a    b
    -------  ---  ---
         12  3    6
         13  3.5  6.5
         14  4    7
         15  5    8
         16       9
    

List or BList
-------------

The underlying data structure can be either blist (default) or list

.. code:: python

    # Construct with blist=True, the default
    df_blist = rc.DataFrame({'a': [1, 2, 3]}, index=[5, 6, 7], use_blist=True)

.. code:: python

    # see that the data structures are all blists
    df_blist.data




.. parsed-literal::

    blist([blist([1, 2, 3])])



.. code:: python

    df_blist.index




.. parsed-literal::

    blist([5, 6, 7])



.. code:: python

    df_blist.columns




.. parsed-literal::

    blist(['a'])



.. code:: python

    # now construct as blist = False and they are all lists
    df_list = rc.DataFrame({'a': [1, 2, 3]}, index=[5, 6, 7], use_blist=False)

.. code:: python

    df_list.data




.. parsed-literal::

    [[1, 2, 3]]



.. code:: python

    df_list.index




.. parsed-literal::

    [5, 6, 7]



.. code:: python

    df_list.columns




.. parsed-literal::

    ['a']


