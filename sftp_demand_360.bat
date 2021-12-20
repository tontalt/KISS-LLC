@echo off
cd "C:\DEV\SRC\HVMG\HVMG_BI\DataPullScripts"
IF "%~1"=="-h" GOTO usage
"C:\Program Files\Python39\python.exe" "C:\DEV\SRC\HVMG\HVMG_BI\DataPullScripts\sftp_demand_360.py" %1
goto alldone
:usage
echo Usage: %~0 [-h] [-s:mm/dd/yyy]
@echo.
@echo  -h             This help screen
@echo  -s:mm/dd/yyyy  StartDate
@echo.
@echo Notes:
@echo  - All dates will be used as entered, no data math will be applied  
@echo  - If you specify one date, you must specify all of them
@echo.
:alldone
exit %errorlevel%