from collections import namedtuple

import raccoon as rc


def test_iterrows():
    df = rc.DataFrame({"first": [1, 2, 3, 4, 5], "second": ["a", 2, "b", None, 5]})

    expected = [
        {"index": 0, "first": 1, "second": "a"},
        {"index": 1, "first": 2, "second": 2},
        {"index": 2, "first": 3, "second": "b"},
        {"index": 3, "first": 4, "second": None},
        {"index": 4, "first": 5, "second": 5},
    ]
    actual = list()
    for x in df.iterrows():
        actual.append(x)

    assert actual == expected

    # index = False
    df = rc.DataFrame({"first": [1, 2, 3, 4, 5], "second": ["a", 2, "b", None, 5]})

    expected = [
        {"first": 1, "second": "a"},
        {"first": 2, "second": 2},
        {"first": 3, "second": "b"},
        {"first": 4, "second": None},
        {"first": 5, "second": 5},
    ]
    actual = list()
    for x in df.iterrows(index=False):
        actual.append(x)

    assert actual == expected


def test_itertuples():
    df = rc.DataFrame(
        {"first": [1, 2], "second": ["a", 2]}, index=["hi", "bye"], index_name="greet", columns=["first", "second"]
    )

    name_tup = namedtuple("Raccoon", ["greet", "first", "second"])
    expected = [name_tup(greet="hi", first=1, second="a"), name_tup(greet="bye", first=2, second=2)]
    actual = list()
    for x in df.itertuples():
        actual.append(x)

    assert actual == expected

    # index == False
    df = rc.DataFrame(
        {"first": [1, 2], "second": ["a", 2]}, index=["hi", "bye"], index_name="greet", columns=["first", "second"]
    )

    name_tup = namedtuple("Raccoon", ["first", "second"])
    expected = [name_tup(first=1, second="a"), name_tup(first=2, second=2)]
    actual = list()
    for x in df.itertuples(index=False):
        actual.append(x)

    assert actual == expected


def test_itertuples_sanitizes_invalid_field_names():
    df = rc.DataFrame({"class": [1], "_hidden": [2], "a-b": [3], "a b": [4]})

    actual = getattr(list(df.itertuples())[0], "_asdict")()

    assert actual == {"index": 0, "col_class": 1, "hidden": 2, "a_b": 3, "a_b_1": 4}


def test_itertuples_handles_index_column_name_collisions():
    df = rc.DataFrame({"index": [1]}, index_name="index")

    actual = getattr(list(df.itertuples())[0], "_asdict")()

    assert actual == {"index": 0, "index_1": 1}


def test_itertuples_handles_tuple_labels():
    df = rc.DataFrame({("first", "second"): [1]}, index=[("row", 1)], index_name=("left", "right"))

    actual = getattr(list(df.itertuples())[0], "_asdict")()

    assert actual == {"left_right": ("row", 1), "first_second": 1}
