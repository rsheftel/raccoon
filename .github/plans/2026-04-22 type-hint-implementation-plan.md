# Type Hint Improvement Plan

Status: planning only. No library code changes are included in this file.

Revision note: updated after the completed dropin-removal work described in `.github/plans/2026-04-21-dropin-removal-plan.md` and after the project minimum Python version was raised to 3.12.

## Goal

Fix the current type-checking problems in `raccoon/dataframe.py`, `raccoon/series.py`, `raccoon/sort_utils.py`, and `raccoon/utils.py` with minimal behavioral change while improving API precision for callers.

## Recommended Direction

1. Make internal plain-list attributes non-optional after construction.
2. Replace imprecise `namedtuple` return annotations with a static type that type checkers can understand.
3. Add overloads for methods whose return type depends on argument shape or flag values.
4. Use Python 3.12 typing features where they simplify repeated local relationships.
5. Tighten the remaining broad annotations in `sort_utils.py` and `utils.py` during the same pass.

## Constraints And Assumptions

1. The project supports Python 3.12+, so `Self`, `Literal`, `TypeAlias`, `TypeVar`, `@overload`, and inline type parameter lists are available.
2. The request mentions `src/montauk/data/structures.py`, but that path does not exist in this repository. For repeated shared typing helpers, use a repo-local module such as `raccoon/_types.py` instead.
3. The plan should prefer minimal runtime change. If a typing improvement would change public behavior, it should be isolated and tested explicitly.
4. The completed dropin removal means the typing pass should assume built-in lists only. Any remaining plan items that previously accounted for alternate list-like containers are obsolete.

## Plan

1. Establish internal invariants for nullable attributes.
   - In `raccoon/dataframe.py`, stop treating `self._index` and `self._columns` as `None` after `__init__` starts. The preferred fix is to initialize them as empty built-in lists immediately and keep them non-optional thereafter.
   - In `raccoon/series.py`, apply the same rule to `self._index` and `self._data` in `SeriesBase` and concrete subclasses.
   - Remove any remaining annotations that imply container polymorphism or delayed initialization now that built-in lists are the only storage model.
   - If a `None` sentinel must temporarily remain for constructor flow, isolate it behind a small private narrowing helper, but treat that as a transitional step rather than the end state.

2. Use inline types by default and add shared typing helpers only when repetition clearly justifies them.
   - Prefer inline types for selectors, row dictionaries, and tuple return shapes by default.
   - Create a repo-local typing module such as `raccoon/_types.py` only if the same type shape is repeated in 3 or more public signatures and the shared name is more informative than the raw type.
   - Do not introduce semantic aliases whose names hide simple built-in types without adding clarity in editor hovers.
   - Prefer inline type parameters for local same-type relationships that appear once or twice. If the same pattern shows up in 3 or more places, promote it into a shared helper only when it improves readability rather than obscuring it.
   - Do not add a list-like protocol or container abstraction layer. That part of the earlier plan is no longer relevant after dropin removal.

3. Replace `namedtuple` annotations with static return types type checkers can follow.
   - In `raccoon/dataframe.py`, change method return annotations that currently use `namedtuple`.
   - For `get_columns()` and `get_location()`, annotate the namedtuple branch as `tuple[Any, ...]` if the implementation remains dynamically generated with `collections.namedtuple`.
   - For `itertuples()`, annotate the iterator as `Iterator[tuple[Any, ...]]` if the tuple type remains dynamic.
   - Do not annotate these returns as `namedtuple`; that is a runtime factory, not a stable return type.
   - Update the docstrings in the same pass so they stop promising a `namedtuple` type hint and instead describe the runtime value accurately.
   - If stronger static typing is desired later, that should be a separate refactor that replaces dynamic tuple creation with a fixed `NamedTuple` class, but that is not a minimal-change first step.

4. Add overloads for the DataFrame read APIs whose return type depends on flags or selector shape.
   - Add `@overload` definitions to `DataFrame.get()` for these cases:
     - single row and single column -> scalar value
     - many rows and one column with `as_list=True` -> `list[Any]`
     - many rows and one column with `as_list=False` -> `Self`
      - one row and many columns with `as_dict=True` -> `dict[Any, Any]`
     - one row and many columns with `as_namedtuple=True` -> `tuple[Any, ...]`
     - matrix selection -> `Self`
   - Add overloads to `get_rows()`, `get_entire_column()`, `get_columns()`, `get_location()`, and `get_slice()` so the boolean flags use `Literal[True]` and `Literal[False]` to drive the return type.
    - Use the current branch structure in `get()` as the source of truth rather than designing a more abstract overload model first.
    - Keep the implementation body unchanged at first; improve annotations before restructuring control flow.

5. Add overloads for the Series and ViewSeries APIs with parameter-dependent returns.
   - In `raccoon/series.py`, add overloads for `SeriesBase.get()` and `get_rows()` so `as_list=True` returns `list[Any]` and `as_list=False` returns `Self`.
   - Add overloads for `get_slice()` so `as_list=True` returns `tuple[list[Any], list[Any]]` and `as_list=False` returns `Self`.
   - Add overloads for `ViewSeries.value()` to distinguish:
     - integer location -> scalar value
     - slice with location semantics -> `list[Any]`
     - list of locations -> `list[Any]`
     - index-based selection with `int_as_index=True` -> scalar value or `list[Any]` depending on selector shape
   - Add overloads to `select_index()` in both `DataFrame` and `Series` so `result="boolean"` returns `list[bool]` and `result="value"` returns `list[Any]`.
   - Revisit `SeriesBase` abstract property annotations during the same pass, because Python 3.12 support makes it practical to tighten those contracts without adding compatibility shims.

6. Tighten helper function signatures in `sort_utils.py`.
   - Update `sorted_list_indexes()` so `key` is typed as `Callable[[Any], Any] | None` instead of `Callable | Any`.
   - Consider an inline type parameter for the element type if it improves local clarity without introducing repeated noise.
   - Keep `sorted_exists()` and `sorted_index()` simple unless the same element-type relationship is reused enough to justify a shared `TypeVar`.

7. Tighten utility function signatures in `utils.py`.
   - Change `data_args: dict | None` to `dict[str, Any] | None` in both assertion helpers.
   - If a repeated union such as `rc.Series | rc.ViewSeries` appears in 3 or more public signatures and a shared helper would be clearer in VS Code than the raw type, introduce it in a repo-local typing module and reuse it.
   - Change `data_function: Callable | None` to a more precise callable shape if the current call pattern can support it cleanly.
   - Keep these changes small and strictly annotation-focused.

8. Reduce annotation noise where the current unions are too broad.
   - Replace broad returns like `Self | list | dict | Any` with overload-driven public signatures and a simpler implementation annotation where needed.
   - Review places that use `list | list[bool]`, `Any | list`, or bare `dict` and convert them to a more precise inline type first. Only extract a shared helper if the same shape repeats often enough and the extracted name is clearly more readable than the raw type.
   - Because the codebase now targets Python 3.12, prefer modern built-in generic syntax and inline type parameters over older, more indirect typing patterns.
   - Prioritize public methods first, then private helpers that type checkers still flag after the public API is improved.

9. Validate the typing cleanup with focused checks.
   - Run Ruff on the edited files.
   - Run the relevant test subsets for DataFrame and Series.
   - Run the chosen type checker against the four target modules and confirm that the `_columns` and `_index` false positives are gone.
   - Add explicit validation for the post-dropin code paths so the typing cleanup does not accidentally reintroduce container-abstraction assumptions.
   - If overloads expose real implementation mismatches, fix those by simplifying control flow rather than weakening the annotations.

## File-Specific Hotspots To Address

### raccoon/dataframe.py

1. Internal nullable attributes set in `__init__`: `_index`, `_columns`.
2. Dynamic-return methods: `get()`, `get_rows()`, `get_columns()`, `get_entire_column()`, `get_location()`, `get_slice()`.
3. Dynamic namedtuple methods: `get_columns()`, `get_location()`, `itertuples()`.
4. Loose helper annotations: `sort_columns()`, `_validate_index()`, `_validate_columns()`, `_validate_data()`, `append()`, `to_dict()`, and `__getitem__()`.

### raccoon/series.py

1. Internal nullable attributes in `SeriesBase` and `Series`: `_index`, `_data`.
2. Dynamic-return methods: `get()`, `get_rows()`, `get_slice()`, `select_index()`.
3. Complex selector dispatch in `ViewSeries.value()`.
4. Loose helper annotations around abstract properties, setters, index manipulation methods, and `__getitem__()`.

### raccoon/sort_utils.py

1. `sorted_list_indexes()` key parameter is too broad.
2. Shared same-type relationships should only use a shared `TypeVar` if the same pattern is reused enough to justify it.

### raccoon/utils.py

1. `data_args` should be typed as a mapping with string keys.
2. `data_function` can likely be typed more precisely than bare `Callable`.
3. Repeated unions involving `Series` and `ViewSeries` can be aliased if they recur after the main cleanup.

## Order Of Implementation

1. Internal invariant fix for nullable containers.
2. Shared helpers and repeated `TypeVar` definitions, if justified.
3. `namedtuple` annotation cleanup.
4. DataFrame overloads.
5. Series and ViewSeries overloads.
6. Helper signature cleanup in `sort_utils.py` and `utils.py`.
7. Docstring cleanup where type descriptions are now misleading.
8. Ruff, tests, and type-checker validation.

## Risks To Watch

1. Overloads can become misleading if the runtime branch conditions are not aligned exactly with the public signatures.
2. The current constructors still assign `None` first and populate later, so the invariant fix should be done carefully to avoid changing initialization behavior accidentally.
3. Dynamic `namedtuple` creation cannot be made strongly field-typed without a larger API refactor.
4. Some methods may be easier to type after small internal helper extraction; if so, extract helpers only where it reduces complexity.
5. Abstract base class signatures in `SeriesBase` may need coordinated updates with both `Series` and `ViewSeries` to keep type checkers and runtime behavior aligned.

## Suggested Commit Message

Add type hint improvement plan
