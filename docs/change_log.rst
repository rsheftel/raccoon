Change Log
==========

1.0.1
~~~~~
- Added isin() method

1.0.2
~~~~~
- Fixed several small bugs
- Added iterators: iterrows() and itertuples()

1.1.0
~~~~~
- Multiple bug fixes
- Speed improvements
- Removed using slices to set values which did not work
- Added sorted functionality

1.1.1
~~~~~
- Multiple bug fixes
- The index and columns data type follow the use_blist parameter
- Added set_locations() and get_locations() methods
- Added as_dict() parameter to get_columns()

1.1.2
~~~~~
- Changed the default for use_blist to False on object initialization

1.1.3
~~~~~
- Added append_row() method

1.1.4
~~~~~
- Added get_entire_column() method and changed get() to use that when asking for only a single column

1.1.5
~~~~~
- Bug fix where df[[columns]] would return wrong results with the column names not matching the correct column data

1.1.6
~~~~~
- Added index parameter to iterrows() and itertuples()

1.1.7
~~~~~
- Added reset_index() method

1.1.8
~~~~~
- Added methods to serialize and deserialize to JSON

1.1.9 (3/7/17)
~~~~~~~~~~~~~~
- Fixed the from_json() for multi-index DataFrames

1.2 (3/8/17)
~~~~~~~~~~~~
- to_json() will convert any non-serializable object to string representation
- Move to new version numbering scheme

1.2.1 (3/8/17)
~~~~~~~~~~~~~~
- bug fix from_json() to work with empty DataFrames

1.2.2 (3/10/17)
~~~~~~~~~~~~~~~
- Added the ability to pass a function and arguments to the assert_frame_equal function to use when comparing data

1.3 (3/26/17)
~~~~~~~~~~~~~
- Added `Python2.7 support <https://github.com/rsheftel/raccoon/pull/4>`_  thanks to `tonycpsu <https://github.com/tonycpsu>`_
- Fixed some logic set_column index check https://github.com/rsheftel/raccoon/issues/5
- Changed method .print() to .show() for Python2 compliance

1.3.1 (3/30/17)
~~~~~~~~~~~~~~~
- Added reverse argument to sort_columns()

1.3.2 (3/31/17)
~~~~~~~~~~~~~~~
- Added key argument to sort_columns()

1.3.3 (4/9/17)
~~~~~~~~~~~~~~
- Moved from_json() to be a class method. This breaks previous API

1.3.4 (4/12/17)
~~~~~~~~~~~~~~~
- Added new get_location() method
- The get() method can now take as_dict parameter to pass to get_columns

1.3.5 (4/22/17)
~~~~~~~~~~~~~~~
- Added new get_index() method
- Several speed up improvements

2.0.0 (5/1/17)
~~~~~~~~~~~~~~
This is a major release that adds the new Series classes but importantly breaks the DataFrame API by renaming the
"sorted" argument with "sort" and all associated properties and setters. This is to remove the naming conflict with
the builtin sorted function

- Added new Series class
- Added new ViewSeries class
- Fix performance bug in the select_index() function in DataFrame
- Change sorted argument on DataFrame to sort
- Change sorted DataFrame property and setters to sort

2.1.0 (5/12/17)
~~~~~~~~~~~~~~~
Another potentially backwards incompatible change by making the .index properties to be a view and no longer a copy.

DataFrame

- Changes the DataFrame.index to return a view and not a copy.
- New get_slice() method for sorted DataFrames
- Changed [] on sort DataFrames to use get_slice() on slices
- New set_location() method for DataFrame
- New append_rows() method for DataFrame

Series

- Changed the Series.data and Series.index properties to return a view and not a copy
- New get_slice() method for sorted Series
- New set_location() method
- New append_rows() method for Series

2.1.1 (5/15/17)
~~~~~~~~~~~~~~~
- Added columns=None default to get_column() on DataFrame
- Fix bug in get_slice for empty DataFrames
- Fix bug in DataFrame append for empty DataFrames

2.1.2 (5/20/17)
~~~~~~~~~~~~~~~
- Added delete_all_rows() to DataFrame

2.1.3 (9/5/17)
~~~~~~~~~~~~~~~
- Added from_series() to ViewSeries to create a ViewSeries from a Series

2.1.4 (9/12/17)
~~~~~~~~~~~~~~~
- Made dataframe and all Series __slots__ classes. This should reduce memory footprint and increase speed ~5%

2.1.5 (12/30/17)
~~~~~~~~~~~~~~~~
- get_location() method of DataFrame will now return single value if single column argument passed and not list
