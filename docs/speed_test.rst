
Raccoon vs. Pandas speed test
=============================

Setup pythonpath, import libraries and initialized DataFrame to store results
-----------------------------------------------------------------------------

.. code:: python

    import sys
    sys.path.append("c:/rmbaries/git/raccoon")
    from copy import deepcopy

.. code:: python

    import raccoon as rc
    import pandas as pd

.. code:: python

    results = rc.DataFrame(columns=['raccoon', 'pandas', 'ratio'])

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

    10 loops, best of 3: 38.4 ms per loop
    

.. code:: python

    res_pd = %timeit -o init_pd()


.. parsed-literal::

    1 loop, best of 3: 2.5 s per loop
    

.. code:: python

    ratio = res_rc.best / res_pd.best

.. code:: python

    add_results('initialize empty')

.. code:: python

    results.print()


.. parsed-literal::

    index               raccoon    pandas      ratio
    ----------------  ---------  --------  ---------
    initialize empty  0.0383512   2.50005  0.0153402
    

Initialize 100 row X 100 col DataFrame()
----------------------------------------

.. code:: python

    data = dict()
    for x in range(100):
        data['a' + str(x)] = list(range(100))

.. code:: python

    res_rc = %timeit -o df=rc.DataFrame(data=data)


.. parsed-literal::

    The slowest run took 4.10 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000 loops, best of 3: 179 µs per loop
    

.. code:: python

    res_pd = %timeit -o df=pd.DataFrame(data=data)


.. parsed-literal::

    100 loops, best of 3: 10.5 ms per loop
    

.. code:: python

    add_results('initialize with matrix')

.. code:: python

    results.print()


.. parsed-literal::

    index                       raccoon    pandas      ratio
    ----------------------  -----------  --------  ---------
    initialize empty        0.0383512    2.50005   0.0153402
    initialize with matrix  0.000179355  0.010501  0.0170797
    

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

    1 loop, best of 3: 695 ms per loop
    

.. code:: python

    res_pd = %timeit -o one_col_add_pd()


.. parsed-literal::

    1 loop, best of 3: 22 s per loop
    

.. code:: python

    add_results('add rows one column')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon     pandas      ratio
    ----------------------  -----------  ---------  ---------
    initialize empty        0.0383512     2.50005   0.0153402
    initialize with matrix  0.000179355   0.010501  0.0170797
    add rows one column     0.695244     22.0031    0.0315975
    

Add 100 rows of 100 columns to empty DataFrame
----------------------------------------------

.. code:: python

    new_row = {('a' + str(x)): x for x in range(100)}
    columns = ['a' + str(x) for x in range(100)]
    
    def matrix_add_rc():
        df = rc.DataFrame(columns=columns)
        for x in range(100):
            df.set(index=x, values=new_row)
    
    def matrix_add_pd():
        df = pd.DataFrame(columns=columns)
        for x in range(100):
            df.loc[x] = new_row

.. code:: python

    res_rc = %timeit -o matrix_add_rc()


.. parsed-literal::

    10 loops, best of 3: 7.95 ms per loop
    

.. code:: python

    res_pd = %timeit -o matrix_add_pd()


.. parsed-literal::

    1 loop, best of 3: 200 ms per loop
    

.. code:: python

    add_results('add matrix')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon     pandas      ratio
    ----------------------  -----------  ---------  ---------
    initialize empty        0.0383512     2.50005   0.0153402
    initialize with matrix  0.000179355   0.010501  0.0170797
    add rows one column     0.695244     22.0031    0.0315975
    add matrix              0.00794682    0.199503  0.0398331
    

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

    10 loops, best of 3: 107 ms per loop
    

.. code:: python

    res_pd = %timeit -o append_pd()


.. parsed-literal::

    1 loop, best of 3: 212 ms per loop
    

.. code:: python

    add_results('append')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon     pandas      ratio
    ----------------------  -----------  ---------  ---------
    initialize empty        0.0383512     2.50005   0.0153402
    initialize with matrix  0.000179355   0.010501  0.0170797
    add rows one column     0.695244     22.0031    0.0315975
    add matrix              0.00794682    0.199503  0.0398331
    append                  0.10712       0.212473  0.504158
    

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

    1 loop, best of 3: 1.05 s per loop
    

.. code:: python

    res_pd = %timeit -o pd_get_cell()


.. parsed-literal::

    1 loop, best of 3: 1.12 s per loop
    

.. code:: python

    add_results('get cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon     pandas      ratio
    ----------------------  -----------  ---------  ---------
    initialize empty        0.0383512     2.50005   0.0153402
    initialize with matrix  0.000179355   0.010501  0.0170797
    add rows one column     0.695244     22.0031    0.0315975
    add matrix              0.00794682    0.199503  0.0398331
    append                  0.10712       0.212473  0.504158
    get cell                1.05107       1.12222   0.936592
    

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

    100 loops, best of 3: 11.6 ms per loop
    

.. code:: python

    res_pd = %timeit -o get_column_all_pd()


.. parsed-literal::

    1000 loops, best of 3: 410 µs per loop
    

.. code:: python

    add_results('get column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                       raccoon        pandas       ratio
    ----------------------  -----------  ------------  ----------
    initialize empty        0.0383512     2.50005       0.0153402
    initialize with matrix  0.000179355   0.010501      0.0170797
    add rows one column     0.695244     22.0031        0.0315975
    add matrix              0.00794682    0.199503      0.0398331
    append                  0.10712       0.212473      0.504158
    get cell                1.05107       1.12222       0.936592
    get column all index    0.0116453     0.000409797  28.4172
    

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

    1 loop, best of 3: 1.32 s per loop
    

.. code:: python

    res_pd = %timeit -o get_column_subset_pd()


.. parsed-literal::

    1 loop, best of 3: 7.25 s per loop
    

.. code:: python

    add_results('get column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    

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

    1 loop, best of 3: 742 ms per loop
    

.. code:: python

    res_pd = %timeit -o get_index_all_pd()


.. parsed-literal::

    10 loops, best of 3: 150 ms per loop
    

.. code:: python

    add_results('get index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    

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

    1 loop, best of 3: 987 ms per loop
    

.. code:: python

    res_pd = %timeit -o pd_set_cell()


.. parsed-literal::

    1 loop, best of 3: 1.18 s per loop
    

.. code:: python

    add_results('set cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    set cell                 0.986949      1.17592       0.839302
    

.. code:: python

    # set column all index
    
    def set_column_all_rc():
        for c in df_rc.columns:
            x = df_rc.set(column=c, values=99)
            
    def set_column_all_pd():
        for c in df_pd.columns:
            x = df_pd[c] = 99

.. code:: python

    res_rc = %timeit -o set_column_all_rc()


.. parsed-literal::

    100 loops, best of 3: 4.97 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_column_all_pd()


.. parsed-literal::

    100 loops, best of 3: 19.8 ms per loop
    

.. code:: python

    add_results('set column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    set cell                 0.986949      1.17592       0.839302
    set column all index     0.00496821    0.0198105     0.250786
    

.. code:: python

    # set subset of the index of the column
    
    def set_column_subset_rc():
        for c in df_rc.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 10))
                x = df_rc.set(index=rows, column=c, values=list(range(10)))
            
    def set_column_subset_pd():
        for c in df_pd.columns:
            for r in range(100):
                rows = list(range(r*10, r*10 + 10))
                x = df_pd.loc[rows, c] = list(range(10))

.. code:: python

    res_rc = %timeit -o set_column_subset_rc()


.. parsed-literal::

    1 loop, best of 3: 748 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_column_subset_pd()


.. parsed-literal::

    1 loop, best of 3: 25 s per loop
    

.. code:: python

    add_results('set column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    set cell                 0.986949      1.17592       0.839302
    set column all index     0.00496821    0.0198105     0.250786
    set column subset index  0.747562     24.9955        0.0299078
    

.. code:: python

    row = {x:x for x in grid.keys()}

.. code:: python

    # set index all columns
    
    def set_index_all_rc():
        for i in df_rc.index:
            x = df_rc.set(index=i, values=row)
            
    def set_index_all_pd():
        for i in df_pd.index:
            x = df_pd.loc[i] = row

.. code:: python

    res_rc = %timeit -o set_index_all_rc()


.. parsed-literal::

    10 loops, best of 3: 64.8 ms per loop
    

.. code:: python

    res_pd = %timeit -o set_index_all_pd()


.. parsed-literal::

    1 loop, best of 3: 718 ms per loop
    

.. code:: python

    add_results('set index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    set cell                 0.986949      1.17592       0.839302
    set column all index     0.00496821    0.0198105     0.250786
    set column subset index  0.747562     24.9955        0.0299078
    set index all columns    0.0647692     0.717767      0.0902371
    

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

    100 loops, best of 3: 13.8 ms per loop
    

.. code:: python

    res_pd = %timeit -o df_pd.sort_index()


.. parsed-literal::

    The slowest run took 9.49 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000 loops, best of 3: 1.02 ms per loop
    

.. code:: python

    add_results('sort index')

.. code:: python

    print(results)


.. parsed-literal::

    index                        raccoon        pandas       ratio
    -----------------------  -----------  ------------  ----------
    initialize empty         0.0383512     2.50005       0.0153402
    initialize with matrix   0.000179355   0.010501      0.0170797
    add rows one column      0.695244     22.0031        0.0315975
    add matrix               0.00794682    0.199503      0.0398331
    append                   0.10712       0.212473      0.504158
    get cell                 1.05107       1.12222       0.936592
    get column all index     0.0116453     0.000409797  28.4172
    get column subset index  1.3213        7.2466        0.182333
    get index all columns    0.742481      0.150376      4.93751
    set cell                 0.986949      1.17592       0.839302
    set column all index     0.00496821    0.0198105     0.250786
    set column subset index  0.747562     24.9955        0.0299078
    set index all columns    0.0647692     0.717767      0.0902371
    sort index               0.0137665     0.00101819   13.5206
    
