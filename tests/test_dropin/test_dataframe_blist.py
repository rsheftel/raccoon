import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal

try:
    from blist import blist
except ImportError:
    pytest.skip("blist is not installed, skipping tests.", allow_module_level=True)


def test_use_blist():
    def check_blist():
        assert isinstance(df.index, blist)
        assert isinstance(df.columns, blist)
        assert isinstance(df.data, blist)
        assert all([isinstance(df.data[x], blist) for x in range(len(df.columns))])

    df = rc.DataFrame(dropin=blist)
    assert isinstance(df, rc.DataFrame)
    assert df.data == []
    assert df.columns == []
    assert df.index == []
    assert df.sort is True
    check_blist()

    # add a new row and col
    df.set_cell(1, 'a', 1)
    check_blist()

    # add a new row
    df.set_cell(2, 'a', 2)
    check_blist()

    # add a new col
    df.set_cell(1, 'b', 3)
    check_blist()

    # add a complete new row
    df.set_row(3, {'a': 4, 'b': 5})
    check_blist()

    # add a complete new col
    df.set_column([2, 3], 'c', [6, 7])
    check_blist()


def test_assert_frame_equal():
    df1 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3])
    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3], dropin=blist)
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)


def test_print():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1], 'c': ['first', 'second', None]}, columns=['b', 'c', 'a'],
                      index=['row1', 'row2', 'row3'], dropin=blist)

    # __repr__ produces a simple representation
    expected = "object id: %s\ncolumns:\nblist(['b', 'c', 'a'])\ndata:\nblist([blist([1.0, 2.55, 3.1]), blist([" \
               "'first', 'second', None]), blist([1, 2, 3])])\nindex:\nblist(['row1', 'row2', 'row3'])\n" % id(df)
    actual = df.__repr__()
    assert actual == expected

    # __string__ produces the standard table
    expected = 'index       b  c         a\n-------  ----  ------  ---\nrow1     1     first     1\n' \
               'row2     2.55  second    2\nrow3     3.1             3'
    actual = df.__str__()
    assert actual == expected

    # print() method will pass along any argument for the tabulate.tabulate function
    df.print()


def test_json():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, sort=False, dropin=blist)

    string = df.to_json()
    actual = rc.DataFrame.from_json(string, blist)
    assert_frame_equal(df, actual)

    # fails with no dropin supplied
    with pytest.raises(AttributeError) as e:
        rc.DataFrame.from_json(string)
        assert e == "AttributeError: the JSON has a dropin : <class 'blist.blist'> : " \
                    "but the dropin parameter was not supplied"

    # fails with the wrong dropin supplied
    with pytest.raises(AttributeError) as e:
        rc.DataFrame.from_json(string, list)
        assert e == "AttributeError: the supplied dropin parameter: <class 'list'> : does not match the value" \
                    " in the JSON: <class 'blist.blist'>"


def test_json_objects():
    # test with a compound object returning a representation
    df = rc.DataFrame({'a': [1, 2], 'b': [4, blist([5, 6])]})

    string = df.to_json()
    actual = rc.DataFrame.from_json(string)

    # the DataFrames are not equal because the blist() was converted to a representation
    with pytest.raises(AssertionError):
        assert_frame_equal(df, actual)

    assert actual[1, 'b'] != blist([5, 6])
    assert actual[1, 'b'] == 'blist([5, 6])'


def test_select_index():
    # simple index, not sort, blist
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=['a', 'b', 'c', 'd', 'e', 'f'], dropin=blist)

    actual = df.select_index('c', 'value')
    assert actual == ['c']

    actual = df.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]


def test_columns_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'],
                          dropin=blist)
    names = actual.columns
    assert names == ['b', 'a']
    assert isinstance(names, blist)

    # test that a copy is returned
    names.append('bad')
    assert actual.columns == ['b', 'a']

    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']
    assert isinstance(actual.columns, blist)

    with pytest.raises(ValueError):
        actual.columns = ['list', 'too', 'long']


def test_index_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'],
                          dropin=blist)
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, blist)

    # test that a view is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c', 'bad']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, blist)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]


def test_data_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'],
                          dropin=blist)
    assert actual.data == [[4, 5, 6], [1, 2, 3]]
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])


def test_default_empty_init():
    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'], dropin=blist)
    assert actual.data == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]
    assert actual.sort is False
    assert isinstance(actual.index, blist)
    assert isinstance(actual.columns, blist)
    assert isinstance(actual.data, blist)
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])


def test_sort_index():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 8, 9], sort=False,
                      dropin=blist)

    df.sort_index()
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'], index=[8, 9, 10],
                                        sort=False, dropin=blist))


def test_sort_column():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9], dropin=blist)

    df.sort_columns('a')
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3], 'b': ['c', 'a', 'b']}, columns=['a', 'b'], index=[8, 10, 9],
                                        dropin=blist))

    df.sort_columns('a', reverse=True)
    assert isinstance(df.index, blist)
    assert_frame_equal(df, rc.DataFrame({'a': [3, 2, 1], 'b': ['b', 'a', 'c']}, columns=['a', 'b'], index=[9, 10, 8],
                                        dropin=blist))
