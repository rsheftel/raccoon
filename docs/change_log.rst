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
