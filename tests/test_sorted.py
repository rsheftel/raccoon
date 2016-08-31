import pytest
import raccoon as rc


def test_sorted_exists():
    a = [1, 2, 3, 6, 7, 8]

    assert rc.dataframe.sorted_exists(a, 0) == (False, 0)
    assert rc.dataframe.sorted_exists(a, 1) == (True, 0)
    assert rc.dataframe.sorted_exists(a, 3) == (True, 2)
    assert rc.dataframe.sorted_exists(a, 4) == (False, 3)
    assert rc.dataframe.sorted_exists(a, 5) == (False, 3)
    assert rc.dataframe.sorted_exists(a, 6) == (True, 3)
    assert rc.dataframe.sorted_exists(a, 8) == (True, 5)
    assert rc.dataframe.sorted_exists(a, 9) == (False, 6)

    a.insert(rc.dataframe.sorted_exists(a, 5)[1], 5)
    a.insert(rc.dataframe.sorted_exists(a, 4)[1], 4)
    a.insert(rc.dataframe.sorted_exists(a, 0)[1], 0)
    a.insert(rc.dataframe.sorted_exists(a, 9)[1], 9)

    assert a == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_sorted_index():
    a = [1, 2, 4, 5]

    assert rc.dataframe.sorted_index(a, 1) == 0
    assert rc.dataframe.sorted_index(a, 2) == 1
    assert rc.dataframe.sorted_index(a, 4) == 2
    assert rc.dataframe.sorted_index(a, 5) == 3

    with pytest.raises(ValueError):
        rc.dataframe.sorted_index(a, 3)
