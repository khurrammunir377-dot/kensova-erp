@echo off
setlocal
cd /d "%~dp0"

echo Removing Windows download security blocks from Kensova ERP files...

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -LiteralPath '%~dp0' -Recurse -File | Unblock-File -ErrorAction SilentlyContinue"

if errorlevel 1 (
    echo.
    echo Windows could not remove all file blocks automatically.
    echo Right-click the downloaded ZIP, choose Properties, tick Unblock, then extract it again.
) else (
    echo.
    echo Done. Kensova ERP files have been unblocked for this Windows user.
)

echo.
pause
