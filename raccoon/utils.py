"""
Raccoon utilities
"""


def assert_frame_equal(left, right, data_function=None, data_args=None):
    """
    For unit testing equality of two DataFrames.

    :param left: first DataFrame
    :param right: second DataFrame
    :param data_function: if provided will use this function to assert compare the df.data
    :param data_args: arguments to pass to the data_function
    :return: nothing
    """
    if data_function:
        data_args = {} if not data_args else data_args
        data_function(left.data, right.data, **data_args)
    else:
        assert left.data == right.data
    assert left.index == right.index
    assert left.columns == right.columns
    assert left.index_name == right.index_name
    assert left.sorted == right.sorted
    assert left.blist == right.blist
