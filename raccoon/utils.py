"""
Raccoon utilities
"""


def assert_frame_equal(left, right):
    """
    For unit testing equality of two DataFrames.

    :param left: first DataFrame
    :param right: second DataFrame
    :return: nothing
    """
    assert left.data == right.data
    assert left.index == right.index
    assert left.columns == right.columns
    assert left.index_name == right.index_name
