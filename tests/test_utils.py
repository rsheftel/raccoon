"""
unit tests for utils module
"""

import raccoon as rc
from raccoon.utils import assert_frame_equal
import pytest


def test_assert_frame_equal():
    df1 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3])
    assert_frame_equal(df1, df1)

    df2 = rc.DataFrame({'a': [1, 1, 1], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['b', 'a'], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[11, 12, 13])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3], use_blist=False)
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3], sorted=True)
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)
