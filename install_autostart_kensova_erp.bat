@echo off
:: Run this ONCE to make KENSOVA-ERP start automatically every time you log into Windows.
:: Safe to double-click normally - it will just show a console window for this one setup step.

set "TASK_NAME=KENSOVAERP_AutoStart"
set "VBS_PATH=%~dp0START_KENSOVA_ERP.vbs"

schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%VBS_PATH%\"" /sc onlogon /f

echo.
echo Done. KENSOVA-ERP will now launch automatically (hidden server + maximized
echo Edge window) whenever you log into this PC.
echo.
echo To undo this later, run uninstall_autostart_KENSOVA_erp.bat
echo.
pause
