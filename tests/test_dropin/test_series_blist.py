import pytest

import raccoon as rc
from raccoon.utils import assert_series_equal

try:
    # noinspection PyUnresolvedReferences
    from blist import blist
except ImportError:
    pytest.skip("blist is not installed, skipping tests.", allow_module_level=True)


def test_assert_series_equal():
    srs1 = rc.Series([1, 2, 3], index=[1, 2, 3])
    srs2 = rc.Series([1, 2, 3], index=[1, 2, 3], dropin=blist)
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)


def test_default_empty_init():
    actual = rc.Series(index=[1, 2, 3], data_name="points", dropin=blist)
    assert actual.data == [None, None, None]
    assert actual.data_name == "points"
    assert actual.index == [1, 2, 3]
    assert actual.index_name == "index"
    assert actual.sort is False
    assert isinstance(actual.index, blist)
    assert isinstance(actual.data, blist)


def test_use_blist():
    def check_blist():
        assert isinstance(srs.index, blist)
        assert isinstance(srs.data, blist)

    srs = rc.Series(dropin=blist)
    assert isinstance(srs, rc.Series)
    assert srs.data == []
    assert srs.index == []
    assert srs.sort is True
    check_blist()

    # add a new row and col
    srs.set_cell(1, 1)
    check_blist()

    # add a new row
    srs.set_cell(2, 2)
    check_blist()

    # add a new col
    srs.set_cell(1, 3)
    check_blist()

    # add a complete new row
    srs.set_rows([3], [5])
    check_blist()


def test_index_blist():
    actual = rc.Series([4, 5, 6], index=["a", "b", "c"], dropin=blist)
    result = actual.index
    assert result == ["a", "b", "c"]
    assert isinstance(result, blist)

    # test that a view is returned
    result.append("bad")
    assert actual.index == ["a", "b", "c", "bad"]

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, blist)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]


def test_data_blist():
    actual = rc.Series([4, 5, 6], index=["a", "b", "c"], dropin=blist)
    assert actual.data == [4, 5, 6]
    assert isinstance(actual.data, blist)


def test_print():
    srs = rc.Series([1.0, 2.55, 3.1], data_name="boo", index=["row1", "row2", "row3"], dropin=blist)

    # __repr__ produces a simple representation
    expected = "object id: %s\ndata:\nblist([1.0, 2.55, 3.1])\nindex:\nblist(['row1', 'row2', 'row3'])\n" % id(srs)
    actual = srs.__repr__()
    assert actual == expected

    # __str__ produces the standard table
    expected = "index      boo\n-------  -----\nrow1      1\nrow2      2.55\nrow3      3.1"
    actual = srs.__str__()
    assert actual == expected

    # print() method will pass along any argument for the tabulate.tabulate function
    srs.print()


def test_sort_index():
    srs = rc.Series([4, 5, 6], index=[10, 8, 9], sort=False, dropin=blist)
    srs.sort_index()
    assert isinstance(srs.index, blist)
    assert_series_equal(srs, rc.Series([5, 6, 4], index=[8, 9, 10], sort=False, dropin=blist))


def test_select_index():
    # simple index, not sort, blist
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=["a", "b", "c", "d", "e", "f"], dropin=blist)
    actual = srs.select_index("c", "value")
    assert actual == ["c"]


def test_from_dataframe():
    df = rc.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, index=["a", "b", 9], dropin=blist)
    actual = rc.ViewSeries.from_dataframe(df, "b")
    expected = rc.ViewSeries([4, 5, 6], data_name="b", index=["a", "b", 9])
    assert_series_equal(actual, expected)


def test_from_series():
    srs = rc.Series(data=[4, 5, 6], data_name="b", index=["a", "b", 9], dropin=blist)
    actual = rc.ViewSeries.from_series(srs)
    expected = rc.ViewSeries([4, 5, 6], data_name="b", index=["a", "b", 9])
    assert_series_equal(actual, expected)
