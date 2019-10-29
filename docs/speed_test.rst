Raccoon vs. Pandas speed test
=============================

Setup pythonpath, import libraries and initialized DataFrame to store
results

.. code:: python

    # Use this statement to import the current development version
    import sys; sys.path.insert(0, '../')

.. code:: python

    from copy import deepcopy

.. code:: python

    import raccoon as rc
    import pandas as pd

Machine information
-------------------

.. code:: python

    import platform
    print(platform.machine())
    print(platform.processor())
    print(platform.platform())
    print("python ", platform.python_version())


.. parsed-literal::

    AMD64
    Intel64 Family 6 Model 142 Stepping 10, GenuineIntel
    Windows-10-10.0.18362-SP0
    python  3.7.4
    

Run the Speed Test
------------------

.. code:: python

    results = rc.DataFrame(columns=['raccoon', 'pandas', 'ratio'], sort=False)

.. code:: python

    def add_results(index):
        results[index, 'raccoon'] = res_rc.best
        results[index, 'pandas'] = res_pd.best
        results[index, 'ratio'] = res_rc.best / res_pd.best

.. code:: python

    results['version', 'raccoon'] = rc.__version__
    results['version', 'pandas'] = pd.__version__
    print(results)


.. parsed-literal::

    index    raccoon    pandas    ratio
    -------  ---------  --------  -------
    version  3.0.0      0.25.2
    

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

    88.7 ms ± 6.1 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o init_pd()


.. parsed-literal::

    4.49 s ± 155 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('initialize empty')

.. code:: python

    results.print()


.. parsed-literal::

    index             raccoon              pandas                 ratio
    ----------------  -------------------  -----------------  ---------
    version           3.0.0                0.25.2
    initialize empty  0.08248082999998588  4.237655099999756  0.0194638
    

Initialize 100 row X 100 col DataFrame()
----------------------------------------

.. code:: python

    data = dict()
    for x in range(100):
        data['a' + str(x)] = list(range(100))

.. code:: python

    res_rc = %timeit -o df=rc.DataFrame(data=data, sort=False)


.. parsed-literal::

    121 µs ± 7.92 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    

.. code:: python

    res_pd = %timeit -o df=pd.DataFrame(data=data)


.. parsed-literal::

    15.3 ms ± 279 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: python

    add_results('initialize with matrix')

.. code:: python

    results.print()


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756     0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878  0.00757611
    

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

    53.7 ms ± 2.67 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o one_col_add_pd()


.. parsed-literal::

    17.1 s ± 193 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('add rows one column')

.. code:: python

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756     0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878  0.00757611
    add rows one column     0.050407570000015764   16.86793469999975     0.00298837
    

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

    10 ms ± 185 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: python

    res_pd = %timeit -o matrix_add_pd()


.. parsed-literal::

    296 ms ± 4.94 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('add matrix')

.. code:: python

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756     0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878  0.00757611
    add rows one column     0.050407570000015764   16.86793469999975     0.00298837
    add matrix              0.009786346000000777   0.28846930000008797   0.0339251
    

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

    77.5 ms ± 3.77 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o append_pd()


.. parsed-literal::

    370 ms ± 19.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('append')

.. code:: python

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756     0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878  0.00757611
    add rows one column     0.050407570000015764   16.86793469999975     0.00298837
    add matrix              0.009786346000000777   0.28846930000008797   0.0339251
    append                  0.07348676999999952    0.346767699999873     0.211919
    

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

    718 ms ± 45.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    res_pd = %timeit -o pd_get_cell()


.. parsed-literal::

    1.02 s ± 71.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('get cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756     0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878  0.00757611
    add rows one column     0.050407570000015764   16.86793469999975     0.00298837
    add matrix              0.009786346000000777   0.28846930000008797   0.0339251
    append                  0.07348676999999952    0.346767699999873     0.211919
    get cell                0.6728431999999884     0.9376910000000862    0.717553
    

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

    42.8 ms ± 743 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o get_column_all_pd()


.. parsed-literal::

    402 µs ± 24.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    

.. code:: python

    add_results('get column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                        ratio
    ----------------------  ---------------------  ---------------------  ------------
    version                 3.0.0                  0.25.2
    initialize empty        0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix  0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column     0.050407570000015764   16.86793469999975        0.00298837
    add matrix              0.009786346000000777   0.28846930000008797      0.0339251
    append                  0.07348676999999952    0.346767699999873        0.211919
    get cell                0.6728431999999884     0.9376910000000862       0.717553
    get column all index    0.041298069999993456   0.0003524336000000403  117.18
    

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

    609 ms ± 62.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    res_pd = %timeit -o get_column_subset_pd()


.. parsed-literal::

    7.1 s ± 40.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('get column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    

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

    1.07 s ± 27.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    res_pd = %timeit -o get_index_all_pd()


.. parsed-literal::

    229 ms ± 9.34 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('get index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    

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

    578 ms ± 33.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    res_pd = %timeit -o pd_set_cell()


.. parsed-literal::

    1.36 s ± 65.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('set cell')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    

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

    5.84 ms ± 512 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: python

    res_pd = %timeit -o set_column_all_pd()


.. parsed-literal::

    17.2 ms ± 516 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: python

    add_results('set column all index')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    

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

    380 ms ± 7.21 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    res_pd = %timeit -o set_column_subset_pd()


.. parsed-literal::

    59 s ± 732 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('set column subset index')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    

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

    64.4 ms ± 513 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o set_index_all_pd()


.. parsed-literal::

    1.41 s ± 15.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('set index all columns')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    set index all columns    0.06374265999997988    1.390037300000131        0.0458568
    

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

    16 ms ± 953 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: python

    res_pd = %timeit -o df_pd.sort_index()


.. parsed-literal::

    859 µs ± 12.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    

.. code:: python

    add_results('sort index')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    set index all columns    0.06374265999997988    1.390037300000131        0.0458568
    sort index               0.014900102999999944   0.0008343847000001006   17.8576
    

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

    27.2 ms ± 381 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o iter_pd()


.. parsed-literal::

    34 ms ± 532 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    add_results('iterate rows')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    set index all columns    0.06374265999997988    1.390037300000131        0.0458568
    sort index               0.014900102999999944   0.0008343847000001006   17.8576
    iterate rows             0.026519559999997      0.03318497000000207      0.799144
    

Insert in the middle
--------------------

.. code:: python

    # First create a 500 row X 100 col matrix for the test. Index is [1, 3, 5, 7,...500] every other
    
    col = [x for x in range(1, 1000, 2)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()), sort=True)
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

    33 ms ± 3.08 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o insert_rows_pd()


.. parsed-literal::

    723 ms ± 30.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('insert rows')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    set index all columns    0.06374265999997988    1.390037300000131        0.0458568
    sort index               0.014900102999999944   0.0008343847000001006   17.8576
    iterate rows             0.026519559999997      0.03318497000000207      0.799144
    insert rows              0.030685470000025816   0.6862636999999268       0.0447138
    

Time Series Append
------------------

Simulate the recording of a stock on 1 minute intervals and appending to
the DataFrame

.. code:: python

    data_row = {'open': 100, 'high': 101, 'low': 99, 'close': 100.5, 'volume': 999}
    
    dates = pd.date_range('2010-01-01 09:30:00', periods=10000, freq='1min')
    
    def time_series_rc():
        ts = rc.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'], index_name='datetime', sort=True)
        for date in dates:
            ts.set_row(date, data_row)
    
    def time_series_pd():
        ts = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        for date in dates:
            ts.loc[date] = data_row

.. code:: python

    res_rc = %timeit -o time_series_rc() 


.. parsed-literal::

    134 ms ± 4.28 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: python

    res_pd = %timeit -o time_series_pd()


.. parsed-literal::

    29.4 s ± 124 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: python

    add_results('time series')

.. code:: python

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                        ratio
    -----------------------  ---------------------  ---------------------  ------------
    version                  3.0.0                  0.25.2
    initialize empty         0.08248082999998588    4.237655099999756        0.0194638
    initialize with matrix   0.0001130529800000204  0.014922300999996878     0.00757611
    add rows one column      0.050407570000015764   16.86793469999975        0.00298837
    add matrix               0.009786346000000777   0.28846930000008797      0.0339251
    append                   0.07348676999999952    0.346767699999873        0.211919
    get cell                 0.6728431999999884     0.9376910000000862       0.717553
    get column all index     0.041298069999993456   0.0003524336000000403  117.18
    get column subset index  0.5668462000003274     7.041264400000273        0.0805035
    get index all columns    1.0389918000000762     0.2065747999999985       5.02962
    set cell                 0.5282995000002302     1.26670009999998         0.417068
    set column all index     0.00548794899999848    0.01662835399999949      0.330036
    set column subset index  0.37289839999994       58.03955229999974        0.0064249
    set index all columns    0.06374265999997988    1.390037300000131        0.0458568
    sort index               0.014900102999999944   0.0008343847000001006   17.8576
    iterate rows             0.026519559999997      0.03318497000000207      0.799144
    insert rows              0.030685470000025816   0.6862636999999268       0.0447138
    time series              0.13054121000000124    29.182044600000154       0.00447334
    

