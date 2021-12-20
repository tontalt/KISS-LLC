@echo off
cd "C:\DEV\SRC\HVMG\HVMG_BI\DataPullScripts"
IF "%~1"=="-h" GOTO usage
"C:\Program Files\Python39\python.exe" "C:\DEV\SRC\HVMG\HVMG_BI\DataPullScripts\HVMG_Logfile_Cleanup.py"
goto alldone
:usage
echo Usage: %~0 [-h] [-s:mm/dd/yyy]
@echo.
@echo  -h             This help screen
@echo.
:alldone
exit %errorlevel%
