import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal


def test_sort_index():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 8, 9])

    df.sort_index()
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'], index=[8, 9, 10]))

    # fails on mixed type columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 'a', 9])
    with pytest.raises(TypeError):
        df.sort_index()


def test_sort_column():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])

    # cannot sort multiple columns
    with pytest.raises(TypeError):
        df.sort_columns(['a', 'b'])

    df.sort_columns('a')
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3], 'b': ['c', 'a', 'b']}, columns=['a', 'b'], index=[8, 10, 9]))

    df.sort_columns('b')
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': ['a', 'b', 'c']}, columns=['a', 'b'], index=[10, 9, 8]))

