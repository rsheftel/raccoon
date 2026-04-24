# Dropin Removal Plan

Status: the dropin removal work is complete across runtime code, tests, docs, examples, and the remaining notebook cleanup.

Current step: complete. Only future notebook-derived doc regeneration should be rechecked if someone rebuilds those outputs later.

## Progress Update

### Completed In This Iteration

1. Removed the `dropin` parameter and public property surface from `DataFrame` and `Series`.
2. Removed `_dropin` state and alternate-container branches from `raccoon/dataframe.py` and `raccoon/series.py`.
3. Simplified JSON serialization and deserialization so `dropin` metadata and `dropin_func` handling are gone.
4. Removed equality checks that compared `.dropin` in `raccoon/utils.py`.
5. Deleted the dedicated dropin tests under `tests/test_dropin/` and updated the remaining suite where needed.
6. Updated non-notebook documentation in `README.rst`, `docs/index.rst`, `docs/make_examples.bat`, and `docs/usage_dataframe.rst`.
7. Deleted the dedicated dropin docs and example notebook: `docs/usage_dropin.rst` and `examples/usage_dropin.ipynb`.
8. Updated planning notes so non-historical references outside the deferred notebook work were removed.
9. Validated the non-notebook changes with Ruff, focused DataFrame and Series tests, and the full pytest suite.
10. Removed the temporary debug cell from `examples/usage_dataframe.ipynb` and regenerated the JSON example output so it no longer includes stale `dropin` metadata.
11. Ran a final repository search across project files and confirmed the remaining matches are limited to this archived plan file.

### Still Left

1. If notebook-derived docs are regenerated later, verify that the generated output still does not reintroduce `dropin` references.

### Validation Status

1. Ruff passed on the edited Python and test files.
2. Focused tests for DataFrame and Series passed.
3. The full pytest suite passed.
4. The follow-up notebook cleanup passed: the temporary debug cell is gone and the stored JSON example no longer contains `dropin` metadata.
5. Final repository searches across the project files found no live `dropin`, `usage_dropin`, or `dropin_func` references outside this archived plan file.

## Goal

Remove the `dropin` concept from the project entirely, including:

1. Public constructor parameters and properties.
2. Internal support for alternate list-like containers.
3. Serialization and deserialization behavior tied to `dropin` metadata.
4. Dedicated dropin tests.
5. Documentation and examples that present dropin as a supported feature.

## Why This Needs A Coordinated Change

The `dropin` concept is not isolated to a single parameter. It is embedded in:

1. Core storage behavior in `raccoon/dataframe.py` and `raccoon/series.py`.
2. Equality helpers in `raccoon/utils.py`.
3. JSON metadata and reconstruction logic.
4. Dedicated tests in `tests/test_dropin/`.
5. Documentation pages, generated example output, notebooks, and the docs index.

Because of that, this should be done as one coherent removal rather than by deleting a few constructor arguments and cleaning up fallout later.

## Scope

### Code areas to change

1. `raccoon/dataframe.py`
2. `raccoon/series.py`
3. `raccoon/utils.py`
4. `raccoon/__init__.py` if public exports or version-facing text need adjustment

### Tests to change or remove

1. Entire `tests/test_dropin/` directory
2. Any assertions in the remaining suite that reference `.dropin`
3. Any JSON-related expectations that currently include `"dropin": null`

### Documentation and examples to change or remove

1. `README.rst`
2. `docs/index.rst`
3. `docs/usage_dropin.rst`
4. `docs/usage_dataframe.rst`
5. `docs/make_examples.bat`
6. `examples/usage_dropin.ipynb`
7. Any generated example output that still mentions dropin metadata or APIs
8. `docs/change_log.rst`

## Recommended Implementation Order

1. Remove the public API surface.
   - Delete the `dropin` parameter from `DataFrame` and `Series` constructors.
   - Remove any `.dropin` property or attribute that is part of the public interface.
   - Let the constructor signature reject `dropin` naturally. Do not add a transitional compatibility layer.

2. Remove internal alternate-container handling.
   - Delete `_dropin` from `__slots__` and object state.
   - Replace all `dropin(...) if dropin else ...` branches with plain built-in list construction.
   - Replace `self._dropin(...) if self._dropin else ...` branches with plain lists.
   - Simplify helper methods such as `_check_list()` so they only reason about built-in lists.

3. Simplify serialization behavior.
   - Remove `dropin` from DataFrame JSON metadata emitted by `to_json()`.
   - Remove the `dropin_func` argument from `DataFrame.from_json()`.
   - Remove any validation logic that compares serialized dropin class names.
   - Treat old JSON payloads that still contain `dropin` metadata as unsupported. Do not add backward-compatibility handling for them.
   - Update any JSON examples and tests to match the new metadata shape.

4. Update copy and view construction paths.
   - Inspect all places where `DataFrame` or `Series` construct new instances from existing ones and remove forwarding of `dropin=self._dropin`.
   - Confirm that the new objects still preserve current behavior for data, index, names, and sort flags.

5. Remove test coverage for the feature and replace only the coverage that still matters.
   - Delete `tests/test_dropin/test_dataframe_blist.py`.
   - Delete `tests/test_dropin/test_series_blist.py`.
   - Remove or update any assertions in the remaining suite that check `.dropin`.
   - Keep or expand non-dropin tests where they currently rely on dropin-specific coverage for normal list behavior.

6. Remove documentation and example references.
   - Remove the dropin section from `README.rst`, especially the "Underlying Data Structure" text that advertises alternate list replacements.
   - Remove `usage_dropin.rst` from `docs/index.rst`.
   - Delete the generated doc page `docs/usage_dropin.rst`.
   - Stop generating that page in `docs/make_examples.bat`.
   - Delete `examples/usage_dropin.ipynb` and the generated `docs/usage_dropin.rst` in the same change.
   - Update any generated docs or notebook-derived content that still shows `dropin` in JSON metadata.

7. Update project history and release notes.
   - Add a concise entry to `docs/change_log.rst` describing removal of dropin support.
   - Reflect clearly in the change log that this is an intentional breaking API change.
   - Leave older historical mentions of dropin in the changelog intact.

8. Validate the removal end to end.
   - Run the relevant unit tests for DataFrame and Series.
   - Run the full test suite if the focused suites pass.
   - Run Ruff on edited Python files.
   - Search the repository again for `dropin`, `usage_dropin`, and `.dropin` and verify only intentional historical mentions remain, if any.

## File-Specific Expectations

### `raccoon/dataframe.py`

1. Remove `_dropin` state and all branches that construct alternate containers.
2. Remove `dropin` from constructor and public property surface.
3. Remove JSON metadata handling for `dropin`.
4. Remove `from_json()` compatibility logic that expects a `dropin_func`.
5. Update any methods that currently pass `dropin=self._dropin` into new `DataFrame` instances.

### `raccoon/series.py`

1. Remove `_dropin` state and all branches that depend on it.
2. Remove `dropin` from constructor signatures and any public property surface.
3. Remove propagation of `dropin` into new `Series` instances.
4. Recheck `ViewSeries` behavior, because some constructors appear to forward dropin implicitly.

### `raccoon/utils.py`

1. Remove equality assertions that compare `.dropin`.
2. Keep the helpers focused on user-visible Series and DataFrame contents.

### Tests

1. Delete the dedicated dropin suite.
2. Update any remaining tests that reference `.dropin` directly.
3. Update JSON string expectations to remove the `dropin` field.

### Docs and examples

1. Remove the dedicated dropin usage page from docs navigation and generated docs.
2. Remove the dropin notebook and generation step if that content is no longer wanted.
3. Rewrite README language so the project consistently describes built-in lists as the storage model, not a configurable abstraction.

## Confirmed Decisions

1. Old JSON payloads that still depend on `dropin` metadata are unsupported after this change.
2. Breaking constructor signatures is intentional and desired.
3. Delete both the notebook source and generated documentation output for the dropin example.
4. Leave historical changelog mentions in place.

## Concrete Search Targets For The Implementation Pass

Use these repository searches during the actual removal work:

1. `dropin`
2. `.dropin`
3. `dropin=`
4. `_dropin`
5. `usage_dropin`
6. `dropin_func`

## Validation Checklist For The Future Implementation Pass

1. Completed: no constructor in the public API accepts `dropin`.
2. Completed: no runtime object exposes a `.dropin` property.
3. Completed: no JSON produced by the runtime library includes a `dropin` metadata field.
4. Completed: no tests remain under `tests/test_dropin/`.
5. Partially complete: no docs page or notebook remains dedicated to dropin support, but `examples/usage_dataframe.ipynb` still contains deferred cleanup work.
6. Partially complete: repository search results for `dropin` are limited to intentional historical notes plus the deferred notebook content in `examples/usage_dataframe.ipynb`.

## Suggested Commit Message

Remove dropin support from project
