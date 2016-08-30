@ECHO OFF
REM Makes the Sphinx documentation files

FOR %%a IN (%~dp0\.) do set RACCOON=%%~dpa
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;%RACCOON%

sphinx-apidoc -f -o . ../raccoon
./make.bat html
set PYTHONPATH=%OLD_PYTHONPATH%
