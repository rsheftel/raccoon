import pytest
import raccoon as rc


def test_sorted_init():
    # initialized with index defaults to False
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13])
    assert df.sorted is False

    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13], sorted=True)
    assert df.sorted is True
    assert df.index == [11, 12, 13]
    assert df.data == [[1, 2, 3], [4, 5, 6]]

    # initialized with no index defaults to True
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'])
    assert df.sorted is True
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], sorted=False)
    assert df.sorted is False

    # if sorted is true, but no index provided it will assume already in sorted order
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], sorted=True)
    assert df.sorted is True
    assert df.index == [0, 1, 2]
    assert df.data == [[2, 1, 3], [5, 4, 6]]

    # start un-sorted, then set to sorted
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13], sorted=False)
    assert df.sorted is False
    assert df.index == [12, 11, 13]
    assert df.data == [[2, 1, 3], [5, 4, 6]]

    df.sorted = True
    assert df.index == [11, 12, 13]
    assert df.data == [[1, 2, 3], [4, 5, 6]]

    # mixed type index will bork on sorted=True
    with pytest.raises(TypeError):
        rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, index=[1, 'b', 3], sorted=True)


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
