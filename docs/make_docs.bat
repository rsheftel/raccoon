@ECHO OFF
REM Makes the Sphinx documentation files

FOR %%a IN (%~dp0\.) do set RACCOON=%%~dpa
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;%RACCOON%

REM jupyter nbconvert --to rst --execute --output usage.rst ..\examples\usage.ipynb
REM jupyter nbconvert --to rst --execute --output speed_test.rst ..\examples\speed_test.ipynb
sphinx-apidoc -f -o . ../raccoon
./make.bat html
set PYTHONPATH=%OLD_PYTHONPATH%
