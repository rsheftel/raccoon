@ECHO OFF
REM Makes the Sphinx documentation files from the Jupyter Notebook examples

FOR %%a IN (%~dp0\.) do set RACCOON=%%~dpa
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;%RACCOON%

jupyter nbconvert --to rst --execute --output usage_dataframe.rst ..\examples\usage_dataframe.ipynb
jupyter nbconvert --to rst --execute --output usage_series.rst ..\examples\usage_series.ipynb
jupyter nbconvert --to rst --execute --output usage_dropin.rst ..\examples\usage_dropin.ipynb
jupyter nbconvert --to rst --execute --output speed_test.rst ..\examples\speed_test.ipynb
set PYTHONPATH=%OLD_PYTHONPATH%
