
Convert to and from Pandas DataFrames
=====================================

There are no built in methods for the conversions but these functions
below should work in most basic instances.

.. code:: python

    import raccoon as rc
    import pandas as pd

Raccoon to Pandas
-----------------

.. code:: python

    def rc_to_pd(raccoon_dataframe):
        """
        Convert a raccoon dataframe to pandas dataframe
    
        :param raccoon_dataframe: raccoon DataFrame
        :return: pandas DataFrame
        """
        data_dict = raccoon_dataframe.to_dict(index=False)
        return pd.DataFrame(data_dict, columns=raccoon_dataframe.columns, index=raccoon_dataframe.index)

.. code:: python

    rc_df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[7, 8, 9])
    print(type(rc_df))
    print(rc_df)


.. parsed-literal::

    <class 'raccoon.dataframe.DataFrame'>
      index    a    b
    -------  ---  ---
          7    1    4
          8    2    5
          9    3    6
    

.. code:: python

    pd_df = rc_to_pd(rc_df)
    print(type(pd_df))
    print(pd_df)


.. parsed-literal::

    <class 'pandas.core.frame.DataFrame'>
       a  b
    7  1  4
    8  2  5
    9  3  6
    

Pandas to Raccoon
-----------------

.. code:: python

    def pd_to_rc(pandas_dataframe):
        """
        Convert a pandas dataframe to raccoon dataframe
    
        :param pandas_dataframe: pandas DataFrame
        :return: raccoon DataFrame
        """
    
        columns = pandas_dataframe.columns.tolist()
        data = dict()
        pandas_data = pandas_dataframe.values.T.tolist()
        for i in range(len(columns)):
            data[columns[i]] = pandas_data[i]
        index = pandas_dataframe.index.tolist()
        index_name = pandas_dataframe.index.name
        index_name = 'index' if not index_name else index_name
        return rc.DataFrame(data=data, columns=columns, index=index, index_name=index_name)

.. code:: python

    pd_df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[5, 6, 7], columns=['a', 'b'])
    print(type(pd_df))
    print(pd_df)


.. parsed-literal::

    <class 'pandas.core.frame.DataFrame'>
       a  b
    5  1  4
    6  2  5
    7  3  6
    

.. code:: python

    rc_df = pd_to_rc(pd_df)
    print(type(rc_df))
    print(rc_df)


.. parsed-literal::

    <class 'raccoon.dataframe.DataFrame'>
      index    a    b
    -------  ---  ---
          5    1    4
          6    2    5
          7    3    6
    
