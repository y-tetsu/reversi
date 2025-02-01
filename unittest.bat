py -3.12 -m unittest discover tests -v

@echo off
IF %ERRORLEVEL% EQU 0 (
    echo "OK"
) ELSE (
    echo "FAILED (%ERRORLEVEL%)"
)
