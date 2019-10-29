Example Usage for Drop-in List Replacements
===========================================

.. code:: python

    # remove comment to use latest development version
    import sys; sys.path.insert(0, '../')

.. code:: python

    # import libraries
    import raccoon as rc

BList
-----

The underlying data structure can be any drop-in replacement for list,
in this example blist is used.

.. code:: python

    from blist import blist

.. code:: python

    # Construct with blist
    df_blist = rc.DataFrame({'a': [1, 2, 3]}, index=[5, 6, 7], dropin=blist)

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

    # the dropin class
    df_blist.dropin




.. parsed-literal::

    blist.blist



All the standard functionality works exactly the same

.. code:: python

    df_blist[6, 'a']




.. parsed-literal::

    2



.. code:: python

    df_blist[8, 'b'] = 44
    print(df_blist)


.. parsed-literal::

      index    a    b
    -------  ---  ---
          5    1
          6    2
          7    3
          8        44
    

Works for Series as well

.. code:: python

    # Construct with blist=True, the default
    srs_blist = rc.Series([1, 2, 3], index=[5, 6, 7], dropin=blist)

.. code:: python

    # see that the data structures are all blists
    srs_blist.data




.. parsed-literal::

    blist([1, 2, 3])



.. code:: python

    srs_blist.index




.. parsed-literal::

    blist([5, 6, 7])


