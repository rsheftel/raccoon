"""
Raccoon utilities
"""


def assert_frame_equal(left, right):
    assert left.data == right.data
    assert left.index == right.index
    assert left.columns == right.columns
