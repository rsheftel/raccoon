import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal
from blist import blist

import sys
PYTHON3 = (sys.version_info >= (3, 0))


def test_sort_index():
    # test on list
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 8, 9], sorted=False)

    df.sort_index()
    assert isinstance(df.index, list)
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'], index=[8, 9, 10],
                                        sorted=False))

    # test on blist
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 8, 9], sorted=False,
                      use_blist=True)

    df.sort_index()
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'], index=[8, 9, 10],
                                        sorted=False, use_blist=True))

    # fails on mixed type columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 'a', 9])
    if PYTHON3:
        with pytest.raises(TypeError):
            df.sort_index()


def test_sort_multi_index():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[(10, 'c'), (10, 'a'), (10, 'b')],
                      sorted=False)

    df.sort_index()
    assert isinstance(df.index, list)
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'],
                                        index=[(10, 'a'), (10, 'b'), (10, 'c')], sorted=False))

    # fails on mixed type columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[(10, 'c'), 'a', (10, 'b')])
    if PYTHON3:
        with pytest.raises(TypeError):
            df.sort_index()


def test_sort_column():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])

    # cannot sort multiple columns
    with pytest.raises(TypeError):
        df.sort_columns(['a', 'b'])

    df.sort_columns('a')
    assert isinstance(df.index, list)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3], 'b': ['c', 'a', 'b']}, columns=['a', 'b'], index=[8, 10, 9]))

    df.sort_columns('b')
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': ['a', 'b', 'c']}, columns=['a', 'b'], index=[10, 9, 8]))

    df.sort_columns('b', reverse=True)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 3, 2], 'b': ['c', 'b', 'a']}, columns=['a', 'b'], index=[8, 9, 10]))

    # test on blist
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9], use_blist=True)

    df.sort_columns('a')
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3], 'b': ['c', 'a', 'b']}, columns=['a', 'b'], index=[8, 10, 9],
                                        use_blist=True))

    df.sort_columns('a', reverse=True)
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [3, 2, 1], 'b': ['b', 'a', 'c']}, columns=['a', 'b'], index=[9, 10, 8],
                                        use_blist=True))
