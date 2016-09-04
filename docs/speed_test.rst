
Raccoon vs. Pandas speed test
=============================

Setup pythonpath, import libraries and initialized DataFrame to store
results

.. code:: python

    import sys
    from copy import deepcopy

.. code:: python

    import raccoon as rc
    import pandas as pd

.. code:: python

    results = rc.DataFrame(columns=['raccoon', 'pandas', 'ratio'], sorted=False)

.. code:: python

    def add_results(index):
        results[index, 'raccoon'] = res_rc.best
        results[index, 'pandas'] = res_pd.best
        results[index, 'ratio'] = res_rc.best / res_pd.best

Initialize 10,000 empty DataFrames
----------------------------------

.. code:: python

    def init_rc():
        for x in range(10000):
            df = rc.DataFrame()
            
    def init_pd():
        for x in range(10000):
            df = pd.DataFrame()

.. code:: python

    res_rc = %timeit -o init_rc()


.. parsed-literal::

    10 loops, best of 3: 86.3 ms per loop
    

.. code:: python

    res_pd = %timeit -o init_pd()


.. parsed-literal::

    1 loop, best of 3: 2.67 s per loop
    

.. code:: python

    add_results('initialize empty')

.. code:: python

    results.print()


.. parsed-literal::

    index               raccoon    pandas      ratio
    ----------------  ---------  --------  ---------
    initialize empty  0.0862797   2.67235  0.0322861
    

Initialize 100 row X 100 col DataFrame()
----------------------------------------

.. code:: python

    data = dict()
    for x in range(100):
        data['a' + str(x)] = list(range(100))

.. code:: python

    res_rc = %timeit -o df=rc.DataFrame(data=data, sorted=False)


.. parsed-literal::

    10000 loops, best of 3: 173 µs per loop
    

.. code:: python

    res_pd = %timeit -o df=pd.DataFrame(data=data)


.. parsed-literal::

    100 loops, best of 3: 9.69 ms per loop
    

.. code:: python

    add_results('initialize with matrix')

.. code:: python

    results.print()


.. parsed-literal::

    index                       raccoon      pandas      ratio
    ----------------------  -----------  ----------  ---------
    initialize empty        0.0862797    2.67235     0.0322861
    initialize with matrix  0.000173366  0.00969091  0.0178896
    

Add 10,000 items in 1 column to empty DataFrame
-----------------------------------------------

.. code:: python

    def one_col_add_rc():
        df = rc.DataFrame()
        for x in range(10000):
            df.set(x, 'a', x)
            
    def one_col_add_pd():
        df = pd.DataFrame()
        for x in range(10000):
            df.at[x, 'a'] = x

.. code:: python

    res_rc = %timeit -o one_col_add_rc()


.. parsed-literal::

    10 loops, best of 3: 53 ms per loop
    

.. code:: python

    res_pd = %timeit -o one_col_add_pd()


.. parsed-literal::

    1 loop, best of 3: 20.9 s per loop
    

.. code:: python

    add_results('add rows one column')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon       pandas       ratio
    ----------------------  -----------  -----------  ----------
    initialize empty        0.0862797     2.67235     0.0322861
    initialize with matrix  0.000173366   0.00969091  0.0178896
    add rows one column     0.0530035    20.9206      0.00253355
    

Add 100 rows of 100 columns to empty DataFrame
----------------------------------------------

.. code:: python

    new_row = {('a' + str(x)): x for x in range(100)}
    columns = ['a' + str(x) for x in range(100)]
    
    def matrix_add_rc():
        df = rc.DataFrame(columns=columns)
        for x in range(100):
            df.set(indexes=x, values=new_row)
    
    def matrix_add_pd():
        df = pd.DataFrame(columns=columns)
        for x in range(100):
            df.loc[x] = new_row

.. code:: python

    res_rc = %timeit -o matrix_add_rc()


.. parsed-literal::

    100 loops, best of 3: 7.87 ms per loop
    

.. code:: python

    res_pd = %timeit -o matrix_add_pd()


.. parsed-literal::

    1 loop, best of 3: 205 ms per loop
    

.. code:: python

    add_results('add matrix')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon       pandas       ratio
    ----------------------  -----------  -----------  ----------
    initialize empty        0.0862797     2.67235     0.0322861
    initialize with matrix  0.000173366   0.00969091  0.0178896
    add rows one column     0.0530035    20.9206      0.00253355
    add matrix              0.00786965    0.2049      0.0384073
    

Append 10x10 DataFrame 1000 times
---------------------------------

.. code:: python

    def append_rc():
        grid = {'a' + str(x): [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for x in range(10)}
        df = rc.DataFrame(data=deepcopy(grid), columns=list(grid.keys()))
        for x in range(100):
            index = [(y + 1) + (x + 1) * 10 for y in range(10)]
            new_grid = deepcopy(grid)
            new_df = rc.DataFrame(data=new_grid, columns=list(new_grid.keys()), index=index)
            df.append(new_df)
    
    def append_pd():
        grid = {'a' + str(x): [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for x in range(10)}
        df = pd.DataFrame(data=grid, columns=list(grid.keys()))
        for x in range(100):
            index = [(y + 1) + (x + 1) * 10 for y in range(10)]
            new_grid = deepcopy(grid)
            new_df = pd.DataFrame(data=new_grid, columns=list(new_grid.keys()), index=index)
            df = df.append(new_df)

.. code:: python

    res_rc = %timeit -o append_rc()


.. parsed-literal::

    10 loops, best of 3: 67.2 ms per loop
    

.. code:: python

    res_pd = %timeit -o append_pd()


.. parsed-literal::

    1 loop, best of 3: 175 ms per loop
    

.. code:: python

    add_results('append')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon       pandas       ratio
    ----------------------  -----------  -----------  ----------
    initialize empty        0.0862797     2.67235     0.0322861
    initialize with matrix  0.000173366   0.00969091  0.0178896
    add rows one column     0.0530035    20.9206      0.00253355
    add matrix              0.00786965    0.2049      0.0384073
    append                  0.0672455     0.175002    0.384256
    

Get
---

.. code:: python

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: python

    # get cell
    
    def rc_get_cell():
        for c in df_rc.columns:
            for r in df_rc.index:
                x = df_rc.get(r, c)
                
    def pd_get_cell():
        for c in df_pd.columns:
            for r in df_pd.index:
                x = df_pd.at[r, c]

.. code:: python

    res_rc = %timeit -o rc_get_cell()


.. parsed-literal::

    1 loop, best of 3: 797 ms per loop
    

.. code:: python

    res_pd = %timeit -o pd_get_cell()


.. parsed-literal::

    1 loop, best of 3: 976 ms per loop
    

.. code:: python

    add_results('get cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon       pandas       ratio
    ----------------------  -----------  -----------  ----------
    initialize empty        0.0862797     2.67235     0.0322861
    initialize with matrix  0.000173366   0.00969091  0.0178896
    add rows one column     0.0530035    20.9206      0.00253355
    add matrix              0.00786965    0.2049      0.0384073
    append                  0.0672455     0.175002    0.384256
    get cell                0.797316      0.97588     0.817023
    

.. code:: python

    # get column all index
    
    def get_column_all_rc():
        for c in df_rc.columns:
            x = df_rc.get(columns=c)
            
    def get_column_all_pd():
        for c in df_pd.columns:
            x = df_pd[c]

.. code:: python

    res_rc = %timeit -o get_column_all_rc()


.. parsed-literal::

    10 loops, best of 3: 42.5 ms per loop
    

.. code:: python

    res_pd = %timeit -o get_column_all_pd()


.. parsed-literal::

    1000 loops, best of 3: 305 µs per loop
    

.. code:: python

    add_results('get column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon        pandas         ratio
    ----------------------  -----------  ------------  ------------
    initialize empty        0.0862797     2.67235        0.0322861
    initialize with matrix  0.000173366   0.00969091     0.0178896
    add rows one column     0.0530035    20.9206         0.00253355
    add matrix              0.00786965    0.2049         0.0384073
    append                  0.0672455     0.175002       0.384256
    get cell                0.797316      0.97588        0.817023
    get column all index    0.0424636     0.000304916  139.263
    

.. code:: python

    # get subset of the index of the column
    
    def get_column_subset_rc():
        for c in df_rc.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 9))
                x = df_rc.get(indexes=rows, columns=c)
            
    def get_column_subset_pd():
        for c in df_pd.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 9))
                x = df_pd.loc[rows, c]

.. code:: python

    res_rc = %timeit -o get_column_subset_rc()


.. parsed-literal::

    1 loop, best of 3: 711 ms per loop
    

.. code:: python

    res_pd = %timeit -o get_column_subset_pd()


.. parsed-literal::

    1 loop, best of 3: 7.04 s per loop
    

.. code:: python

    add_results('get column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    

.. code:: python

    # get index all columns
    
    def get_index_all_rc():
        for i in df_rc.index:
            x = df_rc.get(indexes=i)
            
    def get_index_all_pd():
        for i in df_pd.index:
            x = df_pd.loc[i]

.. code:: python

    res_rc = %timeit -o get_index_all_rc()


.. parsed-literal::

    1 loop, best of 3: 819 ms per loop
    

.. code:: python

    res_pd = %timeit -o get_index_all_pd()


.. parsed-literal::

    10 loops, best of 3: 139 ms per loop
    

.. code:: python

    add_results('get index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    

Set
---

.. code:: python

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: python

    # set cell
    
    def rc_set_cell():
        for c in df_rc.columns:
            for r in df_rc.index:
                df_rc.set(r, c, 99)
                
    def pd_set_cell():
        for c in df_pd.columns:
            for r in df_pd.index:
                df_pd.at[r, c] = 99

.. code:: python

    res_rc = %timeit -o rc_set_cell()


.. parsed-literal::

    1 loop, best of 3: 686 ms per loop
    

.. code:: python

    res_pd = %timeit -o pd_set_cell()


.. parsed-literal::

    1 loop, best of 3: 1.12 s per loop
    

.. code:: python

    add_results('set cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    

.. code:: python

    # set column all index
    
    def set_column_all_rc():
        for c in df_rc.columns:
            x = df_rc.set(columns=c, values=99)
            
    def set_column_all_pd():
        for c in df_pd.columns:
            x = df_pd[c] = 99

.. code:: python

    res_rc = %timeit -o set_column_all_rc()


.. parsed-literal::

    100 loops, best of 3: 4.89 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_column_all_pd()


.. parsed-literal::

    100 loops, best of 3: 14.9 ms per loop
    

.. code:: python

    add_results('set column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    

.. code:: python

    # set subset of the index of the column
    
    def set_column_subset_rc():
        for c in df_rc.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 10))
                x = df_rc.set(indexes=rows, columns=c, values=list(range(10)))
            
    def set_column_subset_pd():
        for c in df_pd.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 10))
                x = df_pd.loc[rows, c] = list(range(10))

.. code:: python

    res_rc = %timeit -o set_column_subset_rc()


.. parsed-literal::

    1 loop, best of 3: 514 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_column_subset_pd()


.. parsed-literal::

    1 loop, best of 3: 25.5 s per loop
    

.. code:: python

    add_results('set column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    

.. code:: python

    row = {x:x for x in grid.keys()}

.. code:: python

    # set index all columns
    
    def set_index_all_rc():
        for i in df_rc.index:
            x = df_rc.set(indexes=i, values=row)
            
    def set_index_all_pd():
        for i in df_pd.index:
            x = df_pd.loc[i] = row

.. code:: python

    res_rc = %timeit -o set_index_all_rc()


.. parsed-literal::

    10 loops, best of 3: 64.3 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_index_all_pd()


.. parsed-literal::

    1 loop, best of 3: 599 ms per loop
    

.. code:: python

    add_results('set index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    set index all columns    0.0643082     0.599027       0.107354
    

Sort
----

.. code:: python

    # make a dataframe 1000x100 with index in reverse order
    
    rev = list(reversed(range(1000)))
    
    df_rc = rc.DataFrame(data=grid, index=rev)
    df_pd = pd.DataFrame(grid, index=rev)

.. code:: python

    res_rc = %timeit -o df_rc.sort_index() 


.. parsed-literal::

    100 loops, best of 3: 12.6 ms per loop
    

.. code:: python

    res_pd = %timeit -o df_pd.sort_index()


.. parsed-literal::

    The slowest run took 10.73 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000 loops, best of 3: 711 µs per loop
    

.. code:: python

    add_results('sort index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    set index all columns    0.0643082     0.599027       0.107354
    sort index               0.012594      0.000711006   17.7129
    

Iterators
---------

.. code:: python

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: python

    # iterate over the rows
    
    def iter_rc():
        for row in df_rc.iterrows():
            x = row
            
    def iter_pd():
        for row in df_pd.itertuples():
            x = row

.. code:: python

    res_rc = %timeit -o iter_rc() 


.. parsed-literal::

    10 loops, best of 3: 23.6 ms per loop
    

.. code:: python

    res_pd = %timeit -o iter_pd()


.. parsed-literal::

    10 loops, best of 3: 22.7 ms per loop
    

.. code:: python

    add_results('iterate rows')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    set index all columns    0.0643082     0.599027       0.107354
    sort index               0.012594      0.000711006   17.7129
    iterate rows             0.0236283     0.0227241      1.03979
    

Insert in the middle
--------------------

.. code:: python

    # First create a 500 row X 100 col matrix for the test. Index is [1, 3, 5, 7,...500] every other
    
    col = [x for x in range(1, 1000, 2)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()), sorted=True)
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: python

    row = {x:x for x in grid.keys()}

.. code:: python

    # set index all columns
    
    def insert_rows_rc():
        for i in range(0, 999, 2):
            x = df_rc.set(indexes=i, values=row)
            
    def insert_rows_pd():
        for i in range(0, 999, 2):
            x = df_pd.loc[i] = row

.. code:: python

    res_rc = %timeit -o insert_rows_rc() 


.. parsed-literal::

    10 loops, best of 3: 44.6 ms per loop
    

.. code:: python

    res_pd = %timeit -o insert_rows_pd()


.. parsed-literal::

    The slowest run took 23.98 times longer than the fastest. This could mean that an intermediate result is being cached.
    1 loop, best of 3: 280 ms per loop
    

.. code:: python

    add_results('insert rows')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    set index all columns    0.0643082     0.599027       0.107354
    sort index               0.012594      0.000711006   17.7129
    iterate rows             0.0236283     0.0227241      1.03979
    insert rows              0.0446384     0.279826       0.159522
    

Time Series Append
------------------

Simulate the recording of a stock on 1 minute intervals and appending to
the DataFrame

.. code:: python

    data_row = {'open': 100, 'high': 101, 'low': 99, 'close': 100.5, 'volume': 999}
    
    dates = pd.date_range('2010-01-01 09:30:00', periods=10000, freq='1min')
    
    def time_series_rc():
        ts = rc.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'], index_name='datetime', sorted=True,
                          use_blist=False)
        for date in dates:
            ts.set_row(date, data_row)
    
    def time_series_pd():
        ts = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        for date in dates:
            ts.loc[date] = data_row

.. code:: python

    res_rc = %timeit -o time_series_rc() 


.. parsed-literal::

    10 loops, best of 3: 127 ms per loop
    

.. code:: python

    res_pd = %timeit -o time_series_pd()


.. parsed-literal::

    1 loop, best of 3: 30.6 s per loop
    

.. code:: python

    add_results('time series')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas         ratio
    -----------------------  -----------  ------------  ------------
    initialize empty         0.0862797     2.67235        0.0322861
    initialize with matrix   0.000173366   0.00969091     0.0178896
    add rows one column      0.0530035    20.9206         0.00253355
    add matrix               0.00786965    0.2049         0.0384073
    append                   0.0672455     0.175002       0.384256
    get cell                 0.797316      0.97588        0.817023
    get column all index     0.0424636     0.000304916  139.263
    get column subset index  0.711387      7.04383        0.100994
    get index all columns    0.818751      0.138998       5.89036
    set cell                 0.685851      1.11982        0.612463
    set column all index     0.00489008    0.0148631      0.329008
    set column subset index  0.514223     25.5079         0.0201594
    set index all columns    0.0643082     0.599027       0.107354
    sort index               0.012594      0.000711006   17.7129
    iterate rows             0.0236283     0.0227241      1.03979
    insert rows              0.0446384     0.279826       0.159522
    time series              0.126713     30.5804         0.00414359
    
