# DataFrame Indexing Overloads Plan

Status: completed.

## Goal

Fix Pylance false positives around `DataFrame` indexing by adding overloads for `__getitem__` and `__setitem__` that reflect the existing runtime behavior.

## Plan

1. Add focused overloads for `DataFrame.__getitem__`.
   - Single-column access like `df['a']` should type as `DataFrame`.
   - Matrix and row-slice access should type as `DataFrame`.
   - Single-cell access like `df[1, 'a']` should type as a scalar value.
2. Add matching overloads for `DataFrame.__setitem__`.
   - Column assignment and cell assignment should both remain supported.
3. Validate the affected diagnostics in the DataFrame tests.
   - Confirm the `to_list()` false positives are gone.
   - Confirm tuple-based indexing on a narrowed `DataFrame` no longer reports list-based errors.

## Result

1. Added focused overloads for `DataFrame.__getitem__` that distinguish DataFrame-returning selections from single-cell access.
2. Added matching overloads for `DataFrame.__setitem__` to document supported assignment shapes.
3. Verified that the earlier false positives around `to_list()`, tuple assignment, and tuple reads on narrowed `DataFrame` values are gone.
4. Remaining Pylance feedback in `tests/test_dataframe/test_dataframe.py` is the intentional invalid-literal call to `select_index('a', 'BAD')` inside a runtime error test.

## Suggested Commit Message

Add DataFrame indexing overloads
