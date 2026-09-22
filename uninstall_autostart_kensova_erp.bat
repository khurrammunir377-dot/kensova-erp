@echo off
:: Run this to remove the auto-start-at-logon task created by install_autostart_KENSOVA_erp.bat

schtasks /delete /tn "KENSOVAERP_AutoStart" /f

echo.
echo Done. KENSOVA-ERP will no longer start automatically at logon.
echo.
pause
