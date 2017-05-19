import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal


def test_delete_row():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    df.delete_rows(['a', 'c'])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b']))

    df.delete_rows('b')
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a'], sort=False))

    # insert back in data
    df[1, 'a'] = 9
    assert df.data == [[None], [9]]

    df[2, 'b'] = 8
    assert df.data == [[None, 8], [9, None]]

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    # cannot delete values not in index
    with pytest.raises(ValueError):
        df.delete_rows(['bad'])

    # length of boolean must be len of index
    with pytest.raises(ValueError):
        df.delete_rows([True, False])

    df.delete_rows([True, False, True])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b']))

    df.delete_rows([True])
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a'], sort=False))


def test_delete_row_sorted():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'],
                      sort=True, use_blist=False)

    df.delete_rows(['a', 'c'])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b'],
                                        sort=True, use_blist=False))

    df.delete_rows('b')
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a'], sort=True, use_blist=False))

    # insert back in data
    df[1, 'a'] = 9
    assert df.data == [[None], [9]]

    df[2, 'b'] = 8
    assert df.data == [[None, 8], [9, None]]

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    # cannot delete values not in index
    with pytest.raises(ValueError):
        df.delete_rows(['bad'])

    # length of boolean must be len of index
    with pytest.raises(ValueError):
        df.delete_rows([True, False])

    df.delete_rows([True, False, True])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b']))

    df.delete_rows([True])
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a'], sort=False))


def test_delete_all_rows():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    link_col = df.get_entire_column('b', as_list=True)
    link_index = df.index

    df.delete_all_rows()
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a'], sort=False))

    assert link_col == []
    assert link_index == []


def test_delete_columns():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, columns=['a', 'b', 'c'])

    # cannot delete bad column
    with pytest.raises(ValueError):
        df.delete_columns(['bad', 'a'])

    df.delete_columns(['a', 'c'])
    assert_frame_equal(df, rc.DataFrame({'b': [4, 5, 6]}))
    assert df.index == [0, 1, 2]

    # insert some data back in
    df[1, 'a'] = 77
    assert df.data == [[4, 5, 6], [None, 77, None]]

    df.delete_columns(['b', 'a'])
    assert_frame_equal(df, rc.DataFrame())
    assert df.columns == []
    assert df.index == []

    # insert some data back in, fresh columns and index
    df[1, 'e'] = 77
    assert df.data == [[77]]
