
Example Usage for Raccoon
=========================

.. code:: python

    # import libraries
    import sys
    sys.path.append("..")
    import raccoon as rc

Initialize
----------

.. code:: python

    # empty DataFrame
    df = rc.DataFrame()
    df




.. parsed-literal::

    object id: 52176560
    columns:
    blist([])
    data:
    blist([])
    index:
    blist([])



.. code:: python

    # with columns and indexes but no data
    df = rc.DataFrame(columns=['a', 'b', 'c'], index=[1, 2, 3])
    df




.. parsed-literal::

    object id: 52363152
    columns:
    blist(['a', 'b', 'c'])
    data:
    blist([blist([None, None, None]), blist([None, None, None]), blist([None, None, None])])
    index:
    blist([1, 2, 3])



.. code:: python

    # with data
    df = rc.DataFrame(data={'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[10, 11, 12], columns=['a', 'b'])
    df




.. parsed-literal::

    object id: 52433296
    columns:
    blist(['a', 'b'])
    data:
    blist([blist([1, 2, 3]), blist([4, 5, 6])])
    index:
    blist([10, 11, 12])



Print
-----

.. code:: python

    df.print()


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

    blist(['a', 'b'])



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

    blist(['a', 'b'])



.. code:: python

    # index
    df.index




.. parsed-literal::

    blist([10, 11, 12])



.. code:: python

    #indexes can be any non-repeating unique values
    df.index = ['apple', 'pear', 7.7]
    df.print()


.. parsed-literal::

    index      a    b
    -------  ---  ---
    apple      1    4
    pear       2    5
    7.7        3    6
    

.. code:: python

    df.index = [10, 11, 12]

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

    blist([blist([1, 2, 3]), blist([4, 5, 6])])



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
    df.print()


.. parsed-literal::

      index    a    b
    -------  ---  ---
         10  100    4
         11    2    5
         12    3    6
    

.. code:: python

    # set a value outside current range creates a new row and/or column. Can also use [] for setting
    df[13, 'c'] = 9
    df.print()


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
    df.print()


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
    

Get Values
----------

.. code:: python

    # get a single cell
    df[10, 'a']




.. parsed-literal::

    100



.. code:: python

    # get an entire column
    df['c'].print()


.. parsed-literal::

      index    c
    -------  ---
         10    1
         11    2
         12    3
         13    9
    

.. code:: python

    # get list of columns
    df[['a', 'c']].print()


.. parsed-literal::

      index    a    c
    -------  ---  ---
         10  100    1
         11    2    2
         12   33    3
         13   33    9
    

.. code:: python

    # get subset of the index
    df[[11, 12, 13], 'b'].print()


.. parsed-literal::

      index    b
    -------  ---
         11   55
         12   99
         13   55
    

.. code:: python

    # get using slices
    df[11:13, 'b'].print()


.. parsed-literal::

      index    b
    -------  ---
         11   55
         12   99
         13   55
    

.. code:: python

    # get a matrix
    df[10:11, ['a', 'c']].print()


.. parsed-literal::

      index    a    c
    -------  ---  ---
         10  100    1
         11    2    2
    

Head and Tail
-------------

.. code:: python

    df.head(2).print()


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         10  100   88    1
         11    2   55    2
    

.. code:: python

    df.tail(2).print()


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         12   33   99    3
         13   33   55    9
    

Delete colunmns and rows
------------------------

.. code:: python

    df.delete_rows([10, 13])
    print(df)


.. parsed-literal::

      index    a    b    c
    -------  ---  ---  ---
         11    2   55    2
         12   33   99    3
    

.. code:: python

    df.delete_columns('b')
    print(df)


.. parsed-literal::

      index    a    c
    -------  ---  ---
         11    2    2
         12   33    3
    

Convert
-------

.. code:: python

    # return a dict
    df.to_dict()




.. parsed-literal::

    {'a': blist([2, 33]), 'c': blist([2, 3]), 'index': blist([11, 12])}



.. code:: python

    # exclude the index
    df.to_dict(index=False)




.. parsed-literal::

    {'a': blist([2, 33]), 'c': blist([2, 3])}



.. code:: python

    # return an OrderedDict()
    df.to_dict(ordered=True)




.. parsed-literal::

    OrderedDict([('index', blist([11, 12])),
                 ('a', blist([2, 33])),
                 ('c', blist([2, 3]))])



.. code:: python

    # return a list of just one column
    df['c'].to_list()




.. parsed-literal::

    blist([2, 3])



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
    

Append
------

.. code:: python

    df1 = rc.DataFrame({'a': [1, 2], 'b': [5, 6]}, index=[1, 2])
    df1.print()


.. parsed-literal::

      index    a    b
    -------  ---  ---
          1    1    5
          2    2    6
    

.. code:: python

    df2 = rc.DataFrame({'b': [7, 8], 'c': [11, 12]}, index=[3, 4])
    print(df2)


.. parsed-literal::

      index    c    b
    -------  ---  ---
          3   11    7
          4   12    8
    

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



