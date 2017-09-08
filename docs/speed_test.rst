
Raccoon vs. Pandas speed test
=============================

Setup pythonpath, import libraries and initialized DataFrame to store
results

.. code:: ipython3

    # Use this statement to import the current development version
    import sys; sys.path.insert(0, '../')

.. code:: ipython3

    from copy import deepcopy

.. code:: ipython3

    import raccoon as rc
    import pandas as pd

.. code:: ipython3

    results = rc.DataFrame(columns=['raccoon', 'pandas', 'ratio'], sort=False)

.. code:: ipython3

    def add_results(index):
        results[index, 'raccoon'] = res_rc.best
        results[index, 'pandas'] = res_pd.best
        results[index, 'ratio'] = res_rc.best / res_pd.best

.. code:: ipython3

    results['version', 'raccoon'] = rc.__version__
    results['version', 'pandas'] = pd.__version__
    print(results)


.. parsed-literal::

    index    raccoon    pandas    ratio
    -------  ---------  --------  -------
    version  2.1.3      0.20.2
    

Initialize 10,000 empty DataFrames
----------------------------------

.. code:: ipython3

    def init_rc():
        for x in range(10000):
            df = rc.DataFrame()
            
    def init_pd():
        for x in range(10000):
            df = pd.DataFrame()

.. code:: ipython3

    res_rc = %timeit -o init_rc()


.. parsed-literal::

    92.4 ms ± 6.36 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o init_pd()


.. parsed-literal::

    2.74 s ± 234 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('initialize empty')

.. code:: ipython3

    results.show()


.. parsed-literal::

    index             raccoon              pandas                 ratio
    ----------------  -------------------  -----------------  ---------
    version           2.1.3                0.20.2
    initialize empty  0.08496840788127305  2.486505687206119  0.0341718
    

Initialize 100 row X 100 col DataFrame()
----------------------------------------

.. code:: ipython3

    data = dict()
    for x in range(100):
        data['a' + str(x)] = list(range(100))

.. code:: ipython3

    res_rc = %timeit -o df=rc.DataFrame(data=data, sort=False)


.. parsed-literal::

    87.8 µs ± 8.43 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o df=pd.DataFrame(data=data)


.. parsed-literal::

    8.11 ms ± 779 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: ipython3

    add_results('initialize with matrix')

.. code:: ipython3

    results.show()


.. parsed-literal::

    index                   raccoon                pandas                    ratio
    ----------------------  ---------------------  --------------------  ---------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119     0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002  0.0108137
    

Add 10,000 items in 1 column to empty DataFrame
-----------------------------------------------

.. code:: ipython3

    def one_col_add_rc():
        df = rc.DataFrame()
        for x in range(10000):
            df.set(x, 'a', x)
            
    def one_col_add_pd():
        df = pd.DataFrame()
        for x in range(10000):
            df.at[x, 'a'] = x

.. code:: ipython3

    res_rc = %timeit -o one_col_add_rc()


.. parsed-literal::

    43.5 ms ± 402 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o one_col_add_pd()


.. parsed-literal::

    16.2 s ± 1.53 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('add rows one column')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119     0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002  0.0108137
    add rows one column     0.04288183311489533    14.87375424325954     0.00288305
    

Add 100 rows of 100 columns to empty DataFrame
----------------------------------------------

.. code:: ipython3

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

.. code:: ipython3

    res_rc = %timeit -o matrix_add_rc()


.. parsed-literal::

    9.32 ms ± 808 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o matrix_add_pd()


.. parsed-literal::

    184 ms ± 3.55 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('add matrix')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119     0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002  0.0108137
    add rows one column     0.04288183311489533    14.87375424325954     0.00288305
    add matrix              0.008299982997955908   0.1785839394495099    0.0464766
    

Append 10x10 DataFrame 1000 times
---------------------------------

.. code:: ipython3

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

.. code:: ipython3

    res_rc = %timeit -o append_rc()


.. parsed-literal::

    62.2 ms ± 7.32 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o append_pd()


.. parsed-literal::

    164 ms ± 5.16 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('append')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119     0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002  0.0108137
    add rows one column     0.04288183311489533    14.87375424325954     0.00288305
    add matrix              0.008299982997955908   0.1785839394495099    0.0464766
    append                  0.05763429718412851    0.15777540076405216   0.365293
    

Get
---

.. code:: ipython3

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: ipython3

    # get cell
    
    def rc_get_cell():
        for c in df_rc.columns:
            for r in df_rc.index:
                x = df_rc.get(r, c)
                
    def pd_get_cell():
        for c in df_pd.columns:
            for r in df_pd.index:
                x = df_pd.at[r, c]

.. code:: ipython3

    res_rc = %timeit -o rc_get_cell()


.. parsed-literal::

    528 ms ± 64.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    res_pd = %timeit -o pd_get_cell()


.. parsed-literal::

    783 ms ± 74.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('get cell')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                     ratio
    ----------------------  ---------------------  --------------------  ----------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119     0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002  0.0108137
    add rows one column     0.04288183311489533    14.87375424325954     0.00288305
    add matrix              0.008299982997955908   0.1785839394495099    0.0464766
    append                  0.05763429718412851    0.15777540076405216   0.365293
    get cell                0.4936867081052583     0.7425185427150893    0.664881
    

.. code:: ipython3

    # get column all index
    
    def get_column_all_rc():
        for c in df_rc.columns:
            x = df_rc.get(columns=c)
            
    def get_column_all_pd():
        for c in df_pd.columns:
            x = df_pd[c]

.. code:: ipython3

    res_rc = %timeit -o get_column_all_rc()


.. parsed-literal::

    36.6 ms ± 5.38 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o get_column_all_pd()


.. parsed-literal::

    313 µs ± 2.39 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    

.. code:: ipython3

    add_results('get column all index')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                   raccoon                pandas                         ratio
    ----------------------  ---------------------  ----------------------  ------------
    version                 2.1.3                  0.20.2
    initialize empty        0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix  8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column     0.04288183311489533    14.87375424325954         0.00288305
    add matrix              0.008299982997955908   0.1785839394495099        0.0464766
    append                  0.05763429718412851    0.15777540076405216       0.365293
    get cell                0.4936867081052583     0.7425185427150893        0.664881
    get column all index    0.032696135984224384   0.00030877898993577447  105.888
    

.. code:: ipython3

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

.. code:: ipython3

    res_rc = %timeit -o get_column_subset_rc()


.. parsed-literal::

    465 ms ± 51.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    res_pd = %timeit -o get_column_subset_pd()


.. parsed-literal::

    6 s ± 425 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('get column subset index')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    

.. code:: ipython3

    # get index all columns
    
    def get_index_all_rc():
        for i in df_rc.index:
            x = df_rc.get(indexes=i)
            
    def get_index_all_pd():
        for i in df_pd.index:
            x = df_pd.loc[i]

.. code:: ipython3

    res_rc = %timeit -o get_index_all_rc()


.. parsed-literal::

    815 ms ± 73.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    res_pd = %timeit -o get_index_all_pd()


.. parsed-literal::

    118 ms ± 10.4 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    add_results('get index all columns')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    

Set
---

.. code:: ipython3

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: ipython3

    # set cell
    
    def rc_set_cell():
        for c in df_rc.columns:
            for r in df_rc.index:
                df_rc.set(r, c, 99)
                
    def pd_set_cell():
        for c in df_pd.columns:
            for r in df_pd.index:
                df_pd.at[r, c] = 99

.. code:: ipython3

    res_rc = %timeit -o rc_set_cell()


.. parsed-literal::

    436 ms ± 59.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    res_pd = %timeit -o pd_set_cell()


.. parsed-literal::

    1 s ± 78.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('set cell')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    

.. code:: ipython3

    # set column all index
    
    def set_column_all_rc():
        for c in df_rc.columns:
            x = df_rc.set(columns=c, values=99)
            
    def set_column_all_pd():
        for c in df_pd.columns:
            x = df_pd[c] = 99

.. code:: ipython3

    res_rc = %timeit -o set_column_all_rc()


.. parsed-literal::

    4.19 ms ± 748 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o set_column_all_pd()


.. parsed-literal::

    12.7 ms ± 1.02 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: ipython3

    add_results('set column all index')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    

.. code:: ipython3

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

.. code:: ipython3

    res_rc = %timeit -o set_column_subset_rc()


.. parsed-literal::

    269 ms ± 3.72 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    res_pd = %timeit -o set_column_subset_pd()


.. parsed-literal::

    22.7 s ± 244 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('set column subset index')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    

.. code:: ipython3

    row = {x:x for x in grid.keys()}

.. code:: ipython3

    # set index all columns
    
    def set_index_all_rc():
        for i in df_rc.index:
            x = df_rc.set(indexes=i, values=row)
            
    def set_index_all_pd():
        for i in df_pd.index:
            x = df_pd.loc[i] = row

.. code:: ipython3

    res_rc = %timeit -o set_index_all_rc()


.. parsed-literal::

    56.3 ms ± 8.04 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o set_index_all_pd()


.. parsed-literal::

    500 ms ± 80.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('set index all columns')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    set index all columns    0.05272717698682072    0.4621994576302768        0.114079
    

Sort
----

.. code:: ipython3

    # make a dataframe 1000x100 with index in reverse order
    
    rev = list(reversed(range(1000)))
    
    df_rc = rc.DataFrame(data=grid, index=rev)
    df_pd = pd.DataFrame(grid, index=rev)

.. code:: ipython3

    res_rc = %timeit -o df_rc.sort_index() 


.. parsed-literal::

    12.4 ms ± 807 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o df_pd.sort_index()


.. parsed-literal::

    539 µs ± 62.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    

.. code:: ipython3

    add_results('sort index')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    set index all columns    0.05272717698682072    0.4621994576302768        0.114079
    sort index               0.011655945561328736   0.0004977774624292124    23.416
    

Iterators
---------

.. code:: ipython3

    # First create a 1000 row X 100 col matrix for the test. Index is [0...999]
    
    col = [x for x in range(1000)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()))
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: ipython3

    # iterate over the rows
    
    def iter_rc():
        for row in df_rc.iterrows():
            x = row
            
    def iter_pd():
        for row in df_pd.itertuples():
            x = row

.. code:: ipython3

    res_rc = %timeit -o iter_rc() 


.. parsed-literal::

    24.1 ms ± 532 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o iter_pd()


.. parsed-literal::

    20.3 ms ± 599 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    add_results('iterate rows')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    set index all columns    0.05272717698682072    0.4621994576302768        0.114079
    sort index               0.011655945561328736   0.0004977774624292124    23.416
    iterate rows             0.02340574597695877    0.01948813583071569       1.20103
    

Insert in the middle
--------------------

.. code:: ipython3

    # First create a 500 row X 100 col matrix for the test. Index is [1, 3, 5, 7,...500] every other
    
    col = [x for x in range(1, 1000, 2)]
    grid = {'a' + str(x): col[:] for x in range(100)}
    
    df_rc = rc.DataFrame(data=grid, columns=sorted(grid.keys()), sort=True)
    df_pd = pd.DataFrame(data=grid, columns=sorted(grid.keys()))

.. code:: ipython3

    row = {x:x for x in grid.keys()}

.. code:: ipython3

    # set index all columns
    
    def insert_rows_rc():
        for i in range(0, 999, 2):
            x = df_rc.set(indexes=i, values=row)
            
    def insert_rows_pd():
        for i in range(0, 999, 2):
            x = df_pd.loc[i] = row

.. code:: ipython3

    res_rc = %timeit -o insert_rows_rc() 


.. parsed-literal::

    26.4 ms ± 381 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o insert_rows_pd()


.. parsed-literal::

    239 ms ± 2.81 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('insert rows')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    set index all columns    0.05272717698682072    0.4621994576302768        0.114079
    sort index               0.011655945561328736   0.0004977774624292124    23.416
    iterate rows             0.02340574597695877    0.01948813583071569       1.20103
    insert rows              0.025894068785544278   0.2348415172963314        0.110262
    

Time Series Append
------------------

Simulate the recording of a stock on 1 minute intervals and appending to
the DataFrame

.. code:: ipython3

    data_row = {'open': 100, 'high': 101, 'low': 99, 'close': 100.5, 'volume': 999}
    
    dates = pd.date_range('2010-01-01 09:30:00', periods=10000, freq='1min')
    
    def time_series_rc():
        ts = rc.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'], index_name='datetime', sort=True, use_blist=False)
        for date in dates:
            ts.set_row(date, data_row)
    
    def time_series_pd():
        ts = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        for date in dates:
            ts.loc[date] = data_row

.. code:: ipython3

    res_rc = %timeit -o time_series_rc() 


.. parsed-literal::

    114 ms ± 9.01 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

.. code:: ipython3

    res_pd = %timeit -o time_series_pd()


.. parsed-literal::

    27.2 s ± 4 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
    

.. code:: ipython3

    add_results('time series')

.. code:: ipython3

    print(results)


.. parsed-literal::

    index                    raccoon                pandas                         ratio
    -----------------------  ---------------------  ----------------------  ------------
    version                  2.1.3                  0.20.2
    initialize empty         0.08496840788127305    2.486505687206119         0.0341718
    initialize with matrix   8.295801655311905e-05  0.007671599044494002      0.0108137
    add rows one column      0.04288183311489533    14.87375424325954         0.00288305
    add matrix               0.008299982997955908   0.1785839394495099        0.0464766
    append                   0.05763429718412851    0.15777540076405216       0.365293
    get cell                 0.4936867081052583     0.7425185427150893        0.664881
    get column all index     0.032696135984224384   0.00030877898993577447  105.888
    get column subset index  0.42664153398601457    5.714989510943553         0.0746531
    get index all columns    0.7787561018819247     0.10775676991503928       7.22698
    set cell                 0.3987260515496587     0.9623946910782024        0.414306
    set column all index     0.00376809479375936    0.011686656340490344      0.322427
    set column subset index  0.26396186901109786    22.454482046778423        0.0117554
    set index all columns    0.05272717698682072    0.4621994576302768        0.114079
    sort index               0.011655945561328736   0.0004977774624292124    23.416
    iterate rows             0.02340574597695877    0.01948813583071569       1.20103
    insert rows              0.025894068785544278   0.2348415172963314        0.110262
    time series              0.10705897210370949    23.24008671488832         0.00460665
    

